####接口
一个Java 接口（interface）是一些方法的集合。这些方法只给出了定义，没有实现。需要在具体的类里面去实现。

    public interface Test{
        public static final int num; //成员常量具有固定的修饰符：public static final
        public abstract void method; //成员函数具有固定的修饰符：public abstract 
    }

    public class Testimpl implements Test{
        // 实现接口中的所有方法
        .....
    }


####implements 和 extends 的关系
extends 是继承父类，只要那个类不是声明为final或者那个类定义为abstract的就能继承。
JAVA中不支持多重继承，但是可以用接口来实现，这样就用到了implements。
继承只能继承一个类，但implements可以实现多个接口，用逗号分开就行了，比如：

    class A extends B implements C,D,E {
        //在 A 类里实现 C，D，E 接口的具体方法
    }


####优雅地对 List 进行初始化：



####遍历map
    for (Map.Entry<Integer, Integer> entry : map.entrySet()) {
        System.out.println("Key = " + entry.getKey() + ", Value = " + entry.getValue());
    }

####去除末尾换行符
    String.trim()

#### String 转 int
    int i = Integer.parseInt(s);