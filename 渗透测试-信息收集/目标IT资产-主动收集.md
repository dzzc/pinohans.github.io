# 1. 交互泄露

1. html，js，css等返回内容中的信息
2. 响应头信息，如CSP（Content-Security-Policy）头，Access-Control-Allow-Origin头
3. RSS订阅

# 2. 爆破

1. oneforall
2. ESD
3. subfinder
4. dirmap
5. subDomainsBrute：https://github.com/lijiejie/subDomainsBrute
6. teemo：https://github.com/bit4woo/teemo
7. Sublist3r：https://github.com/aboul3la/Sublist3r
8. gobuster：https://github.com/OJ/gobuster
9. assetfinder：https://github.com/tomnomnom/assetfinder
10. Sudomy：https://github.com/Screetsec/Sudomy


## 2.1. 字典

1. 弱口令: https://www.bugku.com/mima
2. 默认口令: https://cirt.net/passwords
3. 个人字典: https://github.com/k8gege/PasswordDic


### 2.1.1. 文件路径


#### 2.1.1.1. 组件

| 文件路径              | 类型              |
| --------------------- | ----------------- |
| robots.txt            | 站点信息          |
| crossdomain.xml       | 站点信息          |
| sitemap.xml           | 站点信息          |
| sitemap.html          | 站点信息          |
| sitemapindex.xml      | 站点信息          |
| sitemapindex.xml      | 站点信息          |
| .git/config           | git泄露           |
| .gitignore            | git泄露           |
| .svn/entries          | svn泄露           |
| .DS_Store             | mac泄露           |
| .github               | github泄露        |
| .vscode/settings.json | vscode配置        |
| .bash_history         | bash历史命令泄露  |
| nginx.conf            | nginx配置文件泄露 |
| phpinfo.php           | php信息泄露       |

#### 2.1.1.2. 其他文件

1. [路径字典](渗透测试-信息收集/路径字典.md)

## 2.2. 一些思路

1. 寻找测试业务，如test.bytedance.com
2. 寻找遗弃老版本api，如/api/v3可以尝试/api/v1
3. 泛解析问题：通过解析随机子域名进行判断

# 3. 域传送漏洞

基础信息参考[DNS](渗透测试-信息收集/DNS.md)

> DNS服务器分为：主服务器、备份服务器和缓存服务器。在主备服务器之间同步数据库，需要使用“DNS域传送”。域传送是指后备服务器从主服务器拷贝数据，并用得到的数据更新自身数据库。若DNS服务器配置不当，可能导致匿名用户获取某个域的所有记录。一般有三种方式dig，nmap，nslookup。

- dig

``` bash
# 1. 找到解析域名的dns服务器，或使用whois等
$ dig thnu.edu.cn ns
# 2. 向该服务器发送axfr请求
$ dig axfr @dns1.thnu.edu.cn thnu.edu.cn
```

- nmap

``` bash
# 已知dns服务器dns1.thnu.edu.cn
$ nmap --script dns-zone-transfer --script-args dns-zone-transfer.domain=thnu.edu.cn -p 53 -Pn dns1.thnu.edu.cn
```

- nslookup

``` bash
$ nslookup
# 1. 指定已知dns服务器dns1.thnu.edu.cn
> server dns1.thnu.edu.cn
# 2. 列出域名解析
> ls thnu.edu.cn
```

