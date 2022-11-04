# 类设计者工具

## 面向对象程序设计

- 基类与派生类（继承）

  ```cpp
  class Person{
      //私有修饰符仅可在该类中访问，而保护修饰符可在基类和派生类中访问。
      protected:
      	string name;
  };
  
  //class ClassB:public ClassA{};
  //类B继承类A，类A为基类，类B为类A的派生类。
  class Teacher:public Person{
      public:
      	string GetName() const {return this->name;}
  	protected:
          string Subject;
  };
  ```

- 成员函数的继承

  覆盖/非覆盖

  ```cpp
  //覆盖基类定义的函数，使派生类拥有自己的版本。
  //虚函数
  class Base{
      public:
      	virtual void Func1(){cout<<"virtual func"<<endl;}	//非虚函数，可以进行动态绑定。
      	virtual void Func2()=0;								//纯虚函数，派生类中必须进行定义。
      	void Func3(){cout<<"func"<<endl;}					//静态链接的函数，派生类中重载无效。
  };
  
  ```

  

## 运算符重载、类型转换

### 函数调用运算符

operator()，像函数一样使用该类的对象。类可以储存状态，故比普通函数更加灵活。

- 函数对象

  定义了调用运算符的对象即为函数对象。
  
  ```cpp
  struct absInt{
      int operator() (int val) const{
          return val<0?-val:val;
      }
  };
  int main(void)
  {
      absInt absObj;
      cout<<absObj(-114514)<<endl;
      return 0;
  }
  ```



# 拷贝控制

拷贝、移动、赋值、销毁。

- 拷贝、赋值、销毁
- 拷贝控制、资源管理
- 

## 五种特殊成员函数

拷贝构造成员。

| 拷贝           | 移动           | 销毁     |
| -------------- | -------------- | -------- |
| 拷贝构造函数   | 移动构造函数   | 析构函数 |
| 拷贝赋值运算符 | 移动赋值运算符 |          |

- 赋值运算符不属于构造函数，带参数。



# 拷贝、赋值、销毁

拷贝构造函数、拷贝赋值运算符、析构函数。

## 拷贝构造函数

某一构造函数（无返回值）的第一个参数是自身类类型的引用（可以且一般是const的），且任何额外参数都有默认值，则该构造函数即为拷贝构造函数。

拷贝构造函数*不应该*是explicit的。

```cpp
class Foo {
public:
    Foo();
    Foo(const Foo &);	// 拷贝构造函数
};
```



### 合成的拷贝构造函数

类中没有定义拷贝构造函数时，编译器会定义一个合成的拷贝构造函数，即使已经存在其他构造函数（只有默认构造函数是当存在其他构造函数时不会合成）。

一般情况，该函数的行为是将对象中的成员逐个拷贝（调用成员类的拷贝构造函数）到创建中的对象。

- 例类

  ```cpp
  class Person {
  public:
      Person(const Person &);
  private:
      int age;
      string name;
  };
  ```
  
- 合成拷贝构造函数的等价行为

  ```cpp
  Person::Person(const Person &p)
      : age(p.age), name(p.name) {}	// 此处均为拷贝，调用了int和string的拷贝构造函数。
  ```



### 拷贝初始化

使用等号（=）或其他会调用拷贝构造函数（不包括直接初始化部分）初始化的对象。不使用等号则为直接初始化。

- 拷贝初始化与直接初始化

  ```cpp
  string dots(10, '.');			// 直接初始化
  string s(dots);					// 直接初始化，执行拷贝构造函数
  string s2 = dots;				// 拷贝初始化，拷贝赋值运算符（编译器可能会优化为直接初始化）
  string s3 = "114514";			// 拷贝初始化，
  string nines = string(100, '9');// 拷贝初始化，拷贝赋值运算符（编译器可能会优化为直接初始化）
  ```

- 其他会发生拷贝初始化的情况

  - **值语义传参，或以值语义返回对象时**

    ```cpp
    // 调用两次拷贝构造函数
    Person f(Person p) {
        return p;
    }
    ```

  - 使用初始化列表初始化一个数组中的元素，或初始化一个聚合类的成员时

- 容器的emplace方法是直接初始化，push方法是拷贝初始化

### 参数和返回值

非引用类型的参数要进行拷贝初始化，类似的，非引用类型的返回值也要进行拷贝初始化。

鉴于上述特性，拷贝构造函数的参数必须是引用类型。如果拷贝构造函数的参数为值类型，则在给拷贝构造函数传参时也需要调用拷贝构造函数，如此无限循环。

## 拷贝赋值运算符

拷贝赋值运算符接受与其所在类的相同类类型参数（值、引用均可）。

```cpp
class Foo {
public:
    Foo &operator=(const Foo &);
};
```

为了与内置类型的赋值行为保持一致，其返回值通常为该类型的引用。

### 合成的拷贝赋值运算符

一个类未定义自己的拷贝赋值运算符时，编译器会为该类生成一个**合成的拷贝赋值运算符**。

- 合成拷贝赋值运算符的等价行为

  ```cpp
  Person& Person::operator=(const Person &rhs/* rhs是指右侧引用 */)
  {
      age = rhs.age;
      name = rhs.name;
      return *this;
  }
  ```



## 析构函数

构造函数初始化对象的非static数据成员；析构函数负责释放对象使用的资源，销毁对象的非static成员。

```cpp
class Foo {
public:
    ~Foo();
};
```

- 析构函数无返回值，不接受参数

- 析构函数有一个函数体，有一个析构部分（析构部分是隐式的）

  首先执行函数体（此时仍可访问成员），然后销毁成员，成员按初始化顺序逆序销毁（执行类成员的析构函数）。

- 内置类型没有析构函数

### 析构函数调用的时机

对象被销毁时，都会自动调用其析构函数。

- 变量离开其作用域时（变量作用域一般等同于变量生命期）

- 对象销毁过程中，其成员被销毁时

- 数组被销毁过程中（包括栈上数组），其元素被销毁时（不能用free）

- 堆上对象，当delete（不是free）该对象指针时

- 临时对象，创建它的完整表达式结束时

  ```cpp
  /* ... */
  cout << "temp Foo init" << endl;
  Foo();
  cout << "temp Foo destroy" << endl;
  /* ... */
  ```



### 合成的析构函数

当一个类未定义自己的析构函数时，编译器会为它定义一个**合成的析构函数**。析构部分是隐式的。

- 等价行为

  ```cpp
  ~Foo() {}
  ```



## 三/五法则

何时需要自己定义析构函数、拷贝构造函数、拷贝赋值函数。

### 需要析构函数

此时必须自己定义拷贝构造函数、拷贝赋值函数。

### 需要拷贝构造函数

此时必须自己定义拷贝赋值函数。但不一定需要析构函数。

## 阻止拷贝

### 使用=delete的拷贝控制

声明了该函数但是不能使用该函数，通常用来阻止拷贝。

```cpp
// 使用=delete删除拷贝函数，以阻止拷贝
struct Foo {
    Foo() = default;
    Foo(const Foo&) = delete;
    Foo& operator=(const Foo&) = delete;
    ~Foo() = default;
};
```

- =delete必须出现在函数第一次声明的时候

  与=default不同。原因是需要提前让编译器知道，以便禁止试图使用它的操作；另一个原因，=default只影响成员生成的代码，直到编译器生成代码时才需要。

- =delete可以对任意函数指定

  =default只能作用于默认构造函数或者拷贝控制成员。

- 构造函数不应该是删除的成员

  此时不能销毁该类型的对象（删除的构造函数抑制栈上构造）。

  ```cpp
  struct Foo {
      Foo() = default;
      ~Foo() = delete;
  };
  Foo f;	// 不合法
  Foo *p = new Foo();	// 合法，但不能够delete
  ```



### 合成的拷贝控制成员可能是删除的

编译器会定义合成的拷贝控制成员，合成的成员有可能会被编译器定义为删除的。

如果一个类存在不能默认构造、拷贝、赋值、销毁的成员，则对应的成员函数将被定义为删除的。

- 若类的某个成员的**析构函数**是删除的或不可访问的

  则该类的**合成析构函数**被定义为删除的。

- 某个成员的**拷贝构造函数**或**析构函数**是删除的或不可访问的

  则该类的**合成的拷贝构造函数**被定义为删除的。（删除的构造函数抑制栈上构造）

- 某个成员的**拷贝赋值运算符**是删除的或不可访问的，或是类中存在const的成员或引用成员

  则该类的**合成的赋值运算符**被定义为删除的。（不能对const成员赋值）

- 某个成员的**析构函数**是删除的或不可访问的，或是类中存在没有类内初始化器的const成员且该类型未显式定义默认构造函数，或是类中存在没有类内初始化器的引用

  则该类的默认构造函数被定义为删除的。（必须对不可默认构造的成员显式初始化）

### 使用private的拷贝控制

通过将拷贝构造函数、拷贝赋值运算符声明为private的来阻止拷贝。

希望阻止拷贝的类应该使用=delete，不应该将相关函数声明为private的。

```cpp
class Foo {
    Foo(const Foo&);
    Foo& operator=(const Foo&);
};
```

- 成员函数或友元函数仍可以拷贝对象

- 用户代码不可拷贝（编译阶段）

- 若函数仅声明而没有定义

  成员函数和友元函数中的拷贝操作会导致链接错误。



# 资源管理的拷贝控制

确定该类型对象的拷贝语义，使得类的行为看起来像一个值或者像一个指针。

## 类值类

类值对象的行为像一个值，拥有自己自身的状态。拷贝一个类值对象时，副本与原对象完全独立，改变副本不会影响原对象。

### 例类

类中有一个指向数组的指针，欲使用该类封装一个由原始数组简单实现的线性表。每一个Foo对象都是独立的，Foo是一个类值类。

```cpp
class Foo {
public:
    Foo(size_t length) : arr_(new int[length]), length_(length) {}
    Foo(const Foo &f);
    Foo& operator=(const Foo &rhs);
    ~Foo() { delete p_arr_; }
private:
    int *arr_;
    size_t length_;
};
```

- 由于类中存在动态分配的资源，故需要定义析构函数释放资源。
- 由于需要构造函数，根据三/五法则，同时也需要定义拷贝构造函数、拷贝赋值运算符。

### 拷贝赋值运算符

- 需要销毁左侧运算对象的数据，并将右侧对象的数据拷贝给左侧运算对象
- 需要处理自赋值的情况（ f = f; ）

此版本通过先拷贝rhs来处理自赋值的情况。先分配空间，将rhs的数据拷贝到新空间，然后释放this的数据，再将新空间的指针赋值到this，并拷贝其他成员变量，最后返回\*this。

核心思想是，引入中间变量p，分离\*this与rhs间看似可行的直接拷贝。

```cpp
Foo& Foo::operator=(const Foo &rhs)
{
    auto p = new int[rhs.length_];
    copy(rhs.arr_, rhs.arr_ + rhs.length_, p);
    delete arr_;
    
    arr_ = p;
    length_ = rhs.length_;
    return *this;
}
```

先释放左侧对象数据再拷贝右侧对象的方式看似正确，然而它不能处理自赋值的情况。

```cpp
Foo& Foo::operator=(const Foo &rhs)
{
    // DON'T do it.
    delete arr_;
    arr_ = new int[rhs.length_];
    copy(rhs.arr_, rhs.arr_ + rhs.length_, p);
    length_ = rhs.length_;
    return *this;
}
```

## 类指针类

### 引用计数



# 交换操作

除了拷贝操作成员，管理资源的类还通常定义swap函数。

## 例类

类中有一个指向数组的指针，欲使用该类封装一个由原始数组简单实现的线性表。每一个Foo对象都是独立的，Foo是一个类值类。

```cpp
class Foo {
public:
    Foo(size_t length) : arr_(new int[length]), length_(length) {}
    Foo(const Foo &f);
    Foo& operator=(const Foo &rhs);
    ~Foo() { delete p_arr_; }
private:
    int *arr_;
    size_t length_;
};
```

## 定义swap函数

- swap是Foo的友元函数
- 声明swap为内联以优化代码

```cpp
class Foo {
    friend void swap(Foo &lhs, Foo &rhs);
};
inline void swap(Foo &lhs, Foo &rhs)
{
    using std::swap;
    swap(lhs.arr_, rhs.arr_);
    swap(lhs.length_, rhs.length_);
}
```

## 在赋值运算符中使用swap

- 此版本处理了自赋值的情况

  原版本的赋值运算符需要拷贝操作以处理自赋值的情况，此处使用传值参数的方式提供了拷贝。

- 此版本是异常安全的

  此版本仅在拷贝构造函数中可能抛出异常，发生在改变this前。

```cpp
Foo& Foo::operator=(Foo rhs)
{
    swap(*this, rhs);
    return *this;
}
```

# 对象移动

移动而非拷贝对象会大幅度提升性能。

## 右值引用和左值引用

```cpp
int &&rr = 114514;
int &lr = rr;
```



### 右值引用

- 只能绑定到一个将被销毁的对象

  字面量、表达式的运算结果、临时创建的对象等。

- 绑定对象后，被绑定对象的生命期被延长直到该右值引用被销毁，此时右值引用与左值引用无异

  右值引用可以捕获即将消逝的对象。右值引用是左值，因为右值引用是一个持久的量。

  ```cpp
  int &&rr = 90;
  int &lr = rr;	// 右值引用是左值。
  int &&rr1 = rr;	// DON'T do it.
  ```

- 右值引用绑定的对象没有其他用户

  因为右值引用只能绑定到临时对象。

### 左值引用

- 只能绑定到一个左值

  左值是指拥有持久状态的量。

### std::move()

该函数可以显式地将左值转换为右值引用类型。

```cpp
int &&rr1 = 233;
int &&rr2 = std::move(rr1);
```

## 移动构造函数和移动赋值运算符

定义移动构造函数和移动赋值运算符使得我们自己的类型支持移动操作。

#### 移动操作的行为要求

- 移后源对象须置为析构安全的状态（要保证移后源对象可析构）。
- 须保证移后源对象是仍然有效的（可以使用）。
- 移动构造函数不应该依赖于移后源对象的数据（不能对移后源对象的值进行任何假设）。

### 移动构造函数

移动构造函数不分配任何新内存，通过引用的值构造新的对象。

```cpp
Foo::Foo(Foo &&src) noexcept
    : arr_(src.arr_), length_(src.length_)
{
    src.arr_ = nullptr;
}
```

- 此函数通过拷贝src.arr\_给this-\>arr\_实现对象移动

- 此处使用noexcept承诺该函数不抛出异常

- 此处必须将src.arr_赋值为nullptr，防止资源释放

  当src离开作用域后会调用其析构函数，导致src.arr\_被释放，而delete一个nullptr是合法且安全的，什么事情也不会发生，结合函数应实现的功能，故将src.arr\_置为nullptr。

### 移动操作、标准库容器和异常

