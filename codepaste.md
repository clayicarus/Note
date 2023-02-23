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

wa

```cpp
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        ans = nullptr;
        flag = false;
        pt = p;
        qt = q;
        dfs(root, nullptr);
        return ans;
    }
    void dfs(TreeNode *tr, TreeNode *fa) 
    {
        if(tr && !flag) {
            dfs(tr->left, tr);
            dfs(tr->right, tr);
            if(flag)
                return;
            if(tr == qt || tr == pt) {
                flag = true;
            }
            ans = fa;
        }
    }
    TreeNode *ans;
    bool flag;
    TreeNode *pt, *qt;
};
```

