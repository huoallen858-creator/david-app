Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = oWS.SpecialFolders("Desktop") & "\大卫排版应用程序.lnk"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "C:\Users\rudyh\Desktop\新建cursor文件夹\启动大卫排版.bat"
oLink.WorkingDirectory = "C:\Users\rudyh\Desktop\新建cursor文件夹"
oLink.Description = "大卫排版应用程序"
oLink.Save
WScript.Echo "桌面快捷方式创建成功！"