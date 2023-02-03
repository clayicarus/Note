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

