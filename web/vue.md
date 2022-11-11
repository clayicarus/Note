### 文本插值

使用一对花括号 `{{ var_name }}` 改变`innerHtml`。

```vue
<script>
export default {
	data() {
		return {
			msg: "hello"
        };
    },
};
</script>
<template>
<head>{{ msg }}</head>
</template>
```

### Attribute绑定

带 v- 是标签的一种vue特有的 atribute。

v-bind:*attribute_name*="*var_name*"。

简写为 :*attribute_name*="*var_name*"。

将 data() 中的 *var_name* 绑定到该标签的 *attribute_name* 属性，表现为该标签的 *attribute_name* 属性的值会随着 data() 中的 *var_name* 变化而变化。

```vue
<script>
export default {
	data() {
		return {
            head_id: "head1",
        };
    },
};
</script>
<template>
<head v-bind:id="head_id"></head>
</template>
```

上例的 head 标签的 id 属性被绑定为 head_id 的值。

简写版本：

```vue
<template>
<head :id="head_id"></head>
</template>
```

- v- 属性中不允许有多余的空格。

### 事件监听

`v-on` 指令监听 DOM 事件。

v-on:*event*="func();" 简写为 @*event*="func" 。

```vue
<template>
<button v-on:click="func();">
    {{ count }}
</button>
</template>
<script>
export default {
    data() {
        return {
            count: 0
        };
    },
    methods: {
        func() {
            ++this.count;
        },
    },
};
</script>
```

- 方法都应该写在 `methods` 选项中，而且不能够带 `function` 关键字。
- data() 中的值与变量定义类似。

### 表单绑定

同时使用 `v-bind` 和 `v-on` 对表单的元素双向绑定。

```vue
<template>
<input :value="text" @input="onInput">
</template>

<script>
export default {
    data() {
        text: "",
            
    },
    methods: {
        onInput(e) {
            // v-on 处理函数会接收原生 DOM 事件作为其参数。
            this.text = e.target.value;
        },
    },
};
</script>
```

- `@input` 是 `input` 监听的输入事件，绑定到 `onInput` 方法。
- `:value` 是将 `input` 的 `value` 属性绑定到 data() 中的 text 成员，text的值不会因为输入而变化。
- 貌似只有回调函数而不绑定 value 的效果是一样的？

简化写法：

```vue
<template>
<input v-model="text">
</template>
```

- text的值会随着输入而变化。

### 条件渲染

`v-if`, `v-else`, `v-else-if` 实现条件渲染。

v-if="*expression*"，当表达式为真时渲染标签。

```vue
<div v-if="1 == 1">1 = 1</div>
<div v-else>1 != 1</div>
```

此时只会渲染第一个 div。

### 列表渲染

```vue
<template>
  <form @submit.prevent="addTodo">
    <input v-model="newTodo">
    <button>Add Todo</button>    
  </form>
  <ul>
    <li v-for="todo in todos" :key="todo.id">
      {{ todo.text }}
      <button @click="removeTodo(todo)">X</button>
    </li>
  </ul>
</template>
```

- key 是 vue 一个特殊的 attribute，使得 vue 能够精确移动每一个 `<li>`，以匹配对象在数组的位置。
- `<li>` 里的 `<button>` 同样能获得 v-for 中的 todo 对象。
- `<form>` 中监听的 `@submit.prevent` 事件发生在表单提交。

### 计算属性

computed 组件。计算属性会自动跟踪里面用到的量，发生改变时会自动调用并更新。

与 methods 组件不同，computed 的方法会因为量改变而自动调用，而 methods 只在事件发生时会调用。

```vue
<script>
let id = 0;
export default {
  data() {
    return {
      newTodo: '',
      hideCompleted: false,
      todos: [],
    }
  },
  computed: {
    // 该方法不能放在 methods 里
    filteredTodos() {
      return this.todos.filter((i) => {
        if(this.hideCompleted)
          return !i.done;
        return true;
      });
    },
  },
</script>

<template>
    <li v-for="todo in filteredTodos" :key="todo.id">
      <input type="checkbox" v-model="todo.done">
      <span :class="{ done: todo.done }">{{ todo.text }}</span>
      <button @click="removeTodo(todo)">X</button>
    </li>
  </ul>
  <button @click="hideCompleted = !hideCompleted">
    {{ hideCompleted ? 'Show all' : 'Hide completed' }}
  </button>
</template>
```

### 生命周期模板引用

- 模板引用

  给标签一个 `ref` 属性，此后该标签的 DOM 对象会暴露在 `this.$refs` 中，`this.$refs.name` 即可访问到该对象。

  ref="*dom_name*"。

  ```js
  export default {
    mounted() {	// 发生在组件挂载后。
      this.$refs.dom_name.textContent = 'mounted!'
    }
  }
  ```

### 侦听器

侦听 data() 中的某个量，当这个量发生改变时会使用改变后的量作为参数回调 watch 中的同名函数。

```vue
<script>
export default {
  data() {
    return {
      count: 0
    }
  },
  watch: {
    count(newCount) {	// this.count 改变后会回调这个函数。
      // newCount 是回调传参，作为改变后的值。
      console.log(`new count is: ${newCount}`)
    }
  }
}
</script>
```

### 组件

- 组件导入

  import 并在 components 中注册该组件。

  ```vue
  <script>
  import ChildComp from "./ChildComp.vue"
  export default {
    // register child component
    components: {
      ChildComp,
    },
  }
  </script>
  
  <template>
    <!-- render child component -->
    <ChildComp />
  </template>
  ```

  ./ChildComp.vue 中

  ```vue
  <template>
  <h2>Child component.</h2>
  </template>
  ```

  

- props

  子组件可以通过 props 从父组件中接收动态数据。

  ```js
  // 在子组件中
  export default {
    props: {
      msg: String
    }
  }
  ```

  父组件中将变量绑定到同名属性即可实现数据传递给子组件。

  ```vue
  <template>
    <ChildComp :msg="greeting" />
  </template>
  ```

- emits

  子组件可以通过 emits 向父组件触发事件。

  声明事件。

  ```js
  // 子组件中声明了名为 event 的事件，使用组件时可以侦听到该事件。
  export default {
      emits: ["event"],
      created() {
          this.$emit("event", "message from component");	// 触发该事件，传递参数。
      },
  }
  ```

  使用组件。

  ```vue
  <h2 @event="(msg) => { /*...*/ }"></h2>
  ```

- slots

  父组件可以通过 slots 将模板片段传递给子组件。

  在父组件中：

  ```vue
  <ChildComp>
  希望传递给子组件中的slot的内容。
  </ChildComp>
  ```

  子组件中：

  ```vue
  <slot>当父组件中没有传递内容显示的东西。</slot>
  ```

  

# javascript

## 数组

- splice()

  改变原数组。

  ```js
  let arr = ["a", "b", "c"];
  arr.splice(index, n);	// 从 index 开始删除n个元素，返回删除元素的数组。
  ```

- filter(lambda)

  不改变原数组，返回满足条件的元素的数组。

  

  

  
