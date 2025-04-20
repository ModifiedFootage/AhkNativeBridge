import json
import struct
import sys


def send_message(message):
    encoded = json.dumps(message).encode("utf-8")
    sys.stdout.buffer.write(struct.pack("I", len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()


def get_message():
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) == 0:
        return None
    message_length = struct.unpack("I", raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode("utf-8")
    return json.loads(message)


while True:
    try:
        msg = get_message()
        if msg is None:
            break
        print("Received from Chrome:", msg)  # This goes to console — okay for debugging
        send_message({"echo": msg})
    except Exception as e:
        break
