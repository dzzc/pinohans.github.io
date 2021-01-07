## 1. 反射(Reflection)

反射就是Reflection，Java的反射是指程序在运行期可以拿到一个对象的所有信息。反射是为了解决在运行期，对某个实例一无所知的情况下，如何调用其方法。

### 1.1. 类

<!-- TODO -->

### 1.2. 字段

<!-- TODO -->

### 1.3. 函数

<!-- TODO -->

### 1.4. 构造函数

<!-- TODO -->

### 1.5. 继承关系

<!-- TODO -->

### 1.6. 动态代理

当使用接口时，接口不可以直接被实例化，需要通过类去实现这个接口，才可以实现对这个接口中方法的调用。而动态代理实现了不需要类，直接创建某个接口的实例，对其方法进行调用。当我们调用某个动态代理对象的方法时，都会触发代理类的invoke方法，并传递对应的内容。

#### 1.6.1. 例子

``` java
// Test.java
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;

public class Test {
    public static void main(String[] args){
            InvocationHandler handler = new InvocationHandler() {
                public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
                    System.out.println(method);
                    if (method.getName().equals("morning")) {
                        System.out.println("Good morning, " + args[0]);
                    }
                    return null;
                }
            };
            Hello hello = (Hello)Proxy.newProxyInstance(ClassLoader.getSystemClassLoader(), new Class[]{Hello.class}, handler);
            hello.morning("liming");
    }
}

// Hello.java
public interface Hello {
    void morning(String name);
}
```

1. 首先定义了一个handler，通过其实现对某个类接口的调用。
2. 接着定义了一个代理对象Hello，需要传递三个参数分别为ClassLoader、要代理的接口数组以及调用接口时触发的对应方法。
3. 此时我调用hello.morning,就会触发handler的invoke方法，并传递三个参数进去，分别为proxy即代理对象，method即调用的方法的Method对象，args即传递的参数。

所有的handler都需要实现InvocationHandler这个接口，并实现其invoke方法来实现对接口的调用。

## 2. final关键词

1. 修饰类

当用final修饰一个类时，表明这个类不能被继承。

> tips:
> 1. final类中的成员变量可以根据需要设为final，但是要注意final类中的所有成员方法都会被隐式地指定为final方法。
> 2. 除非这个类真的在以后不会用来继承或者出于安全的考虑，尽量不要将类设计为final类。

1. 修饰方法

一方面把方法锁定，以防任何继承类修改它的含义。另一方面提高效率，在早期的Java实现版本中，会将final方法转为内嵌调用。但是如果方法过于庞大，可能看不到内嵌调用带来的任何性能提升。在最近的Java版本中，不需要使用final方法进行这些优化了。

> tips:
> 1. 如果只有在想明确禁止 该方法在子类中被覆盖的情况下才将方法设置为final的。
> 2. 类的private方法会隐式地被指定为final方法。


3. 修饰变量

如果是基本数据类型的变量，则其数值一旦在初始化之后便不能更改；如果是引用类型的变量，则在对其初始化之后便不能再让其指向另一个对象。
