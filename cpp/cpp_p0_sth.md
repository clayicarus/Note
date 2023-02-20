# 杂项

## 命名空间

一些等价代码。

version1 be like.

```cpp
#include<iostream>
//using namespace name;
using namespace std;
int main(void)
{
    int temp;
    cout<<"enter a num: ";
    cin>>temp;
    
    return 0;
}
```

version2 be like.

```cpp
#include<iostream>
int main(void)
{
    int temp;
    std::cout<<"enter a num: ";
    std::cin>>temp;
    
    return 0;
}
```

version3 be like.

```cpp
#include<iostream>
//using space_name::obj_name;
using std::cout;
int main(void)
{
    int temp;
    cout<<"enter a num: ";
    std::cin>>temp;
    
    return 0;
}
```

## 变量的初始化

- 默认初始化

  定义变量时未指定初值，则会执行默认初始化。

  在块内声明的内置变量不会进行初始化。

  ```cpp
  {
      int a;	//未初始化int型变量a。
  }
  int i;		//默认初始化，执行了int类的默认构造函数。
  ```

- 值初始化

  声明的同时用确切值对其进行初始化。
  
  ```cpp
  int a=0;
  int b(1);
  ```
  
- 列表初始化

  花括号的奇妙用法。

  ```cpp
  int val=0;
  int val={0};
  int val{0};
  int val(0);
  ```

  注意使用列表初始化时不会进行类型转换（故需进行类型转换的列表初始化会报错）。

  ```cpp
  long double ld=1.14;
  int a{ld},b={ld};		//此处不会进行类型转换，报错。
  int c(ld),d=ld;			//隐式类型转换。
  ```



## void返回值

```cpp
void test(void)
{
	return;
}
```

## 可变形参

- 省略符形参(...)

```cpp
#include<strdag.h>		//
int sum(int n,...)
{
    int i,sum;
    va_list argptr;				//declare para ptr.
    va_start(argptr,n);			//init argptr, array len n.
    sum=0;

    for(i=0;i<n;i++)
        sum+=va_arg(argptr,int);//take it as int
    va_end(argptr);				//finish.

    return sum;
}
```

- initializer_list形参

```cpp

```

## 默认实参

```cpp
string screen(int ht=24,int wid=80;char backgrnd=' ');
```

## 内联函数（inline）

编译时进行一个直接替换。

```cpp
inline int max(int a,int b)
{
    return a>b?a:b;
}
```

## 数组指针/引用

```cpp
int *ptrs[LEN];		//int指针为元素的数组。
//int &refs[LEN];	//不存在引用的数组。
int (*pa)[LEN];		//长度为LEN的int数组的指针。
int (&ra)[LEN];		//长度为LEN的int数组的引用。
```

## 尾置返回

原定返回类型处用auto替换，void处为参数列表，->后表示真实返回类型。

```cpp
auto func(void)->int(*)[LEN];	
```

## 使用迭代器的二分搜索

### 适用条件

- text有序

### 实现

```cpp
auto beg=text.begin(),end=text.end();
auto mid=text.begin()+(end-beg)/2;		//初始化中点。
while(mid != end && *mid !=sought){
    if(sought<*mid)			//要找的元素在前半部分？
        end=mid;			//在前半部分：调整右端点。
    else					
        beg=mid+1;			//在后半部分：调整左端点，mid不在搜索范围内（beg所指元素必须在搜索范围内）。
    mid=beg+(end-beg)/2;	//新中点。
}
```

## upper_bound / lower_bound的实现

- 初始化左区间长度（步长）、中点位置、区间长度
- 总区间长度为 0 的时候找到目标，返回左端点first

```cpp
template<class ForwardIt, class T>
ForwardIt lower_bound(ForwardIt first, ForwardIt last, const T& value)
{
    ForwardIt it;
    typename std::iterator_traits<ForwardIt>::difference_type count, step;	// 不知道是static变量还是类型，需要用typename显式表示类型
    count = std::distance(first, last);	// 搜索区间长度
 
    while (count > 0)
    {
        it = first; 		// first是区间的左端点
        step = count / 2; 	// 左区间的长度
        std::advance(it, step);	// it为区间中点
 
        if (*it < value)	// 返回第一个大于等于value的元素
        {	// 中点比目标值小，移动左端点到中点处
            first = ++it; 	// 更新区间左端点
            count -= step + 1; // 区间长度减少了 step + 1（右区间长度）
        }
        else
            count = step;	// 区间长度更新为左区间长度
    }
 
    return first;
}
```

```cpp
template<class ForwardIt, class T>
ForwartIt upper_bound(ForwardIt first, ForwardIt last, const T &value)
{
    ForwartIt it;
    typename std::iterator_traits<ForwardIt>::difference_type count, step;
    count = std::distance(first, last);
    
    while(count > 0) {
        step = count / 2;	// 左区间长度
        it = first;
        std::advance(it, step);
        
        if(!(value < *it)) {	// 第一个大于value的元素，使用 < 表示，由 *it <= value 去推导
            first = ++it;	// 此处不要使用it + 1，不一定有对应的重载
            count -= step + 1;
        } else 
            count = step;
    }
    
    return first;
}
```

