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
- 交换操作
- 对象移动

## 五种特殊成员函数

称为拷贝构造成员。

| 拷贝           | 移动           | 销毁     |
| -------------- | -------------- | -------- |
| 拷贝构造函数   | 移动构造函数   | 析构函数 |
| 拷贝赋值运算符 | 移动赋值运算符 |          |

- 赋值运算符不属于构造函数，有返回值，没有初始化列表。



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

  则该类的**合成的赋值运算符**被定义为删除的。（保持不能对const成员赋值的语义）

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

### 类值类的拷贝赋值运算符

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

## 标准库的std::swap()

对任何类型都适用，需要进行一次拷贝和两次赋值。

```cpp
// 可能的版本。
template<T> 
void swap(T& t1, T &t2)
{
    T temp = t1;
    t1 = t2;
    t2 = temp;
}
```



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

## 定义自己的swap函数

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

## 在赋值运算符中使用交换操作

使用了名为**拷贝并交换**的技术。

- 此版本不传引用参数而改为传值参数，完成了右侧对象的拷贝

  之后将拷贝的副本rhs与\*this交换（swap）即可。如果拷贝的类没有定义自己的swap函数，则会使用std::swap（存在一次拷贝， 两次赋值），此时总共会进行两次拷贝，性能不如传引用参数的赋值运算符。

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

- 只能绑定到一个将被销毁的对象（右值）

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
  
- 右值引用不能绑定到一个左值

  ```cpp
  int &&rr = 1;
  int &&nrr = rr;	// rr 是一个左值，nrr 不能绑定到 rr。
  ```

### 左值引用

- 只能绑定到一个左值

  左值是指拥有持久状态的量。
  
- 左值引用不能绑定到一个右值

### 调用std::move()显式转换为右值

该函数可以显式地将左值转换为右值引用类型。需要使用标准库的std::move()，而不使用::move()。

```cpp
int &&rr1 = 233;
int &&rr2 = std::move(rr1);
```

## 移动构造函数和移动赋值运算符

定义移动构造函数和移动赋值运算符使得我们自己的类型支持移动操作。

### 移动操作的行为要求

析构安全、保持有效。

- 移后源对象须置为析构安全的状态（要保证移后源对象可析构）。
- 须保证移后源对象是仍然有效的（可以使用）。
- 移动构造函数不应该依赖于移后源对象的数据（不能对移后源对象的值进行任何假设）。

通常情况下，移动操作需要是noexcept的。

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

通过使用noexcept关键字通知标准库，移动操作保证不抛出异常。

- 移动操作通常不会抛出异常，但是抛出异常是允许的。

- 标准库容器对异常发生时自身的行为提供保障

  如调用push_back时若发生异常，自身不会发生改变。

#### 移动操作不应该抛出异常的原因

需要保证即使发生异常，源对象和构造对象自身都不会发生改变。

- 考虑一个拷贝构造函数在构造时抛出异常

  拷贝源对象不会发生改变，而对于新分配而未构造的空间直接释放即可。

- 考虑一个移动构造函数在移动的过程中发生异常

  移动源对象和新构造对象都发生了改变。

故如果移动构造函数不保证不抛出异常，只需要将所有移动操作改为拷贝操作即可保证源对象和构造对象自身都不会发生改变。

- 使用拷贝构造函数代替移动构造函数几乎总是安全的。

标准库需要知道移动构造函数是否会抛出异常，然后根据是否抛出异常来决定是否需要将移动操作适配为拷贝操作。

### 移动赋值运算符

- 需要标记为noexcept，需要满足移动操作的行为要求，理由如上。
- 对于移动赋值运算符，还需要处理自赋值的情况。

```cpp
Foo& Foo::operator=(Foo &&rhs) noexcept	// 保证不抛出异常
{
    if(this != &rhs) {
        delete arr_;			// 不能先赋值指针再释放资源
        arr_ = rhs.arr_;		// 移动资源
        length_ = rhs.length_;
        rhs.arr_ = nullptr;		// rhs析构安全的保证
    }
}
```

### 合成的移动操作

与拷贝操作的合成条件大不相同。只有当一个类没有定义任何自己版本的拷贝控制（拷贝构造函数、拷贝赋值运算符、析构函数）成员，并且每一个非static的成员都可以移动（有移动操作的类类型成员）时，编译器才会合成移动构造函数或移动赋值运算符。

```cpp
struct A {
    int i;
    std::string s;
};
struct B {
    A a;
};
A a1, a2 = std::move(a1);	// 使用合成的移动构造函数
B b1, b2 = std::move(b1);	// 使用合成的移动构造函数
```

合成的移动操作可能是删除的（=delete），原则与合成拷贝操作何时定义为删除类似，但是如果显式要求编译器生成default的移动操作，且编译器不能移动所有成员，则编译器会将移动操作定义为删除的函数。

移动构造函数被定义为删除的条件：

- 与拷贝构造不一致的情况。

- 类成员不可移动，或类成员是 const 的，或类成员是引用。
- 类的析构函数是删除的或是不可访问的。

```cpp
// A定义了拷贝构造函数但没有定义自己的移动构造函数。
struct NoMove {
    NoMove() = default;
    NoMove(NoMove &&) = default;
    A a;	// 此时NoMove存在不可移动的对象。
};
NoMove n1, n2 = std::move(n1);	// 错误，NoMove的移动构造函数是删除的。
```

如果类定义了一个移动构造函数或一个移动赋值运算符，则该类的合成拷贝构造函数和拷贝赋值运算符会被定义为删除的。

### 移动构造函数与拷贝构造函数的函数匹配

```cpp
Foo f1, f2;
f1 = f2;	// f2为左值，使用拷贝赋值。f2不会隐式转换为右值引用，不会匹配到移动赋值版本。
f2 = Foo();	// Foo()为右值，使用移动赋值。
```

- 不能隐式地将一个右值引用绑定到一个左值（可以显式使用move将左值转换为右值）。

- 可以将Foo&&转换为const Foo&。故若没有移动构造函数，右值也会被拷贝。

  ```cpp
  // Foo存在拷贝构造函数，未定义移动构造函数。
  Foo f1, f2;
  f1 = std::move(f2);	// 使用拷贝构造函数。由于Foo不存在移动构造函数，Foo&&转换为const Foo&，匹配到了拷贝构造函数。
  ```

### 可以分别匹配左值右值的赋值运算符

运用拷贝/移动构造函数、交换操作。

```cpp
// Foo存在拷贝构造函数、移动构造函数。
Foo& Foo::operator=(Foo rhs) { swap(*this, rhs); return *this; }
```

定义上述版本的赋值运算符的条件下，考虑以下例子

```cpp
Foo f1, f2;
f1 = f2;			// 1
f1 = std::move(f2);	// 2
```

第一次赋值中，f2是左值，传参给rhs时（本质上是rhs对象的构造）会调用拷贝构造函数。

第二次赋值中，std::move(f2)是右值，传参给rhs时会调用移动构造函数。

结合**拷贝并交换**技术，处理了自赋值的情况，并且函数是异常安全的。

## 移动迭代器

调用标准库的make\_move\_iterator将一个普通迭代器转换为一个移动迭代器。

```cpp
vector<int> v(10, 0);
auto i = make_move_iterator(v.begin());
int &&rri = *i;
```

对移动迭代器解引用会返回一个右值引用。

### 应用到uninitialized_copy()

结合移动迭代器，将对象移动到为构造的内存中。



## 右值引用和成员函数

### 为成员函数同时提供拷贝和移动版本

考虑以下情况。

```cpp
Container<T> c;
c.push_back(T());
T t;
c.push_back(t);
```

push_back的一个可行版本。

```cpp
void push_back(T &&rr)
{
    *next++ = rr;
}
void push_back(const T &lr)
{
    *next++ = lr;
}
```

### 右值和左值引用成员函数

我们可能希望在类中阻止对右值进行赋值的行为。

```cpp
Foo f1, f2;
f1 + f2 = Foo();
```

#### 引用限定符

类似const限定符的位置。

引入引用限定符可以强制左侧运算对象（\*this）。用&限定\*this为左值，用&&限定\*this为右值。

```cpp
class Foo {
public:
    Foo& Foo::operator=(const Foo &rhs) &；    
};
```

引用限定符可以与const限定符同时使用。引用限定符必须跟随在const限定符后面。

```cpp
class Foo {
    Foo aFunc() & const;	// 错误的
    Foo bFunc() const &;	// 正确的
};
```

#### 重载与引用限定符

类似const限定符可以区分重载版本，引用限定符也可以。

考虑一个线性容器类Foo，我们希望有一个成员函数sorted()来返回已经排序好的元素的副本。

```cpp
class Foo {
public:
    Foo sorted() &&;
    Foo sorted() const &;
private:
    vector<int> data;
};
```

假设没有限定\*this的限定符，一个可行的版本如下。

```cpp
Foo sorted() const
{
    Foo temp(*this);
    sort(temp.data.begin(), temp.data.end());
    return temp;
};
```

现在存在引用限定符，我们可以处理两种情况。当\*this是右值，我们无需拷贝一个Foo，直接对this->data进行排序即可。

```cpp
Foo sorted() && 
{
    sort(data.begin(), data.end());
    return *this;
}
```

```cpp
Foo sorted() const &
{
    return Foo(*this).sorted();
}
```



- 与const限定符不同，如果需要重载两个或两个以上具有相同参数列表的成员函数，要么都加上引用限定符，要么都不加。

  ```cpp
  using Comp = bool(const int&, const int&);
  Foo Foo::sorted(Comp*);
  Foo Foo::sorted(Comp*) const;
  
  Foo Foo::sorted() &&;
  Foo Foo::sorted() const;	// 错误，必须都加上引用限定符。
  ```




# 重载运算与类型转换

## 重载运算符的基本概念

- 非成员的重载运算符的参数数量与该运算符作用的运算对象的数量一样多。

  成员的重载运算符的参数数量会少一个，左侧运算对象固定为 \*this，与赋值运算符完全一致。

- 除了函数调用运算符 `operator()` 之外，其他重载运算符不能含有默认实参。

  无法改变用于内置类型的运算符的含义。

- 对于一个运算符，它要么是类的成员，要么至少含有一个类类型的参数

  ```cpp
  int operator+(int, int);	// 错误的，不能重载内置的运算符
  ```

- 重载运算符的优先级和结合律与对应的内置运算符保持一致。

### 调用重载运算符

- 非成员运算符的等价调用

  ```cpp
  data1 + data2;
  operator+(data1, data2);
  ```

- 成员运算符的等价调用

  ```cpp
  data1 += data2;
  data1.operator+=(data2);
  ```

### 赋值和复合赋值运算符

- 赋值后，左侧对象的值与右侧对象的值相等，并且应返回左侧运算对象的一个引用。
- 如果含有算术运算符或位运算符，最好也应该提供对应的复合赋值运算符（先 + 后 =）。

### 作为成员或是非成员

- `=` 、`[]` 、`()`、`->` 必须是成员。
- 复合赋值运算符一般应该是成员，但不是必须的，与赋值不同。
- 改变对象状态的运算符或者与给定类型密切相关的运算符，如递增、递减、解引用，通常应该是成员。
- 具有对称性的运算符**可能转换任意一端**的运算对象，如算术、关系、位运算符等，通常应该是非成员。

当运算符是成员函数时，左侧运算对象必须时所属类的一个对象。

```cpp
string s;
string t = s + "wa";	// 正确的，等价于s.operator+("wa")
string u = "wa" + s;	// 如果+是string的成员，则是错误的，等价于"wa".opereator+(s)。
```

若将上例的 `operator+` 定义为非成员函数，则等价于 `operator+("wa", s)` 每个实参都能被转为成形参类型。唯一要求的是至少有一个运算对象是类类型（不能改变内置运算符的含义），并且两个运算对象都能准确无误地转换成 string。

## 输入和输出运算符

- 输入输出运算符必须是非成员函数

  否则左侧运算对象必须是该类的一个对象。

  ```cpp
  cout << stuff;
  stuff << cout;	// 导致必须如此调用
  ```

### 输出运算符

```cpp
class Person {
public:
    string& name();
    int& age();
private:
    string name_;
    int age_;
};
ostream& operator<<(ostream &os, const Person &item)
{
    os << "{ name: " << item.name() << ", age: " << item.age() << " }";
    return os;
}
```

- 第一个形参是 ostream 对象的引用，输出时会改变 osream 的状态，并且该对象无法拷贝。
- 第二个形参时希望打印的类类型，打印不会改变对象的内容。

## 算术和关系运算符

### 算术运算符

如果需要定义算术运算符，则一般也会定义对应的复合赋值运算符。算术运算符一般为非成员。

```cpp
Stuff operator+(const Stuff &lhs, const Stuff &rhs)
{
    return Stuff(lhs) += rhs;
}
```

### 相等运算符

```cpp
bool operator==(const Person &lhs, const Person &rhs)
{
    return lhs.name() == rhs.name() &&
        lhs.age() == rhs.age();
}
bool operator!=(const Person &lhs, const Person &rhs)
{
    return !(lhs == rhs);
}
```

- 相等运算符应该具有传递性

  a == b，b == c，则 a == c。

- 定义了 `==`，也应该定义 `!=`。

- 相等和不相等运算符的工作应该委托给另一个。

## 赋值运算符

### 例类

```cpp
class Foo {
public:
    Foo(size_t length) : arr_(new int[length]), length_(length) {}
    Foo(const Foo &f);
    Foo& operator=(const Foo &rhs);
    Foo& operator=(initializer_list<int> il)
    ~Foo() { delete p_arr_; }
private:
    int *arr_;
    size_t length_;
};
```

### 初始化列表的赋值运算符

赋值运算符必须是成员。先分配空间，拷贝到新空间，然后释放旧资源，更新旧属性，以处理自赋值的情况。

 ```cpp
 Foo& Foo::operator=(initializer_list<int> il)
 {
     try {
         int *newArr = new int[il.size()];
             copy(il.begin(), il.end(), newArr);
         delete[] arr_;
         arr_ = newArr;
         length_ = il.size();
     } catch (e) {
         abort();
     }
     return *this;
 }
 ```

### 复合赋值运算符

虽然不一定是成员，但还是倾向于定义在类的内部。

```cpp
Person& Person::operator+=(const Person &rhs)
{
    name += rhs.name;
    age += rhs.age;
    return *this;
}
```

## 下标运算符

- 返回元素的引用。
- 最好同时定义常量版本和非常量版本。

```cpp
Foo& Foo::operator[](size_t n)
{ return arr_[n]; }
const Foo& Foo::operator[](size_t n)
{ return arr_[n]; }
```

## 递增和递减运算符

在迭代器类通常会实现递增递减运算符。

### 区分前置和后置

```cpp
class Foo {
public:
    FooPtr operator++(int);	// 提供一个int区分其为后置版本。
    FooPtr operator++();	// 前置版本。
};
```

## 成员访问运算符

在迭代器类和指针类常常会用到解引用符 `*`。

```cpp
class Ptr {
public:
    string& operator*() const { return *this; }
    string* operator->() const { return &this->operator*(); }
};
```

### 箭头运算符返回值的限定

必须返回类的指针，或者自定义了箭头运算符的某个类的对象（如果执行的结果本身含有重载的 `->` ，则会重复调用该运算符，直到返回类的指针）。

## 函数调用运算符

```cpp
struct AbsInt {
    int operator()(int val) const {
        return val < 0 ? -val : val;
    }
};
AbsInt absObj;
auto i = absObj(-1);
```

## 重载、类型转换与运算符

构造函数：其他类型 -> 此类

类转换运算符：此类 -> 其他类型

### 类型转换运算符

`operator type() const`

```cpp
class SmallInt {
public:
    SmallInt(int i = 0) : val(i)
    {
        if(i < 0 || i> 255)
            throw std::out_of_tange("Bad SmallInt value");
    }
    operator int() const { return val; }
};
```

```cpp
SmallInt si;
si = 5;	// 5 隐式转换为SmallInt
si + 3;	// si 隐式转换为 int，然后执行整数加法
```

