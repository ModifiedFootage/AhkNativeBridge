#SingleInstance Force
SetBatchLines -1

NumpadAdd::
    pipe := "\\.\pipe\NativeEventPipe"

    ; Open the named pipe
    hPipe := DllCall("CreateFile"
        , "Str", pipe
        , "UInt", 0x40000000  ; GENERIC_WRITE
        , "UInt", 0           ; no sharing
        , "Ptr", 0            ; default security
        , "UInt", 3           ; OPEN_EXISTING
        , "UInt", 0           ; default flags
        , "Ptr", 0)           ; no template

    if (hPipe = -1) {
        MsgBox, 48, Pipe Error, ❌ Failed to open pipe.`nError code: %A_LastError%
        return
    }

    ; Prepare the JSON message
    msg := "{""event"":""numpad_add""}"
    VarSetCapacity(buf, StrLen(msg) * 2)
    StrPut(msg, &buf, StrLen(msg), "UTF-8")

    ; Write the message to the pipe
    DllCall("WriteFile"
        , "Ptr", hPipe
        , "Ptr", &buf
        , "UInt", StrLen(msg)
        , "UIntP", bytesWritten
        , "Ptr", 0)

    ; Close the pipe
    DllCall("CloseHandle", "Ptr", hPipe)
return
