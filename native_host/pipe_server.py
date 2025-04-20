import json

import win32file
import win32pipe

pipe_name = r"\\.\pipe\NativeEventPipe"


def listen_pipe():
    pipe = win32pipe.CreateNamedPipe(
        pipe_name,
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
    print("Waiting for AHK...")
    win32pipe.ConnectNamedPipe(pipe, None)
    print("AHK connected.")
    while True:
        try:
            result, data = win32file.ReadFile(pipe, 4096)
            message = data.decode()
            print(f"Got from AHK: {message}")
            # Do something here, like send it to Chrome using stdin
        except Exception as e:
            print("Pipe read failed:", e)
            break


listen_pipe()
