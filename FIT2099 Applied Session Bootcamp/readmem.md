



![image-20250819111828243](readmem.assets/image-20250819111828243.png)



![image-20250819112016339](readmem.assets/image-20250819112016339.png)



![image-20250819111923559](readmem.assets/image-20250819111923559.png)



![image-20250819112113596](readmem.assets/image-20250819112113596.png)



![image-20250819112047669](readmem.assets/image-20250819112047669.png)

![image-20250819112131462](readmem.assets/image-20250819112131462.png)



![image-20250819112213003](readmem.assets/image-20250819112213003.png)



![image-20250819112303856](readmem.assets/image-20250819112303856.png)

![image-20250819112314849](readmem.assets/image-20250819112314849.png)





![image-20250819112229765](readmem.assets/image-20250819112229765.png)

![image-20250819112327310](readmem.assets/image-20250819112327310.png)

具体类（Concrete Class）和抽象类（Abstract Class）是面向对象编程中的两个核心概念，二者在设计和功能上有明显的区别。以下是它们的主要区别：

### 1. **定义**

- **具体类（Concrete Class）**：是一个可以被实例化的类，包含了所有方法的完整实现。在一个具体类中，所有的方法都有定义，可以直接创建对象。
- **抽象类（Abstract Class）**：是不能被直接实例化的类，它只能作为其他类的基类。抽象类中可以有一些方法是**抽象方法**，即没有方法体的，需要由子类来实现。

### 2. **方法实现**

- **具体类**：所有方法都有具体的实现。
- **抽象类**：可以包含抽象方法（没有实现的，仅声明的方法），也可以包含已经实现的方法。抽象方法必须在子类中实现。

### 3. **实例化**

- **具体类**：可以直接创建对象。
- **抽象类**：不能直接创建对象，只能通过继承来创建子类。

### 4. **使用场景**

- **具体类**：通常是开发完成的类，能够直接使用。
- **抽象类**：用于作为基类，提供统一的接口和部分实现，子类继承后可以按需补充或重写方法。

### 示例：

```java
// 具体类示例
class Car {
    void drive() {
        System.out.println("Car is driving");
    }
}

// 抽象类示例
abstract class Vehicle {
    abstract void move();  // 抽象方法
    void fuel() {           // 具体方法
        System.out.println("Vehicle is fueled");
    }
}
```

- **Car** 是具体类，可以直接实例化并调用 `drive` 方法。
- **Vehicle** 是抽象类，不能直接实例化，但它的 `fuel` 方法可以被继承和调用，而 `move` 方法必须由子类实现。

------

你提到的例子中，可能需要根据 **Action** 类的需求来决定是创建一个抽象类，还是使用具体类。比如：

- **如果 Action 是一个通用的基类**，且每种具体的 Action 都需要有不同的实现，通常会定义为**抽象类**，并在子类中实现 `execute()` 等方法。
- **如果 Action 是某种具体的操作，并且不再需要扩展或重写方法**，那么它可以是一个**具体类**。

希望这有助于理解具体类和抽象类的区别！如果你需要更深入的解析或代码示例，可以继续询问！

![image-20250819112340362](readmem.assets/image-20250819112340362.png)

![image-20250819112524897](readmem.assets/image-20250819112524897.png)

![image-20250819112534578](readmem.assets/image-20250819112534578.png)

![image-20250819112549723](readmem.assets/image-20250819112549723.png)

![image-20250819221637027](readmem.assets/image-20250819221637027.png)



![image-20250819112603661](readmem.assets/image-20250819112603661.png)

![image-20250819112616647](readmem.assets/image-20250819112616647.png)

![image-20250819112626331](readmem.assets/image-20250819112626331.png)

![image-20250819112636055](readmem.assets/image-20250819112636055.png)

![image-20250819112743580](readmem.assets/image-20250819112743580.png)

![image-20250819112814239](readmem.assets/image-20250819112814239.png)



![image-20250819112713406](readmem.assets/image-20250819112713406.png)

![image-20250819112830421](readmem.assets/image-20250819112830421.png)

![image-20250819112842335](readmem.assets/image-20250819112842335.png)



![image-20250819112855932](readmem.assets/image-20250819112855932.png)

![image-20250819112936712](readmem.assets/image-20250819112936712.png)

![image-20250819112946133](readmem.assets/image-20250819112946133.png)

![image-20250819112958371](readmem.assets/image-20250819112958371.png)

![image-20250819113037403](readmem.assets/image-20250819113037403.png)

![image-20250819113051070](readmem.assets/image-20250819113051070.png)

![image-20250819113103702](readmem.assets/image-20250819113103702.png)

![image-20250819113114602](readmem.assets/image-20250819113114602.png)

![image-20250819113157636](readmem.assets/image-20250819113157636.png)

![image-20250819113217483](readmem.assets/image-20250819113217483.png)

![image-20250819113229838](readmem.assets/image-20250819113229838.png)

![image-20250819113314208](readmem.assets/image-20250819113314208.png)

![image-20250819113324515](readmem.assets/image-20250819113324515.png)

![image-20250819113336125](readmem.assets/image-20250819113336125.png)

![image-20250819113410361](readmem.assets/image-20250819113410361.png)

![image-20250819113418654](readmem.assets/image-20250819113418654.png)

![image-20250819113429476](readmem.assets/image-20250819113429476.png)

![image-20250819113505682](readmem.assets/image-20250819113505682.png)

![image-20250819113513351](readmem.assets/image-20250819113513351.png)

![image-20250819113535092](readmem.assets/image-20250819113535092.png)

![image-20250819113626780](readmem.assets/image-20250819113626780.png)

![image-20250819113636100](readmem.assets/image-20250819113636100.png)

![image-20250819113722394](readmem.assets/image-20250819113722394.png)

![image-20250819113734673](readmem.assets/image-20250819113734673.png)

![image-20250819113744376](readmem.assets/image-20250819113744376.png)

![image-20250819113835330](readmem.assets/image-20250819113835330.png)

![image-20250819113848536](readmem.assets/image-20250819113848536.png)









第一个ppt



![image-20250819180625546](readmem.assets/image-20250819180625546.png)

![image-20250819180727427](readmem.assets/image-20250819180727427.png)

![image-20250819180741366](readmem.assets/image-20250819180741366.png)

![image-20250819181011156](readmem.assets/image-20250819181011156.png)

![image-20250819181019887](readmem.assets/image-20250819181019887.png)





![image-20250819181030671](readmem.assets/image-20250819181030671.png)

![image-20250819181114518](readmem.assets/image-20250819181114518.png)

![image-20250819181121871](readmem.assets/image-20250819181121871.png)

![image-20250819181133557](readmem.assets/image-20250819181133557.png)

![image-20250819181216355](readmem.assets/image-20250819181216355.png)

![image-20250819181228757](readmem.assets/image-20250819181228757.png)

![image-20250819181238543](readmem.assets/image-20250819181238543.png)



![image-20250819181345520](readmem.assets/image-20250819181345520.png)



![image-20250819181407349](readmem.assets/image-20250819181407349.png)



![image-20250819181317597](readmem.assets/image-20250819181317597.png)

![image-20250819181420175](readmem.assets/image-20250819181420175.png)

![image-20250819181431097](readmem.assets/image-20250819181431097.png)

![image-20250819181536711](readmem.assets/image-20250819181536711.png)



![image-20250819181551390](readmem.assets/image-20250819181551390.png)

、





![image-20250819181456037](readmem.assets/image-20250819181456037.png)

![image-20250819181603991](readmem.assets/image-20250819181603991.png)

![image-20250819181612749](readmem.assets/image-20250819181612749.png)



![image-20250819181621666](readmem.assets/image-20250819181621666.png)

![image-20250819181714950](readmem.assets/image-20250819181714950.png)

![image-20250819181725608](readmem.assets/image-20250819181725608.png)





![image-20250819181646077](readmem.assets/image-20250819181646077.png)

![image-20250819181735421](readmem.assets/image-20250819181735421.png)

![image-20250819181747379](readmem.assets/image-20250819181747379.png)

![image-20250819181854910](readmem.assets/image-20250819181854910.png)



![image-20250819181903435](readmem.assets/image-20250819181903435.png)



![image-20250819181819717](readmem.assets/image-20250819181819717.png)

![image-20250819181914172](readmem.assets/image-20250819181914172.png)

![image-20250819181927299](readmem.assets/image-20250819181927299.png)

![image-20250819182030852](readmem.assets/image-20250819182030852.png)

![image-20250819182040955](readmem.assets/image-20250819182040955.png)

![image-20250819181959021](readmem.assets/image-20250819181959021.png)

![image-20250819182049810](readmem.assets/image-20250819182049810.png)

![image-20250819182057439](readmem.assets/image-20250819182057439.png)

![image-20250819182145028](readmem.assets/image-20250819182145028.png)

![image-20250819182155037](readmem.assets/image-20250819182155037.png)