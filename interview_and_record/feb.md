# 二月刷题记录

# day2

## [剑指 Offer 24. 反转链表 - 力扣（Leetcode）](https://leetcode.cn/problems/fan-zhuan-lian-biao-lcof/description/?envType=study-plan&id=lcof&plan=lcof&plan_progress=b3onxkr)

### 递归解法

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        if(!head || !head->next) {
            h = head;
        } else {
            tra(head);
        }
        return h;
    }
    void tra(ListNode *head) 
    {
        if(head->next->next) {
            tra(head->next);
            // 此处状态为满足head->next->next不为空
            // 需要执行翻转操作
        } else {
            // 此处位置不满足head->next->next不为空
            // 即此处的head为倒数第一个结点的head
            // 需要执行交换操作
            h = head->next;
        }
        auto temp = head->next->next;
        head->next->next = head;
        head->next = temp;
    }
    ListNode *h;
};
```

### 栈解法

```cpp
ListNode* reverseList(ListNode* head) {
    if(!head || !head->next)
        return head;
    vector<ListNode*> v;
    while(head) {
        // while(head) 会将所有非空结点指针入栈，出口head为nullptr
        // while(head->next) 则除了最后一个结点均入栈，出口head为倒数第一个结点指针
        v.push_back(head);
        head = head->next;
    }
    head = v.back();
    while(!v.empty()) {
        auto temp = v.back();
        v.pop_back();
        temp->next = v.empty() ? nullptr : v.back();
    }
    return head;
}
```

## [剑指 Offer 35. 复杂链表的复制 - 力扣（Leetcode）](https://leetcode.cn/problems/fu-za-lian-biao-de-fu-zhi-lcof/solutions/)

### 哈希表

保存原链表的地址对应的结点序号，由原链表中random指向的地址，可以确定其指向结点的序号。复制链表，将新链表每个结点的地址保存到数组中，通过数组的下标即可按次序索引到每个结点。同时遍历新旧链表，根据旧链表的random可以映射到对应的序号，再由该序号可以索引到新链表的对应的结点地址。

```cpp
Node* copyRandomList(Node* head) {
    map<Node*, int> r;
    vector<Node*> v;
    if(!head) 
        return head;

    Node *h = new Node(head->val);
    int i = 0;
    auto n = h;
    r[head] = i++;
    v.push_back(h);
    auto temp = head->next;
    while(temp) {
        r[temp] = i++;
        n->next = new Node(temp->val);
        n = n->next;
        v.push_back(n);
        temp = temp->next;
    }
    temp = h;
    while(temp) {
        temp->random = head->random ? v[r[head->random]] : nullptr;
        temp = temp->next;
        head = head->next;
    }

    return h;
}
```

# day8

## [70. 爬楼梯 - 力扣（Leetcode）](https://leetcode.cn/problems/climbing-stairs/solutions/)

```cpp
dp[i] = dp[i - 2] + dp[i - 1]
```

dp[i] 为走到第i层的方法数目。由于只能由第i - 1和第i - 2层走到第i层，故有上述转移方程。

## [剑指 Offer 46. 把数字翻译成字符串 - 力扣（Leetcode）](https://leetcode.cn/problems/ba-shu-zi-fan-yi-cheng-zi-fu-chuan-lcof/description/)

当数字小于等于25，大于等于10时，相当于普通跳台阶的状态转移；

除此之外的情况，只能由dp[i - 1]转移到dp[i]。

```cpp
if(s[i - 2] == '2' && s[i - 1] <= '5'
|| s[i - 2] == '1') {
    dp[i] = dp[i - 1] + dp[i - 2];
} else {
    dp[i] = dp[i - 1];
}
```

# day12

## [剑指 Offer 25. 合并两个排序的链表 - 力扣（Leetcode）](https://leetcode.cn/problems/he-bing-liang-ge-pai-xu-de-lian-biao-lcof/?envType=study-plan&id=lcof&plan=lcof&plan_progress=b3onxkr)

```cpp
ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
    ListNode *res;
    auto p = &res;
    while(l1 && l2) {
        if(l1->val > l2->val) {
            *p = new ListNode(l2->val);
            l2 = l2->next;
        } else {
            *p = new ListNode(l1->val);
            l1 = l1->next;
        }
        p = &(*p)->next;
    }
    *p = l1 ? l1 : l2;
    return res;
}
```

# day7

## [剑指 Offer 26. 树的子结构 - 力扣（Leetcode）](https://leetcode.cn/problems/shu-de-zi-jie-gou-lcof/description/)

子结构与子树不一样。子结构是树中随意挖一块，不需要遍历到叶子结点；而子树要求遍历到叶子结点。

```cpp
// 判断t1中是否包含子结构t2，要求t2遍历完即可。
bool isExist(TreeNode *t1, TreeNode *t2)
{
    if(t1 && t2) {
        if(t1->val != t2->val) {
            return false;
        } else {
            return isExist(t1->left, t2->left) 
                && isExist(t1->right, t2->right);
        }
    } else if(!t2) {
        // t2遍历结束，t1不需要继续遍历，t1包含子结构t2。
        return true;
    } else {
        // t1遍历结束，t2没有遍历结束，t1不包含子结构t2。
        return false;
    }
}
```

```cpp
// 判断t1、t2是否为两棵一样的树。
bool isSame(TreeNode *t1, TreeNode *t2) 
{
    if(t1 && t2) {
        if(t1->val != t2->val) {
            return false;
        } else {
            return isSame(t1->left, t2->left)
                && isSame(t1->right, t2->right);
        }
    } else if(!t1 && !t2) {
        // t1、t2同时遍历结束
        return true;
    } else {
        // 不同时
        return false;
    }
}
```

# day9

## [剑指 Offer 47. 礼物的最大价值 - 力扣（Leetcode）](https://leetcode.cn/problems/li-wu-de-zui-da-jie-zhi-lcof/description/)

```cpp
// 无记忆的dfs
// m是延路径的价值加和，dfs返回的是遍历到底部时，所有路径对应的m的最大值。
class Solution {
public:
    int maxValue(vector<vector<int>>& grid) {
        return dfs(0, 0, 0, grid);
    }
    int dfs(int i, int j, int m, vector<vector<int>>& grid)
    {
        if(i < grid.size() && j < grid[0].size()) {
            int n = m + grid[i][j];
            return max(dfs(i + 1, j, n, grid), dfs(i, j + 1, n, grid));
        } else {
            return m;
        }
    }
};
```

```cpp
// 带记忆的dfs
// mat[i][j]表示以(i,j)为起点的路径最大价值。则mat[i][j] = max(mat[i + 1], mat[j + 1])
// dfs(i, j)返回mat[i][j]
class Solution {
public:
    int maxValue(vector<vector<int>>& grid) {
        mat.assign(grid.size(), vector<int>(grid[0].size(), -1));
        return dfs(0, 0, grid);
    }
    int dfs(int i, int j, vector<vector<int>>& grid)
    {
        if(i < grid.size() && j < grid[0].size()) {
            if(mat[i][j] == -1) {
                mat[i][j] = max(dfs(i + 1, j, grid), dfs(i, j + 1, grid)) + grid[i][j];
            }
            return mat[i][j];
        } else {
            return 0;
        }
    }
    vector<vector<int>> mat;
};
```

# day10

## [剑指 Offer 48. 最长不含重复字符的子字符串 - 力扣（Leetcode）](https://leetcode.cn/problems/zui-chang-bu-han-zhong-fu-zi-fu-de-zi-zi-fu-chuan-lcof/?envType=study-plan&id=lcof&plan=lcof&plan_progress=b3onxkr)

双指针，当[i, j)没有重复字符时，mark[s[j++]] = false，直到出现重复字符mark[j]；出现重复字符后mark[s[i++]] = true，直到mark[s[j]] == true。然后继续移动j，长度即为 j - i 。

- [i, j) ，[i] 为第一个未被占用的。
- j 的终态为 j == s.size() 或者 mark[s[j]] == false。
- i 的终态为 i == j 或者 mark[s[j]] == false。
- 当 i == j 时，令mark[s[j++]] == false，开始下一轮迭代。

```cpp
int lengthOfLongestSubstring(string s) {
    vector<bool> mark(128, true);
    int res = 0;
    for(int i = 0, j = 0; i < s.size() && j < s.size(); mark[s[i++]] = true) {
        if(i == j) {
            mark[s[j++]] = false;
        }
        while(j < s.size() && mark[s[j]]) {
            mark[s[j++]] = false;
        }
        auto len = j - i;
        res = max(len, res);
    }
    return res;
}
```

# day15

## [剑指 Offer 34. 二叉树中和为某一值的路径 - 力扣（Leetcode）](https://leetcode.cn/problems/er-cha-shu-zhong-he-wei-mou-yi-zhi-de-lu-jing-lcof/submissions/402892122/)

- wa

```cpp
class Solution {
public:
    vector<vector<int>> pathSum(TreeNode* root, int target) {
        t = target;
        if(root)
            dfs(root, 0, true);
        return v;
    }
    void dfs(TreeNode *tree, int sum, bool flag) 
    {
        if(tree) {
            p.push_back(tree->val);
            dfs(tree->left, sum + tree->val, true);
            // 在此处pop只能保证延左结点返回时会回溯。
            dfs(tree->right, sum + tree->val, false);
            p.pop_back();	// 该位置防止v空时的pop，此处的val必然存在；在此处pop时保证经过该节点返回时都会pop。
        } else if(t == sum && flag) {
            // 不能在此处使用flag判断p是否符合条件
            // 原因是此处的状态不能保证是叶子结点，只知道tree是nullptr，而不知道tree的父节点是否为叶子结点
            // 故需要使用另外一种递归结构
            if(t == sum) {
                v.push_back(p);
            }
        }
    }
    int t;
    vector<vector<int>> v;
    vector<int> p;
};
```

- ac

```cpp
class Solution {
public:
    vector<vector<int>> pathSum(TreeNode* root, int target) {
        t = target;
        // root 为空时不能返回[[]]，只能返回[]
        if(root)
            dfs(root, 0);
        return v;
    }
    void dfs(TreeNode *tree, int sum) 
    {
        // tree必不为空
        p.push_back(tree->val);
        if(!tree->left && !tree->right) {
            if(sum + tree->val == t)	// 注意此处的sum还未加上tree->val
                v.push_back(p);
        } else {
            if(tree->left) 
                dfs(tree->left, sum + tree->val);
            if(tree->right) 
                dfs(tree->right, sum + tree->val);
        }
        p.pop_back();
    }
    int t;
    vector<vector<int>> v;
    vector<int> p;
};
```

## [剑指 Offer 54. 二叉搜索树的第k大节点 - 力扣（Leetcode）](https://leetcode.cn/problems/er-cha-sou-suo-shu-de-di-kda-jie-dian-lcof/)

二叉搜索树的中序遍历为 **递增序列** 。

```cpp
class Solution {
public:
    int kthLargest(TreeNode* root, int k) {
        t = k;
        dfs(root);
        return res;
    }
    void dfs(TreeNode *root)
    {
        if(root && t) {	// t为0时提前返回
            dfs(root->right);
            if(!--t) {
                res = root->val;	// 此时的res符合题意
                return;				// 提前返回
            }
            dfs(root->left);
        }
    }
    int t;
    int res;
};
```

## [剑指 Offer 36. 二叉搜索树与双向链表 - 力扣（Leetcode）](https://leetcode.cn/problems/er-cha-sou-suo-shu-yu-shuang-xiang-lian-biao-lcof/)

中序遍历后，遍历两次数组，将节点连接。

```cpp
class Solution {
public:
    Node* treeToDoublyList(Node* root) {
        if(!root)	// root为nullptr时不能返回v.front()
            return nullptr;
        dfs(root);
        for(int i = 0; i < v.size() - 1; ++i) {
            v[i]->right = v[i + 1];
        }
        for(int i = 1; i < v.size(); ++i) {
            v[i]->left = v[i - 1];
        }
        v.back()->right = v.front();
        v.front()->left = v.back();

        return v.front();
    }
    void dfs(Node *tree) 
    {
        if(tree) {
            dfs(tree->left);
            v.push_back(tree);
            dfs(tree->right);
        }
    } 
    vector<Node*> v;
};
```

## [剑指 Offer 54. 二叉搜索树的第k大节点 - 力扣（Leetcode）](https://leetcode.cn/problems/er-cha-sou-suo-shu-de-di-kda-jie-dian-lcof/?envType=study-plan&id=lcof&plan=lcof&plan_progress=b3onxkr)

- 搜索二叉树的中序遍历为递增序列，从右子树开始即为递减序列
- 故只需记录在中序位置返回了k次时的val

```cpp
void dfs(TreeNode *root)
{
    if(root && t) {	// k为0时提前返回
        dfs(root->right);
        if(!--t) {
            res = root->val;	// 只记录--k为0时的值，并于此返回
            return;
        }
        dfs(root->left);
    }
}
```

# day16

## [面试题45. 把数组排成最小的数 - 力扣（Leetcode）](https://leetcode.cn/problems/ba-shu-zu-pai-cheng-zui-xiao-de-shu-lcof/?envType=study-plan&id=lcof&plan=lcof&plan_progress=b3onxkr)

```cpp
sort(v.begin(), v.end(), [](const auto &a, const auto &b){
    return a + b < b + a;
});
```

# day17

## [剑指 Offer 40. 最小的k个数 - 力扣（Leetcode）](https://leetcode.cn/problems/zui-xiao-de-kge-shu-lcof/description/)

- 直接排序是最快的

- 求数组中最小的k个数应该想起来堆排序

  注意小根堆的声明方法，greater<>即为递增序列。

```cpp
vector<int> getLeastNumbers(vector<int> &arr, int k) {
    priority_queue<int, vector<int>, greater<int>> q(arr.begin(), q.end());
    vector<int> res(k);
    for(auto &i : res) {
        i = q.top();
        q.pop();
    }
    return res;
}
```

## [剑指 Offer 41. 数据流中的中位数 - 力扣（Leetcode）](https://leetcode.cn/problems/shu-ju-liu-zhong-de-zhong-wei-shu-lcof/?envType=study-plan&id=lcof&plan=lcof&plan_progress=b3onxkr)

需要考虑到堆的性质：

- 小根堆asc：堆中所有元素都大于等于根
- 大根堆dsc：堆中所有元素都小于等于根

考虑堆在数轴中的区间表示，只需要维护小根堆的根大于等于大根堆的根，并且两个堆中的元素数目相差不大于1，则两个堆的根的平均数即为中位数（元素数目为偶数的情况）。

实际实现中可以保持小根堆的元素数目总是大于等于大根堆的元素数目，可在插入元素后，调整中位数端点来防止元素数目相差大于1。

需要维护的不变量：

- 小根堆的根大于等于大根堆的根
- 小根堆的元素数目总是大于等于大根堆的数目，且相差不大于1（注意分别讨论等于1、等于0的情况）

需要注意不变量的维护的过程：

- 初始化时的维护，两个堆均为空时优先将元素放在小根堆中

- 当asc.size() - dsc.size() == 2时，维护后，asc.size() - dsc.size() == 0

  当dsc.size() - asc.size() == 1时，维护后，asc.size() - dsc.size() == 1

  需要由维护后的状态反推应该什么时候维护之。

```cpp
void addNum(int num) {
    if(asc.empty() || num >= asc.top()) {	// 进入asc的条件
        asc.push(num);
        if(asc.size() - 1 > dsc.size()) {	// 注意此处应该在asc元素数目相差大于1的时候才需要调整。
            assert(asc.size() - dsc.size() == 2);
            dsc.push(asc.top());
            asc.pop();
            assert(asc.size() - dsc.size() == 0);	// 调整后数目相等。
        }
    } else {	
        dsc.push(num);
        // 由于两堆为空时优先插入asc，此处插入后dsc的数目要么比asc多1，要么与asc相等。
        if(dsc.size() > asc.size()) {	// dsc多1的情况，此时才需要调整。
            assert(dsc.size() - asc.size() == 1);
            asc.push(dsc.top());
            dsc.pop();
            assert(asc.size() - dsc.size() == 1);	// 调整后asc比dsc多1。
        }
    }
}
```

# day18

## [剑指 Offer 55 - I. 二叉树的深度 - 力扣（Leetcode）](https://leetcode.cn/problems/er-cha-shu-de-shen-du-lcof/?envType=study-plan&id=lcof&plan=lcof&plan_progress=b3onxkr)

动态规划的思想，左右子树的深度最大值 + 1即为树的高度。

```cpp
int maxDepth(TreeNode* root) {
    return root ? max(maxDepth(root->left) + 1, maxDepth(root->right) + 1) : 0;
}
```

## [剑指 Offer 55 - II. 平衡二叉树 - 力扣（Leetcode）](https://leetcode.cn/problems/ping-heng-er-cha-shu-lcof/description/)

注意平衡二叉树的每一个子树都是平衡二叉树，故需要对每棵子树判断。

```cpp
class Solution {
public:
    bool isBalanced(TreeNode* root) {
        if(root) {
            auto t = abs(dfs(root->left) - dfs(root->right)) <= 1;
            if(t) {
                return isBalanced(root->left) && isBalanced(root->right);
            } else {
                return false;
            }
        } else {
            return true;
        }
    }
    int dfs(TreeNode *tree) {
        return tree ? max(dfs(tree->left) + 1, dfs(tree->right) + 1) : 0;
    }
};
```

# day19

## [剑指 Offer 64. 求1+2+…+n - 力扣（Leetcode）](https://leetcode.cn/problems/qiu-12n-lcof/description/)

```cpp
int res() {
    bool arr[n][n + 1];
    return sizeof(arr) >> 1;	// n * (n + 1) / 2
}
```

## [剑指 Offer 68 - II. 二叉树的最近公共祖先 - 力扣（Leetcode）](https://leetcode.cn/problems/er-cha-shu-de-zui-jin-gong-gong-zu-xian-lcof/description/)

p，q都不为nullptr，故树非空。

遍历时记录所有结点的父节点fa[node->left] = node。

之后从fa[p]开始遍历，直到遍历到根节点的父节点（nullptr），记录是否访问过。

最后从fa[q]开始遍历，遍历到访问过的结点就即为最近的祖先。

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        fa[root->val] = nullptr;
        dfs(root);
        while(p != nullptr) {
            mark[p->val] = true;
            p = fa[p->val];
        }
        while(q != nullptr) {
            if(mark[q->val]) return q;
            q = fa[q->val];
        }
        return nullptr;
    }
    void dfs(TreeNode *tr) 
    {
        if(tr->left) {
            fa[tr->left->val] = tr;
            dfs(tr->left);
        }
        if(tr->right) {
            fa[tr->right->val] = tr;
            dfs(tr->right);
        }
    }
    map<int, TreeNode*> fa;
    map<int, bool> mark;
};
```

## [剑指 Offer 68 - I. 二叉搜索树的最近公共祖先 - 力扣（Leetcode）](https://leetcode.cn/problems/er-cha-sou-suo-shu-de-zui-jin-gong-gong-zu-xian-lcof/description/)

思路与上一道题相同，这道题可以快速遍历到p、q结点，然后直接返回即可。

```cpp
void dfs(TreeNode *tr, int val)
{
    if(tr->val < val) {
        fa[tr->right] = tr;
        dfs(tr->right, val);
    } 
    if(val < tr->val) {
        fa[tr->left] = tr;
        dfs(tr->left, val);
    }
}
```

# day20

## [剑指 Offer 07. 重建二叉树 - 力扣（Leetcode）](https://leetcode.cn/problems/zhong-jian-er-cha-shu-lcof/description/)

- 考虑前序、中序遍历的性质

  ```
  preorder: [根, [左子树], [右子树]]
  inorder: [[左子树], 根, [右子树]]
  ```

- 考虑构造二叉树需要知道什么条件：

  需要知道根节点的值，左子树，右子树。

  ```cpp
  build() {
      ...
      auto *p = new TreeNode(root_val);
      p->left = build();
      p->right = build();
      ...
  }
  ```

- 定义tr_in<int, int>表示需要构造的树在inorder中的范围

  定义tr_pre<int, int>表示需要构造的树在preorder中的范围

  - 则root_val = preorder[tr_pre.first]

  - 需要知道左子树的大小才可以确定左子树在preorder中的范围

    而左子树的大小lsz = 根在inorder的位置 - tr_in.first。

  - 此后也可以确定右子树在preorder的位置 [tr_pre.first + 1 + lsz, tr_pre.second)
  - 当需要构造树的大小为0时返回nullptr

- 定义build函数，输入树在数组的范围，返回构造后的树

  ```cpp
  TreeNode *build(pair<int, int> tr_pre, pair<int, int> tr_in)
  {
      auto sz = tr_pre.first - tr_pre.second;
      assert(sz == tr_in.first - tr_in.second);
      if(!sz) 
          return nullptr;
      auto root_val = (*pre)[tr_pre.first];
      auto tree = new TreeNode(root_val);
      auto lsz = rt_idx.at(root_val) - tr_in.first;
      tree->left = build({tr_pre.first + 1, tr_pre.first + 1 + lsz}, {tr_in.first, tr_in.first + lsz});
      tree->right = build({tr_pre.first + 1 + lsz, tr_pre.second}, {tr_in.first + lsz + 1, tr_in.second});
      return tree;
  }
  ```

- 递归初始化

  考虑到经常需要搜索root_val在inorder中的位置，可以用哈希表保存每个值的索引。

  ```cpp
  root_val = preorder[0];
  tr_pre/in = {0, pre/in.size()}
  auto lsz = rt_idx[root_val] - 0;
  ```

## [剑指 Offer 16. 数值的整数次方 - 力扣（Leetcode）](https://leetcode.cn/problems/shu-zhi-de-zheng-shu-ci-fang-lcof/description/)

快速幂：x^n = x^(n/2) * x^(n/2)

```cpp
class Solution {
public:
    double quickMul(double x, long long n) {
        assert(n >= 0);
        if (n == 0) {
            return 1.0;
        }
        auto temp = quickMul(x, n / 2);
        return n % 2 == 0 ? temp * temp : temp * temp * x;
    }
    double myPow(double x, int n) {
        return n < 0 ? 1. / quickMul(x, -static_cast<long long>(n)) : quickMul(x, -n);
    }
};
```

## [剑指 Offer 33. 二叉搜索树的后序遍历序列 - 力扣（Leetcode）](https://leetcode.cn/problems/er-cha-sou-suo-shu-de-hou-xu-bian-li-xu-lie-lcof/description/)

- 后序遍历：[[左], [右], 根]

- 搜索二叉树：[左] <= 根 <= [右]

- 节点值均不相同：[左] < 根 < [右]

- 右子树end：p.begin() + end - 1;

- root_val：*rend

- 第一个大于root_val的位置即为右子树的起始位置

  注意搜索区间为 [p.begin() + beg, rend) 而不是 [p.begin() + beg, p.begin() + end) ，因为右子树的起始位置不可能大于rend

```cpp
// 直接从 [0, postorder.size()] 开始递归
class Solution {
public:
    bool verifyPostorder(vector<int>& postorder) {
        post = &postorder;
        return verify(0, postorder.size());
    }
    bool verify(int beg, int end)
    {
        assert(end >= beg);
        auto sz = end - beg;
        assert(sz >= 0);
        if(!sz)
            return true;
        auto &p = *post;
        auto rend = p.begin() + end - 1;
        auto root_val = *rend;
        auto rbeg = find_if(p.begin() + beg, rend, [root_val](const auto &a){return a > root_val;});
        auto lsz = distance(p.begin() + beg, rbeg);
        auto rsz = distance(rbeg, rend);
        assert(rbeg <= rend);

        if(find_if(rbeg, rend, [root_val](const auto &a){return root_val > a;}) != rend)
            return false;
        return verify(beg, beg + lsz) && verify(beg + lsz, beg + lsz + rsz);
    }
    vector<int> *post;
};
```

# day21

## [剑指 Offer 65. 不用加减乘除做加法 - 力扣（Leetcode）](https://leetcode.cn/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof/description/)

还没看。

# day22

## [剑指 Offer 56 - I. 数组中数字出现的次数 - 力扣（Leetcode）](https://leetcode.cn/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-lcof/description/)

考虑异或的性质：对某一位异或，该位相同则为0，不同则为1。

不是0就是1。对整个数组异或，等价于有两个不同的数字异或，结果至少有一位为1，据该位是否为0就可以将数组分成两组，相同数字必在同一组，不同数字必然不在同一组。

## [剑指 Offer 65. 不用加减乘除做加法 - 力扣（Leetcode）](https://leetcode.cn/problems/bu-yong-jia-jian-cheng-chu-zuo-jia-fa-lcof/description/)

不带进位加法结果为 a ^ b，进位结果为 (a & b) << 1。

```cpp
int add(int a, int b) {
    while (b != 0) {
        unsigned int carry = (unsigned int)(a & b) << 1;
        a = a ^ b;
        b = carry;
    }
    return a;
}
```

## [剑指 Offer 56 - II. 数组中数字出现的次数 II - 力扣（Leetcode）](https://leetcode.cn/problems/shu-zu-zhong-shu-zi-chu-xian-de-ci-shu-ii-lcof/description/)

直接上哈希表。

# day23

## [剑指 Offer 66. 构建乘积数组 - 力扣（Leetcode）](https://leetcode.cn/problems/gou-jian-cheng-ji-shu-zu-lcof/description/)

前缀和（？）。x[i] 为 [0, i) 所有数的乘积，y[i] 为 (i, end) 所有数的乘积，则 res[i] = x[i] * y[i]。

- x[i] = x[i - 1] * a[i - 1]
- y[i] = y[i + 1] * a[i + 1]

```cpp
vector<int> constructArr(vector<int>& a) {
	.....
    y.back() = 1;
    for(int i = y.size() - 2; i >= 0; --i) {	// 注意此处是 --i
        y[i] = y[i + 1] * a[i + 1];
    }
	.....
    return res;
}
```

# day24

## [剑指 Offer 14- I. 剪绳子 - 力扣（Leetcode）](https://leetcode.cn/problems/jian-sheng-zi-lcof/description/)

- 需要考虑到底应该分成多少份，大于等于两份

- 设dp[i]为将i分成两份以上得到的最大乘积
- i = (i -j) + j，j <= i / 2

```cpp
int res = 0;
for(int j = 1; j <= i/2; ++j) {
    vector<int> temp(4);
    temp[0] = j * (i - j);
    temp[1] = dp[j] * (i - j);
    temp[2] = j * dp[i - j];
    temp[3] = dp[j] * dp[i - j];
    res = max(res, *max_element(temp.begin(), temp.end()));
}
dp[i] = res;
```

## [剑指 Offer 62. 圆圈中最后剩下的数字 - 力扣（Leetcode）](https://leetcode.cn/problems/yuan-quan-zhong-zui-hou-sheng-xia-de-shu-zi-lcof/description/)

不会。

# day25

## [剑指 Offer 31. 栈的压入、弹出序列 - 力扣（Leetcode）](https://leetcode.cn/problems/zhan-de-ya-ru-dan-chu-xu-lie-lcof/description/)

可以使用一个栈模拟该过程。栈中元素不重复，可以哈希表来记录栈中有哪些元素。遍历弹出序列的元素，元素要么在栈中，要么在待入栈序列中。

- 元素在栈中时，弹出栈的元素，直到找到该元素被弹出。
- 元素在待入栈序列时（即不在栈中时），将待入栈元素入栈并在哈希表中标记，直到找到该元素出现。若没有找到该元素，则返回false。
- 弹出元素顺利遍历结束即可返回true。

# day26

## [剑指 Offer 20. 表示数值的字符串 - 力扣（Leetcode）](https://leetcode.cn/problems/biao-shi-shu-zhi-de-zi-fu-chuan-lcof/description/)

自动机？不会。

## [面试题67. 把字符串转换成整数 - 力扣（Leetcode）](https://leetcode.cn/problems/ba-zi-fu-chuan-zhuan-huan-cheng-zheng-shu-lcof/description/)

可以模拟，比较冗长。

自动机？不会。



