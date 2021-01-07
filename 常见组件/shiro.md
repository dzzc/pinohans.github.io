## 组件简介

Apache Shiro是一款开源安全框架，提供身份验证、授权、密码学和会话管理。Shiro框架直观、易用，同时也能提供健壮的安全性。

Shiro提供了应用安全API，被Shiro框架开发团队成为安全四大基石的Authentication（认证）, Authorization（授权）, Session Management（会话管理）, Cryptography（加密）

- Authentication（认证）：证明用户身份，通常称之为“登录”。
- Authorization（授权）：访问控制。
- Cryptography（加密）：保护或隐藏数据，防止数据被窃取。
- Session Management（会话管理）： 管理每一个用户的会话状态。

在概念层，Shiro 架构包含三个主要的理念：Subject,SecurityManager和 Realm。

- Subject：当前用户，Subject 可以是一个人，但也可以是第三方服务、守护进程帐户、时钟守护任务或者其它–当前和软件交互的任何事件。
- SecurityManager：管理所有Subject，SecurityManager 是 Shiro 架构的核心，配合内部安全组件共同组成安全伞。
- Realms：用于进行权限信息的验证，我们自己实现。Realm 本质上是一个特定的安全 DAO：它封装与数据源连接的细节，得到Shiro 所需的相关的数据。在配置 Shiro 的时候，你必须指定至少一个Realm 来实现认证（authentication）和/或授权（authorization）。

## 漏洞列表

| 漏洞名称                                            | 漏洞ID                                               | 影响版本       | CVSS |
| --------------------------------------------------- | ---------------------------------------------------- | -------------- | ---- |
| Apache Shiro 1.2.4反序列化远程代码执行漏洞          | [CVE-2016-4437/SHIRO-550](漏洞列表/CVE-2016-4437.md) | Shiro <= 1.2.4 | 8.1  |
| Apache Shiro Padding Oracle Attack 远程代码执行漏洞 | CVE-2019-12422/SHIRO-721                             | Shiro < 1.4.2  | 7.5  |
| Apache Shiro 身份验证绕过漏洞                       | CVE-2020-1957/SHIRO-682                              | Shiro < 1.5.2  | 9.8  |
| Apache Shiro 身份验证绕过漏洞                       | CVE-2020-11989/SHIRO-782                             | Shiro < 1.5.3  | 9.8  |
| Apache Shiro 身份验证绕过漏洞                       | CVE-2020-13933                                       | Shiro < 1.6.0  | 7.5  |
| Apache Shiro 身份验证绕过漏洞（AJP协议绕过）        | SHIRO-760                                            | 基于Tomcat版本 | 无   |
| Apache Shiro < 1.2.3 身份验证绕过漏洞               | CVE-2014-0074/SHIRO-460                              | Shiro < 1.2.3  | 7.5  |

## 组件指纹

```
header="rememberMe=deleteMe"
```
