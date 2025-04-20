pipeName := "\\.\pipe\NativeEventPipe"
hPipe := DllCall("CreateFile", "Str", pipeName, "UInt", 0x40000000, "UInt", 0, "Ptr", 0, "UInt", 3, "UInt", 0, "Ptr", 0)

if (hPipe = -1) {
    MsgBox, Failed to open pipe. Error: %A_LastError%
    return
}

msg := "{""event"":""numpad_add""}"
VarSetCapacity(buf, StrLen(msg)*2)
StrPut(msg, &buf, StrLen(msg), "UTF-8")
DllCall("WriteFile", "Ptr", hPipe, "Ptr", &buf, "UInt", StrLen(msg), "UIntP", written, "Ptr", 0)
DllCall("CloseHandle", "Ptr", hPipe)
