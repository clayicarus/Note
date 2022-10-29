# 出错处理

## errno

```cpp
extern int *__errno_location(void);
#define errno (*__errno_location())
```

## 打印出错信息

### strerror()

将指定errno的值映射为出错消息字符串。

```cpp
#include<string.h>
char *strerror(int errnum);
```

### perror()

打印当前error值对应的字符串并附加msg信息。

msg: *错误字符串*

```cpp
#include<stdio.h>
void perror(const char *msg);
```



# 文件I/O

## open(), openat()

### 函数原型

```cpp
#include<fcntl.h>
int open(const char *path, int oflag, ... /* mode_t mode */);
int openat(int fd, const char *path, int oflag, ... /* mode_t mode */);
```

- oflag

    | oflag    | 功能 |
    | -------- | ---- |
    | O_RDONLY |      |
    | O_WRONLY |      |
    | O_RDWR   |      |
    | O_APPEND |      |
    | O_CREAT  |      |

## lseek

用于显式设置打开文件的偏移量。

### 函数原型

```cpp
#include<unistd.h>
off_t lseek(int fd, off_t offset, int whence);
```



# POSIX信号处理

## 信号的基本性质

- 信号不排队（当有一个信号未处理完毕时新信号不起作用，且之后也不会起作用）。

## sigaction()

设置信号处理函数的函数。

### 函数原型

```cpp
int sigaction(int signo, const struct sigaction *act, struct sigaction *oldact);
```

```c
//简化
typedef void Sigfunc(int);
```

将原来的处理方法写入oldact。

### struct sigaction

```cpp
struct sigaction{
    Sigfunc *sa_handler;
    void (*sa_sigaction)(int, siginfo_t* ,void*);
    sigset_t sa_mask;
    int sa_flags;
    void (*sa_restorer)(void);
};
```

- sa_flags

  用于设置可选标志。

  | 标志         | 作用                                                 |
  | ------------ | ---------------------------------------------------- |
  | SA_RESETHAND |                                                      |
  | SA_RESTART   | 若信号中断了某个系统调用，则系统自动启动该系统调用。 |
  | SA_NODEFER   |                                                      |

- sa_handler

  与signal的handler参数相同，作为信号触发时需要调用的函数。

- sa_mask

  用于屏蔽不需要捕获的信号，对设置的信号不做响应。

- 其余属性没用到。

## 常用信号源

| 名      | 产生时机                                                     |
| ------- | ------------------------------------------------------------ |
| SIGCHLD | 子进程结束时发送给父进程的信号。                             |
| SIGPIPE | 向一个接收到RST后的套接字write的时候产生的信号。需要适当处理。 |



## 僵尸进程的处理

### 僵尸进程概念

当子进程比父进程先结束，而父进程又没有回收子进程（释放子进程占用的资源），则子进程会变成僵尸进程。

若父进程先结束，子进程将会被init接管，子进程退出后init会回收其占用的相关资源。

- 使用fork时必须捕获SIGCHLD信号。
- 捕获信号时必须处理被中断的系统调用。
- 使用waitpid（非阻塞）以清理所有僵尸进程。

### wait() 处理

等待一个子进程结束，并释放其资源。

- 函数原型

  ```cpp
  #include<sys/wait.h>
  pid_t wait(int *stat);
  ```

  阻塞至有一个子进程结束。

  返回值为wait到的一个子进程。

  stat保存子进程结束时的返回值。

- SIGCHLD信号辅助处理

    为不进入阻塞状态使用SIGCHLD信号辅助回收僵尸进程。
    
    ```cpp
    void sig_chld(int signo)
    {
        pid_t pid;
        int sta;
    
        pid=wait(&stat);
        cout<<"child "<<pid<<" terminated."<<endl;
        return;
    }
    
    int main()
    {
        pid_t p;
        
        Signal(SIGCHLD,sig_chld);
        
        p=fork();
        if(p==0){
            //制造僵尸进程。
            sleep(5);
            exit(0);
        }else{
            //捕获到信号并调用函数时会中断休眠，故实际休眠时间不足100s。此时会返回EINTR错误。
            sleep(100);	
            //重新休眠，以便观察。
            sleep(5);
            exit(0);
        }
    }
    ```

### waitpid() 处理

- 函数原型

  ```cpp
  #include<sys/wait.h>
  pid_t waitpid(pid_t pid, int *statloc, int options);
  ```

- pid

  允许指定需要等待的子进程的pid，-1表示等待第一个终止的子进程。

- options

  | 选项    | 作用                   |
  | ------- | ---------------------- |
  | WNOHANG | 无终止子进程时不阻塞。 |

#### 处理示例

```cpp
void sig_chld(int signo)
{
    pid_t pid;
    int stat;
    while((pid=waitpid(-1,&stat,WNOHANG))>0)
        cout<<pid<<" terminated."<<endl;
   	return;
}
```

# 进程间通信

## pipe()

用于创建一个管道，进程间可以通过该管道进行通信。

### 函数原型

成功返回0，失败返回-1。

```cpp
#include<unistd.h>
int pipe(int fd[2]);
```

- fd[2]

  用于构成管道的两端。

  - fd[0]，读端，只可以用于读取数据。
  - fd[1]，写端，只可以用来写入数据。

## socketpair()

可用来方便地创建双向管道，本质为套接字，仅能用于本地通信。

### 函数原型

成功返回0，失败则-1。

```cpp
#include<sys/socket.h>
int socketpair(int domain, int type, int protocol, int fd[2]);
```

- domain

  协议族，只可用AF_UNIX，表示本地通信。

- type

  套接字类型。

- protocol

  协议。

- fd[2]

  两个双向管道（与pipe的fd不一样）。

  



# I/O函数

## splice()

零拷贝。用于在两个文件描述符之间移动数据。两个描述符必须有一个或一个以上是管道描述符。

### 函数原型

返回移动字节数。失败则返回-1。

```cpp
#include<fcntl.h>
ssize_t splice(int fd_in, loff_t *off_in, int fd_out, loff_t *off_out, size_t len, unsigned int flags);
```

- fd_in/fd_out

  输入/输出。

- off_in/off_out

  用于指出流的偏移位置，无偏移则令其为NULL。

  若fd_in/fd_out为管道描述符时，对应的off_in/off_out必须设置为NULL。

- flags

  指定splice的参数。

  | 选项              | 作用                                               |
  | ----------------- | -------------------------------------------------- |
  | SPICE_F_MOVE      | 按整页内存移动数据。实现存在bug，实际无效果。      |
  | SPLICE_F_NONBLOCK | 执行非阻塞的splice操作，受描述符本身的阻塞性影响。 |
  | SPLICE_F_MORE     | 提示给内核，后续的splice将传输更多的数据。         |

### 错误值

| 值     | 含义                                                         |
| ------ | ------------------------------------------------------------ |
| EBADF  | 描述符错误。                                                 |
| EINVAL | 目标描述符不支持splice；或文件以a模式打开；或两个描述符均不为管道；或offset参数用于不支持随机访问的设备。 |
| ENOMEM | 内存不足。                                                   |
| ESPIPE | 管道描述符对应的off不为NULL。                                |



# 文件描述符

## fcntl()

用于控制套接字的属性或操作。

### 函数原型

cmd为get时返回对应的值；cmd为set时返回是否成功（0）。

```cpp
#include<fcntl.h>
int fcntl(int fd, int cmd, ... /* int arg */);
```

- fd

  需要操作的描述符。

- cmd

  执行什么样的操作。

  | cmd      | 操作             |
  | -------- | ---------------- |
  | F_SETFL  | 设置套接字类型。 |
  | F_GETFL  | 获取套接字类型。 |
  | F_SETOWN | 设置套接字属主。 |
  | F_GETOWN | 获取套接字属主。 |

- ... /\* int arg \*/

  需要设置的属性。

  | arg        | 作用                |
  | ---------- | ------------------- |
  | O_NONBLOCK | 设置为非阻塞式I/O。 |
  | O_ASYNC    | 信号驱动式I/O。     |



# 线程

## 线程的创建与终止

### pthread_create()

出错返回非0值，不设置errno，直接返回错误码。成功返回0。

```cpp
#include<pthread.h>
int pthread_create(pthread_t *tid, const pthread_attr_t *attr, void *(*func)(void *), void *arg);
```

- tid

  线程变量指针。

- attr

  属性设置，默认为NULL。

- func

  线程函数指针，指向一个返回值为void\*、参数为void\*的函数。指定该线程做什么事情。

- arg

  作为线程函数的参数。



### 汇合线程：pthread_join()

如果主线程先到达汇合点，而新线程未返回，主线程则阻塞等待回收资源。

等待一个线程终止，类似waitpid()，但不能设置-1等待任意一个线程。

成功则0，失败则返回非0错误码。

```cpp
#include<pthread.h>
int pthread_join(pthread_t *tid, void **status);
```

- tid

  需要等待的线程tid。

- status

  所等待线程的返回值存入的位置（线程函数的返回值类型为void*），NULL则不存入返回值。

### pthread_self()

返回自身的线程ID。

```cpp
#include<pthread.h>
pthread_t pthread_self(void);
```



### 线程脱离：pthread_detach()

使线程脱离。

线程或是汇合的（joinable，默认值），或是脱离的（detached）。

汇合：主线程知道另一个线程终止。

脱离：线程返回时自动回收资源。主线程不知道线程终止，如守护进程。脱离线程的返回值和tid将留存至进程内的某个线程对其调用pthread_join()。

```cpp
#include<pthread.h>
int pthread_detach(pthread_t pid);
```

- 自我脱离

  ```cpp
  pthread_detach(pthread_self());
  ```




### pthread_exit()

终止一个线程。

```cpp
#include<pthread.h>
void pthread_exit(void *status);
```

### 其他终止线程的情况

- main返回，或某个线程调用了exit()时，进程终止，所有该进程的线程均终止。
- 线程函数返回。

## 线程特定数据

特定于线程的全局变量（静态变量）。以解决多线程函数必须共用静态变量的问题，避免不同线程在调用时访问静态变量（静态变量是线程共用的）造成的冲突问题。

可用于保存不同线程的公共状态。

### 可重入函数

- 可以被中断的函数。
- 不依赖自己栈外的任何变量。
- 可以被多个线程同时调用的函数。
- 线程安全的函数。

### 函数原型

#### pthread_key_create()

返回Key结构中的第一个空闲的键（Key的元素的索引）（到keyptr所指的位置）。

```cpp
#include<pthread.h>
int pthread_key_create(pthread_key_t *keyptr, void (*destructor)(void* value));
```

#### pthread_once()

在进程范围内仅执行一次该函数（init）。

```cpp
#include<pthread.h>
int pthread_once(pthread_once_t *onceptr, void (*init)(void));
```

#### pthread_getspecific()

返回键对应的线程特定的值。

```cpp
#include<pthread.h>
void *pthread_getspecific(pthread_key_t key);
```

#### pthread_setspecific()

对键设定一个值，该值是线程特定的。

```cpp
#include<pthread.h>
int pthread_setspecific(pthread_key_t key, const void *value);
```

### 使用线程特定的数据

func1和func2都需要用到Data。

```cpp
static pthread_key_t key;
static pthread_once_t once=PTHREAD_ONCE_INIT;
void func_destructor(void *ptr)
{
    free(ptr);
}
void func_once(void)
{
	pthread_key_create(&key, func_destructor);
}
struct Data{
    int cnt;
};

/* 记录该线程的func2的调用次数。 */
type func1()
{
    Data *pd;
    
    pthread_once(&once,func_once);
    pd=(Data*)pthread_getspecific(key);
    //没有则创建，有则使用之。
    if(pd==NULL){
        pd=(Data*)malloc(sizeof(Data));
        pd->cnt=0;
        pthread_setspecific(key,pd);
    }
    func2(pd);
    cout<<pd->cnt<<endl;
    
    return type();
}
type func2(Data *pd)
{
    pd->cnt++;
    
    return type();
}
```

## 互斥锁

用于保护一个共享变量。

### 函数原型

- pthread_mutex_lock()

  成功返回0，失败返回Exxx。

  ```cpp
  #include<pthread.h>
  int pthread_mutex_lock(pthread_mutex_t *mptr);
  ```

  

- pthread_mutex_unlock()

  成功返回0，失败返回Exxx。

  ```cpp
  #include<pthread.h>
  int pthread_mutex_unlock(pthread_mutex_t *mptr);
  ```

  

- pthread_mutex_init()

  若互斥锁变量是**静态分配**的，需要初始化为PTHREAD_MUTEX_INITIALIZER。

  若在共享内存区分配，则需用pthread_mutex_init()初始化。
  
  成功返回0，失败返回Exxx。
  
  ```cpp
  ```
  

### 可能会出错的地方

- 若试图对被另外的线程锁住的互斥锁上锁，则本线程将被阻塞，直到互斥锁被解锁。

## 条件变量

等待某个条件发生期间，让程序进入睡眠。





# 进程

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
