## 美团24暑期实习笔试

笔试平台赛码网。4 + 1 题编程。

美团、平台、题目都要恶心你一下。

### 编程题 Q1

有 n 个整数，依次用加号 `+` 将它们连接。有 m 次操作，每次操作改变第 t 个 `+` 变成  `+` `-` `*` `/`  中任意的一种，输出操作后整个串的运算结果。注意，每次操作都是独立的，每次操作后，整个串都会回到最初用 `+` 连接的状态。

>第一行输入 n。
>
>第二行输入 n 个整数 ai。
>
>第三行输入 m 。
>
>第四行输入 2m 个字符，t1, o1, t2, o2, ..., tm, om，t 表示要修改的第 t 个 `+`，o 代表要将原来的 `+` 修改成运算符 o。

**模拟**

```cpp
cin >> n;
double res = 0;
vector<double> v(n);
for(int i = 0; i < n; ++i) {
    double temp;
    cin >> temp;
    v[i] = temp;
    res += temp;
}
cin >> m;
for(int i = 0; i < m; ++i) {
    char o;
    int t;
    cin >> t >> o;
    auto temp = res - v[i - 1] - v[i];
    char fmt[] = "%.1f";
    switch(o) {
        case '+':
            printf(fmt, res);
            break;
        case '-':
            temp += v[i - 1] - v[i];
            printf(fmt, temp);
            break;
        case '*':
            temp += v[i - 1] * v[i];
            printf(fmt, temp);
            break;
        case '/':
            temp += v[i - 1] / v[i];
            printf(fmt, temp);
            break;
        default:
            break;
    }
}
```



### 编程题 Q2

有一个长度为 n 的数组。定义数组的丑陋值为数组中相邻两个数的差值的绝对值之和。现在可以对这个数组中的元素进行任意次交换操作，求该数组的最小丑陋值。

**排序**

相邻两个数的差值尽可能小。

```cpp
cin >> n;
vector<int> v(n);
for(int i = 0; i < n; ++i) {
    cin >> v[i];
}
sort(v.begin(), v.end());
long long res;
for(int i = 1; i < v.size(); ++i) {
    res += abs(v[i] - v[i - 1]);
}
cout << res << '\n';
```

### 编程题 Q3

有一个长度为 n 的数组，数组的初始值为 0，编号从 1 开始。

对数组进行 m 次操作，op 为 0 表示数组的更新操作，将编号为 xi 的元素的值改为 yi；op 为 1 表示一次查询操作，查询 [xi, yi] 之间的元素的和。输出每次查询操作的结果。

>第一行输入 n、m，代表数组的长度以及操作数目。
>
>第二行 m 个整数，opi，代表第 i 次操作的类型。
>
>第三行 m 个整数，xi。
>
>第四行 m 个整数，yi。

>1 <= xi <= n
>
>0 <= yi <= 1e4
>
>1 <= n, m <= 5e4
>
>op == 0 || op == 1

**暴力解法**

还没想到别的方法。注意输入的方式。

```cpp
cin >> n >> m;
vector<int> v(n);
vector<vector<int>> arr(n);	// arr[i][0] == op, [1] == x, [2] == y
for(int j = 0; j < 3; ++j) {
    for(int i = 0; i < m; ++i) {
        int temp;
        cin >> temp;
        arr[i].push_back(temp);
    }
}
for(auto &i : arr) {
    auto op = i[0];
    auto x = i[1];
    auto y = i[2];
    if(op == 0) {
        v[x - 1] = y;
    } else {
        auto temp = accumulate(v.begin() + x - 1, v.begin() + y, 0LL);
        cout << temp << '\n';
    }
}
```

### 编程题 Q4

有 n 个杯子，可以对任意一个杯子进行加水；当第 i 个杯子加满水后，多余的水会流入第 i + 1 个杯子，而最后一个杯子加满水则会溢出，对其他杯子没有影响；对第 i 个杯子加 1 单位水的魔力为 zi。有 m 次查询，每次查询要求对第 qi 个杯子加满水，输出加满第 qi 个杯子至少需要消耗多少魔力，查询后杯子恢复原来的状态。

>第一行输入 n。
>
>第二行输入 n 个整数 xi，代表第 i 个杯子能够容纳的水量。
>
>第三行输入 n 个整数 yi，代表第 i 个杯子的初始水量。
>
>第四行输入 n 个整数 zi，代表对第 i 个杯子加 1 单位水需要的消耗的魔力。
>
>第五行输入 m。
>
>第六行输入 m 个整数 qi。

>1 <= n, m <= 3000。
>
>1 <= yi <= xi <= 1e9。
>
>1 <= zi <= 300。
>
>1 <= qi <= n。

**前缀和**

O(mn)，pre[i] 表示往下标为 0 的杯子加水，加满下标为 i 的杯子需要多少水，则往下标为 j 的杯子加水，加满 i 需要的水总共为 pre[i] - pre[j - 1]，枚举从 1 号到 q 号的所有杯子的情况即可。

```cpp
cin >> n;
vector<vector<int>> g(n);
for(int j = 0; j < 3; ++j) {
    for(int i = 0; i < n; ++i) {
        int temp;
        cin >> temp;
        g[i].push_back(temp);
    }
}
// g[i][0] == xi, g[i][1] == yi, g[i][2] == zi
vector<long long> pre(n);
pre[0] = g[0][0] - g[0][1];
for(int i = 1; i < n; ++i) {
    int con = g[i][0] - g[i][1];
    pre[i] = pre[i - 1] + con;
}
cin >> m;
for(int k = 0; k < m; ++k) {
    int q;
    cin >> q;
    int ma = g[0][2];
    long long res = pre[q - 1] * ma;
    for(int i = 1; i < q; ++i) {
        auto &gi = g[i];
        int magic = gi[2];
        auto temp = pre[q - 1] - pre[i - 1];
        res = min(res, magic * temp);
    }
}
```

### 专项编程题 Q1

有一棵节点数目为 n 的树，每个节点有自己的价值，若节点没有儿子节点，则该节点的价值为 1；若有儿子节点，则当该节点是红色时，则该节点的价值为两个儿子节点价值之和，当该节点是绿色时，该节点的价值为两个儿子节点的价值的异或。保证要么没有儿子节点，要么有两个儿子节点。

设 1 号节点为根节点。要求输出根节点的值。

> 第一行输入 n。
>
> 第二行输入 n - 1 个整数 pi，代表第 i 个节点的父亲。
>
> 第三行输入 n 个整数 ci，ci == 1 表示第 i 个节点是红色，ci == 2则为绿色。

> n <= 5e4

**记忆化搜索**

一眼记忆化搜索，但是没时间写了，对树的存储方式不太熟悉。

```cpp
cin >> n;
vector<vector<int>> adj(n);
adj[0] = 0;
for(int i = 1; i < n; ++i) {
    int temp;
    cin >> temp;
    adj[i].push_back(temp);
}
vector<int> c(n);
for(int i = 0; i < n; ++i) {
    cin >> c[i];
}
vector<int> rec(n, -1);
function<void(int)> dfs = [](int i){
    if(rec[i] != -1) return rec[i];
    if(!adj[i].size()) {
        rec[i] = 1;
        return rec[i];
    }
    if(c[i] == 1) {
        rec[i] = dfs(rec[i][0]) + dfs(rec[i][1]);
    } else {
        rec[i] = dfs(rec[i][0]) ^ dfs(rec[i][1]);
    }
    return rec[i];
};
cout << dfs(0) << '\n';
```

