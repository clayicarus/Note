# 二月刷题记录

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

