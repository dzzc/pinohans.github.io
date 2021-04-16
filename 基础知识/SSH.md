## ssh

### 端口转发

```bash
# 将rhost:rport转到lhost:lport
# ssh -fgN -L lhost:lport:rhost:rport ruser@rhost
ssh -fgN -L 127.0.0.1:8080:127.0.0.1:5601 root@116.196.100.51

# 将lhost:lport转到rhost:rport
```

### 服务器断开

```bash
# 0 - 不向客户端确认存活
# 60 - 每隔1分钟确认存活
sed -i "s/#ClientAliveInterval 0/ClientAliveInterval 60/g" /etc/ssh/sshd_config
# 3 - 超过3次不活断开
sed -i "s/#ClientAliveCountMax 3/ClientAliveCountMax 3/g" /etc/ssh/sshd_config
# 查看修改
grep ClientAlive /etc/ssh/sshd_config
# 重启服务
service sshd reload
```

