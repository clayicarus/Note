# 输入输出

## cout/标准输出流(ostream)

``` cpp
#include<iostream>
#include<iomanip>	//setiosflags();
using namespace std;
int main(void)
{
    //左对齐。
    cout<<setiosflags(ios::left|ios::showpoint);
    //固定的浮点显示 
    setiosflags(ios::fixed);
    //科学记数法
    setiosflags(ios::scientific);
    //忽略前导空白 
    setiosflags(ios::skipws); 
    //16进制数大写输出
    setiosflags(ios::uppercase);
    //16进制小写输出 
    //setiosflags(ios::lowercase);
    //强制显示小数点 
    setiosflags(ios::showpoint);
    //强制显示符号 
    setiosflags(ios::showpos);

    //hex output.
    cout<<hex;
    //5位小数。 cout<<setiosflags(ios::fixed);
    cout.precision(5);
    //显示区域宽度10。
    cout.width(10);
    //填充空白区域。
    cout.fill('*');			//before output.
    cout<<"wocao"<<endl;

    return 0;
}
```

## cin/标准输入流(istream)

```cpp
//机制与scanf()类似
//空白停止，剩余置于缓冲区(cin流中)。
using namespace std;
int main(void)
{
    int temp,t1,t2;
    istream is;
    cin>>temp;
    cout<<temp;
    //表通过is流对t1，t2分别进行输入。
    is>>t1>>t2;

    return 0;
}
```

## 文件重定向

将标准输入重定向为infile文件；将标准输出重定向为outfile。

```bash
$ cmd < infile > outfile
```

# IO库

## 常用设施列举

- istream

- ostream

- cin

- cout

- cerr

- getline(istream &is, string &str)

  遇到换行符即停止，str不含换行符，输入缓冲中也不含换行符（换行符被丢弃了）。

  可用于清空输入缓冲，包括回车。

  ```cpp
  getline(cin,str);
  ```

## IO类

### 常用IO流及其特性

- 标准IO流

  #include\<iostream\>

  istream, wistream

  ostream, wostream

  iostream,wiostream

- 文件流

  #include\<fstream\>

  ifstream, wifstram

  ofstream, wofstream

  fstream, wfstream

- string流

  #include\<sstream\>

  istringstream, wistringstream

  ostringstream, wostringstream

  stringstream, wstringstream

- 其中w前缀以支持使用宽字符的语言

- IO对象无拷贝或赋值

  ```cpp
  ostream o1,o2;
  o1=o2;						//不可赋值。
  ofstream print(oftream);	//不可初始化。
  o2=print(o2);				//不可拷贝。
  ```

### IO对象的条件状态

- 状态及其方法

  ```cpp
  //strm为某一种IO类类型。
  strm::iostate;			//
  strm::badbit;			//指出流已崩溃，无法使用。
  strm::failbit;			//指出一个IO操作失败了。
  strm::eofbit;
  strm::goodbit;
  
  s.eof();				//返回eofbit==1。
  s.fail();
  s.clear();				//复位所有状态位。
  s.clear(strm::iostate);	//复位某个状态位。
  s.setstate(flag);
  s.rdstate();			//返回当前流的状态，类型为strm::iostate。
  ```

- IO错误例子

  ```cpp
  int val;
  cin>>val;
  //当输入为非数字时cin进入错误状态。>>返回值为流的状态。
  while(cin>>val)
      continue;
  //正常输入则循环，遇到EOF(^D)或输入错误则跳出循环。
  ```

### 输出缓冲的管理

- 缓冲区

  每个输出流都有一个独立的缓冲区，只有缓冲区刷新时才会真正写到输出设备或文件。

- 导致缓冲区刷新的常见情况

  程序正常结束。

  缓冲区满。

  用户显式刷新。

  与之关联的流进行了刷新。

- 刷新缓冲的命令

  ```cpp
  cout<<"hi"<<endl;		//输出换行，然后刷新。
  cout<<"hi"<<flush;		//输出，直接刷新。
  cout<<"hi"<<ends;		//输出空字符，然后刷新。
  ```

- 无缓冲操作符（长度只有1的缓冲）

  ```cpp
  cout<<unitbuf;		//进入无缓冲方式
  /* 此处内容立即刷新 */
  cout<<nounitbuf;	//回到正常模式
  ```

- 关联流

  - 关联流的刷新

    ```cpp
    cin>>val;
    //此操作会引起cout刷新。
    ```

  - 关联流的创建

    ```cpp
    cin.tie(&cout);	//指针
    ```

## 文件流（ftream）

### 文件流声明及其基本方法

```cpp
fstream fs;	//可读可写。
fstream fs("path",mode);
ofstream of;//只写。
ifstream if;//只读。

fs.open("path");		//打开模式依赖于流类型。
fs.open("path",mode);	

fs.close();
fs.is_open();
```

### 文件流的读写方法

```cpp
fs.open("file");
fs<<"abc"<<flush;
fs.close();
```

### 文件流的打开模式（ios::mode）

| 模式     | 含义                               |
| -------- | ---------------------------------- |
| ios::in  | "r"，只可对fstream或ifstream使用。 |
| ios::out | "w"，只可对fstream或ofstream使用。 |
| ios::app | 每次写操作前均定位到文件尾。       |
| ios::ate | "a"，打开文件后立即定位到文件尾。  |
| trunc    | 舍弃原文件内容（默认）。           |
| binary   | "b"，二进制模式。                  |

## string流（sstream）

常用于类型转换。

### 声明及其基本方法

```cpp
stringstream ss;
stringstream ss(str);	//用str初始化ss。
istringstream iss;
ostringstream oss;

//返回ss的string拷贝。
ss.str();
//将s拷贝至ss，返回void。
ss.str(s);
```

### 应用

- itoa

  ```cpp
  stringstream ss;
  string str;
  int val;
  
  cin>>val;
  ss<<val;
  ss>>str;
  ```

- atoi

  ```cpp
  stringstream ss;
  string str;
  int val;
  
  str="114514";
  ss<<str;
  ss>>val;
  ```

- 读取所有行

  ```cpp
  //输入格式为“人名 电话1 电话2 ... 电话n”：Alice 10086 10000 110 120 114
  string line,word;
  vector<Person> ps;
  while(getline(cin,line))
  {
      Person p;
      istringstream record(line);
      //读取到第一个空白的位置。
      record>>info.name;
      //EOF则结束循环。
      while(record>>word)
          p.phones.push_back(word);
     	ps.push_back(p);
  }
  ```

  





# 泛型算法 (algorithm)

## max_element / min_element

O(n)。

```cpp
vector<int> v;
int max;
vector<int>::iterator iv;
iv=max_element(v.cbegin(),b.cend());
max=*max_element(v.begin(),v.end());
```

## 定制操作

给排序函数提供比较方法。

- 函数指针定制

  ```cpp
  bool isShorter(const string &s1,const string &s2){return s1.size()<s2.size();}
  sort(words.begin(),words.end(),isShorter);
  ```

- lambda表达式定制

  lambda是可调用对象。

  需用尾置返回表示lambda函数。

  - 声明与定义

    ```cpp
    /* 完整定义 */
    [capture list](parameter list)->return type{/* function */}
    /* 简略，可忽略参数列表或返回类型 */
    auto lf=[]{/* function */ return x;}
    ```

  - lambda的调用

    ```cpp
    auto lf=[]{return 114514;}
    lf();
    ```

  - lambda捕获列表

    capture_list

    捕获列表中可以有lambda外部的变量，以供lambda的函数体调用之，克服了参数列表固定的缺点。

    ```cpp
    //sz为find_if之外的变量。
    find_if(words.begin(),words.end(),
           [sz](const string &a){return a.size()>=sz});
    ```

    

  - lambda定制

    ```cpp
    stable_sort(words.begin(),words.end(),
                [](const string &a,const string &a){return a.size()<b.size();});
    ```



# 顺序容器

| 类型         | 外部表现                 | 访问方式     | 插入/删除效果                    |
| ------------ | ------------------------ | ------------ | -------------------------------- |
| vector       | 变长数组                 | 快速随机访问 | 尾部快。其他位置可能很慢。       |
| deque        | 双端队列                 | 快速随机访问 | 头尾都很快。                     |
| list         | 双向链表                 | 双向顺序访问 | 任何位置都快（前提是访问到了）。 |
| forward_list | 单向链表                 | 单向顺序访问 | 任何位置都快（前提是访问到了）。 |
| array        | 固定长度的数组           | 快速随机访问 | 不可插入或删除。                 |
| string       | 类似vector，只能保存字符 | 快速随机访问 | 尾部快。其他位置可能很慢。       |

- 顺序容器几乎可以保存任意类型的元素。

## 容器通用成员

容器库操作成员分为三个层次。

- 所有容器类型都提供的操作。
- 仅分别针对顺序容器、关联容器、无序容器的操作。
- 适用与一小部分容器的操作。

### 通用操作成员（顺序、关联）

| 类型别名        | 作用                                     |
| --------------- | ---------------------------------------- |
| iterator        | 对应类型容器的迭代器                     |
| const_iterator  | const迭代器                              |
| size_type       | 无符号整数类型，保存该容器最大大小的类型 |
| difference_type | 带符号整数类型，保存两个迭代器之间的距离 |
| value_type      | 元素的类型                               |
| reference       | value_type &                             |
| const_reference | const value_type &                       |

| 构造函数                                      | 作用                                      |
| --------------------------------------------- | ----------------------------------------- |
| Container()                                   | 默认构造函数，构造空容器（array与之不同） |
| Container(const Container &c)                 | 拷贝构造函数                              |
| Container(const_iterator b, const_iterator e) | 拷贝b, e范围的元素进行构造                |
| Container(initialize_list\<T\>)               | 列表初始化                                |

| 赋值与swap         | 作用                  |
| ------------------ | --------------------- |
| c1 = c2            | 将c2赋值给c1          |
| c = {a, b, c, ...} | 替换c中元素为列表元素 |
| c1.swap(c2)        | 交换c1，c2中的元素    |
| swap(c1, c2)       | c1.swap(c2)           |

| 大小相关                               | 作用             |
| -------------------------------------- | ---------------- |
| size_type size()（forward_list不支持） | 返回保存元素数目 |
| size_type max_size()                   | 可保存的最大数目 |
| bool empty()                           | 是否为空         |

| 添加/删除元素（不适用于array）（*args*表示不同容器的不同接口） | 作用                             |
| ------------------------------------------------------------ | -------------------------------- |
| c.insert(*args*)                                             | 插入元素                         |
| c.emplace(*inits*)                                           | 通过*inits*参数构造c中的一个元素 |
| c.erase(*args*)                                              | 删除元素                         |
| c.clear()                                                    | 清空容器，返回void               |

| 关系运算符   | 支持容器           |
| ------------ | ------------------ |
| ==, !=       | 所有容器           |
| <, <=, >, >= | 不支持无序关联容器 |

| 通用迭代器           | 作用 |
| -------------------- | ---- |
| c.begin(), c.end()   |      |
| c.cbegin(), c.cend() |      |

| 反向迭代器成员（不支持forward_list） | 作用           |
| ------------------------------------ | -------------- |
| reverse_iterator                     | 反向迭代器类型 |
| const_reverse_iterator               | const的        |
| c.rbegin(), c.rend()                 | 尾后迭代器     |
| c.crbegin(), c.crend()               | const的        |

### 迭代器使用

迭代器范围。[b, e)。

```cpp
const auto begin = c.cbegin();
const auto end = c.cend();
while(begin != end) {	// 所有迭代器都支持!=
    *begin++ = val;		// 所有迭代器都支持*和++
}
```

### begin和end成员

- 不以c开头的成员都是带重载的成员函数，形式可能如下

  ```cpp
  const_iterator begin() const;
  iterator begin();
  ```

- 以c开头的是新版本为了支持auto与begin，end结合使用而引入的。

  ```cpp
  auto i1 = c.begin();	// 当且仅当c是const时，i1是const_iterator
  auto i2 = c.cbegin();	// i2是const_iterator
  ```

### 赋值和swap

- 赋值，assign操作，只支持顺序容器

  ```cpp
  vector<int> v;
  v.assign(il);
  v.assign(n, t);
  v.assign(b, e);	// 可以用这个重载将不同但相容的容器元素赋值到另外的容器里
  ```

  ```cpp
  list<string> names;
  vector<const char*> old;
  names.assign(old.cbegin(), ole.cend());	// const char* 转换为string
  ```

- swap

  除了array（真正交换），swap不会对任何元素进行拷贝、删除、插入操作。

  swap操作之后，容器的迭代器、引用、指针都不会失效，都指向原来的元素（除了string）。

  例如，iter在swap前指向vec1[3]，swap之后iter指向vec2[3]。

- 赋值和 swap 与迭代器

  赋值操作会导致左侧容器的迭代器、引用、指针失效。

  swap 操作不会导致容器的迭代器、引用、指针失效（除了 array 和 string）。

### 关系运算符

与string的比较方式相似。



## 顺序容器操作

### 与大小相关的构造函数

```cpp
vector<int> v(n);	// 大小为n的vector
vector<int> v(n, v);// 大小为n，n个元素的初始值都为v的vector

string s(n);
string s(n, 'a');
```

### 向顺序容器添加元素

array没有添加元素的方法。

| 方法                                       | 作用                                                       |
| ------------------------------------------ | ---------------------------------------------------------- |
| c.push_back(t), c.emplace_back(*args*)     | 在尾部追加元素。                                           |
| c.push_front(t), c.emplace_front(*args*)   | 在首部添加元素。                                           |
| c.insert(iter, t), c.emplace(iter, *args*) | 在iter位置前插入元素。返回新插入元素的迭代器。             |
| c.insert(iter, begin, end)                 | 插入。若b到e为空，则返回iter；否则返回新添加元素的迭代器。 |
| c.insert(iter, il)                         | 同上。                                                     |

#### insert的使用

- 在特定位置添加元素

  ```cpp
  auto iter = v.begin();
  v.insert(iter, t);
  ```

- 插入范围内元素

  ```cpp
  vector<int> v;
  list<int> l{1, 2, 3};
  v.insert(v.end(), l.begin(), l.end());
  ```

- 源迭代器不能与目的迭代器指向相同位置

  ```cpp
  vector<int> v{1, 2, 3};
  auto dest = v.begin();
  auto src_b = v.begin();
  auto src_e = v.end();
  v.insert(dest, src_b, src_e);	// 运行时错误。
  ```

- 使用insert的返回值

  insert返回新插入元素的迭代器，如果为空则返回原迭代器。

  即返回值在容器的位置与插入在容器的相对位置相同。

  可以利用insert的返回值持续在一个特定位置反复插入元素。

  ```cpp
  list<string> l;
  auto iter = l.begin();
  while(cin >> word)
      iter = l.insert(l, word);
  // iter的值可能会改变，但是使用insert返回值更新后，仍然指向l.begin()。
  ```



#### 使用emplace操作

emplace(*args*)是直接通过*args*调用构造函数，直接在容器上构造对象，而非拷贝对象到容器上（push操作可能是拷贝）。

### 访问元素

at 和下标操作只适用于 string、vector、deque、array。

back 不适用于 forward_list。

| 操作                | 作用                                      |
| ------------------- | ----------------------------------------- |
| c.at(index)         | 返回下标为 index 的引用，越界则抛出异常。 |
| c[index]            | 越界未定义。                              |
| c.front(), c.back() | 返回引用，越界未定义。                    |

#### 下标操作和安全的随机访问

- 使用 at 成员函数以确保下标是合法的。
- 下标运算符不检查下标是否在合法范围内。

### 删除元素

| 操作                        | 作用                                                         |
| --------------------------- | ------------------------------------------------------------ |
| c.pop_back(), c.pop_front() |                                                              |
| c.erase(p)                  | 删除迭代器 p 指向的对象，返回指向下一个对象的迭代器。        |
| c.erase(b, e)               | 删除迭代器范围的对象，返回指向最后一个被删除元素之后元素的迭代器。 |
| c.clear()                   | 删除 c 中所有元素。                                          |

- 删除 deque 中除首尾位置之外的任何元素都会使得所有的迭代器、引用、指针失效。
- 指向 vector 或者 string 中删除点之后位置的迭代器、引用、指针都会失效。

#### 从容器内部删除一个元素

删除 list 中所有奇数元素。

```cpp
list<int> l({1, 2, 3, 4, 5});
auto it = l.begin();
while(it != l.end()) {
    if(*it & 1) {
        it = l.erase(it);	// 是则删除，赋值后 it 指向被删除元素的下一个元素。
    } else {
        ++it;	// 不是则继续遍历。
    }
}
```

#### 删除多个元素

```cpp
it1 = l.erase(it1, it2);	// 调用后，it1 == it2
```

### 改变容器大小

顺序容器的大小操作（不支持 array）

| 操作           | 作用                                                         |
| -------------- | ------------------------------------------------------------ |
| c.resize(n)    | 调整 c 的大小为 n。多出来的元素会被丢弃，新元素执行值初始化。 |
| c.resize(n, t) | 调整 c 的大小为 n。新添加的元素初始化为 t。                  |

### 容器操作可能使迭代器失效

添加元素的情况：

- vector 或者 string，当空间重新分配，指向容器的迭代器、指针、引用都会失效。若没有重新分配，则添加位置之后的迭代器、指针、引用都会失效。
- deque，插入到除首尾之外的任何位置都会使迭代器、指针、引用失效。在首尾位置添加元素，迭代器会失效，但指向存在的元素的引用和指针不会失效。
- list 和 forward_list，指向容器的迭代器、指针、引用仍有效。

指向被删除元素的迭代器、指针、引用都会失效。

删除一个元素的情况：

- 对于 list 和 forward_list，指向其他位置的迭代器、引用、指针仍有效。
- 对于 deque，如果删除首尾之外的任何元素，所有元素的迭代器、引用、指针也会失效。删除首/尾的情况，除了首前/尾后迭代器失效外，其他不会受到影响。
- 对于 vector 和 string，被删除元素之前的迭代器、引用、指针仍有效。删除元素时，尾后迭代器总是会失效。

## string

严格来说不属于容器。字符串。标准库类型string (std::string)。

- 运算符重载方法

  ```cpp
  string str3;
  string str1="abc";		//字面量字符串的隐式转换。
  string str2="123";
  
  str3=str1+str2;			//str3=="abc123"
  str2<str1;				//compare by [index] to [index].
  str1=="abc"				//true. 此处表明string可以直接使用重载运算符与const char[]比较。但char[]与char[]之间不可以直接比较。
  ```

- 迭代器

  ```cpp
  string str="abcd";
  string::iterator is1=str.begin();
  string::iterator is2=str.end();
  while(is1<is2)
      cout<<*is1++;
  cout<<endl;
  ```

- 标准库类型字符串初始化

  ```cpp
  string str1;
  
  //copy str1 to str2, the same.
  string str2=str1;
  string str2(s1);	
  
  //传统字符串的隐式转换。
  string str3="something strange.";
  //传统字符串的显式转换。
  string str3("something strange.");
  
  //directly create ccccccccccc.
  string str4(10,'c');
  ```

- 标准库类型字符串方法

  ```cpp
  string str="wdnmd";
  
  str.empty();	//return true or false.
  str.length();	//return length without '\0'.
  str.size()==str.length();
  
  str.at(0)==str.c_str()[0]=='w';
  
  str.find("wd");										//return index of "wd", or string::npos for none.
  str.find('m');										//return index of 'm', or string::npos.
  str.insert(str.begin()+i,'x');						//generally in container.
  str.insert(1,"xxx");								//particularly in string.
  str.replace(str.find("xxx"),sizeof("xxx"),"a");		//replace the first "xxx" to "a" for one time.
  
  str.erase(poz);										//erase the element of address poz(not index).
  str.erase(index,n);									//erase str[index : n+1];
  ```

- 标准库类型字符串的拓展方法

  ```cpp
  string str;
  //getline(input_stream,string str);		'\n' will be deserted (not in buffer)
  while(getline(cin,str))		//maybe EOF. 
      cout<<str<<endl;
  ```

  ```cpp
  //cctype	字符处理类。
  #include<cctype>
  #include<iostream>
  ```

- 需注意的

  传统字符串与string不是同一种类型。



## vector<**T**>

线性表。

### 声明与初始化

```cpp
#include<vector>
using std::vector;

int main(void)
{
    //vector<class_name> vec_name;
    vector<int> int_vec;
    //v1,v2,v3 have the same value.
    vector<int> v1;
    vector<int> v2(v1);
    vector<int> v3=v1;
    //init v4 with n elements maybe values 0, v5 with n elements values x.
    vector<int> v4(n);
    vector<int> v5(n,x);
    //v6 and v7 have the same value.
    vector<int> v6{a,b,c};		//列表初始化。
    vector<int> v7={a,b,c};		//列表初始化。
}

```

### 列表初始化

当无法进行列表初始化时，则将{}内的值作为构造函数的参数进行构造。

```cpp
vector<string> sth={"ixixi","wa","x"};	//等价于vector<string> sth{"ixixi","wa","x"};
vector<string> vs{10,"wa"};				//等价于vector<string> vs(10,"wa");	
```

### 数组初始化vector

STL的begin()方法，用来获得C风格数据类型的迭代器。

```cpp
int arr[]={1,2,3,4};
vector<int> v(begin(arr),end(arr));
```

### vector方法

```cpp
typename T
vector<T> v={1,2,3};

v.back();		//return the last element.
v.front();		//return the first element.

v.push_back(x);
v.pop_back();	//erase the last element.
v.erase(x);		//erase the element of address x(iterator).
v.insert(find(v.begin(),v.begin(),x),a);
v.insert(poz,v.begin(),v.end());			//insert a vector.
v.insert(poz,x);

v.size();		//length of v.
v[i];			//[i] element.
v1==v2;			//sequence and value both the same.
```

- 添加新元素的方法

  ```cpp
  /* wrong method */
  vector<int> v;	//v without init.
  int i;
  for(i=0;i<len;i++)
      v[i]=i;
  
  /* available method */
  vector<int> v;
  int i;
  for(i=0;i<len;i++)
      v.push_back(i);
  ```

## 容器适配器

适配器（adaptor）是一种机制，能够使某种事物的行为看起来像另外一种事物一样。

### 标准库定义的适配器

| 标准库定义的适配器 | 外在表现 | 默认实现 |
| ------------------ | -------- | -------- |
| stack              | 栈       | deque    |
| queue              | 队列     | deque    |
| priority_queue     | 优先队列 | vector   |

### 适配器支持的操作

| 操作           | 作用                             |
| -------------- | -------------------------------- |
| size_type      | 足以保存当前类型的最大对象的大小 |
| value_type     | 保存元素的类型                   |
| container_type | 实现适配器的底层容器类型         |

### 定义适配器

通过第二个类型参数重载默认容器类型。

```cpp
stack<int, vector<int>> s;
```

- 要求容器拥有添加和删除元素的能力。

# 关联容器

## 无序unordered_map<KEY,VAL> 

哈希函数实现，元素类型为pair{KEY first; VAL second;}。

初始化

```cpp
#include<unordered_map>
struct pair<KEY,VAL>{
    KEY key;
    VAL val;
};
unordered_map<string,int> hash={
    {"watashi",1106},
    {"kare",801},
};
```

## 有序map<KEY,VAL>

红黑树实现，中序遍历之即可获得有序序列。

```cpp
#include<map>
map<string,string> dict;
```

## map

| map容器             | 特性 |
| ------------------- | ---- |
| map                 |      |
| unordered_map       |      |
| unordered_multi_map |      |
| multi_map           |      |

## set

| set容器 | 特性 |
| ------- | ---- |
|         |      |

# 泛型算法

- 算法不依赖于容器，依赖于元素类型的操作

- 算法永远不会执行容器的操作，不会改变底层容器的大小

  可能会改变容器中元素的值，可能移动元素，但永远不会直接添加或删除元素。

## 算法类别

### 只读算法

`find`、`count`、`accumulate` 等不改变元素，不改变元素顺序的算法。

- accumulate 方法

  `decltype(v) accumulate(b, e, v);`

  在 numeric 中，返回以 v 为初值的加和拷贝，返回值 sum 的类型只与 v 有关。

  ```cpp
  list<string> l;
  auto sum = accumulate(l.begin(), l.end(), string(""));
  ```

- equal 方法

  `bool equal(a1, a2, b1);`

  操作两个序列的算法。返回 a、b 两个序列是否保存相同的值，b 序列的迭代长度取决于序列 a。

  ```cpp
  vector<string> a;
  vector<const char *> b;
  equal(a.begin(), a.end(), b.begin());	// 只要元素间能够使用 == 比较即可。
  ```

### 写容器元素的算法

会将新值赋给容器中的元素的算法。

- fill 方法

  `fill(b, e, v);`

  将 b, e 范围内的值全部赋为 v。

  ```cpp
  vector<int> v(10);
  fill(v.begin(), v.end(), 1);
  ```

- copy 方法

  `decltype(dest) copy(src.begin(), src.end(), dest.begin());`

  将 src 范围内的元素拷贝到 dest 中。返回 dest 容器的 `src.end() - src.begin()` 位置。

- replace 方法

  `replace(a.begin(), a.end(), old, new);`

  将范围内 old 值全部替换为 new。

- replace_copy 方法

  `replace(a.begin(), a.end(), dest.begin(), v);` 

  保持原序列不变，将替换后的拷贝保存到 dest 中。

### 重排容器元素的算法

- sort 方法

- unique 方法

  ` a::itereator unique(a.begin(), a.end());`

  将 a 中不一样的元素重排到前面，要求 a 为有序序列，返回重排后最后一个不重复元素的下一个元素的迭代器，该迭代器之后的元素的值是未定义的。

  ```cpp
  // 删除重复元素
  vector<int> a = {4, 3, 2, 1, 3, 3, 2, 1};
  sort(begin(a), end(a));
  auto i = unique(begin(a), end(a));
  while(i != a.end()) {
  	i = a.erase(i);
  }
  ```

  

## lambda 表达式

- 一种可调用对象。

- 一个 lambda 表达式表示一个可调用的代码单元。

- 可以理解为一个未命名的内联函数。
- 可以定义在函数内部。

### lambda 表达式的一般形式

`[capture list] (parameter list) -> return type { function body }`

- lambda 表达式可以忽略参数列表和返回类型，但必须包含捕获列表和函数体。

  ```cpp
  auto f = []{ return 1; }
  cout << f() << endl;
  ```

- 返回类型必须使用尾置返回。

  如果函数体包含任何单一 return 语句之外的内容，且未指定返回类型，则返回 void。

  如果函数体只有单一的 reutrn 语句，且未指定返回类型，则会自动推断 return 的类型。

### 向 lambda 传递参数

- lambda 不能有默认参数，因此实参数目永远与形参数目相等。

```cpp
auto isShorter(const string &a, const string &b) -> bool {
    return a < b;
}
// 与 isShorter 功能相同的 lambda 表达式
[](const string &a, const string &b){ return a < b; }
```

### 使用捕获列表

使用捕获列表可以将 **lambda 表达式所在函数中**的局部变量传递给 lambda 表达式，否则这些局部变量不能在 lambda 表达式中使用。

- 使用 find_if 查找第一个符合条件的对象

  find_if 会使用迭代到的元素的引用回调传入的 lambda 表达式。

  ```cpp
  // 返回第一个 size() >= sz 的元素的迭代器
  auto wc = find_if(words.begin(), words.end(), [sz](const auto &a){ return a.size() >= sz; });
  ```

- for_each 算法

  与 for 类似。

  ```cpp
  for_each(words.begin(), words.end, [](const auto &a){ cout << a << " "; });
  ```

  注意 lambda 函数体中的 cout 对象，由于该对象不是 **lambda 表达式所在函数中**的局部变量，所以可以在 lambda 函数体内直接只用该变量。

### lambda 的捕获和返回

lambda 生成的类都包含一个对应 lambda 所捕获变量的数据成员。与任何普通类类似，lambda 的数据成员也在 lambda 对象创建时被初始化。

- 值捕获

  能够采用值捕获的前提是变量可以拷贝。与 lambda 参数列表不同，被捕获的变量的值是在 lambda 创建时拷贝，而非调用时拷贝。

  ```cpp
  {
      auto i = 1998;
      auto f = [i] { return i; };	// 直接在捕获列表中写入变量名即可值捕获局部变量。
      i = 0;
      auto j = f();	// 注意此时 j == 1998，因为 i 在 f 创建时被值捕获。
  }
  ```

- 引用捕获

  ```cpp
  {
      auto i = 1998;
      auto f = [&i] { return i; };
      i = 1987;
      auto j = f();	// 此时 j 为1987。
  }
  ```

  引用捕获与返回引用有相同的问题和限制（不要返回局部对象的引用）。使用引用捕获时，要确保引用的对象在 lambda 执行的时候是存在的。

- 使用 os 输出 words，分隔符为 c

    ```CPP
    void print(vector<string> &words, ostream &os = cout, char c = ' ')
    {
        for_each(words.begin(), words.end(), [&os, c] (const auto &a) { 	// 函数参数列表的对象也属于该函数的局部对象？
            os << a << c;	// ostream 不可拷贝，c 可以拷贝。
        });
    }
    ```

- 隐式捕获和显式捕获的混合使用

  隐式捕获符必须写在第一个的位置。

  `[=, identifier_list]` 显式捕获列表 list 中的名字必须使用 &，统一采用引用捕获的方式。

  `[&, identifier_list]` 显式捕获列表 list 中的名字不能使用 &，统一采用值捕获的方式。

- 可变 lambda 

  默认情况下，不会改变值捕获的变量的值（值捕获到 lambda 的量是 const 的，即便它只是拷贝）。

  ```cpp
  auto i = 1;
  auto f = [=] { return ++i; };	// 会报错
  ```

  如果希望修改值捕获到的量，则必须在参数列表后加上关键字 `mutable` ，对于可变 lambda 不能省略参数列表。

  ```cpp
  auto i = 1;
  auto f = [=] () mutable { return ++i; };
  ```

  - 对于引用捕获的变量没有此限制

    ```cpp
    auto i = 1;
    auto f = [&] { return ++i; };
    f();	// i == 2;
    ```



## 参数绑定

在 functional 头文件中。

```cpp
auto newCallable = bind(callable, arglist);
```

返回一个可调用对象 newCallable，调用 newCallable 时会按照 arglist 中参数的顺序传递给 callable 对象，并调用 callable。

```cpp
// 调用 newCallable() 的等价调用
callable(arglist);
```

### 占位符

如果希望在调用 bind 返回的对象 newCallable 时传递参数，则需要在 bind 中用到占位符。

`using std::placeholders::_n` ，n 对应 newCallable(*arglist*) 的参数列表中的第 n 个参数。

当 newCallable 回调 callable 时，首先会将 newCallable 中的 arglist 按照占位符的映射规则映射到 bind 中的 arglist，然后再回调 callable。

占位符的个数等于 newCallable 的形参列表的参数个数。

```cpp
void callable(string end, string s1, string s2, string s3) 
{
    cout << s1 << " " << s2 << " " << s3 << " " << end << endl;
}
auto newCallable = bind(callable, "!", _3, _1, _2);
newCallable("Maji"/* 映射到_1 */, "Tenshi"/* 映射到_2 */, "Aqua"/* 映射到_3 */);
// 此时等价于 bind(callable, "!", "Auqa", "Maji", "Tenshi");
// 等价调用 callable("!", "Aqua", "Maji", "Tenshi")
// 输出：Aqua Maji Tenshi !
```

- 使用占位符定制 sort 的比较函数

  ```cpp
  bool isSmaller(const string &a, const string &b);
  sort(v.begin(), v.end(), bind(isSmaller, _1, _2));	// 此时按照升序排序
  sort(v.begin(), v.end(), bind(isSmaller, _2, _1));	// 此时按照降序排序
  ```

### 引用参数的绑定

默认情况下，bind 中非占位符的参数会被拷贝到 bind 返回的可调用对象中。

使用标准库中的 `ref` 函数，返回包含给定的引用的对象，此对象可以拷贝。`cref` 则返回保存 const 的引用的对象。

## 定制操作

### 谓词

可调用的表达式，返回结果是 bool 类型，用作条件。标准库算法会使用的谓词只有一元谓词、二元谓词，元表示该谓词会接受多少个参数。调用算法时，算法会使用迭代到的元素的引用回调该谓词，然后根据谓词的返回结果做相应操作。

### 通过传递函数指针定制排序算法

```cpp
bool isShorter(const string &s1, const string &s2)
{
    // 排序算法的默认操作
    return s1 < s2;
}
sort(word.begin(), word.end(), isShorter);
```

## 泛型算法与迭代器

### back_inserter



## 泛型算法结构

## 特定容器算法



# 动态内存

## 智能指针

用于动态分配的，自动释放指向对象的指针。

- shared_ptr<*T*>类

  - shared_ptr的声明与初始化

    ```cpp
    #include<memory>
    template<typename T>
    shared_ptr<T> pt;
    template<typename T>
    pt=make_shared<T>(/* T的构造函数对应参数 */)
    
    auto pt=make_shared<T>();
    
    //隐式转换的拷贝构造。
    shared_ptr<int> p1(p2);
    ```

  - shared_ptr不能进行的操作

    ```cpp
    // 不能使用&操作符进行赋值，故只适用于动态分配对象时生成的指针。
    shared_ptr<int> pint;
    int a;
    pint=&a;			
    ```

  - shared_ptr独有方法

    ```cpp
    shared_ptr<T> p,p1,p2;
    
    //交换指针。
    p.swap(q);
    swap(p,q);
    
    //返回共有几个与p指向同一对象的共享指针数目。
    p.use_count();
    //return p.use_count()==1;
    p.unique();
    
    //r指向对象的引用次数递增，p指向对象的引用次数递减。
    p1=p;
    
    //返回传统指针。
    p.get();
    ```
  
  - shared_ptr的特性
  
    1，p的析构函数会递减其指向对象的引用次数，当计数等于0，其析构函数会销毁指针，并且释放所指对象。
  
    2，若有其他计数不为0的shared_ptr指向某一对象，则该对象不会被释放。
    
    3，p离开其作用域时，在符合前两条规则的情况下会释放p指向的对象。
    
  - 使用智能指针的情形
  
    1，未知使用对象的数目。
  
    2，未知对象的类型。
  
    3，需要在多个对象间共享数据。
  
- unique_ptr

  指向某一对象的唯一指针。指针与对象同生共死。

  - 声明与初始化

    需要进行直接初始化，与引用类似。

    ```cpp
    unique_ptr<int> p(new int(114514));
    int *q=new int(1024);
    unique_ptr<int> p(q);
    ```

    不可拷贝与赋值。

    ```cpp
    unique_ptr p1,p2;
    /* wrong */
    //unique_ptr p(p1);
    //p1=p2;
    ```

  - 独有方法

    ```cpp
    unique_ptr<T> u;
    u=nullptr;			//释放对象并且置空指针。
    u.release();		//放弃控制权，u置空。
    u.reset();			//置空。
    u.reset(p);			//p为内置指针，u指向p所指对象。
    ```

  - 传参与返回unique_ptr

  - 删除器

- weak_ptr

  指向由shared_ptr管理的对象，不改变shared_ptr的引用次数，不影响指向对象的生存期。

  - 方法

    ```cpp
    weak_ptr<T> w;
    w.use_count();	//返回共享对象的shared_ptr的数量。
    w.expired();	//return w.use_count()==0;
    w.lock();		//返回一个指向该对象的shared_ptr；若对象已被释放，则返回nullptr。
    ```

    

## 直接管理内存

现代c++程序不应出现delete。

- 使用new动态分配内存

  返回对应类型且指向动态分配的对象的指针。

  ```cpp
  //指向未初始化的int类型内存空间。
  int *p=new int;
  //指向初始值为0的int类型内存空间。
  int *p=new int(0);
  //const int类型。
  int *p=new const int(1024);
  ```

- 内存耗尽与异常处理

  ```cpp
  int *p=new int;				//分配失败时抛出std::bad_alloc。
  //处理异常
  int *p=new (nothrow) int;	//分配失败则返回nullptr。
  ```

- 使用delete释放**动态分配**的内存

  不可用于静态内存。

  动态分配的内存的生存周期由分配到手动释放。

  释放内存后，p将变为空悬指针，需手动赋值nullptr，以防止非法访问。

  ```cpp
  //单一对象。
  int *p=new const int(114514);
  delete p;
  //数组。
  int *p=new int[LEN];
  delete[] p;
  //释放后的处理。
  p=nullptr;
  ```

  若有多个指针指向同一个对象，则不能只赋值一个nullptr。

  找到所有指向同一对象的指针十分困难。

  ```cpp
  int *p,*p1,*p2;
  p=new int(114514);
  p1=p2=p;
  delete p;
  p1=p2=p=nullptr;
  ```

- shared_ptr与new的结合使用

  ```cpp
  shared_ptr<int> p;
  
  //错误，不可将int *直接赋值给。
  //p=new int(114514);
  
  //正确的。
  shared_ptr<int> p(new int(114514));
  ```

  不要用p.get()返回的指针初始化shared_ptr。

  不要对p.get()返回的指针进行delete。

  ```cpp
  shared_ptr<int> p(new int(114514));
  int *q=p.get();
  
  //non non dayo.
  //delete q;
  //shared_ptr np(q);
  ```

- 应用

  判断是否独占，只有独占才进行赋值操作，否则拷贝之。

  ```cpp
  if(!p.unique())
      p.reset(new string(*p));
  else
      *p="ahh";
  ```



## 智能指针和异常

- 异常发生时智能指针会自动释放资源，而普通指针不会。



## 智能指针陷阱

- 不使用相同内置指针值初始化多个智能指针。
- 不delete get()返回的指针。
- 不使用get()初始化新的智能指针。
- 删除器。

## allocator类

分配一大块内存，按需构造对象，分配与构造对象分离。

```cpp
allocator<T> alloc;
T * p=alloc.allocate(n);					//分配n个未初始化的T，不可直接使用。
alloc.construct(p,/* T的构造函数对应参数 */);	//对已分配的内存进行T构造。
alloc.destroy(p);	//对p所指对象执行构造函数，但不回收已分配内存。
alloc.deallocate(p,n);	//释放p所指的一大块内存，n为之前申请的大小，执行该命令前需对涉及到的对象执行析构函数。
```

- 拷贝和填充未初始化内存的算法

