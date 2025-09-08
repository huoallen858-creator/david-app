Set WshShell = CreateObject("WScript.Shell")
Set oShellLink = WshShell.CreateShortcut(WshShell.SpecialFolders("Desktop") & "\大卫排版应用程序.lnk")
oShellLink.TargetPath = "python.exe"
oShellLink.Arguments = """" & "C:\Users\rudyh\Desktop\新建cursor文件夹\大卫排版_交互版.py" & """"
oShellLink.WorkingDirectory = "C:\Users\rudyh\Desktop\新建cursor文件夹"
oShellLink.Description = "大卫排版应用程序"
oShellLink.Save

