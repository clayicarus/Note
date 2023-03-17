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

## [字母交换](https://www.nowcoder.com/questionTerminal/43488319efef4edabada3ca481068762)

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

## [手串](https://www.nowcoder.com/questionTerminal/429c2c5a984540d5ab7b6fa6f0aaa8b5)

- 连续m个珠子不能出现两种相同的颜色

  枚举所有颜色，记录每种颜色所在的索引，只要每个珠子之间的距离 >= m（左闭右开的思想），就不会在连续m颗珠子中出现两种相同的颜色。

- 环形距离

  考虑两个平面的夹角，夹角 a > pi 时，a = pi - a，pi为总长度2pi的一半。

  ```cpp
  int dis = idx[j] - idx[i];
  if(dis > n / 2) dis = n - dis;
  ```

- 暴力求解最小值

```cpp
int main() 
{
    int n, m, c;
    cin >> n >> m >> c;
    vector<vector<int>> col_idx(51);
    for(int i = 0; i < n; ++i) {
        cin >> num_col;
        for(int j = 0; j < num_col; ++j) {
            cin >> c;
            col_idx[c].push_back(i);
        }
    }
    int res = 0;
    for(auto &idx : col_idx) {
        for(int i = 0; i < idx.size(); ++i) {
            for(int j = i + 1; j < idx.size(); ++j) {
                auto dis = idx[j] - idx[i];
                if(dis > n / 2) dis = n - dis;
                if(dis < m) {
                    ++res;
                    i = idx.size();
                    break;
                }
            }
        }
    }
    cout << res << '\n';
    return 0;
}
```

## [用户喜好](https://www.nowcoder.com/questionTerminal/66b68750cf63406ca1db25d4ad6febbf)

记录每个喜好值 k 对应的用户的索引，此时得到的索引数组是递增的。

查询时根据 k 找到喜好用户的索引列表，找到 i >= l，i <= r 的区间范围（二分查找），计算区间长度即可得到答案。

```cpp
int main() 
{
    int n;
    cin >> n;
    for(int i = 1; i <= n; ++i) {
        int k;
        cin >> k;
        k_idx[k].push_back(i);
    }
    cin >> q;
    for(int i = 0; i < q; ++i) {
        int l, r, k;
        cin >> l >> r >> k;
        auto &idx = k_idx[k];
        auto b = lower_bound(idx.begin(), idx.end(), l);
        auto e = upper_bound(idx.begin(), idx.end(), r);
        if(e > b) cout << distance(b, e) << '\n';
        else cout << 0 << '\n';
    }
}
```

## [推箱子](https://www.nowcoder.com/questionTerminal/d66a7a8b8e8a4acca7b1e1c8ef476354)

求人的最少移动次数。从题目中抽象出状态。

- 为什么要用四维数组存状态？

  如果将箱子和人切割，分别用两个二维数组作为记录数组，则会导致无法进行bfs，因为箱子在开始bfs时没有进行移动。

  ```cpp
  if(... || p_vis[p_n.first][p_n.first] || b_vis[b_n.first][b_n.second]) 
      continue;
  ```

  应当将人和箱子联合考虑，设空间的大小为 n * m ，人和箱子在空间中的分布情况就有 (n * m) * (n * m) 种，所以要用四维数组保存其状态，进行对状态的bfs。

- 此时bfs会遍历地图上所有的空间分布情况，所以其返回值即为最小移动步数。

- 当人物移动到箱子所在的位置时，箱子才会发生移动，移动的方向和人物移动的方向是一致的。

- 本质上是将转移后的状态入队。

- 一个状态可以由多种状态转移得来（一个节点可由多个节点转移得到）。

  所以不仅要在入队前判断是否访问过，在出队后也需要加以判断是否访问过。

  可以在入队前就把下一个状态标记为已访问，这样就不会在入队时重复入队（在转移前就标记之）。

```cpp
int bfs(const pair<int, int> &p, const pair<int, int> &b)  
{
    auto &mat = *pm;
    int m_i = mat.size();
    int m_j = mat.front().size();
    
    vector status(m_i, vector(m_j, vector(m_i, vector<int>(m_j))));
    
    queue<pair<pair<int, int>, pair<int, int>>> q;
    status[p.first][p.second][b.first][b.second] = true;	// (+)
    q.emplace(p, b);
    int step = 0;
    while(!q.empty()) {
        auto sz = q.size();
        while(sz--) {	// 这种求距离的方法只适合边权固定的题目。
            const auto [p_c, b_c] = q.front();
            q.pop();
            // if(status[p_c.first][p_c.second][b_c.first][b_c.second]) continue; 
            // status[p_c.first][p_c.second][b_c.first][b_c.second] = true;
            if(mat[b_c.first][b_c.second] == 'E') return step;
            for(const auto &d : dir) {	// 此处可能会导致没有访问过的状态多次入队。可以考虑在这里就将下一个将要访问的状态标记。
                pair<int, int> p_n = { p_c.first + d[0], p_c.second + d[1] };
                pair<int, int> b_n = b_c;
                if(p_n == b_c) {
                    b_n.first += d[0];
                    b_n.second += d[1];
                }
                if(p_n.first < 0 || p_n.second < 0 || b_n.first < 0 || b_n.second < 0
                    || p_n.first == m_i || p_n.second == m_j || b_n.first == m_i || b_n.second == m_j
                    || status[p_n.first][p_n.second][b_n.first][b_n.second]) 
                    continue;
                status[p_n.first][p_n.second][b_n.first][b_n.second] = true;	// (+)
                if(mat[b_n.first][b_n.second] != '#' && mat[p_n.first][p_n.second] != '#')
                    q.emplace(p_n, b_n);
            }
        }
        ++step;
    }
    return -1;
}
```

## [1263. 推箱子 - 力扣（Leetcode）](https://leetcode.cn/problems/minimum-moves-to-move-a-box-to-their-target-location/)

求箱子最少被推动的次数。与字节的推箱子不同。

- 字节的推箱子，只要人发生移动就会状态转移，转移的权值均为 1。
- 这道题的推箱子也是只要人发生移动就会状态转移，但是转移的权值需要分类讨论。

带权有向图的最小距离，箱子发生移动时的状态转移的边权为 1，只有人发生移动的边权为 0 。比较特殊的dijkstra算法（不需要优先队列）。

考虑在入队前就更新并判定状态。

### dijkstra算法

每次都从最小权值边开始处理，只要他能到达，就一定是最短路径。

**最短路径的子路径仍然是最短路径**

设S->T的最短路径经过 A ，则这条由S->A的路径也是所有由S->A的路径中最短的一条路径，否则S->T这条路径就不是最短的。这也是为什么算法每次都从当前节点开销最少的邻接节点开始下一轮处理。

入队时使用优先队列优化之。

**类比电梯题，需要准备一个距离数组**

dis[A] 表示起始状态到 A 状态的最小距离。

```cpp
deque<pair<pair<int, int>, pair<int, int>>> q;
vector visited(m, vector(n, vector(m, vector<bool>(n, false))));
vector dis(m, vector(n, vector(m, vector<int>(n, -1))));

visited[p.first][p.second][box.first][box.second] = true;
dis[p.first][p.second][box.first][box.second] = 0;
q.emplace_back(p, box);
while(!q.empty()) {
    const auto [cp, cbox] = q.front();
    auto &[cp_i, cp_j] = cp;
    auto &[cbox_i, cbox_j] = cbox;
    q.pop_front();

    for(const auto &d : dir) {
        auto weight = 0;
        pair<int, int> np { cp_i + d.first, cp_j + d.second };
        pair<int, int> nbox { cbox_i, cbox_j }; 
        auto [np_i, np_j] = np;
        auto &[nbox_i, nbox_j] = nbox;
        if(np_i == cbox_i && np_j == cbox_j) {
            nbox_i += d.first;
            nbox_j += d.second;
            weight = 1;
        }

        if(nbox_i < 0 || nbox_j < 0 || np_i < 0 || np_j < 0
        || nbox_i == m || nbox_j == n || np_i == m || np_j == n
        || visited[np_i][np_j][nbox_i][nbox_j])
            continue;

        dis[np_i][np_j][nbox_i][nbox_j] = dis[cp_i][cp_j][cbox_i][cbox_j] + weight;
        visited[np_i][np_j][nbox_i][nbox_j] = true;
        if(grid[cbox_i][cbox_j] == 'T') return dis[cp_i][cp_j][cbox_i][cbox_j];
        if(grid[np_i][np_j] != '#' && grid[nbox_i][nbox_j] != '#') {
            if(weight == 0) q.emplace_front(np, nbox);
            else q.emplace_back(np, nbox);
        }
    }
}
return -1;
```



# 剑心游戏3月笔试

## 数据结构题

设 ABCDEFGH 为某二叉树的中序遍历，其中 D 为根节点，求可能的二叉树的个数。

设中序遍历的长度为 L ，则所有可能的二叉树的数目为 catalanNumber(L)。

catalanNumber(n) =  ΣcatalanNumber(i)*catalanNumber(n-i-1); 其中，i=0, 1, 2, ……, n-1。

这道题的答案即为 cata(4) * cata(3) = 14 * 5 = 70

## 祭祖题

在一台 32 位计算机上，有数组 int arr[1234]，缓存每次只能读入 64 字节，求缓存不命中的次数。

Cache Misses = (Array Size / Cache Line Size) + (Array Size % Cache Line Size > 0 ? 1 : 0)

这道题的答案为 1234 * 4 / 64 + 1234 * 4 % 64 = 77 + 1 = 78

## 简答题

### c++ 为什么要有头文件和源文件？

使用头文件和源文件的主要原因是为了提高编译效率。头文件包含函数声明，变量声明和宏定义，而源文件则包含函数实现和变量定义。当编译器遇到一个函数被调用时，它会在头文件中查找函数声明，使得编译能够顺利进行。又因为每个源文件都会被独立编译，所以在修改某一函数定义之后，只需要重新编译该函数所在的源文件即可，而不需要重新编译所有源文件，提高编译效率。
