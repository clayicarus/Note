# 文件I/O

## 标准I/O

### 特性

- 输入输出均自带缓冲区。
- 操作对象为FILE\*（文件指针）。
- 可移植。

### 文件打开 fopen()

FILE \* fopen(const char * file,const char * mode);

#### 二进制模式与文本模式

- 二进制

  原文件内容，不做映射。

- 文本模式

  根据不同的系统对换行符号以及文件尾符号做映射，以兼容不同系统的文本。

#### 文件打开模式

| mode | 作用                     | 定位      |
| ---- | ------------------------ | --------- |
| "r"  | 读模式，文件不存在则错误 | 文件头    |
| "w"  | 覆写模式，不存在则创建   | 文件头    |
| "a"  | 续写模式，不存在则创建   | 文件尾    |
| "b"  | 是否以二进制模式打开     | 取决于rwa |
| "+"  | 读写                     | 取决于rwa |

### 文件关闭 fclose()

成功返回0，失败EOF。

```c
int fclose(FILE *stream);
```



### 文件操作

#### 文本标准I/O函数

- fprintf()和fscanf()

  与printf和scanf()类似。

  ```c
  fprintf(FILE * fp,const char * str,...);
  fscanf(FILE *fp,const char * str,void * des);
  ```

- fgets()和fputs()

  get string and put string.

  ```c
  // from fp get stirng. buf remain '\n' as an end flag for fputs().
  fgets(void * buf,size_t str_size/* with '\0' */,FILE * fp);
  // output fp from buf. fp without '\n'.
  fputs(void * buf,FILE * fp);
  ```
  
- ungetc()

  将ch（int大小的char，实际只取char大小）回退到输入流，实现倒序输出？

  ```c
  int ungetc(int ch, FILE *fp);
  ```

  

#### 二进制标准I/O函数

- fread()和fwrite()

  返回操作成功的块的数目。

  ```c
  size_t fwrite(const void * ptr, size_t block_size, size_t nblocks, FILE *fp);
  size_t fwrite(const void * ptr, size_t block_size, size_t nblocks, FILE *fp);
  ```

### 随机访问

#### fseek()和ftell()

只能随机访问32位的文件。

- fseek()

    设置指针指向文件的位置。成功返回0，失败返回非0。
    
    | fromwhere | 定位     |
    | --------- | -------- |
    | SEEK_SET  | 文件头   |
    | SEEK_CUR  | 当前位置 |
    | SEEK_END  | 文件尾   |
    
    ```c
    // 将文件指针设置为以fromwhere为原点，offset为偏移量的位置。
    int fseek(FILE *stream, long offset, int fromwhere);
    ```

- ftell()

  返回指针到文件头的距离。

  ```c
  long ftell(FILE * fp);
  ```

#### fgetpos()和fsetpos()

失败返回非0。fpos_t应该是64位。

```c
// 将位置存入*pos。
int fgetpos(FILE * fp, fpos_t * pos);
// *pos设为位置。
int fsetpos(FILE * fp, const fpos_t * pos);
```

### 缓冲区操作

- fflush()

  手动刷新缓冲，将标准I/O内置缓冲区的内容输出。

  fp==NULL时未定义。

  ```c
  int fflush(FILE *fp);
  ```

  

- setvbuf()

  自定义针对某个fp操作时的缓冲区以及缓冲模式。

  | mode   | 缓冲模式 |
  | ------ | -------- |
  | _IOFBF | 完全缓冲 |
  | _IOLBF | 行缓冲   |
  | _IONBF | 无缓冲   |

  ```c
  int setvbuf(FILE * fp, char * buf, int mode, size_t size);
  ```

  当buf为NULL时自动根据size创建缓冲区。



## 底层IO



# 格式化输入/输出

```cpp
void fmt_scanf(void)
{
    const int max_len = 5;
    char temp[max_len];
    char fmt[10];
    sprintf(fmt, "%%%ds", max_len - 1);
    scanf(fmt, temp);   // fmt == "%4s"
    printf("%s", temp);
}
```

