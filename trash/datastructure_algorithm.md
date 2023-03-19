# 数据结构

## 排序

### 选择排序(SelectionSort)

数组arr[LEN]。设待排序子数组temp[n]，找出temp的最值的索引index，交换arr[index]与arr[n+1]。直至待排序子数组长度为0。

```cpp
template<typename T>
void SelectionSort(T arr[],int n){
    int temp;
    int index;
    int i,j;
    for(i=n-1;i>=0;i--){
        index=MaxIndex(arr,i);
      	//swap(arr[index],arr[i]);
        temp=arr[index];
        arr[index]=arr[i];
        arr[i]=temp;
    }
}

template<typename T>
int MaxIndex(T arr[],int n){
    int index;
    int i,j;
    for(i=0;i<n;i++){
        for(j=0;j<n;j++)
            if(arr[j]<arr[i])
                break;
        if(j==n)
            index=i;
    }
    return index;
}
```



### 冒泡排序(BubbleSort)

arr[LEN]。设待排序子数组temp[n]，比较arr[i+1]和arr[i]决定是否交换arr[i+1]与arr[i]。直至i=n，此时arr[n+1:LEN]为有序子数组。当n=0时排序结束。

```cpp
void BubbleSort(int arr[],int n){
    int i,j;
    int temp;
    for(i=0;i<LEN-1;i++)
        for(j=0;j<LEN-i;j++)
            if(arr[j]<arr[j+1]){
                temp=arr[j];
                arr[j]=arr[j+1];
                arr[j+1]=temp;
            }
}
```

- 插入排序(InsertionSort)

  arr[LEN]。设arr[0:n]为已排序的数组temp，将arr[n+1]插入至temp中合适的位置。直至n=LEN，排序结束。

  有序数组的最左端最大(小)，最右端最小(大)。

  ```cpp
  template<typename T>
  void InsertSort(T arr[],int n,int flag=1,int step=1);
  
  //将arr[i+1]与arr[0:i]从左到右比较，越往左越大(小)，找到一个合适的位置插入即可停止遍历arr[0:i]。
  template<typename T>
  void InsertSort(T arr[],int n,int flag,int step){
      int i,j,k;
      int temp;
      for(i=0;i<n-step;i+=step){
          for(j=0;j<i+step;j+=step){
              if(flag*(arr[j]-arr[i+step])>0){
                  temp=arr[i+step];
                  for(k=i;k>=j;k-=step)
                      arr[k+step]=arr[k];
                  k+=step;
                  arr[k]=temp;
  
                  break;
              }
          }
      }
  }
  ```

  ```cpp
  template<typename T>
  void InsertSort(T arr[],int n,int flag=1,int step=1);
  
  //从arr[step]开始，将arr[i]与arr[i-step]比较并将arr[i-step]向右移动，i-=step，为temp腾出空间，直到数组的首位或者找到合适的位置时停止移动。将temp赋值到腾出的空间。
  template<typename T>
  void InsertSort(T arr[],int n,int flag,int step){
      int i,j;
      int temp;
      //n>=step;
      for(i=step;i<n;i++){
          temp=arr[i];
          for(j=i;j>=step/*最左端*/&&flag*(temp-arr[j-step])<0/*由右至左比较*/;j-=step)
              arr[j]=arr[j-step];//右移
          arr[j]=temp;
      }
  }
  ```

  

## 线性表

- 链式存储

  ```cpp
  typedef struct person
  {
      string name;
      unsigned age;
  } Item;
  
  typedef struct node
  {
      Item item;
      struct node *next;
  } Node;
  
  typedef Node * List;
  ```

  

## 渐近记法

- 1>logn<n<nlogn<2^n<n!

  