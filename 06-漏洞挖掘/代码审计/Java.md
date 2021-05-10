## 1. 代码漏洞

### 1.1. 任意文件读写(文件上传、文件下载)、文件遍历、文件删除、文件重命名等漏洞
### 1.2. SQL注入漏洞

| 特征                                  | 漏洞触发                                                                           | 修复          |
| ------------------------------------- | ---------------------------------------------------------------------------------- | ------------- |
| `request.getParameter(`, `String sql` | 字符串拼接                                                                         | 做好过滤      |
| `Order by`, `from`                    | 字符串拼接，无法预编译                                                             | 做好过滤      |
| `prepareStatement`                    | 预编译使用有误，在使用占位符后未进行`setObject`或者`setInt`或者`setString`。       | -             |
| `mybatis` 搜索 `$`                    | `#{}`会进行过滤，`${}`不会进行过滤，如`like '%${x}%'`, `in(${x})`, `order by ${x}` | 尽量使用`#{}` |

### 1.3. XXE(XML实体注入攻击)

流程

1. 判断使用哪种XML解析器
2. 搜索是否有禁用外部实体配置
3. 是否有外部输入点进行解析

各种xml解析器禁用外部实体配置

``` java
// 1. saxReader
saxReader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true); 
saxReader.setFeature("http://xml.org/sax/features/external-general-entities", false); 
saxReader.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

// 2. saxBuilder
SAXBuilder builder = new SAXBuilder(); 
builder.setFeature("http://apache.org/xml/features/disallow-doctype-decl",true); 
builder.setFeature("http://xml.org/sax/features/external-general-entities", false); 
builder.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

// 3. saxTransformerFactory
Document doc = builder.build(new File(fileName));
SAXTransformerFactory sf = SAXTransformerFactory.newInstance();
sf.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
sf.setAttribute(XMLConstants.ACCESS_EXTERNAL_STYLESHEET, ""); 
sf.newXMLFilter(Source);
// Note: Use of the following XMLConstants requires JAXP 1.5, which was added to Java in 7u40 and Java 8: 
javax.xml.XMLConstants.ACCESS_EXTERNAL_DTD
javax.xml.XMLConstants.ACCESS_EXTERNAL_SCHEMA
javax.xml.XMLConstants.ACCESS_EXTERNAL_STYLESHEET

// 4. schemaFactory
SchemaFactory factory = SchemaFactory.newInstance("http://www.w3.org/2001/XMLSchema");
factory.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
factory.setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
Schema schema = factory.newSchema(Source);

// 5. xmlInputFactory
xmlInputFactory.setProperty(XMLInputFactory.SUPPORT_DTD, false); // This disables DTDs entirely for that factory
xmlInputFactory.setProperty("javax.xml.stream.isSupportingExternalEntities", false); // disable external entities

// 6. xmlReader
XMLReader reader = XMLReaderFactory.createXMLReader(); 
reader.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true); 
// This may not be strictly required as DTDs shouldn't be allowed at all, per previous line.
reader.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false); 
reader.setFeature("http://xml.org/sax/features/external-general-entities", false); 
reader.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

// 7. XPathExpression
DocumentBuilderFactory df = DocumentBuilderFactory.newInstance();
df.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
df.setAttribute(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");
DocumentBuilder builder = df.newDocumentBuilder();
String result = new XPathExpression().evaluate( builder.parse(new ByteArrayInputStream(xml.getBytes())) );

// 8. transformerFactory
TransformerFactory tf = TransformerFactory.newInstance();
tf.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
tf.setAttribute(XMLConstants.ACCESS_EXTERNAL_STYLESHEET, "");

// 9. Validator
SchemaFactory factory = SchemaFactory.newInstance("http://www.w3.org/2001/XMLSchema"); 
Schema schema = factory.newSchema();
Validator validator = schema.newValidator(); 
validator.setProperty(XMLConstants.ACCESS_EXTERNAL_DTD, "");
validator.setProperty(XMLConstants.ACCESS_EXTERNAL_SCHEMA, "");

// 10. Unmarshaller
SAXParserFactory spf = SAXParserFactory.newInstance(); 
spf.setFeature("http://xml.org/sax/features/external-general-entities", false);
spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
spf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false); 
Source xmlSource = new SAXSource(spf.newSAXParser().getXMLReader(), new InputSource(new StringReader(xml)));
JAXBContext jc = JAXBContext.newInstance(Object.class);
Unmarshaller um = jc.createUnmarshaller();
um.unmarshal(xmlSource);
```

利用

``` xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE replace [<!ENTITY test SYSTEM "file:///tmp/flag">]>
<msg>&test;</msg>
```

burpsuite插件collaborator

### 1.4. 表达式执行(SpEL、OGNL、MVEL2、EL等)

| 特征                   | 漏洞触发                       | 修复 |
| ---------------------- | ------------------------------ | ---- |
| `SpelExpressionParser` | 用户可控的SpelExpressionParser | -    |

利用

``` java
// SpelExpressionParser
String el="T(java.lang.Runtime).getRuntime().exec(\"open /tmp\")";
ExpressionParser PARSER = new SpelExpressionParser();
Expression exp = PARSER.parseExpression(el);
System.out.println(exp.getValue());
```

### 1.5. 系统命令执行漏洞(ProcessBuilder)
### 1.6. 反序列化攻击(ObjectInputStream、JSON、XML等)
### 1.7. Java反射攻击
### 1.8. SSRF攻击

常见特征函数

- HttpClient.execute
- HttpClient.executeMethod
- HttpURLConnection.connect
- HttpURLConnection.getInputStream
- URL.openStream

常用协议

- file
- ftp
- http
- https
- jar
- mailto
- netdoc

修复

- 使用白名单校验HTTP请求url地址
- 避免将请求响应及错误信息返回给用户
- 禁用不需要的协议及限制请求端口,仅仅允许http和https请求等

### 1.9. XSS

| 特征                    | 漏洞触发               | 修复             |
| ----------------------- | ---------------------- | ---------------- |
| `request.getParameter(` | 未做转译或编码直接使用 | 处理好转译或编码 |

### 1.10. csrf

| 特征       | 漏洞触发                                                                            | 修复                     |
| ---------- | ----------------------------------------------------------------------------------- | ------------------------ |
| `session[` | 一些增删改查方法，是否进行Referer头检验、token检验 无法构造的随机数参数、验证码密码 | Referer头检验、token检验 |

## 2. 业务漏洞
