## rpmdb 损坏

不要轻易杀死yum进程，如果出现错误执行以下命令

```bash
mv /var/lib/rpm/__db* /tmp
rpm --rebuilddb
yum clean all
```

