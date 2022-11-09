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

