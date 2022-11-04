# 动态规划

*   121（炒股题）

    ```cpp
    //dp AC
    /* 
        1,	dp[i][0]表示i天持有股票状态的最大现金
            dp[i][1]表示i天没有股票状态的最大现金
        2,	dp[i][0]=max(dp[i-1][0],-prices[i]);			//昨天有股票，于第i天买股票（只能买一次）
            dp[i][1]=max(dp[i-1][1],prices[i]+dp[i-1][0]);	//昨天没有股票，今天卖了昨天的股票
        3,	dp[0][0]=-prices[0];
            dp[0][1]=0;
        4,	从i=1到i=prices.size()-1;
        5,	测试dp
    */
    class Solution {
    public:
        int maxProfit(vector<int>& prices) {
            vector<vector<int>> dp(prices.size(),vector<int>(2));
            int i;
            dp[0][0]=-prices[0];
            dp[0][1]=0;
            for(i=1;i<prices.size();i++)
            {
                dp[i][0]=max(dp[i-1][0],-prices[i]);
                dp[i][1]=max(dp[i-1][1],prices[i]+dp[i-1][0]);
            }

            return dp[prices.size()-1][1];
        }
    };
    ```

*   2100（抢银行的最佳时间）

    前缀和。

    某一天连续递增了多少天（从左到右）（类似连续打卡）

    某一天连续递减了多少天（从右到左）

    重新遍历一次序号即可

*   2055（蜡烛间的盘子数目）

    2.5h used.

    前缀和。

    可用前缀和记录盘子的数目，找到最近的盘子的位置做差即可。

    最近盘子的位置也可以用从前到后遍历、从后到前遍历的方法记录。

    ```cpp
    //record nearest plate.
    for(i=0,poz=-1;i<s.size();i++)
    {
        if(s.at(i)=='|')
            poz=i;
        lp[i]=poz;
    }
    for(i=s.size()-1,poz=-1;i>=0;i--)
    {
        if(s.at(i)=='|')
            poz=i;
        rp[i]=poz;
    }
    ```

*   53（最大子序列和）

    ```cpp
    //dp[i]=max(dp[i-1]+x[i],x[i]);
    ```

# 位运算

*   393（UTF-8编码验证）

    注意UTF-8的字节数不大于4。

    判断某一位是否为0或1。

    ```cpp
    unsigned char a;
    (a&0x80)==0x80;		//最高位是否为1，注意括号。
    (a&0x80)==0x00;		//最高位是否为0。
    ```

    UTF-8第一个字节前n位均为1，第n+1位为0，则该UTF-8码占n个字节（4>=n>1，出现n==1则不是UTF-8）。

    UTF-8后n-1个字节的前两位为10B，若不是则非UTF-8码。

    ASCII码可以看做n=0但位数为1的UTF-8码。

*   693

    取最后一位的方法。

    ```cpp
    while(n>0){
        if(n%2==(n/2)%2) return false;
        n/=2;
    }
    return true;
    ```

# 二叉树

## 101.对称二叉树

中序遍历即可判断是否对称。

中序遍历生成的数组在**数值**以及**层数**上对称的，需给每层的数值做标记，以检测层数是否也对称相等。

如\[1,2,NULL,2,NULL,2]的中序遍历为\[2(2),2(3),1(1),2(2),2(3)]，数值是对称的，但层数不对称，故不是对称二叉树。

## 100.相同的树

### 递归解法1

使用前序遍历，依次存入数组构成数组描述的二叉树。

之后比较数组即可。

```cpp
class Solution {
public:
    bool isSameTree(TreeNode* p, TreeNode* q) {
        Tra(p, vp);
        Tra(q, vq);
        if(vp == vq)
            return true;
        return false;
    }
    void Tra(TreeNode *tree, vector<int> &v)
    {
        if(tree != NULL){
            v.push_back(tree->val);
            Tra(tree->left, v);
            Tra(tree->right, v);
        }else{
            v.push_back(10001);
        }
    }
    vector<int> vp, vq;
};
```

### 递归解法2

不使用辅助数组，直接在遍历过程中判断之。注意遍历的返回值。

```cpp
bool isSameTree(TreeNode* p, TreeNode* q) {
    if (p == nullptr && q == nullptr) {
        return true;
    } else if (p == nullptr || q == nullptr) {
        return false;
    } else if (p->val != q->val) {
        return false;
    } else {
        //两个值相同的情况，再判断左右子树是否相同。
        return isSameTree(p->left, q->left) && isSameTree(p->right, q->right);
    }
}
```

# 图论

## [565. 数组嵌套](https://leetcode.cn/problems/array-nesting/)

太抽象了。dfs。

*   将循环想象成一个环。

*   一定会在循环开始处结束循环。

*   A中不存在重复元素意味着环之间不存在交叉。

*   故只需原地标记，作为环的结束标记。

```cpp
int arrayNesting(vector<int>& nums) {
    int res, cur, next, temp;
    int i;
    for(i = 0, res = 0; i < nums.size(); ++i){
        if(nums[i] == -1){
            continue;
        }
        cur = 1;
        next = nums[i];	//下一个索引
        while(next != i){
            temp = nums[next];	//保存下一个索引
            nums[next] = -1;	//原地标记
            ++cur;			//该环长度计数
            next = temp;	//下一个的索引
        }
        res = max(res, cur);
    }
    return res;
}
```

## [51. N 皇后](https://leetcode.cn/problems/n-queens/)

问如何在n\*n的棋盘上摆放n个皇后，使得棋盘上的皇后都不能相互攻击。

*   皇后可以走直线、斜线

    一行上不可能有两个皇后，故每行有且仅有一个皇后。

*   需要遍历所有情况，以找到所有可行解

    由于每行有且仅有一个皇后，考虑摆放一个皇后的过程，遍历完所有行就可以得到一个解。可用col\[i]表示第i行的皇后在col\[i]列。

*   摆放一个皇后的情况

    用j表示该皇后摆在第j列。

    摆放一个皇后之后，该皇后所在的行列及对角线都不能够摆放其他皇后，按行遍历已经保证行中不会有两个或两个以上的皇后，故只需考虑列和斜线是否有冲突。可用avlb\_col\[j]表示第j列是否可用。

*   斜线的冲突判断

    i, j表示正在摆放第i行第j列的皇后。

    考虑直线方程c = i + j和c = i - j，斜率确定，对一个确定的皇后都有一个确定的点（点斜式），对斜线上所有的点都满足该直线方程，所以可以用avlb\_cross1\[i + j]和avlb\_cross2\[j - i]表示对应皇后的斜线是否被占用。

*   dfs(int i)

    表示摆放第i行的皇后。对于每一行都有n种摆法，所以题目的本质是对n层n叉树的深度优先搜索（需要找到所有的解）。

```cpp
int nq;
vector<vector<string>> res;
int main()
{
    int i, j;
    vector<int> col(n);
    vector<bool> avlb_col(n, true);
    vector<bool> cross1(2 * n, true);
    unordered_map<int, bool> cross2;

    nq = n;
    for(i = 0; i < n; ++i){
        for(j = 0; j < n; ++j){
            cross2[i - j] = true;
        }
    }
    dfs(0, col, avlb_col, cross1, cross2);
    
    cout << res << endl;
}

void dfs(int i, vector<int> &a, vector<bool> &b, vector<bool> &c, unordered_map<int, bool> &d)
{
    int j;
    for(j = 0; j < nq; ++j){
        //遍历摆放在每一列的情况。
        if(b[j] && c[i + j] && d[i - j]){
            //需要满足行列斜线都不冲突。
            a[i] = j;
            c[i + j] = false;
            d[i - j] = false;
            b[j] = false;
            if(i < nq - 1){
                //摆放下一行的皇后。
                //需要摆放nq次，从0到nq - 1。
                dfs(i + 1, a, b, c, d);
            }else{
				//摆放完nq个皇后，即找到了一个解。
                printRes(a);
            }
            //回溯，无论有无找到解都需要恢复到原来的状态。
            c[i + j] = true;
            d[i - j] = true;
            b[j] = true;
        }
    }
}
```

## [P1135 奇怪的电梯](https://www.luogu.com.cn/problem/P1135)

从a楼到b楼，至少需要按几次按钮。

fl\[i]为在i层能够上下的层数。

*   只有1-n楼，不能到达以外的楼层

    对第i层来说最多有两种选择（上fl\[i]层或下dl\[i]层），本质上是二叉树的最短路径搜索，bfs实现。

*   bfs的起点为a层，寻找由a层到b层的最短路径。

```cpp
int minDistance(const vector<int> &fl, int n, int a, int b)
{
    // fl: 1-n
    queue<int> q;
    vector<bool> mark(n + 1, false);
    vector<int> dis(n + 1, -1);
    int i;
    q.push(a);
    dis[a] = 0;		//a层到a层的距离初始化为0。
    mark[a] = true;	//表示a已经访问过。
    //bfs起手式。
    while(!q.empty()){
        i = q.front();	//在第i层。
        q.pop();
        if(i + fl[i] <= n && !mark[i + fl[i]]){
            //层数是否超出n，是否已经被访问过。
            q.push(i + fl[i]);	
            dis[i + fl[i]] = dis[i] + 1;
            mark[i + fl[i]] = true;
        }
        if(i - fl[i] >= 1 && !mark[i - fl[i]]){
            q.push(i - fl[i]);
            dis[i - fl[i]] = dis[i] + 1;
            mark[i - fl[i]] = true;
        }
        if(mark[b])
            //访问到了b，则对应的最短路径也找到了。
            break;
    }

    return dis[b];
}
```

## [542. 01 矩阵 - 力扣（LeetCode）](https://leetcode.cn/problems/01-matrix/)

距离自己最近的0的距离。四叉树遍历。

### 暴力思路tle

*   由1开始，bfs寻找距离自己最近的0。

*   每一次由1开始时都需要初始化标记数组，以免走回头路。

    找到0时就可以进行下一次迭代。

*   可用sz记录当前队列的大小，sz即为该层的所有节点数，当sz为0时进入下一层，令d递增即可得到下一层的距离。

```cpp
vector<vector<int>> updateMatrix(vector<vector<int>>& mat) {
    // bfs shortest dis
    // 16:31-16:48 0为搜索起点
    // 23:53-1:19 1为搜索起点，找最近的0
    int i, j, m, n;
    int sz, d;
    queue<pair<int, int>> q;
    vector<vector<int>> res(mat.size(), vector<int>(mat[0].size(), -1));
    vector<vector<bool>> mk;

    // i = 0, j = 1;
    for(i = 0; i < mat.size(); ++i){
        for(j = 0; j < mat[0].size(); ++j){
            //每次都需要开一个新的标记数组。
            mk = vector<vector<bool>>(mat.size(), vector<bool>(mat[0].size(), true));
            q.push({i, j});
            d = 0;
            while(!q.empty()){
                sz = q.size();
                while(sz--){
                    m = q.front().first;
                    n = q.front().second;
                    q.pop();
                    if(mat[m][n] == 0){
                        //找到答案，直接进行下一个1的迭代。
                        res[i][j] = d;
                        while(!q.empty())
                            q.pop();
                        break;
                    }else{
                        if(m - 1 >= 0 && mk[m - 1][n]){
                            mk[m - 1][n] = false;
                            q.push({m - 1, n});
                        }
                        if(m + 1 < mat.size() && mk[m + 1][n]){
                            mk[m + 1][n] = false;
                            q.push({m + 1, n});
                        }
                        if(n + 1 < mat[0].size() && mk[m][n + 1]){
                            mk[m][n + 1] = false;
                            q.push({m, n + 1});
                        }
                        if(n - 1 >= 0 && mk[m][n - 1]){
                            mk[m][n - 1] = false;
                            q.push({m, n - 1});
                        }
                    }
                }
                //当sz为0时，一层遍历完毕，距离自加。
                ++d;
            }
        }
    }
    return res;
}
```

### 0作为搜索起点

*   若只有单个0

    由0开始搜索，res\[i + 1]\[j] = res\[i]\[j] + 1。进行一次遍历即可得知所有1距0的距离。

*   多个0的情况

    将所有0看作一个0即可（将所有0的结点首先放入队列中）。

    ```cpp
    for(int i = 0; i < mat.size(); ++i){
        for(int j = 0; j < mat[0].size(); ++j){
            if(mat[i][j] == 0)
                q.emplace(i, j);
        }
    }
    ```

*   只需一个标记数组，故可将结果数组初始化为-1复用为标记数组。

```cpp
vector<vector<int>> updateMatrix(vector<vector<int>>& mat) {
    int i, j;
    queue<pair<int, int>> q;
    vector<vector<int>> res(mat.size(), vector<int>(mat[0].size(), -1));

    for(i = 0; i < mat.size(); ++i){
        for(j = 0; j < mat[0].size(); ++j){
            if(mat[i][j] == 0){
                q.push({i, j});
                res[i][j] = 0;
            }
        }
    }
    while(!q.empty()){
        i = q.front().first;
        j = q.front().second;
        q.pop();
        if(i + 1 < res.size() && res[i + 1][j] == -1){
            res[i + 1][j] = res[i][j] + 1;
            q.push({i + 1, j});
        }
        if(i - 1 >= 0 && res[i - 1][j] == -1){
            res[i - 1][j] = res[i][j] + 1;
            q.push({i - 1, j});
        }
        if(j - 1 >= 0 && res[i][j - 1] == -1){
            res[i][j - 1] = res[i][j] + 1;
            q.push({i, j - 1});
        }
        if(j + 1 < res[0].size() && res[i][j + 1] == -1){
            res[i][j + 1] = res[i][j] + 1;
            q.push({i, j + 1});
        }
    }

    return res;
}
```

# 散列表

## 599（序列和最小、且对应值相等）

找两个数组中的相同元素使用散列表即可。

## 890（abb模式判断）

注意双向映射，word和pattern互换后仍可以匹配。

```cpp
if (match(word, pattern) && match(pattern, word)) {
    ans.emplace_back(word);
}
```

## [6164. 数位和相等数对的最大和](https://leetcode.cn/problems/max-sum-of-a-pair-with-equal-sum-of-digits/)

*   数位和（数字的各个位相加得到的和）相等的整数需要匹配

    故考虑到使用**哈希表**，并用数位和作为**键**。

*   满足数位和相等的整数不止一对，而题目要求得到最大数对和

    故需知道匹配整数中*最大的两个数*。

    故使用大顶堆作为键值。

*   我是傻逼

## [1331. 数组序号转换 - 力扣（LeetCode）](https://leetcode.cn/problems/rank-transform-of-an-array/)

*   排序后，元素对应的下标即该元素的排位

    故需要对原数组进行排序。

*   按原数组的顺序，需要知道每一个元素对应的排位

    故考虑到哈希表，用元素值匹配其排位。

*   我是傻逼。

# 栈

## 735.行星碰撞

行星的速度大小相同，数值的绝对值表示行星的大小，在数组的位置表示行星间的相对位置，正表示向右运动、负表示向左运动。

*   遍历顺序为从左到右（想象成一颗行星的运动方向），只关注在最前面的一颗向右运动的行星。

    故正的需优先入栈，无限制条件。

*   若下一颗行星是向左运动的，且栈顶的行星是向右运动的，需循环比较栈顶（最前面的向右运动的行星）与之的相对大小。

*   当栈空或栈顶的行星是向左运动时，向左运动的行星可以无限制入栈（此时向右运动的行星仍然可以无限制入栈）。

### 栈+模拟

```cpp
vector<int> sta;
int temp;
int i;
for(i = 0; i < asteroids.size(); ++i){
    if(asteroids[i] > 0){	//向右运动的行星无限制入栈。
        sta.push_back(asteroids[i]);
    }else{					//向左运动的需满足相应条件才可入栈。
        win:
        if(sta.empty()){
            sta.push_back(asteroids[i]);
        }else{
            if(sta.back() < 0){
                sta.push_back(asteroids[i]);
            }else{// sta.back() > 0
                temp = asteroids[i] + sta.back();
                if(temp < 0){       //win
                    sta.pop_back();
                    goto win;
                }else if(temp > 0){ //not win
                    continue;;
                }else{              //draw
                    sta.pop_back();
                    continue;;
                }
            }
        }
    }
return sta;
```

## [636. 函数的独占时间](https://leetcode.cn/problems/exclusive-time-of-functions/)

一个时间段内只能执行一个函数，函数可以被挂起、可以递归。问每个函数分别运行了多长时间。

### 基本思路

*   start入栈，end出栈。

### 错误的想法

*   尝试在出栈时计算重叠的时间dt，以便在出栈时计算去除重叠时间后的持续时间。

### 要点

*   每次输入的时间是非递减的

    考虑使用栈将start / end配对，栈中的函数都是挂起函数，遇到end时启动栈顶函数，并修改栈顶函数的启动时间。

*   想象函数挂起后重新启动

    考虑在启动新函数时更新被挂起函数start的时间，以避免dt的计算。

*   注意start与start之间的时间间隔（运行期间要启动新函数）和start与end之间的时间间隔的计算方法。

*   存储函数对应的序号及其start的时间。

```cpp
vector<int> exclusiveTime(int n, vector<string> &logs){
    vector<int> res(n, 0);
    vector<pair<int, int>> ts;	//{idx, t}
    for(auto &i : logs){
        char type[10];
        int idx, t;
        sscanf(i.c_str(), "%d:%[^:]:%d", &idx, type, &t);
        if(type[0] == 's'){
            if(!ts.empty()){
                res[ts.back().first] += t - ts.back().second;
            }
            ts.push_back({idx, t});
        }else{
            //无需判断，一定有与之配对的start。
            auto ff = ts.back();
            ts.pop();
            res[ff.first] += t - ff.second + 1;
            if(!ts.empty()){
                //更新栈顶被挂起函数的启动时间。
                ts.back().second = t + 1;
            }
        }
    }
    return res;
}
```

# 队列

## [剑指 Offer II 041. 滑动窗口的平均值](https://leetcode.cn/problems/qIsx9U/)

队列傻瓜题。

\[0], \[1], \[2] -> \[0], \[1], \[2], \[3] -> \[1], \[2], \[3]

```cpp
double next(int val) {
    q.push(val);
    sum += val;
    if(q.size() > winSize){
        sum -= q.front();
        q.pop();
        return static_cast<double>(sum) / winSize;
    }else{
        return static_cast<double>(sum) / q.size();
    }
}
```

# 模拟

## 2028

思路是对每个未知骰子进行分摊（nogori--;res\[i]++;）。

有解的条件是1n<=sum(res\[i])<=6n（平均分摊）。

有解的条件下必能进行平均分摊。

## [2343. 裁剪数字后查询第 K 小的数字 - 力扣（LeetCode）](https://leetcode.cn/problems/query-kth-smallest-trimmed-number/)

*   本题有两件事要做

    *   裁剪字符串
    *   查询第k小的数

*   关于裁剪字符串

    可以直接用string的substr方法。

    ```cpp
    //从off处开始，返回长度为cnt的字符串；若不指定cnt，则裁剪至末尾。
    int off, cnt;
    string s;
    s.substr(off, cnt);
    ```

    本题的裁剪

    ```cpp
    //从len-queries[i][1]处开始裁剪到结尾。（为了剩下queries[i][1]位）
    nums[j].substr(len - queries[i][1]);
    ```

*   关于查询第k小的数

    考虑到题目提供的数组长度较短，可以使用小顶堆来解决问题。

    ```cpp
    priority_queue<pair<string, int>, vector<pair<string, int>>, greater<pair<string, int>> > q;
    for(int i = 0; i < k - 1; ++i){
        q.pop();
    }
    ```

*   还需要注意的东西

    *   题目中要求返回的数组的元素是nums的索引

        故需要建立字符串对应数字大小和字符串对应索引的联系。

        此处使用pair\<string, int>作为解决方法。

    *   题目要求若nums中出现相同大小的string，则索引小则小

        故将pair作为小顶堆的元素（字符串相同则比较索引）。

# 暴力

## [1668. 最大重复子字符串](https://leetcode.cn/problems/maximum-repeating-substring/description/)

可能是考察kmp？

### 暴力必须注意的点

- 先检查是否越界，再构造string

  ```cpp
  string temp;
  while(j + word.size() <= sequence.size() 
        && temp.assign(sequence.begin() + j, sequence.begin() + j + word.size()) == word) {
  	// ...
  }
  // SHIT, DON'T do it
  // string temp(sequence.begin() + i, sequence.begin() + i + word.size());
  // int c = 0, j = i;
  // while(temp == word && j + word.size() <= sequence.size()) {
  //     j += word.size();
  //     ++c;
  //     temp = string(sequence.begin() + j, sequence.begin() + j + word.size());
  // }
  ```

  

- word.size()是size_t类型，无符号整型

  ```cpp
  // DON'T do it
  // i <= sequence.size() - word.size();
  i + word.size() <= sequence.size();	// good
  ```

  

## [731. 我的日程安排表 II - 力扣（LeetCode）](https://leetcode.cn/problems/my-calendar-ii/)

### 暴力解法

*   记待新增区间为\[start, end)，搜素到的区间为\[l, r)

*   此题不同于安排表I，使用二分搜索的效果与直接遍历相差无几（数据量较少）

    考虑使用线性存储结构来保存预定区间，预定区间仍使用pair\<int, int>来存储。

*   题目要求最多只能出现二次重复预订，而不能出现三次及三次以上

    意思是同一个预定之间最多只能出现一个交集。故考虑使用另外一个存储结构保存所有的交集（防止出现三次重复）。

*   题目的主要矛盾转换为交集的求解

    考虑到待新增区间可能会与已经预定的区间产生较多的交集，故不考虑使用二分搜索来搜索所有可能产生交集的区间（此时复杂度为O(log^2(n))，且代码复杂容易出错），而题目的数据量较少，选择线性存储结构直接遍历更为简洁。

*   主要求解思路

    遍历交集数组，用待插入区间比较，若与交集数组的元素有交集，则一定不能新增预定（交集数组的元素是待插入区间与已预定区间的交集）；若无交集，则一定能够插入。

    无交集的充要条件是：start >=  r 或 l >= end，则有交集的充要条件是：start < r && l < end。

    交集区间为\[max(start, l), min(end, r))。

```cpp
class MyCalendarTwo {
public:
    MyCalendarTwo() {

    }

    bool book(int start, int end) {
        for (auto &[l, r] : overlaps) {
            if (l < end && start < r) {
                return false;
            }
        }
    	// lambda表达式    
        for (auto &[l, r] : booked) {
            if (l < end && start < r) {
                overlaps.emplace_back(max(l, start), min(r, end));
            }
        }
        booked.emplace_back(start, end);
        return true;
    }
private:
    vector<pair<int, int>> booked;
    vector<pair<int, int>> overlaps;
};
```

### 二分解法（WA）

```cpp
class MyCalendarTwo {
public:
    bool book(int start, int end) {
        auto ip = booked.lower_bound({end, 0});
        if(ip == booked.begin() || (--ip)->second <= start){
            booked.emplace(start, end);
            return true;
        }else{
            // 计算交集（-多个连续区间）
            // 扩展预定区间（插入填充），更新交集区间
            auto sip = booked.lower_bound({start, 0});
            if(sip == booked.begin()){
                if(start < sip->first){
                    booked.insert({start, sip ->first});
                }else{
                    // [start, sip->second)
                    auto rip = re.lower_bound({sip->second, 0});
                    if(rip == re.begin() || (--rip)->second <= start){
                        re.emplace(start, sip->second);
                        }else{
                        return false;
                    }
                    booked.emplace(sip->second, (++sip)->first);
                }
                
            }else{
                if((--sip)->second < start){
                    ++sip;
                    booked.emplace(start, sip->first);
                }else{
                    // [start, sip->second)
                    auto rip = re.lower_bound({sip->second, 0});
                    if(rip == re.begin() || (--rip)->second <= start){
                        re.emplace(start, sip->second);
                    }else{
                        return false;
                    }
                    booked.emplace(sip->second, (++sip)->first);
                }
                
            }
            // between sip1 and sip2
            while(sip != ip && sip != booked.end()){
                auto rip = re.lower_bound({sip->second, 0});
                // slow
                if(rip == re.begin() || (--rip)->second <= sip->first){
                    re.emplace(sip->first, sip->second);
                }else{
                    return false;
                }
                booked.emplace(sip->second, (++sip)->first);
            }
            // sip == ip
            if(sip->second < end){
                // [sip->first, sip->second]
                auto rip = re.lower_bound({sip->second, 0});
                if(rip == re.begin() || (--rip)->second <= sip->first){
                    re.emplace(sip->first, sip->second);
                }else{
                    return false;
                }
                booked.emplace(sip->second, end);
            }else{
                // [sip->first, end]
                auto rip = re.lower_bound({end, 0});
                if(rip == re.begin() || (--rip)->second <= sip->first){
                    re.emplace(sip->first, end);
                }else{
                    return false;
                }
            }
            return true;
        }
        return false;
    }
    set<pair<int, int>> booked;
    set<pair<int, int>> re;
};
```

# 二分搜索

在**有序的**排列中，快速找到**特定的**元素。

## 729.我的日程安排表I

假定有两个区间\[l1, r1)和\[l2, r2)，其中\[l2, r2)在\[l1, r2)相邻的右边。

只需满足r1<= start < end <= l2即可插入。

*   lower\_bound / upper\_bound

    ```cpp
    booked.lower_bound(a);	//返回大于等于a的第一个元素，没有则返回end。
    booked.upper_bound(a);	//返回大于a的第一个元素，没有则返回end。
    ```

*   搜索具有特定端点的区间元素

    所有区间分布在\[0, 10e9)。

    pair的比较与字符串的比较方式一致。

    ```cpp
    booked.lower_bound({end, 0});	//搜索开始端点大于等于end的区间
    booked.lower_bound({start, 0});	//搜索开始端点大于等于start的区间
    ```

    ```cpp
    booked.lower_bound({0, end});	//搜索结束端点大于等于end的区间
    booked.lower_bound({0, start});
    ```

*   通过搜索{r1, 0}来达到搜索\[l2, r2)的目的

```cpp
class MyCalendar {
    set<pair<int, int>> booked;

public:
    bool book(int start, int end) {
        auto it = booked.lower_bound({end, 0});	// 搜索第一个大于等于end的元素（设此时返回[l2, r2)），此时已经满足end <= l2。
        if (it == booked.begin()/* 此时所有的区间都在[start, end)的右边 */ || (--it)/* 此时为[l1, r1) */->second/* r1 */ <= start/* 再满足start >= r1即可插入 */) {
            booked.emplace(start, end);
            return true;
        }
        return false;
    }
};
```

## [704. 二分查找](https://leetcode.cn/problems/binary-search/)

在有序序列中寻找特定元素，没有则-1。

*   标准库左闭右开的思想，每次迭代的区间均为左闭右开

    序列排序为升序。

    ```cpp
    int search(vector<int>& nums, int target) {
        // 11:21-11:34
        int x1, x2, x;.
        // 初始化搜索区间为[0, nums.size())。
        x1 = 0;
        x2 = nums.size();
        // 当x1 == x2时，[x1, x2)为空集。
        while(x1 != x2){
            x = (x1 + x2) / 2;
            if(nums[x] > target){
                // target小于nums[x]，故缩小x2。
                // 需要搜索[x1, x)。
                x2 = x;
            }else if(nums[x] == target){
                return x;
            }else{
                // target大于nums[x]，故放大x1，此时nums[x]已经不包括在搜索区间。
                // 需要搜索[x + 1, x2)。
                x1 = x + 1;
            }
        }
        // 必然无解。
    	return -1;
    }
    ```

*   需注意(x1 + x2)可能会溢出

    ```cpp
    // x = (x1 + x2) / 2;
    x = x1 + (x2 - x1) / 2;
    ```

# 双指针

## 532.差值为k的不同数对

### 排序+双指针

*   排序

    ```cpp
    sort(nums.begin(), nums.end());
    ```

*   在 y > x 的条件下搜索差值为k的数对

    寻找到一个符合条件的数对即停止。配合下面的代码能跳过重复数对。

    ```cpp
    while (/* 防止y越界 */y < n 
           && /* y要大于x，并且满足题目条件 */(nums[y] < nums[x] + k || y <= x)) {
        ++y;
    }
    if (y < n && nums[y] == nums[x] + k) {
        ++res;
    }
    ```

*   对x的循环

    ```cpp
    for (int x = 0; x < n; ++x) {
        while (y < n && (nums[y] < nums[x] + k || y <= x)) {
        	++y;
    	}
        // 此处 y<n 是必要的（nums的长度可能只有1，需要防止在调用nums[y]时越界）。
        if (y < n && nums[y] == nums[x] + k) {
            ++res;
        }
    }
    ```

*   为防止找到同样的数对

    此时保证移动 y 判断是否为符合题意的数对之前，nums\[x] 与 nums\[x-1] 是不同的数（相同时移动 x ），如此便能跳过重复数对。

    ```cpp
    for (int x = 0; x < n; ++x) {
    	// 此处考虑了长度为1的条件。
        if(x == 0 || nums[x] != nums[x-1]){
            while (y < n && (nums[y] < nums[x] + k || y <= x)) {
                ++y;
            }
            // 长度为1时防止越界。
            if (y < n && nums[y] == nums[x] + k) {
                ++res;
            }
        }
    }
    ```

#### 解法的其他说明

*   nums.size() == 1 时的情况已考虑

    当长度为1时，y < n 不成立，不会执行nums\[y]，res不会自加，最终结果仍为0。

*   逻辑运算符的执行顺序是从左到右。

    以下代码不会越界。

    x == 0时不会执行nums\[x-1]。

    ```cpp
    if(x == 0 || nums[x-1] != nums[x]);
    ```

### 排序+二分搜索

*   排序

*   对nums\[i]，搜索(nums\[i + 1], nums\[nums.size() - 1])

    复杂度为O(nlogn)。

# 杂题

## 326

精度处理。

```cpp
class Solution {
public:
    bool isPowerOfThree(int n) {
        if(n>0)
            return abs(round(log(n)/log(3))-log(n)/log(3))<0.00000000000001;
        else
            return false;
    }
};
```

## 数质数

```cpp
bool IsPrime(int n){
    int i(2);
    while(i * i <= n){
        if(n % i == 0)
            return false;
        ++i;
    }
    return true;
}
```

## [189. 轮转数组](https://leetcode.cn/problems/rotate-array/)

结论kana。考虑ABCDE循环左移/右移2位后C的位置，左移：C在第一位，故最后再整个翻转；右移：C在最后一个，所以先整个翻转。

*   循环左移k位

    最后整个翻转。

    ```cpp
    reverse(nums.begin(), nums.begin() + k);
    reverse(nums.begin() + k, nums.end());
    reverse(nums.begin(), nums.end());
    ```

*   循环右移k位

    先整个翻转。

    ```cpp
    reverse(nums.begin(), nums.end());
    reverse(nums.begin(), nums.begin() + k);
    reverse(nums.begin() + k, nums.end());
    ```

# 贪心

## [769. 最多能完成排序的块 - 力扣（LeetCode）](https://leetcode.cn/problems/max-chunks-to-make-sorted/)

*   此题跟子序列的升降序没有必然关系

    如\[4,3,2,1,0]、\[4,1,2,3,0]、\[2,3,4,0,1]都只能分成1个块。

*   最多的块

    故要求分块尽可能小。

*   arr长度为n，元素范围在\[0, n - 1]，每个元素都不一样

    故按升序排序后，arr\[i] == i。即要求每个分块排序后都有arr\[i] == i。

*   若arr\[a] == b，a < b

    则必须对arr\[a, b]内的元素进行排序，此时arr\[i]才有可能等于i（a <= i <= b）。

    当\[a, b]区间内的最大值为arr\[a] == b时，arr\[a]必被搬运到arr\[b]处（升序排序），才有arr\[b] == b。

    当\[a, b]区间内的最小值为a时，排序后arr\[a]处才为a。

    *   又因为每个元素都不一样，最大值为a，最小值为b，故arr\[a, b]区间的元素必在\[a, b]内取值。

        因此能够将arr\[a, b]作为一个分块的必要条件是区间\[a, b]内的元素都分布在arr\[a, b]中。

    *   又因为假设区间\[a, b]内的元素都分布在arr\[a, b]中，排序后必有arr\[i] == i。

        充分性。

*   贪心

    遍历找到所有满足条件的\[a, b]即可。令a = 0，arr\[a] == b。若在遍历到arr\[b]的过程中有arr\[c] > b，则变更遍历区间的右边界为c；若遍历到b时最大值仍为b，则块数自加（arr\[0, b]之间没有比b大的数，即最大值为b，所以arr\[0, b]取值范围一定是在\[0, b]，结论可以推广至\[a, b]，a大于0的情况）。然后设起点为b + 1，重复上述过程直到数组尾。

# 阿尔茨海默

*   引用或指针才能改变该变量，否则仅是拷贝。

*   答案对10^9+7取模

    ```cpp
    (a * b * c) % (1e9+7) == (a % (1e9+7) + b % (1e9+7) + c % (1e9+7)) % (1e9+7);
    ```

*   判断一个数是否为奇数

    ```cpp
    if(a & 1);
    if(a % 2);
    ```

# 抄的题

## [768. 最多能完成排序的块 II - 力扣（LeetCode）](https://leetcode.cn/problems/max-chunks-to-make-sorted-ii/)

## [761. 特殊的二进制序列 - 力扣（LeetCode）](https://leetcode.cn/problems/special-binary-string/submissions/)
