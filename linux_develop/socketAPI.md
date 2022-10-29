# 套接字编程的简要框架

## 套接字简介

网络数据传输用的软件设备。“套接字”表连接——两台计算机之间的连接。

### 监听套接字

用于监听欲连接主机，生成已连接套接字。

### 已连接套接字

处于ESTABLISHED状态的套接字，用于与已连接客户通信。

## 所需基本函数

### socket()

安装电话。

```c
//返回文件描述符(sockfd)，失败则-1。
int socket(int domain,int type,int protocol);
```

### bind()

给电话分配电话号码。

bind()调用的有无不影响connect()或是listen()的调用。无调用bind()则内核选择IP地址和端口。

```c
//成功返回0，失败则-1。
int bind(int sockfd,struct sockaddr *paddr,socklen_t addrlen);
```

TCP服务端

| IP                     | 端口 | 结果                         |
| ---------------------- | ---- | ---------------------------- |
| INADDR_ANY（通配地址） | 0    | 内核选择IP和端口             |
| INADDR_ANY（通配地址） | 非0  | 内核选择IP，进程指定端口     |
| 本地IP地址             | 0    | 进程指定IP地址，内核选择端口 |
| 本地IP地址             | 非0  | 进程指定IP和端口             |



### listen()

将套接字转换为监听套接字，并指定套接字排队的最大连接个数。

CLOSED状态转换为LISTEN状态。

```c
//成功返回0，失败则-1。
int listen(int sockfd,int backlog);
```

#### backlog参数

未完成连接队列：处于SYN_RCVD状态的套接字队列。

已完成连接队列：处于ESTABLISHED状态的套接字队列。

上述两队列之和不超过backlog。

- 不要把backlog定义为0。
- 当队列满，SYN到达，则该SYN将被忽略，从而不发送RST（以防导致对端终止）。
- 大于内核支持的最大backlog是合理的。

### connect()

打电话。

### accept()

听电话咯。

```c
//成功返回文件描述符，失败则-1。
int accept(int sockfd,struct sockaddr *paddr,socklen_t *addrlen);
```

### read()/write()

数据交换。非阻塞情况。

#### 阻塞式I/O的函数特性

- read()

  其余情况均阻塞。

  | 接收内容            | 返回值       |
  | ------------------- | ------------ |
  | 数据或数据捎带的ACK | 数据的字节数 |
  | FIN                 | 0（EOF）     |

  故在未知需接收数据大小时，需自定义应用级EOF或利用FIN作为接收完毕的标志。

- write()

  

### close()

引用计数减1。当引用次数为0时发送FIN，关闭套接字。

### getsockname()/getpeername()

```cpp
#include<sys/socket.h>
int getsockname(int fd, sockaddr *localaddr, socklen_t *addrlen);
int getpeername(int fd, sockaddr *peeraddr, socklen_t *addrlen);
```

- getsockname

  返回与该套接字相关联的本地协议地址。

  - 在未调用bind()的TCP客户端上获得内核赋予该连接（必须已经建立连接才可获得）的本地IP和本地端口。

    需在connect()成功返回后调用。

  - bind()通配地址的TCP服务端上获得内核分配的本地IP地址以及本地端口。

    需在accept()成功返回后对已连接套接字调用。

- getpeername

  返回与该套接字相关联的外地协议地址（对端地址）。



## 套接字构建

socket(domain,type,protocol);

### 协议族(domain)

协议是计算机间对话的通信规则。协议族为协议的大分类。

| 名称      | 协议族       |
| --------- | ------------ |
| PF_INET   | IPv4         |
| PF_INET6  | IPv6         |
| PF_LOCAL  | 本地通信UNIX |
| PF_PACKET | 底层套接字   |
| PF_IPX    | IPX Novell   |

### 套接字类型(type)

- 面向连接的套接字(SOCK_STREAM)

  TCP套接字满足该特性。

  字节流、可靠（数据不会消失）、有序（按顺序传输）、无边界（发送次数与接收次数无关）、提供流量控制（通告窗口

  ）。

  需注意只能一对一通信。

- 面向消息的套接字(SOCK_DGRAM)

  UDP套接字满足该特性。

  数据报、不可靠、无序、有边界、高速。

  可以多对多通信。


### 协议(protocol)

IPv4中，确定了套接字类型后，协议也一并确定，故该参数填0即可。

| 名称        | 协议 |
| ----------- | ---- |
| IPPROTO_TCP | TCP  |
| IPPROTO_UDP | UDP  |

## 套接字的地址绑定

bind(int sockfd,struct sockaddr *paddr,socklen_t addrlen);

### 地址族(Address Family)

- 套接字的IP地址

  IP地址用于确定目标主机。

  IPv4，4Bytes；IPv6，16Bytes。

  | IPv4地址分类 | 信息                             | 第一字节的范围 |
  | ------------ | -------------------------------- | -------------- |
  | A类          | 前1字节为网络ID，后3字节为主机ID | 0-127          |
  | B类          | 2，2                             | 128-191        |
  | C类          | 3，1                             | 192-223        |
  | D类          | 4字节表示多播IP地址              |                |
  | E类          |                                  |                |

- 套接字的端口

  区分某主机中的套接字。

  2Bytes，0-65535。

  0-1023为知名端口，21为FTP，80为HTTP。

### 地址信息的表示(sockaddr)

| 地址族(Address Family) | 含义         |
| ---------------------- | ------------ |
| AF_INET                | v4           |
| AF_INET6               | v6           |
| AF_LOCAL               | UNIX本地通信 |

sockaddr_in用于保存IPv4地址信息，可作为sockaddr传递。

```c
struct sockaddr_in
{
    sa_family_t sin_family;	//地址族，sockaddr的必要信息。
    uint16_t sin_port;		//port，2字节无符号short。
    in_addr sin_addr;		//ip地址结构体，4字节无符号int大小的结构体in_addr。
    char sin_zero[8];		//对齐用，必须初始化为0。
};

struct in_addr{
    In_addr_t s_addr;		//4字节无符号int。
};

```

sockaddr_in的初始化。

```c
//IPv4，端口2233，地址127.0.0.1。
struct sockaddr_in adr4={
	AF_INET,
    htons(2233),
    (struct in_addr)inet_addr("127.0.0.1"),
    {0,0,0,0,0,0,0,0},
};
```

- 网络字节序

  网络传输数据的约定存储方式，统一为大端序（而主流CPU为小端序）。

  通过网络传输数据过程中会自动转换，对sockaddr_in进行读写时需要考虑字节序。

  小端序：原数据的高位对应内存的高位。80x86CPU的数据存储顺序。

  大端序：低位对应高位。

- 数据转换函数

  ```c
  //返回网络字节序的32位ip地址，失败则INADDR_NONE。
  In_addr_t inet_addr(const char *ip_str);
  //将转换结果填入in_addr结构体（不是sockaddr_in）中，成功返回1，失败返回0（除结构体外均为-1）。
  int inet_aton(const char *ip_str,in_addr *paddr);
  //ip地址结构体转字符串，返回字符串指针，失败返回-1。
  char *inet_ntoa(in_addr adr);
  
  //主机字节序转换为网络字节序，host to network short(2bytes).
  unsigned short htons(unsigned short);
  //转换为网络字节序，host to network long(4bytes).
  unsigned long htonl(unsigned long);
  
  /* windows特供 */
  //返回s_addr，可调用直接赋值。
  s_addr inet_addr(const char *adr);
  //没有inet_aton。
  ```

- 为套接字分配地址

  bind(sockfd,psadr,adrlen);

  ```c
  struct sockaddr_in adr4={
  	AF_INET,
      htons(2233),
      (struct in_addr)inet_addr("127.0.0.1"),
      {0,0,0,0,0,0,0,0},
  };
  int skfd=socket(PF_INET,SOCK_STREAM,IPPROTO_TCP);
  bind(skfd,(sockaddr *)&adr4,sizeof(adr4));
  ```

- 服务器端自动分配地址

  ```c
  struct sockaddr_in adr4;
  adr4.sin_addr.s_addr=htonl(INADDR_ANY);
  ```

  

## TCP服务器/客户端

### 网络传输协议的补充

- 链路层（IP协议）

  负责提供传输路径信息。仅关注单个数据包的传输。不可靠，无序。

- 传输层（TCP/UDP协议）

  TCP赋予IP协议可靠性。确认对方接收数据，判断是否重传数据。

  UDP。

- 应用层

  用于网络通信的高度封装软件。

### TCP服务器

- 调用顺序

  ```c
  socket();
  bind();
  listen();
  accept();
  read()/write();
  close();
  ```

- 等待连接请求状态

  开辟套接字的通道。

  ```c
  //成功返回0，失败-1。
  /* backlog为等待队列的长度，表示可容许的连接请求数目。 */
  int listen(int sockfd,int backlog);
  ```

- 接受连接请求

  ```c
  //成功返回函数自身为访问客户 创建的skfd，失败-1。
  /* paddr为用于保存客户端地址信息的内存地址，调用后填入客户端地址信息。 */
  /* plen为地址，用于保存客户端地址信息的长度。 */
  int accpet(int ssk,sockaddr *pclient_addr,socklen_t *plen);
  ```

### TCP客户端

- 调用顺序

  ```c
  socket();
  connect();
  read()/write();
  close();
  ```

- 请求连接

  ```c
  //成功0，失败-1。
  /* pserv_addr目标服务器的addr。 */
  int connect(int csk,sockaddr *pserv_addr,sicklen_t addrlen);
  ```


### TCP服务端、TCP客户端的交互

调用bind()、listen()进入等待状态，此时客户端才可以调用connect()。调用accept()后会进入阻塞(blocking)状态，直至客户端调用connect()。



# 套接字选项

## 影响套接字选项的函数

- getsockopt(), setsoclopt()
- fcntl()
- ioctl()

## getsockopt, setsockopt

### getsockopt函数

```c
int getsockopt (int sockfd, int level, int optname, void *optval, socklen_t *optval);
```

- *optval

  已获取的选项当前值存放位置。

- *optlen

  值-结果参数。告知optval的大小，并返回实际获取的大小到*optlen。

### setsockopt函数

```c
int setsockopt (int sockfd, int level, int optname, const void *optval, socklen_t optval);
```

- *optval

  据该值设定指定选项。

- optval

  值参数。告知optval的大小。

## 选项级别

| level          | 含义           | 头文件                    |
| -------------- | -------------- | ------------------------- |
| SOL_SOCKET     | 通用套接字选项 | #include<sys/socket.h>    |
| IPPROTO_IP     | IP协议选项     |                           |
| IPPROTO_IPV6   | IPv6协议选项   |                           |
| IPPROTO_ICMPV6 | ICMPv6选项     |                           |
| IPPROTO_TCP    | TCP协议选项    | #include\<netinet/tcp.h\> |

## 选项属性

| 名       | 含义                          |
| -------- | ----------------------------- |
| get      | 是否可获得                    |
| set      | 是否可设置                    |
| 标志     | 是否为启动/禁止类型的二元选项 |
| 数据类型 | optval的类型                  |

## 通用套接字选项

### 常见选项的属性

| 选项         | 作用              | get  | set  | 标志 | 数据类型       |
| ------------ | ----------------- | ---- | ---- | ---- | -------------- |
| SO_LINGER    | 改变close()的操作 | Y    | Y    | N    | struct linger  |
| SO_REUSEADDR | 允许重用本地地址  | Y    | Y    | Y    | int            |
| SO_RCVBUF    | 接收缓冲区大小    | Y    | Y    | N    | int            |
| SO_SNDBUF    | 发送缓冲区大小    | Y    | Y    | N    | int            |
| SO_RCVTIMEO  | 接收超时          | Y    | Y    | N    | struct timeval |
| SO_SNDTIMEO  | 发送超时          | Y    | Y    | N    | struct timeval |

### SO_RCVBUF和SO_SNDBUF

TCP缓冲区的可用空间限定了TCP通告对端的窗口大小。TCP接收缓冲区不可能溢出，因为不会允许对端发出超过本端通告窗口大小的数据。

由于窗口规模选项时在SYN分节互相交换时得到的，而对已连接套接字设置该选项不会有效果，故须在建立连接前就设置SO_RCVBUF选项。

缓冲区大小至少为MSS的4倍。

## TCP套接字选项

### 常见选项的属性

| 选项        | 作用          | get  | set  | 标志 | 数据类型 |
| ----------- | ------------- | ---- | ---- | ---- | -------- |
| TCP_MAXSEG  | MSS大小       | Y    | Y    | N    | int      |
| TCP_NODELAY | 禁用Nagle算法 | Y    | Y    | Y    | int      |

### Nagle算法与TCP_NODELAY

#### 关闭Nagle算法

```c
#include<netinet/tcp.h>
int opt;
socklen_t optlen;

opt=1;
optlen=sizeof(opt);
setsockopt(fd,IPPROTO_TCP,TCP_NODELAY,&opt,optlen);
```

- Nagle算法

  最多只能发送一个未被确认的分节，在ACK到达之前不能发送其他TCP报文段。

  待接收到对端的ACK才开始发送下一个数据。期间尽可能将数据进行组合，接收到ACK后发送一个组合后的数据包。

  用于减少广域网的小分组（小于MSS）数目。

- ACK延滞算法

  接收到数据后不立即发送ACK，等待一段时间（典型值为50-200ms）后才发送。延滞发送的ACK则可以由本端需要发送的数据捎带。

  与Nagle算法联合使用。

- 关闭Nagle算法的影响

  数据传输的速率增大；链路中的数据包变多；对链路的损害变大。

#### 需要关闭Nagle算法的情形

- 传输大文件。

- 需要发送小片数据作为逻辑请求的客户。

  （不推荐）设置TCP_NODELAY，连续调用两次write()。有损于网络。

# 杂项

## 文件指针与描述符的转换

### fdopen

将描述符转换为文件指针。

```c
FILE * fdopen(int fd, const char *mode);
```

### fileno

将文件指针转换为描述符。

```c
int fileno(FILE *fp);
```

# 错误



## 常见错误及其产生条件

### ECONNRESET(104)

接收到RST时产生的错误。

### ETIMEDOUT(110)

服务器主机崩溃，客户进程不知道的情况下。发送数据超时产生的错误。

### EHOSTUNREACH(113)

中间路由器判定服务器主机不可达，响应“destination unreachable”的ICMP信息，此时返回的错误是EHOSTUNREACH或ENETUNREACH。





# RST分节

### 定义

TCP发生错误时发送的分节。

### 发送时机

- SYN到达，但没有监听套接字。
- TCP想取消一个已有连接。
- TCP接收到不存在的连接的分节。

### 一些遇到的情况

- 对CLOSE套接字write时，本端会接收到RST。
- 对LISTEN套接字read时，本端会接收到RST。
- SO_LINGER一种特定模式，会使得在调用close()时发送RST而非FIN。

# 琐碎的问题

- 传输数据时（未发送完全），接收端崩溃而引起的套接字写入错误。
  - 第一次write时会使对端发送RST（接收套接字处于CLOSE状态）。
  - 接下来的write会触发SIGPIPE信号（本端套接字接收到了RST）。
- 

# I/O模型

## 阻塞式I/O

阻塞于如read()、accept()等的系统调用。待数据完全复制到用户缓冲区后才返回。

## I/O复用

### select() 函数

阻塞，等待多个事件中任何一个发生，并且只有在有一个或多个事件发生或经历指定的时间后才会被唤醒。

#### 原理

检查0,1,...,maxfdp1-1共maxfdp1个描述符，若fd_set某位被设为1，且该位对应描述符就绪，则保持该位为1；若未就绪，则该位将被清0。若fd_set某位为0，则select后不论对应描述符是否就绪，该位仍位0。

#### 函数原型

返回fd_set中fd已就绪的总个数。

0则表示定时器到时。

-1则表示错误（如被一个信号中断）。

```cpp
#include<sys/select.h>
#include<sys/time.h>

//读、写、错。
int select(int maxfdp1, fd_set *readset,fd_set *writeset, fd_set *exceptset, struct timeval *timeout);
```

#### 参数解释

- *timeval

  ```cpp
  struct timeval{
      long tv_sec;	//sec
      long tv_usec;	//ms
  };
  ```

  | *timeout  | 效果                    |
  | --------- | ----------------------- |
  | NULL      | 永远等待                |
  | 有一个非0 | 等待一段时间            |
  | 全为0     | 不阻塞，轮询（polling） |

- *fd_set

  值-结果参数。用于指定需要监视的描述符，本质是对该数据的指定前n位进行测试。每一位（bit）对应一个描述符，描述符0对应fd_set的第0位。

  常用的fd_set操作函数

  - FD_ZERO()

    清空fd_set所有位为0。

    ```cpp
    void FD_ZERO(fd_set *fdset);
    ```

  - FD_SET()

    打开指定描述符fd对应的fd_set上的位（设为1）。

    ```cpp
    void FD_SET(int fd, fd_set *fdset);
    ```

  - FD_CLR()

    关闭指定描述符fd对应的fd_set上的位（设为0）。

    ```cpp
    void FD_CLR(int fd, fd_set *fdset);
    ```

  - FD_ISSET()

    判断fd在fd_set的对应位是否为开（1）。

    ```cpp
    int FD_ISSET(int fd,fd_set *fdset);
    ```



#### 使用流程

初始化 -> 设置关心fd -> 取maxfdp1 -> 遍历nready、FD_ISSET -> FD_CLR -> 设置关心fd。

- 使用范例

  循环检查标准输入是否可读。

  ```cpp
  char buf[LEN];
  int maxfdp1;
  fd_set rset;
  FD_ZERO(&rset);
  while(1){
      FD_SET(fileno(fp),&rset);
      maxfdp1=fileno(fp)+1;
      select(maxfdp1,&rset,NULL,NULL,NULL);
      
      if(FD_ISSET(fineno(fp),&rset)){
          read(fileno(stdin),buf,LEN);
          cout<<buf<<endl;
      }
  }
  ```

  

### 套接字描述符就绪条件

#### 套接字可读

- 缓冲区字节数大于等于低水位。
- 读半部关闭时，不阻塞，read返回0（EOF）。
- 监听套接字，已完成连接数不为0，此时accept()不阻塞。
- 套接字有错误需处理。

#### 套接字可写

- 字节数小于低水位。
- 写半部关闭时，此时对其写将SIGPIPE。
- 使用非阻塞connect() 的套接字成功连接，或连接失败。
- 错误待处理。

### 其他描述符的就绪条件

#### fileno(stdin)

- 缓冲区有内容时则可读。无内容时不可读。

### 应用select()使套接字不阻塞于特定源上

str_cli() 的修改。echo的客户端。

- v1（停-等）

  阻塞于Fgets()时不能马上对RST或FIN做出响应。

  ```c
  void str_cli(FILE * fp,int sk)   //v1
  {
      char sendline[MAXLINE],recvline[MAXLINE];
      while(Fgets(sendline,MAXLINE,fp)!=NULL)
      {
          writen(sk,sendline,strlen(sendline));
          if(readline(sk,recvline,MAXLINE)==0)
              err_sys("str_cli: server termanated prematurely.");
          cout<<"echo: "<<ends;
          Fputs(recvline,stdout);
      }
  }
  ```

  

- v2（I/O复用）

  阻塞于所有源（stdin或套接字），当有描述符可读时会立刻做出反应。但select() 不会检查用户自定义的缓冲区，故有可能存在数据丢失的情况。

  ```c
  void str_cli(FILE *fp,int sk)   //v2
  {
      int maxfdp1;
      fd_set rset;
      char sendline[MAXLINE],recvline[MAXLINE];
      FD_ZERO(&rset);
      while(1){
          FD_SET(fileno(fp),&rset);
          FD_SET(sk,&rset);
          maxfdp1=max(fileno(fp),sk)+1;
          Select(maxfdp1,&rset,NULL,NULL,NULL);
  
          if(FD_ISSET(sk,&rset)){
              if(readline(sk,recvline,MAXLINE)==0)
                  err_sys("strcli: server terminated prematurely.");
              cout<<"serv: "<<ends;
              Fputs(recvline,stdout);
          }
          if(FD_ISSET(fileno(fp),&rset)){
              if(Fgets(sendline,MAXLINE,fp)==NULL)
                  return;
              writen(sk,sendline,strlen(sendline));
          }
      }
  }
  ```

  

- v3

  这下正确了。使用read()代替readline()来解决用户缓冲区不受监视的问题，并且使用自定义的EOF标志表示到达文件尾，stdineof!=0时不再对fileno(fp)进行监视。

  此版本不使用readline()读取，而使用read()直接读批量数据。
  
  ```cpp
  void str_cli(FILE *fp,int sk)
  {
      int maxfdp1,stdineof;
      fd_set rset;
      char buf[MAXLINE];
      int n;
  
      stdineof=0;
      FD_ZERO(&rset);
      while(1){
          //只有未到达EOF时才监视fp。
          if(stdineof==0)
              FD_SET(fileno(fp),&rset);
          FD_SET(sk,&rset);
          maxfdp1=max(fileno(fp),sk)+1;
          Select(maxfdp1,&rset,NULL,NULL,NULL);
          
          if(FD_ISSET(sk,&rset)){
              if((n=read(sk,buf,MAXLINE))==0){
                  if(stdineof==1)
                      return;
                  else
                      err_sys("str_cli: server terminated prematurely.");
  
              }
              write(fileno(stdout),buf,n);
          }
  
          if(FD_ISSET(fileno(fp),&rset)){
              //循环read。
              if((n=read(fileno(fp),buf,MAXLINE))==0){
                  stdineof=1;
                  shutdown(sk,SHUT_WR);
                  FD_CLR(fileno(fp),&rset);
                  continue;
              }
  
              write(sk,buf,n);
          }
      }
  }
  ```
  
  

## 非阻塞式I/O

### 非阻塞描述符的设置

必须在原本设置的基础上再进行设置。

```cpp
int flags;

if((flags=fcntl(fd, F_GETFL, 0))<0)
    err_sys("F_GETFL error.");
flags|=O_NONBLOCK;
if(fcntl(fd, F_SETFL, flags)<0)
    err_sys("F_SETFL error.");
```



# 线程

## 使用线程的str_cli()

```cpp
static int sk;
static FILE *fp;
//从服务器获取回声。
void str_cli(FILE *fp_arg,int sk_arg)
{
    char recvline[MAXLINE];
    pthread_t tid;

    sk=sk_arg;
    fp=fp_arg;

    Pthread_create(&tid,NULL,pth_copyto,NULL);

    while(readline(sk,recvline,MAXLINE)>0)
        Fputs(recvline,stdout);
}
//从fp里获取数据，并将其发送给服务器。
void *pth_copyto(void *arg)
{
    char sendline[MAXLINE];

    while(Fgets(sendline,MAXLINE,fp)!=NULL)
        writen(sk,sendline,strlen(sendline));
    
    shutdown(sk,SHUT_WR);

    return (NULL);
}
```

# Windows

## Windows环境配置

*   链接wsock32.dll

        gcc -l wsock32

## Windows Error Shoot

*   10014 accept() err

    将编译环境从POSIX改为Win32。

