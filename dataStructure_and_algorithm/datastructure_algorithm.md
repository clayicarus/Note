# 排序算法

## 选择排序(SelectionSort)

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



## 冒泡排序(BubbleSort)

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

## 插入排序(InsertionSort)

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



# 背包 DP 

## 01背包

### 状态转移方程

有 N 件物品、容量为 M 的背包，每件物品的重量为 w[i\]、价值为 v[i\]，问放进背包里物品的最大价值是多少。

设状态 f(i, j) 表示用容量为 j 的背包装前 i 件物品时的最大价值，考虑处理到第 i 件物品时只有放与不放两种状态，则有 ：
$$
f(i,\ j) = max\{\ f(i - 1,\ j),\ f(i - 1,\ j - w[i]) + v[i]\ \}
$$
前半部分表示没有将第 i 件物品放进背包，此时背包容量仍为 j ；后半部分表示，前 i - 1件物品处理完毕，预留出了放置第 i 件物品的空间的最大价值并加上第 i 件物品的价值。

- 定义dp数组

  ```cpp
  vector dp(n, vector<int>(m + 1, 0));
  ```

- 循环从 i = 1，j = 0 开始

- i = 1 时的初态处理

  ```cpp
  for(int j = w[0]; j <= m; ++j) {
      dp[0][j] = v[i];
  }
  ```

- 错误的核心代码

  ```cpp
  // DONT do it.
  for(int i = 1; i < n; ++i) {
      for(int j = w[i]; j <= m; ++j) {
          dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w[i]] + v[i]);
      }
  }
  ```

  - 没有考虑到 j 在 0 到 w\[i\] 之间的情况，此时是剩余空间无法再容纳第 i 件物品的情况，的最大价值应为 dp[i\][j\] = dp[i - 1\][j\]。

- 正确的版本

  ```cpp
  for(int i = 1; i < n; ++i) {
      for(int j = 0; j < w[i]; ++j) {
          dp[i][j] = dp[i - 1][j];
      }
      for(int j = w[i]; j <= m; ++j) {
          dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - w[i]] + v[i]);
      }
  }
  ```

- 输出答案

  ```cpp
  cout << dp[n - 1][m];
  ```

### 空间复杂度的优化

只要想办法使得 f(i, j) == f(j) 即可，即只需在遍历过程中使得：f(j) == max\{ f(i - 1,  j), f(i - 1, j - w[i]) + v[i] \}。
$$
f(j) = max\{\ f(j),\ f(j - w[i]) + v[i]\ \}
$$
事实上这是在要求从 j = M 开始逆序遍历：

```cpp
for(int i = 0; i < n; ++i) {
    for(int j = m; j >= w[i]; --j) {
        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    }
}
```

#### 不能正序遍历的原因

```cpp
// DONT do it
for(int i = 0; i < n; ++i) {
    for(int j = w[i]; j <= m; ++j) {
        dp[j] = max(dp[j], dp[j - w[i]] + v[i]);
    }
}
```

- 考虑代码遍历的过程，当遍历到第 i 件物品，且 j >= 2 * w[i\] 时，会将第 i 件物品重复地放进背包。
- 上述代码的实现使得 f(i, j) 由 f(i, j - w[i]) 推导而来（第 i 件物品多次选择）。 
- 为了排除 f(i, j) 由 f(i, j - w[i]) 推导得到的可能性，我们需要从后往前遍历 j，这样就能保证 f(i, j) 在 f(i, j - w[i]) 之前就已经完成推导。



# 其他

- 1>logn<n<nlogn<2^n<n!

  

