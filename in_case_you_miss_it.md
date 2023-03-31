## c语言
#### 函数指针

```c
int Func(int a,int b);
int (*pFunc)(int a,int b)=Func;
//pFunc(a,b)==Func(a,b)==*pFunc(a,b);
```

#### 结构体

声明与初始化。

```c
typedef struct sth{
    char name[LEN];
    int mass;
}sth;

//需要按照顺序
sth a={
    "amaterasu",
    120,
};
//无需顺序
sth b={
    .mass=120,
    .name="amamiya",
};
```



#### 变量储存类别

- **作用域**：变量的使用范围。
  - 块作用域（块内声明）：{}内或不带{}的块内可以使用。
  - 函数作用域：与goto相关。
  - 函数原型作用域（函数声明处声明）：形参定义处到函数声明结束。
  - 文件作用域（所有函数外声明）：
    - 外部链接文件作用域（可选extern声明）：程序内（需引用式声明）均可使用。
    - 内部链接文件作用域（带static声明）：翻译单元内可使用。
- **储存期**：变量存在时间。
  - 自动（auto）：块之外会被释放。
  - 静态（static）：在程序执行期间。
  - 线程：并发程序设计。
  - 动态分配：从分配到free()。
- **链接**：可否跨翻译单元使用变量。
  - 外部链接（extern）：多个翻译单元间（一般一个源文件为一个翻译单元）。
  - 内部链接：单个翻译单元内。
  - 无链接：在翻译单元内不可通用。
- **特殊变量类型**
  - 寄存器（register）。
- **需注意的**：指针可以无限制地使用变量。
- **外部变量的使用**：

## windows

#### 右键菜单

- 对文件右键
```
	HKEY_CLASSES_ROOT\*\shell
	HKEY_CLASSES_ROOT\*\shellex\ContextMenuHandlers
```

- 对文件夹右键

```
	HKEY_CLASSES_ROOT\Directory\shell
```

- 对所有文件或文件夹右键
```
	HKEY_CLASSES_ROOT\AllFilesystemObjects\shell
	HKEY_CLASSES_ROOT\AllFilesystemObjects\shellex\ContextMenuHandlers
```
- 在目录下直接右键

```
	HKEY_CLASSES_ROOT\Directory\Background\shell
```

- command

```
	notepad %1														//对文件
	powershell.exe -noexit -command Set-Location -literalPath '%V'	//对文件夹
```

## 数电
- 编码器比译码器好做一万倍
- 对于固定不变的数据使用rom而没必要使用译码器
