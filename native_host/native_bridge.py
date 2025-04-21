import json
import struct
import sys
import threading
import traceback

import win32file
import win32pipe

PIPE_NAME = r"\\.\pipe\NativeEventPipe"


def send_message(msg):
    """Send a JSON message to Chrome via stdout, with logging."""
    try:
        sys.stderr.write(f"[bridge] → Sending to Chrome: {msg}\n")
        sys.stderr.flush()
        payload = json.dumps(msg).encode("utf-8")
        sys.stdout.buffer.write(struct.pack("<I", len(payload)))
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()
        sys.stderr.write("[bridge] → Sent successfully.\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[bridge] ✖ Error sending to Chrome: {e}\n")
        sys.stderr.write(traceback.format_exc() + "\n")
        sys.stderr.flush()


def chrome_listener():
    """Listen for messages from the extension on stdin."""
    sys.stderr.write("[bridge] → Chrome listener started.\n")
    sys.stderr.flush()
    while True:
        raw = sys.stdin.buffer.read(4)
        if not raw:
            sys.stderr.write("[bridge] → Chrome stdin closed, exiting listener.\n")
            sys.stderr.flush()
            break
        length = struct.unpack("<I", raw)[0]
        data = sys.stdin.buffer.read(length).decode("utf-8")
        sys.stderr.write(f"[bridge] ← Received from Chrome: {data}\n")
        sys.stderr.flush()
        try:
            obj = json.loads(data)
            send_message({"echo": obj})
        except:
            sys.stderr.write("[bridge] ✖ Invalid JSON from Chrome.\n")
            sys.stderr.flush()


def ahk_listener():
    """Listen for AHK events via named pipe."""
    sys.stderr.write(f"[bridge] → AHK listener starting on pipe: {PIPE_NAME}\n")
    sys.stderr.flush()
    while True:
        try:
            sys.stderr.write("[pipe] → Creating named pipe...\n")
            sys.stderr.flush()
            pipe = win32pipe.CreateNamedPipe(
                PIPE_NAME,
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE
                | win32pipe.PIPE_READMODE_MESSAGE
                | win32pipe.PIPE_WAIT,
                1,
                65536,
                65536,
                0,
                None,
            )
            sys.stderr.write("[pipe] → Waiting for AHK connection...\n")
            sys.stderr.flush()
            win32pipe.ConnectNamedPipe(pipe, None)
            sys.stderr.write("[pipe] → AHK connected.\n")
            sys.stderr.flush()

            result, data = win32file.ReadFile(pipe, 4096)
            message = data.decode("utf-8")
            sys.stderr.write(f"[pipe] ← Received from AHK: {message}\n")
            sys.stderr.flush()
            try:
                obj = json.loads(message)
                send_message({"type": "ahk_event", "payload": obj})
            except Exception:
                sys.stderr.write("[pipe] → JSON parse failed, sending raw.\n")
                sys.stderr.flush()
                send_message({"type": "ahk_event", "raw": message})

        except Exception as e:
            sys.stderr.write(f"[pipe] ✖ Error in pipe listener: {e}\n")
            sys.stderr.write(traceback.format_exc() + "\n")
            sys.stderr.flush()
        finally:
            try:
                win32file.CloseHandle(pipe)
                sys.stderr.write("[pipe] → Pipe handle closed.\n")
                sys.stderr.flush()
            except:
                pass


if __name__ == "__main__":
    sys.stderr.write("[bridge] 🌉 Native Bridge Starting\n")
    sys.stderr.flush()

    # Start AHK listener thread
    t = threading.Thread(target=ahk_listener, daemon=True)
    t.start()

    # Start Chrome listener (blocks)
    chrome_listener()
