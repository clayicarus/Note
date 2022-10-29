# 一些经验

- 获取数组的最大（小）值

  选择排序的一次遍历。

  ```cpp
  int max;
  for(auto &i:v)
      max=max(i,max);
  ```

- 散列表的遍历

  ```cpp
  unordered_map<int,int> ht;
  for(auto i:ht)
      cout<<i.first<<": "<<i.second<<endl;
  ```


