## demo

```cmake
cmake_minimum_required(VERSION 3.23)
project(project_name)
set(CMAKE_CXX_STANDARD 17)
set(SRC_LIST a.cpp b.cpp)
add_executable(target_name main.cpp ${SRC_LIST})
target_link_libraries(target_name PRIVATE lib_list)
```

## 库文件

```cmake
add_library(libhello SHARED hello.c) #生成动态库文件
add_library(libhello STATIC hello.c) #生成静态库文件
set_target_properties(libhello PROPERTIES OUTPUT_NAME "hello")	# 生成文件名为libhello的库
```

## 语句

### set()

- 变量名在set中声明，用 ${var} 引用

### target_link_libraries()

| parameter | 作用                                                         |
| --------- | ------------------------------------------------------------ |
| PUBLIC    | 在public后面的库会被Link到你的target中，并且里面的符号也会被导出，提供给第三方使用。 |
| PRIVATE   | 在private后面的库仅被link到你的target中，并且终结掉，第三方不能感知你调了啥库。 |
| INTERFACE | 在interface后面引入的库不会被链接到你的target中，只会导出符号。 |

### 路径

库的？头文件的？

```
include_directories()
link_directories()
```

### find_package()

`find_package`用于查找包（通常是使用三方库），并返回关于包的细节（使用包所依赖的头文件、库文件、编译选项、链接选项等）。

```cpp
find_package(<package> CONFIG REQUIRED)
```

- REQUIRED

  找不到就报错。

- CONFIG、MODULE

  搜索方式不同？CONFIG一般用于搜索第三方库。



## 杂物

- cmake的参数名都是大写的。

