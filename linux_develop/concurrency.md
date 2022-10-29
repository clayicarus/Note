# 多进程

## fork（）

创建当前进程的副本作为子进程。

### 函数原型

```c
#include<unistd.h>
pit_t fork(void);
```

### 返回值

```cpp
pit_t pid;
pid=fork();
if(pid==0)
    cout<<"here is child process."<<endl;
else
    cout<<"here is parent process."<<endl;
```

- pid==0;

  此时为子进程。

- pid==n;

  此时为父进程。n为该父进程的子进程的pid。

### 应用场景

- 多进程并发服务器。
