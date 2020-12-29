## 1. 证书透明度查询

> 要向用户提供加密流量，网站必须先向可信的证书授权中心 (CA) 申请证书。然后，当用户尝试访问相应网站时，此证书即会被提供给浏览器以验证该网站。近年来，由于 HTTPS 证书系统存在结构性缺陷，证书以及签发证书的 CA 很容易遭到入侵和操纵。Google 的证书透明度项目旨在通过提供一个用于监测和审核 HTTPS 证书的开放式框架，来保障证书签发流程安全无虞。 -- google

1. crtsh: https://crt.sh
2. facebook: https://developers.facebook.com/tools/ct
3. entrust: https://www.entrust.com/ct-search
4. certspotter: https://sslmate.com/certspotter/api
5. spyse: https://spyse.com/search/certificate
6. censys: https://censys.io/certificates
7. google: https://google.com/transparencyreport/https/ct

## 2. 网络空间搜索引擎

1. fofa: https://fofa.so
2. shodan: https://www.shodan.io
3. zoomeye: https://www.zoomeye.org
4. binaryedge: https://app.binaryedge.io/services/domains

### 2.1. 搜索技巧

```bash
# 较为准确的方式，如搜索域名domain、证书cert
domain='qq.com'
cert='9569783962220322900207065437'

# 不太准确的方式，如搜索title、body中的内容
title="腾讯"
body="腾讯"

# ==等符号准确查找
domain='qq.com' && app='shiro'
```

### 2.2. fofa

直接输入查询语句，将从标题，html 内容，http 头信息，url 字段中搜索，其他语法如下表：

| 例句                                | 用途说明                                                 | 注                                                            |
| ----------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------- |
| title="beijing"                     | 从标题中搜索“北京”                                       | -                                                             |
| header="jboss"                      | 从 http 头中搜索“jboss”                                  | -                                                             |
| body="Hacked by"                    | 从 html 正文中搜索 abc                                   | -                                                             |
| domain="qq.com"                     | 搜索根域名带有 qq.com 的网站。                           | -                                                             |
| icon_hash="-247388890"              | 搜索使用此 icon 的资产。                                 | 仅限高级会员使用                                              |
| host=".gov.cn"                      | 从 url 中搜索”.gov.cn”                                   | 搜索要用 host 作为名称                                        |
| port="443"                          | 查找对应“443”端口的资产                                  | -                                                             |
| ip="1.1.1.1"                        | 从 ip 中搜索包含“1.1.1.1”的网站                          | 搜索要用 ip 作为名称                                          |
| ip="220.181.111.1/24"               | 查询 IP 为“220.181.111.1”的 C 网段资产                   | -                                                             |
| status_code="402"                   | 查询服务器状态为“402”的资产                              | -                                                             |
| protocol="https"                    | 查询 https 协议资产                                      | 搜索指定协议类型(在开启端口扫描的情况下有效)                  |
| city="Hangzhou"                     | 搜索指定城市的资产。                                     | -                                                             |
| region="Zhejiang"                   | 搜索指定行政区的资产。                                   | -                                                             |
| country="CN"                        | 搜索指定国家(编码)的资产。                               | -                                                             |
| cert="google"                       | 搜索证书(https 或者 imaps 等)中带有 google 的资产。      | -                                                             |
| banner=users && protocol=ftp        | 搜索 FTP 协议中带有 users 文本的资产。                   | -                                                             |
| type=service                        | 搜索所有协议资产，支持 subdomain 和 service 两种。       | 搜索所有协议资产                                              |
| os=windows                          | 搜索 Windows 资产。                                      | -                                                             |
| server=="Microsoft-IIS/7.5"         | 搜索 IIS 7.5 服务器。                                    | -                                                             |
| app="HIKVISION-视频监控"            | 搜索海康威视设备                                         | -                                                             |
| after="2017" && before="2017-10-01" | 时间范围段搜索                                           | -                                                             |
| asn="19551"                         | 搜索指定 asn 的资产。                                    | -                                                             |
| org="Amazon.com, Inc."              | 搜索指定 org(组织)的资产。                               | -                                                             |
| base_protocol="udp"                 | 搜索指定 udp 协议的资产。                                | -                                                             |
| is_ipv6=true                        | 搜索 ipv6 的资产                                         | 搜索 ipv6 的资产,只接受 true 和 false。                       |
| is_domain=true                      | 搜索域名的资产                                           | 搜索域名的资产,只接受 true 和 false。                         |
| ip_ports="80,161"                   | 搜索同时开放 80 和 161 端口的 ip                         | 搜索同时开放 80 和 161 端口的 ip 资产(以 ip 为单位的资产数据) |
| port_size="6"                       | 查询开放端口数量等于"6"的资产                            | 仅限 FOFA 会员使用                                            |
| port_size_gt="3"                    | 查询开放端口数量大于"3"的资产                            | 仅限 FOFA 会员使用                                            |
| port_size_lt="12"                   | 查询开放端口数量小于"12"的资产                           | 仅限 FOFA 会员使用                                            |
| ip_country="CN"                     | 搜索中国的 ip 资产(以 ip 为单位的资产数据)。             | 搜索中国的 ip 资产                                            |
| ip_region="Zhejiang"                | 搜索指定行政区的 ip 资产(以 ip 为单位的资产数据)。       | 搜索指定行政区的资产                                          |
| ip_city="Hangzhou"                  | 搜索指定城市的 ip 资产(以 ip 为单位的资产数据)。         | 搜索指定城市的资产                                            |
| ip_after="2019-01-01"               | 搜索 2019-01-01 以后的 ip 资产(以 ip 为单位的资产数据)。 | 搜索 2019-01-01 以后的 ip 资产                                |
| ip_before="2019-07-01"              | 搜索 2019-07-01 以前的 ip 资产(以 ip 为单位的资产数据)。 | 搜索 2019-07-01 以前的 ip 资产                                |

## 3. 普通搜索引擎

1. baidu: https://www.baidu.com
2. bing: https://cn.bing.com
3. google: https://www.google.cn

### 3.1. google

```bash
# 搜索jd.com子域名，排除www子域名
site:jd.com  -www
# 搜索c段
site:x.x.x.*
```

## 4. 威胁情报搜索引擎

1. 微步: https://x.threatbook.cn/
2. alienvault: https://otx.alienvault.com/
3. riskiq: https://www.riskiq.com/
4. threatminer: https://www.threatminer.org/
5. virustotal: https://www.virustotal.com/gui/home/search

## 5. 代码仓库

1. github: https://github.com
2. 阿里云: https://code.aliyun.com
3. 码云: https://gitee.com

### 5.1. 泄露内容

1. 口令
2. 邮箱
3. api

## 6. 网盘

1. 百度网盘: https://pan.baidu.com
2. google 网盘: https://www.google.cn/drive/apps.html

### 6.1. 百度网盘检索工具

1. www.dashengpan.com

## 7. 记录

1. ★ ip138：https://site.ip138.com/{domain}/domain.htm
2. ★ 百度云观测：http://ce.baidu.com/index/getRelatedSites?site_address={domain}
3. ★ hackertarget：https://hackertarget.com/find-dns-host-records
4. riddler：https://riddler.io/search?q=pld:{domain}
5. bufferover：https://dns.bufferover.run/dns?q={domain}
6. ★ dnsdb：https://dnsdb.io/zh-cn/search?q={domain}
7. ipv4info：http://ipv4info.com
8. robtex：https://www.robtex.com/dns-lookup
9. chinaz：https://alexa.chinaz.com
10. ★ netcraft：https://searchdns.netcraft.com
11. dnsdumpster：https://dnsdumpster.com
12. sitedossier：http://www.sitedossier.com
13. ★ findsubdomains：https://findsubdomains.com/

## 8. 证书内容泄露

证书指明domain范围等信息

## 9. 终端程序

1. mobile: apk、ipa
2. pc: exe、elf、Mach-O
