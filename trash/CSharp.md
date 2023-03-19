# CSharp
## 数据类型
### 基本数据类型
#### 无符号整型
```c#
    byte b=1;
    ushort us=1;
    uint ui=1;
    ulong ul=1;
```
#### 有符号整型
```c#
    sbyte sb=1;
    short s=1;
    int i=1;
    long l=1;
```
#### 浮点
```c#
    float f=1f;
    double d=1f;
    decimal dec=1m;
```
#### 其他
```c#
    bool bo=true;
    char c;
    string str="shabi";
```
### 复杂数据类型

#### 字符串

输出函数与格式化

```c#
string str=string.Format("1+1={0}",1+1);
Console.WriteLine("1+1={0}",1+1);
```



#### 枚举
声明
```c#
    enum en{
        red,			//red==0
        green,			//green==1
        blue,			//blue==2
        yellow=5,		//yellow==5
        pink,			//pink==6
        pupple=10,		//pupple==10
    }
```
使用
```c#
    en.pink;			//enum use
```

#### 数组
- 一维数组


声明

```c#
	int[] arr;			
	arr=new int[]{1,2,3,4};
	
  //先声明一个数组的引用arr，将新数组的地址赋值给arr
```

```c#
	int[] arr1={1,2,3,4};
	//直接进行一个数组的声明
	//需注意直接声明对象需要有对象名，而用new则不需要
```
```c#
	int[] arr=new int[10];
	//生成一个长度为10的空数组
```
使用

```c#
    arr[0];
```

- 二维数组

声明

```c#
    int[,] arr1;
    arr1=new int[,]{
        {1,2,3},
        {4,5,6},
        {7,8,9},
    }
```

```c#
    int[,]arr2={{...},{...},{...}};
```

```c#
    int[,]arr3=new int[,]{{},{},{}};
```
```c#
	int[,]arr4=new int[a,b];
```

使用

```c#
    arr[0,0];
```

```c#
    arr.GetLength(0);	//取行长度
    arr.GetLength(1);	//取列长度
    arr.Length;			//取元素数目
```
#### 结构体
```c#
//结构体为值类型

namespace Structure
{
	struct Book{				//结构体的声明放在命名空间里
		private double price;	
		string bookname;		//默认为private
		public string owner;
		
		public void ShowInf()	//结构体里可以有函数
		{
			Console.WriteLine("This book's price is "+this.price+".");
			Console.WriteLine("Its bookname is "+bookname+".");
			Console.WriteLine("Its owner is {0}",owner);//注意此处字符串的占位符
		}
		
        //构造函数
        //函数内必须有参数
        //无类型，public，需对所有变量进行初始化
		public Book(double price,string bookname,string owner)
		{
			//price=price;	//命名有冲突时才需要用this
			this.price=price;
			this.bookname=bookname;
			this.owner=owner;
		}
	};

	class Test
	{
		static void Main(string[] args)
		{
			Book bk=new book(12.58,"Gone with the wind","sb.");
			bk.ShowInf();
			//bk.price==12.58;
		}
	}
}
```
### 类
- 声明

```c#
	访问修饰符 class Sth{		//public, private, protected
		//成员变量：普通变量
		//成员方法：函数
		//成员属性：赋值变量
		
		//构造函数、析构函数
		//索引器
		//静态成员
	}
```

- 注意
```
类（实例）为引用类型。
```

- 类中的成员变量及成员方法


```c#
	namespace Class
	{
		enum Sex{
			male,
			female, 
		};
        
        protected class Sth{}	//自身及其子类
		public class Pet{}		//都可用
		private class Person{	//默认为private，仅可在自身
			string name="233";	//可以声明赋值变量
			uint age;
			Sex sex;
			Pet pet=new Pet();	//可以声明初始化的别的类
            Person goodfriend;	//可以声明自身类，但不可对其初始化
            Person[] friend;	//类数组is also ok desu
            
            //访问修饰符 函数类型 函数名(...)
            //不可使用static关键字
            public void Cum()
            {
            	Console.WriteLine("Wellcum");
            }
		}
		
        
        static void Main(string[] args)
        {
            Person p1;
            Person p2=new Person();	//必须用构造函数进行类的实例化。
            
            Person p3;
            p3=new Person();
        }
	}
```

- 类的构造函数

```c#
class Person{
    public string name;
    public uint age;

    //注意若类中仅有有参构造函数，则不可使用无参构造函数来创建对象。
    //当类中没有有参构造函数或有参无参都存在时，可以使用无参构造函数创建对象。
    public Person()
    {
        name="";
        age=0;
    }
    //可以对构造函数进行重载。
    //this可以理解为该类的另外的标识符。
    //:this()的作用为先调用Person()后调用Person(string,uint)来创建对象。
    //this()可传入参数，与函数重载一致。
    public Person(string name,uint age):this()
    {
        this.name=name;
        this.age=age;
    }      
}
```

- 类的析构函数

```c#
class Person{
	//当发生垃圾回收时会自动调用之。
	~Person()
	{...};
}

```
## 特殊关键字
### ref/out：使传递原变量的引用
ref
```c#
	//传递该变量的引用
	static void Test(ref int num)
	{
		num++;
	}
	static void Main(string[] args)
	{
		int num=0;
		Test(ref num);
	}
	//num==1
```
out
```c#
	//传递该变量的引用
	static void Test(ref int num)
	{
		num=1;
	}
	static void Main(string[] args)
	{
		Test(ref num);
	}
	//num==1
```

区别

- ref的变量需声明，而out不需要
- out的变量必须在函数内赋值，而ref不需要

## 杂项
- 变长参数

```c#
	static void Sum(int n,params int[] ar)
	{
		int sum=0;
		for(int i=0;i<ar.Length;i++)
			sum+=ar[i]+n;
		return sum;
	}
	//必须为数组类型，变长参数必须在参数的最后一个，只能有一个或一个以下的参数
```

- 默认参数

```c#
	static void Imiganai(int n=1)
	{
		return n;
	}
	//默认参数必须在参数的最后一个
```

- 函数重载

对函数可以进行多次定义。编译器会依据传入的参数数目或类型，进行函数的选择性调用。
```c#
class Main{
	static int Fun(int a)
	{
		return a;
	}
	static int Fun(int a,int b)
	{
		return a+b;
	}
	static void Main(string[] args)
	{
		Fun(1);		//func returns 1.
		Fun(1,2);	//func returns 3.
	}
}
```

- 垃圾回收机制(GC)
  对堆中的内存进行回收。
  栈：存放值类型变量的内存。系统管理之。
  堆：存放引用指向对象的内存。

  0代内存：快速。
  1代内存：快速。
  2代内存：大对象的默认储存位置。

- 反射机制

  运行中的程序查看其自身或其他程序的元数据的行为。
