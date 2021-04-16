## 1. 基本信息

由于大量的生产环境中都会导入这个包，所以此包中的众多反序列化链已经成为经典链条。

CommonsCollections2利用链影响范围为
- commons-collections4 == 4.0

## 2. 分析

CommonsCollections2如果从漏洞触发位置向前逆推入口，可以更好地理解这个漏洞，也是比较经典的漏洞挖掘思路。

### 2.1. 漏洞成因

#### 2.1.1. 后半部分

这部分使用了class对象生成时自动执行static模块代码，具体使用了`com.sun.org.apache.xalan.internal.xsltc.trax.TemplatesImpl`类中使用loader.defineClass将bytecodes还原为Class后，调用了类实力化函数，因此触发static模块代码，从而进行漏洞利用。其中涉及到javassit的基础知识。

#### 2.1.2. 中间部分
#### 2.1.3. 前半部分


### 2.2. 触发过程

### 2.3. 调用栈

### 2.4. 修复

## 3. 复现
