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



# LeetCode

## [2584. 分割数组使乘积互质](https://leetcode.cn/problems/split-the-array-to-make-coprime-products/)

- 由互质想到质因子分解，相乘会使得质因子叠加

  只要找到一个分割点使得两边没有相同的质因子即可。

- 考虑一个数组分解后有两个相同质因子的情况

  设两个质因子在数组的 l, r ，则分割点只有可能在 [0, l) U [r, sz)。

- 答案不可能在 [l, r) ，题目要求找最小的分割点，可以考虑对所有的不可能区间按左端点排序，则答案只有可能在 0 处，或者右端点。

### 质因数分解

```cpp
void devide(int num, vector<int> &s) 
{
    if(num < 2) {
        return;
    }
    for(long long i = 2; i * i <= num; ++i) {
        while(num % i == 0) {
        	s.push_back(i);
            num /= i;
        }
    }
    if(num > 1)
        s.push_back(num);
}
```

- i * i <= num 是为了处理 4 的情况
- 最后的特判是为了避免漏掉大质数因子的情况，同时排除 1 作为因子的情况。

### 需要找到最左边和最右边的相同质因子

找最大的区间。

```cpp
struct interval {
    int a = -1;
    int b = -1;
};
unordered_map<int, interval> hash;	// 相同质因子的最大区间
for(int i = 0; i < nums.size(); ++i) {
    auto num = nums[i];
    if(num < 2) continue;
    for(long long p = 2; p * p <= num; ++p) {
        while(num % p == 0) {
            auto &[l, r] = hash[p];
            if(l == -1) {
                l = i;	// 第一个 l 一定是最左边的
            } else {
                r = i;	// 最后一个 r 一定是最右边的
            }
            num /= p;
        }
    }
    if(num > 1) {
        auto &[l, r] = hash[num];
        if(l == -1) {
            l = i;	
        } else {
            r = i;	
        }
    }
}
```

### 按左端点排序，遍历得到答案

```cpp
vector<interval> v(hash.size());
for(auto &[_, val] : hash) {
    v.push_back(val);
}
sort(v.begin(), v.end(), [](const auto &a, const auto &b){
    return a.a < b.a || a.b < b.b;
});
int res = 0;
for(auto [nl, nr] : v) {
    if(nl > res) return res;
    res = max(nr, res);
}
```

### 返回值需要注意的地方

注意遍历到最大的右端点时没有下一个区间并且最大右端点 < nums.size() - 1 的情况。nums.size() - 1 按照题意不可能是答案之一。

```cpp
return res < nums.size() - 1 ? res : -1;
```

# 字节笔试

## 字母交换

只能交换相邻两个字母。

### dp解法（不懂）

复杂度 O(n2)

#### 确定最大连续的字母

枚举所有字母的情况，得到目标字母。

#### 形成相邻相同字母串的操作次数

设字符 c，poz[i] 表示第 i 个 c 在字符串中的位置。

设 dp\[i\]\[j\] 为将第 i 个 c 和第 j 个 c 之间填满 c 的最少操作次数，即使得 poz[i] 和 poz[j] 之间形成长度为 j - i + 1 的连续字母串的操作次数，思路是将两个端点的字母（第 i 个 c 和第 j 个 c）往中间凑。

当 i == j 时，不需要操作，次数为0。

当 i + 1 == j 时，poz[i]  到 poz[j] 之间只有端点处为 c，则需要操作的次数为 poz[j] - poz[i] - 1。

其他情况 dp\[i\]\[j\] = dp\[i + 1\]\[j - 1\] + (poz\[j\] - poz\[i\] - 1) - (j - i - 1) 。考虑这一种情况，dp\[i + 1\]\[j - 1\] 表示第 i+1 个和第 j+1 个 c 之间已经形成相邻相同字符串，只要把两个端点处的字母通过相邻交换移动到连续区间的两端即可，即相邻交换次数就等于两个端点各自到连续区间的距离之和，即第 j 个和第 i 个 c 之间字母的个数减去中间不需要移动的 c 的个数。

### 暴力解

复杂度 O(n2)，想个暴力解不香吗。

#### 沿用dp的思路

设枚举到的字符为c，第 i 个c的位置为poz\[i\]，从i开始，将poz\[0, i -1]的字符c都搬运到第i个字符c的左边，对右边的字符c也如此操作。

则poz[i - 1] 上的c需要交换poz\[i - 1] - poz[i] - 1次才能到达第 i 个的左边（贴贴）。下一次则需要将poz[i - 2]的c移动到第i-1个c的左边（注意此刻第 i - 1个c的位置已经不是 poz \[i -1]了）。

需要注意的点：

- 当移动当前字符所需步数 `req_step` 加上已经移动的步数 `step` 后大于最大交换次数时需要跳出此次循环，不能再进行移动操作。需要记录中止后连续串的长度。
- 设需要贴贴的下标为cur_poz，每次贴贴结束后需要更新下一个待贴贴坐标 `--cur_poz` ，注意不能更新为 poz\[j]，因为此时第 j 个字符已经被移动了。

```cpp
for(int i = 0; i < poz.size(); ++i) {
    int step = 0;
    int cur_poz = poz[i];
    int cur_len = 1;
    for(int j = i - 1; j >= 0; --j) {
        int req_step = cur_poz - poz[j] - 1;
        if(req_step + step > m) break;
        step += req_step;
        ++cur_len;
        --cur_poz;	// 需要贴贴的字符更新为新移动过来的位置。
    }
    cur_poz = poz[i];
    for(int j = i + 1; j < poz.size(); ++j) {
        int req_step = poz[j] - cur_poz - 1;
        if(req_step + step > m) break;
        step += req_step;
        ++cur_len;
        ++cur_poz;
    }
    assert(step <= m);
    res = max(res, cur_len);
}
```

