## 一些经验

### 获取数组的最大（小）值

选择排序的一次遍历。

```cpp
int max;
for(auto &i:v)
    max=max(i,max);
```

### 散列表的遍历

```cpp
unordered_map<int,int> ht;
for(auto i:ht)
    cout<<i.first<<": "<<i.second<<endl;
```

### 不要返回local对象的引用

a的作用域只在f内部。

```cpp
/* DON'T do it */
int& f()
{
    int a(114514);
    return a;
}
```

### shared_ptr\<T\>的默认行为

默认行为是delete T\*。定制行为后会覆盖delete。p为待delete指针的引用。

```cpp
shared_ptr<T> sp(&t, [](auto &p){ delete p; })
```

### 不要用shared_ptr\<T\>管理栈对象

```cpp
/* DON'T do it */
weak_ptr<T> f()
{
    Foo a;
    shared_ptr<T> sp(&a);
    return sp;
}
```

### 不要free一个对象指针

delete会调用一个对象的析构函数而free()不会，不要混用free()来管理对象。

```cpp
Foo *p = new Foo();
// free(p);
delete p;
```

