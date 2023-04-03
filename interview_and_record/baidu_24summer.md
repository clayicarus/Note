## 百度24暑期实习笔试

笔试平台牛客网。15 题单选，5 题多选，3 道编程。

### 编程题 Q1

有一个数组长度为n，其中的一些数字是红色，其他的数字则是蓝色。定义选择的两个数是一红一蓝时，该组合是合法的；定义权值为两个数的乘积。求所有合法的组合的权值之和是多少，答案对1e9 + 7取模。

第一行输入n。

第二行输入n个正整数ai，作为数组。

第三行输入仅由'R'、'B'组合而成的长度为n的字符串，第i个字符代表数组第i个元素的颜色。

n [1, 1e5]，ai [1, 1e9]。

**ans = sum(B) \* sum(R)**

```cpp
const auto MOD = 1e9 + 7;
cin >> n;
vector<int> v(n);
for(int i = 0; i < n; ++i) {
    cin >> v[i];
}
long long s1 = 0, s2 = 0;
for(int i = 0; i < n; ++i) {
   	char temp;
    cin >> temp;
    if(temp == 'R') { s1 = (s1 + v[i] % MOD) % MOD; }
    else { s2 = (s2 + v[i] % MOD) % MOD; }
}
cout << s1 * s2 % MOD << '\n';
```



### 编程题 Q2

有一个字符串表示的小数，可以删除（或者不删除）该字符串中小数点后任意的字符，问经过处理后可以得到的最大的小数是多少（不能输出末尾0）。

s.length [0, 2e5]

保证输入的字符串是正数，且没有末尾0。

**后缀最大值**

在前面的数应该尽可能大。

```cpp
string num;
cin >> num;
string_view n(num);
string_view s = n.substr(2);
string res;
char m = s.back();
for(int i = s.size() - 2; i >= 0; ++i) {
    auto temp = s[i];
    if(temp >= m) {
        res.push_back(temp);
        m = temp;
    }
}
res.append(".0");
reverse(res.begin(), res.end());
cout << res '\n';
```

### 编程题 Q3

一颗有根树，i 号节点的权值为 ai。设 1 号节点为根。

有 q 次操作，每次操作会选择一个节点 x，使得 x 为根的树的所有节点的权值都乘上 y。

求 q 次操作结束后，对于以 i 号节点为根的树的所有节点的权值的乘积末尾有多少个 0。

第一行输入 n，表示节点数量。

第二行输入 n 个正整数 ai，代表每个节点的权值。

接下来的 n - 1 行，每行输入两个正整数 u、v，代表节点 u、v 有一条边相连。

接下来的 q 行，每行输入两个正整数 x、y，代表一次操作。

1 <= n, q <= 1e5

1 <= ai, y <= 1e9

1 <= x, u, v <= n

分别输出所有节点 [1, n] ，每颗树的乘积末尾0的数量。

**不会。**

