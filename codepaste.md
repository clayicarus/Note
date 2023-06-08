### index.js, index.html

```js
const url = "http://localhost:8752";

let getList = (endpoint, do_sth) => {
    req = new Request(url + endpoint);
    fetch(req).then((res) => {
        res.json().then(do_sth);
        // if (res.status === 200) {
        //     // res.json()/.blob()/.arrayBuffer is promise
        //     res.json().then(do_sth);
        // } else {
        //     console.log("Something wrong with api");
        // }
    }).catch(e => {
        let a = { data: [{ title: endpoint, id: 1 }] };
        do_sth(a);
    });
};

let getElementsByTagWithAttribute = (tag, attr) => {
    let a = document.getElementsByTagName(tag);
    let lst = [];
    for (let i = 0; i < a.length; ++i) {
        if(a[i].getAttribute(attr) != null) {
            lst.push(a[i]);
        }
    }
    return lst;
};

const lst = getElementsByTagWithAttribute("li", "list");
let ep2idx = {};
for (let i = 0; i < lst.length; ++i) {
    let r = lst[i];
    const endpoint = r.getAttribute("list");
    console.log(r);
    if(!ep2idx[endpoint]) {
        ep2idx[endpoint] = [i];
    } else {
        ep2idx[endpoint].push(i);
    }
}
a = [];
for(ep in ep2idx) {
    a.push(ep);
}
console.log(ep2idx);
for(ep in ep2idx) {
    // let ep = a[i];
    console.log(ep);
    function Handle(j) {
        this.endp = ep;
        let idx = ep2idx[this.endp];
        console.log(this.endp);
        console.log(endp);  // a,b,c
        console.log(idx);
        for (i of idx) {
            let r = lst[i];
            console.log(i);
            r.removeAttribute("list");
            // console.log(j["data"]);
            let d = j["data"];
            for (i of d) {
                const e = r.cloneNode();
                e.innerHTML = JSON.stringify(i);
                r.parentNode.appendChild(e);
            }
        }
    }
    getList(ep, Handle
        // only capture non object by value, others capture by name (in block it execute)
    );
}

```

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <!-- 必须的 meta 标签 -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap 的 CSS 文件 -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>Hello, world!</h1>
    <ul>
      <li list="/article/a">1</li>
    </ul>

    <ul>
      <li>2</li>
      <li list="/article/b">3</li>
      <li>4</li>
    </ul>

    <ul>
      <li list="/article/c">5</li>
      <li>6</li>
    </ul>

    <!-- JavaScript 文件是可选的。从以下两种建议中选择一个即可！ -->

    <!-- 选项 1：jQuery 和 Bootstrap 集成包（集成了 Popper） -->
    <!-- <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-7ymO4nGrkm372HoSbq1OY2DP4pEZnMiA+E0F3zPr+JQQtQ82gQ1HPY3QIVtztVua" crossorigin="anonymous"></script> -->

    <!-- 选项 2：Popper 和 Bootstrap 的 JS 插件各自独立 -->
    
    <script src="https://cdn.jsdelivr.net/npm/jquery@3.5.1/dist/jquery.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js" integrity="sha384-Lge2E2XotzMiwH69/MXB72yLpwyENMiOKX8zS8Qo7LDCvaBIWGL+GlRQEKIpYR04" crossorigin="anonymous"></script>
   
  </body>
  <script src="index.js"></script>
</html>


```



