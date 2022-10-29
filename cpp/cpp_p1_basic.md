# 数据类型与类型修饰符

## 基本内置类型

算术类型、空类型（void）。

### 算术类型

- 整型

    | 类型      | 含义        | 最小尺寸         |
    | --------- | ----------- | ---------------- |
    | bool      | 布尔类型    | 未定义           |
    | char      | 字符        | 8bit             |
    | wchar_t   | 宽字符      | 16bit            |
    | char16_t  | unicode字符 | 16bit            |
    | char32_t  | unicode字符 | 32bit            |
    | short     | 短整型      | 16bit            |
    | int       | 自然整型    | 计算机的自然字长 |
    | long      | 长整型      | 32bit            |
    | long long | 超长整型    | 64bit            |

    除布尔型外，其余整型可以带符号（signed）或无符号（unsigned）。

- 浮点型

    | 类型        | 含义           | 最小尺寸     | 存储尺寸 |
    | ----------- | -------------- | ------------ | -------- |
    | float       | 单精度浮点数   | 6位有效数字  | 1个字    |
    | double      | 双精度浮点数   | 10位有效数字 | 2个字    |
    | long double | 扩展精度浮点数 | 10位有效数字 | 3或4个字 |

### 字面量

- 整型字面量

  | 进制     | 表示法 | 对应十进制值 |
  | -------- | ------ | ------------ |
  | 十进制   | 233    | 233          |
  | 八进制   | 0233   | 155          |
  | 十六进制 | 0x233  | 563          |

- 浮点型字面量

  ```cpp
  double a;
  a=3.14;
  a=3.14E0;
  a=0.;
  a=0e0;
  a=.001;
  /* 均为double字面量 */
  ```

- 字符、字符串字面量

  ```cpp
  'a';
  "shabi";
  ```

- 指定字面量类型

  - 字符和字符串

      | 前缀 | 含义                          | 类型     | 样例    |
      | ---- | ----------------------------- | -------- | ------- |
      | u    | unicode16字符                 | char16_t | u'A'    |
      | U    | unicode32字符                 | char32_t | U'B'    |
      | L    | 宽字符                        | wchar_t  | L'哇'   |
      | u8   | utf-8（仅适用于字符串字面量） | char[]   | u8"hi!" |

  - 整型字面量

      | 后缀  | 最小匹配类型 |
      | ----- | ------------ |
      | u/U   | unsigned     |
      | l/L   | long         |
      | ll/LL | long long    |

  - 浮点型字面量

      | 后缀 | 类型        |
      | ---- | ----------- |
      | f/F  | float       |
      | l/L  | long double |

  - 布尔字面量

    false、true。
  
  - 指针字面量
  
    nullptr（NULL）

## 变量

临时对象不属于变量？

### 声明与定义的关系

- 声明

  使得名字被程序知道。

- 定义

  创建与名字关联的实体。

### 作用域

全局作用域、块作用域。

- 全局作用域

  定义于所有花括号之外，整个程序内都可使用（跨文件时需要声明才可以使用）

- 块作用域

  从变量声明到块结束（函数结束）都可以访问它，所在块结束后不可访问。

#### 嵌套的作用域

外层作用域、内层作用域

- 外层作用域

  包含着别的作用域的作用域。

- 内层作用域

  嵌套在别的作用域的作用域。

  内层作用域可以访问外层作用域的变量（外层作用域 >= 内层作用域，外层作用域的变量没有被销毁）。

  内层作用域先结束然后外层作用域才会结束。

```cpp
{	// B作用域嵌套在A作用域中，B中可以访问到A的变量
    // scope A
    int a;
    {
        // scope B
        int b;
        a = 1;
        b = 0;
    }
}
```

- 允许在内层作用域重新定义外层作用域已有的名字。

  ```cpp
  int a(100);
  int main() 
  {
      int a(200);
      std::cout << a << std::endl;	// 200
      // 使用作用域操作符覆盖默认的操作符规则。
      std::cout << ::a << std::endl;	// 100
  }
  ```

  

## 传统字符串

```cpp
#include<iostream>
#define MAXLEN 10;
using namespace std;

int main(void)
{
    int i;
    char str[MAXLEN];
    char temp[MAXLEN];
    char * pstr,ptemp;
    char s1[MAXLEN];
    char s0[]="12356";	//比较特殊的初始化方法。
    
    //get input.
    i=0;
    do
        temp[i++]=getchar();
    while (i<LEN&&temp[i-1]!='\n');
    if(i==MAXLEN&&temp[i-1]!='\n')	//clear buffer.
        while(getchar()!='\n')
            continue;
    temp[i-1]='\0';
    
    pstr=str;
    ptemp=temp;
    //copy temp to str.
    while(*ptemp!='\0')
        *pstr++=*ptemp++;
    *pstr='\0';
    
    while(*temp!='\0')
        cout<<*temp++;
    
    return 0;
}
```



## 结构体

```cpp
struct Book {
    char title[50];
    char author[50];
    int price;
};

int main(void)
{
    Book bk1;
    
    return 0;
}
```

## 引用

类型修饰符 &。

### 声明与使用

```cpp
int t=0;
int & rt=t;	//must declare with init.

rt=10;
t==10;		//true.
```

### 引用作为函数参数

```cpp
void swap(int & a,int & b);
void swap(int & a,int & b)
{
    int temp;
    temp=a;
    a=b;
    b=temp;
}

int a,b;
swap(a,b);
```

### 指向指针的引用

从变量名从右往左读其定义，离变量被最近的符号对变量的类型有最直接的影响。

```cpp
int i=42;
int *p;
//最近的符号是&，故r为指针的引用。
int *&r=p;
r=&i;
*r=0;	//i=0;
```

### const的引用

```cpp
const int ci=1024;
const int &r1=ci;		//ci的引用。

r1=42;					//错误：r1是const的引用。
int &r2=ci;				//错误：让一个非常量引用指向一个常量对象。
const int &r3=ci;		//正确：常值引用可以绑定常量。
const int &r4=42;		//正确：常值引用可以绑定字面量。
```


## 指针

类型修饰符 *。

- 注意指针指向对象类型。

## 数组

类型修饰符 []。

### 定义和初始化内置数组

- 常值表达式初始化数组

  ```cpp
  constexpr unsigned get_size();
  int arr[get_size()];
  ```

  

- 显式初始化数组元素

  ```cpp
  const unsigned sz=3;
  int a1[sz]={1,2,3};
  //字符数组的特殊性，s1和s2为等价声明。
  char s1[]="xixi";
  char s2[]={'x','i','x','i','\0'};
  ```

### 复杂数组声明

类型修饰符从右到左结合。

```cpp
int *ptrs[LEN];			//首先ptrs是一个数组【[]】，数组的元素是【int*】。
/*int &refs[LEN];*/		//不存在引用的数组。
int (*parr)[LEN];		//首先parr是一个指针【*】，指向的对象是长度为LEN的数组【int[LEN]】。
int (&rarr)[LEN];		//首先rarr是一个引用【&】，引用的对象是长度为LEN的数组。
```

```cpp
int *(&arry)[LEN]=ptrs;	//arry是一个引用【&】，引用的对象是长度为LEN、元素为【int*】的数组【int*[LEN]】。
```

### 数组元素的访问

```cpp
size_t index;
int arr[LEN];
arr[index];
```

- 访问下标的类型通常为size_t。
- 注意索引下标不可越界，编译器通常不能检测出越界错误。

### 指针和数组

p1和p2指向对象相同（指向类型相同，对象值相同）。

```cpp
int *p1,*p2;
int arr[LEN];
p1=arr;
p2=&arr[0];
```



### 标准库函数begin()和end()

获取数组的迭代器。

```cpp
int arr[]={1,2,3,6,8};
int *beg=begin(arr);
int *last=end(arr);
while(beg!=last)
    cout<<beg++<<endl;
```

## const

### const和指针

从右往左阅读

- 常量指针（*const）

  首先是一个常量。

  该指针变量的值不可变。

  ```cpp
  int a=10;
  int *const pa=&a;
  ```

- 指向常量（const int）的指针（*）

  首先是一个指针。

  不可通过该指针改变其指向的对象的值。

  ```cpp
  int a=10;
  const int *cpa=&a;
  ```

- 指向常量的（const double）常量指针（*const）

  不可改变指针的值，且不可通过该指针改变指向对象的值。

  ```cpp
  const double pi=3.14;
  const double *const ppi=&pi;
  ```

#### 顶层const/底层const

- 顶层const

  该变量不可修改。

  ```cpp
  const int ci;		//ci不可修改，ci是顶层const。
  ```

- 底层const

  该变量本身可以修改。

  ```cpp
  int i;
  const int *pi;		//pi可以修改，pi是底层const。
  pi=&i;
  ```

  

### const和成员函数

```cpp
//防止成员函数修改调用方法对象的值。
class Test
{
    public:
    	Test(){}
    	Test(int _m):_cm(_m){}
    	int get_cm() const
        {
            return _cm;
        }
}
```

### const对象仅在文件内有效

不同的文件等同于进行了多次定义。

```cpp
/* file1.cpp */
const int a=1;
```

```cpp
/* file2.cpp */
const int a=2;
```

- 解决方法

    ```cpp
    /* file1.cpp */
    extern const int a=1;	//此处extern用于允许外部文件访问。
    ```

    ```cpp
    /* file2.cpp */
    extern const int a;		//此处extern是file1.cpp里a的引用式声明。
    ```

## 处理类型

### 类型别名

#### typedef

```cpp
typedef double wages;
typedef wages base, *p;	//p是double*的一个别名。
```

- typedef不是直接的编译替换

  ```cpp
  typedef char *str;
  const str cs;
  const char *pcc;
  ```

  pcc和cs的类型不一样（不等同于直接替换）：cs是指向char的常量指针（const修饰的是str类型）；pcc则是指向char常量的指针。

#### using

```cpp
using S=Student;	//S是Student类型的别名。
```

### auto

```cpp
auto i=0,*p=&i;		//正确：i是整型，p是整型指针。顺序由左到右。
auto sz=0,pi=3.14;	//错误：sz是整型，pi是浮点型，类型不一致。
```

- auto与引用

  ```cpp
  int i=0,&r=i;
  auto a=r;		//此时a为整型，r作为i的别名。
  auto &ri=i;		//ri为i的引用。
  auto &rc=42;	//错误：42为字面量。
  const auto &crc=42;	//正确：常值引用可以绑定字面量。
  ```

  ```cpp
  const int ci=0;
  auto &cri=ci;		//此时cri为常值引用，ci是int常量。
  ```

  

- auto与const

  auto一般会忽略顶层const而保留底层const。

  ```cpp
  const int ci=i, &cr=ci;
  auto b=ci;		//ci为顶层const，故b为普通整型。
  auto c=cr;		//cr是ci的别名，c的类型与b相同。
  auto d=&i;		//d是i的指针。
  auto e=&ci;		//e是指向整型常量的指针（对常量对象取地址是底层const）。
  ```

  显式保留顶层const。
  
  ```cpp
  const int ci=i, &cr=ci;
  const auto f=ci;
  ```
  
  

### decltype

取类型。

```cpp
//编译器自动判断类型。
int a=1,b=2;
auto sum=a+b;
//decltype变量类型获取。
decltype(var) var_0;	//声明一个与var同类型的变量var_0。
```

- decltype((expression))

  若表达式是一个变量，则decltype是一个引用类型。

  ```cpp
  int i=0;
  decltype((i)) ci;	//错误：ci为引用，必须初始化。
  decltype(i) a;		//正确：a与i的类型相同。
  ```

  



## 迭代器(iterator)

访问容器的元素的方法。低配指针，比指针好用且不容易出错。

- 迭代器类型与初始化

    ```cpp
    //must be init.
    vector<int>::iterator it1;			//rw
    string::iterator it2;				//rw
    
    vector<int>::const_iterator it3;	//r
    string::const_iterator it4;			//r
    ```

- 获取迭代器的方法

  ```cpp
  //指向v的迭代器的两种声明法。it1, it2 are the same.
  vector<int> v;
  vector<int>::iterator it1=v.begin();
  auto it2=v.begin();
  auto it3=v.end();		//pay attention to this method.
  //获得只读迭代器。
  vector<int> v;
  auto it=v.cbegin();	//vector<int>::const_iterator.
  ```

- 使用方法

  ```cpp
  vector<int> v;
  auto iv=v.begin();
  
  (*iv).empty()==iv->empty();		//成员方法似乎不可用。
  iv[i];							//the same as pointer.
  ```

- 迭代器运算符

  ```cpp
  vector<int> v1,v2;
  auto iv1=v1.begin();
  auto iv2=v2.begin();
  
  iv1-iv2;		//distance
  iv1>=iv2;		//position
  ```

  

## 类(class)

接口、实现分离编程。封装。

### 类的声明

- class与struct

  除默认访问权限不一样外，仅有形式上的区别。class默认为private。

    ```cpp
    struct Person{
    public:
        Person()=default;				//默认构造函数。
        Person(string name,Sex sex):
            name(name),sex(sex){}		//括号外的name为类中的name，将括号内的name赋值给括号外的name；花括号中写逻辑语句，可以不写但必须要有。
        Person(string name,string sex);	//需要在此进行声明后才可才外部定义。
    private:    
        string name="";
        Sex sex=male;
    };
    ```
  
- 声明例

  ```cpp
  struct Sales_data
  {
  
      std::string isbn(void) const
      {
          return this->bookNo;
      }
      Sales_data& combine(const Sales_data &);
      double avg_price(void) const;
  
      std::string bookNo;
      unsigned unit_sold=0;
      double revenue=0.;
  };
  Sales_data add(const Sales_data &,const Sales_data &);
  std::ostream &print(std::ostream &,const Sales_data &);
  std::istream &read(std::istream &,Sales_data);
  ```

### this关键字

调用方法对象的指针。

```cpp
struct Sth
{
    //隐式形参get_name(const Sth * const this) 第一个const使Sth为常量。
    std::string get_name(void) const	//防止修改调用方法对象的值。
    {
        return this->name;
    }
    std::string name;
};
Sth sth;
sth.get_name();							//隐式实参sth.get_name(&sth); 
//注意是指针而非引用。
```

### 成员方法的声明与定义

- 外部定义成员方法

  ```cpp
  struct Sth
  {
      int sum(void) const;
      int a,b;
      std::string name;
  };
  
  int Sth::sum(void) const		//继承Sth类。
  {
      return this->a+this->b;
  }
  ```

- 类相关的非成员方法（例类）

  ```cpp
  istream &read(istream &is,Sales_data & item);
  {
      //直接定义即可。
  }
  ```

### 构造函数

构造函数无返回类型，函数名为类名，具有一个初始化部分和一个函数体。

```cpp
class Foo {
public:
    Foo(...) 
        : // 初始化部分
    {}	// 函数体
};
```

#### 构造函数两个部分的执行顺序

先执行初始化部分，再执行函数体。

```cpp
class A {
public:
    A(const B &b)
        : b_(b) { cout << "A ctor." << endl; }
private:
    B b_;
};
class B {
public:
    B() { cout << "B ctor." << endl; }
};
```

输出

> B ctor.
>
> A ctor.

#### 默认构造函数

- 合成的默认构造函数

  没有声明任何构造函数时会自动生成，其名曰合成的默认构造函数。

  声明过任何构造函数后均不会自动合成构造函数。
  
  类中定义的初值将用于初始化；若没有定义初值则进行默认初始化。
  
  ```cpp
  struct Person{
      //合成的默认构造函数。
      Person()=default;
     	string name;
  };
  ```
  
  
  
- 默认构造函数的定义

    能够进行无实参构造的函数称为默认构造函数。

    用默认实参实现。

    ```cpp
    struct Person{
        //可以进行无实参构造，为默认构造函数。
        Person(string _name=""):
            name(_name){}
        string name;
    };
    ```

- 默认构造函数的作用

    当对象被**默认初始化**或**值初始化**时自动执行默认构造函数。

    - 默认初始化

        在块作用域内不使用任何初始值定义一个非静态变量时。

        ```cpp
        void main()
        {
            string a;
        }
        ```

        

        一个类本身含有类类型成员且使用合成的默认构造函数时。

        ```cpp
        struct A{
            int i;
        };
        struct B{
            A a;
        };
        ```

        

        类类型成员没有在构造函数初始值列表中显式初始化时。

        ```cpp
        struct A{
            //没有显示初始化s2。
            A():
            	s1("1"){}
            string s1;
            string s2;
        };
        ```

        

    - 值初始化（用确切的值对变量进行初始化）

        用数量少于数组大小的值进行数组初始化时。

        不使用初始值定义一个局部静态变量时。

        使用形如T()的表达式显式地请求值初始化时。

    - 缺少默认构造函数的情况

        ```cpp
        class NoDefault{
            public:
            	//此时不会有合成的默认构造函数。
            	NoDefault(const string &sth);
        };
        struct A{
            NoDefault sth;
        };
        A a;	//错误，无默认构造函数。
        struct B{
            B(){}	//错误，没有对sth进行初始化。
            NoDefault sth;
        };
        ```

- 默认构造函数的使用

  ```cpp
  struct A{/* ... */};
  int main()
  {
      A obj();	//此时声明了一个函数，而非对象。
      obj.func();	//错误，函数非对象。
      A obj_;
      obj_.func();	//此时执行了默认构造函数。
  }
  ```
  
  

#### 构造函数的声明与定义

- 声明与定义

  ```cpp
  struct Person{
      Person()=default;				//合成的默认构造函数。
      Person(string name,Sex sex):
      	name(name),sex(sex){}		//括号外的name为类中的name，将括号内的name赋值给括号外的name；花括号中写逻辑语句，可以不写但必须要有。
      Person(string name,string sex);	//需要在此进行声明后才可才外部定义。
      
      string name="";
      Sex sex=male;
  };
  Person::Person(string name,string sex):
  	name(name){
          if(sex=="male")
              this->sex=male;
          else if(sex=="female")
              this->sex=female;
          else 
              this->sex=male;
      } 
  ```
- 初始化列表与初始化顺序

  初始化的顺序与在**类中声明的顺序**一致。

  ```cpp
  class X{
      private:
          int i;
          int j;
      public:
      	//此处的实际效果为先用未定义的j初始化i，再用val初始化j。
      	//实际初始化顺序与初始化列表的顺序无关。
      	X(int val):
      		j(val),i(j);
  };
  ```

#### 委托构造函数

使用类中其他的构造函数进行构造的构造函数。

```cpp
struct Person{
public:
    Person(string name,Sex sex):
        name(name),sex(sex){}		//括号外的name为类中的name，将括号内的name赋值给括号外的name；花括号中写逻辑语句，可以不写但必须要有。
    Person(string name,string sex);	//需要在此进行声明后才可才外部定义。
    Person():Person("",male){}		//委托构造函数，调用了第一个构造函数。
private:    
    string name="";
    Sex sex=male;
};
```

#### 隐式的类类型转换

本质为调用构造函数进行类型转换。

- 隐式转换例

  ```cpp
  class Person{
      public:
          Person():
              name("_NAMELESS_"){}
          Person(string _name):
              name(_name){}
          string Name()const{
              return name;
          }
      private:
          string name;
  };
  
  int main()
  {
      //传统字符串隐式转换为string。
      string name="Tairitsu";
      //隐式转换string为Person。
      Person p1=name;
      //隐式转换"Hikari"为string。
      Person p2("Hikari");
      //错误的转换，单个语句只能够进行一次类型转换。
      /* Person p3="NULL"; */
      
      cout<<p1.Name()<<endl;
      cout<<p2.Name()<<endl;
  
      return 0;
  }
  ```

- 抑制构造函数定义的隐式转换（explicit）

  显式转换无影响。

  ```cpp
  class Person{
      public:
          Person():
              name("_NAMELESS_"){}
          explicit Person(string _name):
              name(_name){}
          string Name()const{
              return name;
          }
      private:
          string name;
  };
  
  int main()
  {
      string name="Tairitsu";
      //string到Person的显式转换不抑制。
      Person p1=(Person)name;
      //错误，抑制隐式转换。
      /* Person p1=name; */
      Person p2("Hikari");
      cout<<p1.Name()<<endl;
      cout<<p2.Name()<<endl;
  
      return 0;
  }
  ```

  

### 字面值常量类

- 要求

  成员必须为字面值类型。

  类至少含有一个constexpr构造函数。

  类成员若含有类内初始值，则该初始值必须是常量表达式；若成员属于某种类类型，则初始值必须使用该成员的constexpr构造函数。

  类必须使用析构函数的默认定义。

- 例

  ```cpp
  class Debug{
      public:
      	constexpr Debug(bool b=true):
      		hw(b),io(b),other(b){}
      	constexpr Debug(bool h,bool i,bool o):
      		hw(h),io(i),other(o){}
      	constexpr bool any(){return hw||io||other;}
      	void set_io(bool b){io=b;}
      	void set_hw(bool b){hw=b;}
      	void set_other(bool b){other=b;}
      private:
      	bool hw;
      	bool io;
      	bool other;
  };
  ```


### 类的静态成员

可以是常量、引用、指针、类类型、函数等。

#### 声明

```cpp
class Account{
public:
    static double rate() {return r;}
    static void rate(double);
private:
    static double r;
    static double initRate();
};
```

- 静态成员方法不包含this指针（不与任何对象绑定，不能修改普通成员属性）

- 静态成员方法不能后置const

  const仅对实例有效，静态成员方法本身就不能修改普通成员变量。

- const的普通成员方法可以修改static成员（const仅对实例有效）

#### 使用

无须实例化对象，可以通过作用域运算符直接访问限定符允许访问的静态成员。

```cpp
double a = Account::rate();
```

成员函数无须通过作用域运算符即可访问到静态成员。

#### 定义

类内或类外均可以对静态成员进行定义。注意static只能出现在声明语句。

- 类外

    ```cpp
    class Account{...};
    Account::rate(double n){
        r = n;
    }
    //从Account开始，语句的剩余部分都在类的作用域内，故可用私有方法初始化r。
    double Account::r = initRate();
    ```

- 类内

  一般不能在类内部初始化。必须是字面值常量类型的静态成员才可。

  ```cpp
  class Account{
      static int r = 5;	//错误的初始化方法。
      static constexpr double pi = 3.14;
  };
  constexpr double Account::pi;	//最好在外部也声明，避免在类外部使用该常量时编译出错。
  ```

#### 别的

- 静态成员的类型可以是它所属的类的类型

  ```cpp
  class A{
      static A mem1;
      A *mem2;
      A mem3;	//不合法，数据成员必须是完全类型。
  };
  ```

  

  

### 别的特性

- 内联

  在类中定义的函数会被隐式内联。

- 构造函数的初始值列表

  ```cpp
  class ConstInit{
      ConstInit(const int a,int & ra):
      	i(a),ri(ra);	//不可在语句块内赋值，只可在初始值列表中初始化。常量、引用的初始化。初始化的顺序与在类中定义顺序一致而与列表顺序无关。
      
      const int i;
      int & ri;
  };
  
  ```
  
- 友元(friend)

  允许其他类或函数访问类的私有成员。

  ```cpp
  class Person{
  public:
      friend void ShowPerson(Person person,ostream & os);//friend关键字。注意此时函数尚未被声明。
      
  private:
      string name;
      Sex sex;
  };
  
  void ShowPerson(Person person,ostream & os);		//内外都要声明。
  
  int main(void){
      return 0;
  }
  
  void ShowPerson(Person p,ostream & os){
      os<<p.name<<endl;
      os<<p.sex<<endl;
  }
  ```

- 聚合类

  成员均为public；

  没有定义任何构造函数；

  无类内初始值；

  无基类、虚函数。

  聚合类的初始化

  ```cpp
  struct Data{
      int ival;
      string s;
  };
  Data val1={0,"Anna"};
  ```



# 表达式

## 左值和右值

当一个对象被用作右值的时候，用的是对象的值；当一个对象被用作左值的时候，用的是对象在内存的位置。

### 左值和右值与decltype

decltype(expression);

- 表达式为左值

  decltype得到一个引用类型。

- 表达式为右值

  decltype得到一个指针类型。

```cpp
int *p;
decltype(*p);	//*p是左值，所以得到的是int&。
decltype(&p);	//&p是右值，所以得到的是int**。
```



## 逗号运算符

对左侧求值，对右侧求值，返回右侧的值。

若右侧的运算对象是左值，则逗号表达式的求值结果也是左值。

```cpp
left_expression, right_expression;
```

## 类型转换

### 隐式转换的发生

- 比int类型小的整型会被提升为较大的整数类型。
- 在条件中，非布尔值转换为布尔类型。
- 初始化过程中，初始值转换成变量的类型。
- 赋值语句中，右侧运算对象转换为左侧运算对象类型。
- 函数调用也会发生类型转换。
- 算术运算转换为同一个类型。

### 算术转换

类型大小是指占用内存的大小。

- 所有运算对象将转换为最宽类型

  若存在long double，则所有类型都会转换为long double。

- 整型提升

  小整数类型转换成较大的整数类型。

- 无符号类型的运算对象

  若无符号 >= 有符号，则转换为无符号（大小相同，无符号优先）。

  若无符号 < 有符号，则转换为有符号。
  
  ```cpp
  int a;
  unsigned b;
  a = -21;
  b = 20;
  cout << a + b << endl;
  /* 输出4294967295（a, b的类型大小相同，a转换为无符号） */
  ```
  
  ```cpp
  long long a;
  unsigned b;
  a = -21;
  b = 20;
  cout << a + b << endl;
  /* 输出-1 */
  ```
  
  

### 其他隐式类型转换

#### 指针的转换

- 0和nullptr能够转换为任意指针类型。
- 指向任意非常量的指针能转换成void\*。
- 指向任意对象的指针能转换成const void\*。

### 显式转换

#### 命名的强制类型转换

*cast-name*\<*type*\>(*expression*);

| cast-name        | 作用                                                        |
| ---------------- | ----------------------------------------------------------- |
| static_cast      | 任何具有明确定义的类型转换（不包含底层const）               |
| dynamic_cast     | 支持运行时的类型识别                                        |
| const_cast       | 只能用于改变运算对象的底层const                             |
| reinterpret_cast | 为运算对象的位模式提供底层的重新解释（C风格的强制类型转换） |

- static_cast

  ```cpp
  double r = static_cast<double>(x) / y;
  ```

- const_cast

  ```cpp
  const char *pc;
  char *p = const<char*>(pc);
  //此时通过p写值是未定义的行为。
  ```

- reinterpret_cast

  ```cpp
  int *ip;
  char *p = reinterpret_cast<char*>(ip);
  ```



# 语句

## 异常处理语句

异常处理机制包括**异常检测**（try、throw）部分和**异常处理**（catch）部分。

- throw表达式

  异常检测部分，使用throw表达式抛出异常信号，**引发(raise)**异常。

- try语句块

  在try语句块内抛出的异常信号，会被紧随其后的匹配的catch子语句捕获。

  ```cpp
  try{
      /* 可能于此抛出异常 */
  }catch(exception_type1 &e){
      /* 异常类型1的处理 */
  }catch(exception_type2 &e){
      /* 异常类型2的处理 */
  } // ...
  ```

  - catch子语句块

    紧跟在try语句块后面，用于捕获异常信号，并提供异常处理方法。

    ```cpp
    try{}catch(exception_type2 &e){}
    ```

- 一套异常类（exception_type）

  用于传递异常信息。

### 处理例

输入a, b后，试输出a / b的结果。

```cpp
int a, b;
int res;
cin>>a>>b;
try{
    if(b != 0){
		res = a / b;
    }else{
        throw runtime_error("Division is 0.");
    }
}catch(runtime_error &e){
    cerr<<e.what()<<endl;
    exit(-1);
}
cout<<res<<endl;
```



try会触发寻找合适的catch()函数，无则调用terminate，并异常结束程序。

```cpp
throw runtime_error("ERROR");
```

## 迭代语句

- for

  传统for(;;)。

  ```cpp
  int main(void)
  {
      int i;
      for(i=0;i<8;i++)
          cout<<i;
  }
  ```

  范围for(auto i:arr)。

  ```cpp
  #iunclude<iostream>
  using namespace std;
  int main(void)
  {
      int arr[8]={0,1,2,3,4,5,6,7};
      //auto使编译器自动识别变量类型。必须在for内声明语句块变量。
      for(auto i:arr)
          cout<<i;
  }
  ```


## 条件语句

- switch(int/enum)	必须是整数或枚举类型。

  ```cpp
  int a;
  switch(a){
      case 0:
          break;
      case 114514:
          break;
      default:
          break;
  }
  ```



# 函数

## constexpr函数

const_expression.

能用于常量表达式的函数。允许该函数返回常量表达式，而并非必须返回常量表达式。

```cpp
constexpr scale(size_t num)
{
    return *cnt;
}
//正确的。
int arr1[scale(2)];
int i=2;
//错误的，只有i为常量时，该表达式正确。
int arr2[scale(i)];
```



## 返回类型

### 实例：返回特定大小数组的指针的函数

#### 使用类型别名实现

```cpp
typedef int arrT[10];	//arrT为含有10个int的数组的类型别名
using arrT = int[10];	//与上一行等价
arrT* func(int i);		//返回类型为指针，指针指向arrT的变量；即返回类型为指向int[10]的指针。
```

#### 一般实现

```cpp
int (*func(int i))[10];	//func是一个函数（函数运算符()），返回类型为int(*)[10]，需要注意[]一定要在右边。
```

- func(int i)表示调用func函数时需要一个int类型的实参。
- (*func(int i))意味着可以对函数调用的结果执行解引用操作。
- (*func(int i))[10]表示解引用func的调用结果会得到大小为10的数组。
- int (*func(int i))[10]表示数组中的元素是int类型。

#### 使用尾置返回类型

使用auto声明类型，通过->运算符指定返回类型。

```cpp
auto func(int i) -> int(*)[10];
```

#### 使用decltype

```cpp
int arr[] = {1, 2, 3, };
decltype(arr) *func(int i);	//需要注意arr的类型为长度为3的数组而非指针，是执行了类型转换后才变成了指针。
```



## 调试帮助

### assert(expr)

如果表达式为假，则打印一条错误信息，中断程序；若为真，则程序继续运行。

```cpp
#include<cassert>
assert(a > b);
```

### NDEBUG

```cpp
#define NDEBUG
#ifndef NDEBUG
/* debug code */
#endif
```

### 调试辅助变量

| 变量名       | 内容                           |
| ------------ | ------------------------------ |
| \_\_func\_\_ | 存放函数名字的局部静态变量     |
| \_\_FILE\_\_ | 存放文件名的字符串字面值       |
| \_\_LINE\_\_ | 存放当前行号的整型字面值       |
| \_\_TIME\_\_ | 存放文件编译时间的字符串字面值 |
| \_\_DATE\_\_ | 存放文件编译日期的字符串字面值 |

## 函数匹配

编译器对重载函数的选择。

### 确认候选函数以及可行函数

| 术语     | 解释                                                   |
| -------- | ------------------------------------------------------ |
| 候选函数 | 与调用函数同名、可见的函数                             |
| 可行函数 | 形参数量与提供实参数量相等、参数类型相同或能够转换相同 |

### 寻找最佳匹配

实参类型与实参类型越接近（匹配等级以及匹配数量），则匹配得越好。若匹配效果相当，则会出现调用二义性的编译错误。

- 匹配类型及其等级

  | 类型                       | 等级 | 条件                                                         |
  | -------------------------- | ---- | ------------------------------------------------------------ |
  | 精确匹配                   | 1    | 实参类型与形参相同；数组或函数类型转换为指针；对实参添加或删除顶层const |
  | 通过const转换实现的匹配    | 2    | void\*转换为const void\*                                     |
  | 通过类型提升实现的匹配     | 3    | 小整型提升为大整型                                           |
  | 通过算术类型转换实现的匹配 | 4    | 小类型转换为大类型                                           |
  | 通过类类型转换实现的匹配   | 5    | 类类型转换                                                   |

- 类型转换之间无优先级

  ```cpp
  void f(long);
  void f(float);
  f(3.14);	//二义性调用，转换为long或float没有优先级之分。
  ```


## 函数指针

### 成员方法的函数指针

一定要有'&'。

- 静态成员函数指针

  ```cpp
  void (*pFunc)() = &ClassName::staticFunc;
  ```

- 普通成员方法的函数指针

  作用域名也是类型（？）的一部分。

  ```cpp
  void (ClassName::*pFunc)() = &ClassName::func;
  ```

