## Javascript

### Async

- 回调：参数传递。

  函数作为参数，使用构造函数function()。

  ```js
  function test(function(a,b){
      return a+b;
  },function(a,b){
      return a*b;
  }){
      /* test code */
  };
  ```

  

- Promise： 一种数据类型。

  示例

  ```js
  <script>
  function Show(sth){
      document.getElementById("demo").innerHTML=sth;
  }
  let myPromise=new Promise(function(Resolve,Reject){
      let x=0;
      
      if(x==0){
          Resolve("OK");
      }else{
          Reject("Error");
      }
  });
  
  //构造一个Promise对象，名为myPromise。
  myPromise.then(
      function(value){
          Show(value);
      },
      function(error){
          Show(error);
      }
  );
  </script>
  ```
  
  一般结构
  
  ```js
  let promise=new Promise(function(Resolve,Reject){
      
      /* Produce code, 同步执行的代码 */
      
      if(condition)
      	Resolve(value);		//对应Promise构造函数的第一个回调函数，将value传递给then(success(value),fail)的success的value形参，并使得在执行then方法时（不会因为调用resolve()而直接跳转）跳转至success(value)。一般用作成功时。
      else
          Reject(value);		//对应Promise构造函数的第二个回调函数，将value传递给then(success,fail(value))的fail的value形参，fail(value)。一般用作出错时。
  });
  
  /* Consuming code, 等待P code结束后执行的代码 */
  promise.then(function(value){
      /* Success code */
  },function(value){
      /* Failed code */
  })
  /* 简便Consuming code */
  promise.then(value=>{
      
  });
  ```
  
  Promise的执行顺序
  
  ```js
  /* outside code 1 */
  new Promise(function func(res,rej){
      /* produce code */
      if(/* condition */)
         res(value_res);
      else
         rej(value_rej);
      
  }).then(function(value_res){
      /* func1 */
  },function(value_rej){
      /* func2 */
  });
  /* outside code 2 */
  // 若调用了res(value_res)，则oc1->pc->oc2->func1（then()最后执行）。
  // 若调用了rej(value_rej)，则将func1替换为func2。
  ```
  
  并列Promise以及Promise嵌套的运行顺序
  
  ```js
  /* oc1 */
  new Promise(function(res){
      /* p1_pc1 */
      new Promise(function(res){
          /* pin_pc */
      }).then(function(value){
          /* pin_cc */
      });
      res(value);
      /* p1_pc2 */
  }).then(function(value){
      /* p1_cc */
  });
  /* oc2 */
  new Promise(function(res){
      /* p2_pc */
  }).then(function(value){
      /* p2_cc */
  });
  /* oc3 */
  
  //oc1->p1_pc1->pin_pc->p1_pc2->oc2->p2_pc->oc3->pin_cc->p1_cc->p2_cc
  ```
  
  切割then代码和外代码。先执行外代码，then代码按照由里到外，由上到下的顺序执行。
  
- async、await关键字。

  ```js
  ```

  

### 杂项

- 空对象的判断方法

  ```js
  let temp={};
  temp=={};					//false
  JSON.stringify(temp)=="{}";	//true
  
  ```

  

