# 蓝桥杯模拟赛

## 进制转换

### 已知今天星期 x，求 n 天后是星期几

有效数字为 1-7 共七个数，毫无疑问是七进制，故对 7 取模即可。

但是由于起始为1，而取模后的范围为 [0, 6] ，故需要使其对齐，方法是作 x - 1 处理，然后在最终结果后 + 1。

```cpp
int func(int x, int n) {
    return (x - 1) % 7 + 1;
}
```

### 从 1 开始的 26 进制转换

模 26 的结果是 [0, 26)，而题目的范围是 [1, 26] 故每次取模前都需要 -1 再取模。

```cpp
class Solution {
public:
    string convertToTitle(int columnNumber) {
        recur(columnNumber);
        return res;
    }
    void recur(int num) {
        if(num > 0) {
            recur((num - 1) / 26);
            res.push_back((num - 1) % 26 + 'A');
        }
    }
    string res;
};
```

## 输入输出

input() 会读一整行，读出的结果为字符串。

```python
# 假设一行有 4 个数字
# 读一行并将其拆分转换为 int
a, b, c, d = map(int, input().split(' '));
```

## 二维数组

python 的 * 运算是通过对象拷贝实现的。

```python
[0] * 3 == [0, 0, 0]
```

而 python 中除了内置对象都是传址的。故不能用以下方法创建多维数组。

```python
a = [0, 0, 0]
arr = a * 2
arr == [[0, 0, 0], [0, 0, 0]]
arr[0][1] == [[0, 1, 0], [0, 1, 0]]	# 发生联动改变
```

应该使用生成器生成二维数组

```python
[[0 for i in range(n)] for i in range(m)] # m 行 n 列
```



