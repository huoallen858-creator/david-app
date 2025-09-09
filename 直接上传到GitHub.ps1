# 直接上传到GitHub
Write-Host "============================================================"
Write-Host "直接上传到GitHub"
Write-Host "Direct Upload to GitHub"
Write-Host "============================================================"
Write-Host ""

# 检查是否已安装Git
try {
    git --version | Out-Null
    Write-Host "✓ Git已安装"
} catch {
    Write-Host "❌ Git未安装，正在下载..."
    
    # 创建临时目录
    if (!(Test-Path "C:\temp")) {
        New-Item -ItemType Directory -Path "C:\temp" -Force
    }
    
    # 下载Git
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitPath = "C:\temp\Git-installer.exe"
    
    Write-Host "正在下载Git..."
    Invoke-WebRequest -Uri $gitUrl -OutFile $gitPath
    
    if (Test-Path $gitPath) {
        Write-Host "正在安装Git..."
        Start-Process -FilePath $gitPath -ArgumentList "/SILENT", "/NORESTART" -Wait
        Write-Host "✓ Git安装完成"
        
        # 添加到PATH
        $env:PATH += ";C:\Program Files\Git\bin"
    } else {
        Write-Host "❌ Git下载失败"
        Write-Host "请手动安装Git: https://git-scm.com/download/win"
        Read-Host "按回车键退出"
        exit 1
    }
}

Write-Host ""
Write-Host "正在初始化Git仓库..."
git init
git config user.name "David App"
git config user.email "david@example.com"
git add .
git commit -m "Initial commit: 大卫排版应用程序"

Write-Host ""
Write-Host "正在上传到GitHub..."
git remote add origin https://github.com/huoallen858-creator/david-app.git
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ 上传成功！"
    Write-Host ""
    Write-Host "下一步："
    Write-Host "1. 访问: https://github.com/huoallen858-creator/david-app"
    Write-Host "2. 点击 'Actions' 标签"
    Write-Host "3. 等待构建完成（约5-10分钟）"
    Write-Host "4. 点击构建任务，下载APK文件"
    Write-Host ""
    Write-Host "或者直接访问："
    Write-Host "https://github.com/huoallen858-creator/david-app/actions"
} else {
    Write-Host "❌ 上传失败，请检查网络连接"
    Write-Host "可能需要输入GitHub用户名和密码"
}

Read-Host "按回车键退出"

