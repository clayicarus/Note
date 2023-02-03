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

