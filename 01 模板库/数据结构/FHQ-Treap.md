---
tags:
  - 数据结构
  - 模板
status: 模板
---
FHQ Treap 功能强大，几乎覆盖 Treap 的所有功能，而且十分好写且适合持久化。~~以至于我非常后悔学了 Treap，浪费时间。~~

FHQ 的核心思想在于 **分裂和合并。** 对于每个节点，需要存储左右儿子 $ls,rs$、权值 $val$、子树大小 $sz$ 以及 FHQ 特有的随机值 $rd$ 以保证树的深度为 $\log$ 级别。下面介绍该算法的细节。

---

> 动态的维护一个可重集 $M$，支持：插入、删除一个数，将一段区间翻转；查 $x$ 的排名、位于第 $x$ 名的数，$x$ 的前驱、后继。
##### 更新答案

```cpp
void push(int x) {
	sz[x] = sz[ls[x]] + sz[rs[x]] + 1;
}
```

#### 基础操作
##### 分裂

FHQ Treap：我裂开来。

可以按照权值 $val$ 分裂和大小 $sz$ 分裂。

- 按照权值分裂：给定 $v$，我们将原来的平衡树分裂成两个平衡树 $T_{x}$ 和 $T_{y}$，满足对于任意的 $i\in T_{x}$ 和 $j\in T_{y}$，均有 $val_{i} \leq v \leq val_{j}$。
  
  假设当前的节点为 $p$：
	- 如果 $val_{p}\leq v$，那么 $p$ 应该属于 $T_{x}$，而 $p$ 的左儿子 $ls_{p}$ ~~（lsp）~~ 也应该属于 $T_{x}$，故只需要向右递归 $rs_{p}$ 即可；
	- 如果 $val_{p}>v$，那么 $p$ 应该属于 $T_{y}$，而 $p$ 的右儿子 $rs_{p}$ 显然也属于 $T_{y}$，故只需要向右递归 $ls_{p}$ 即可。
  
  代码实现：
  
  ```cpp
  void split(int p, int v, int &x, int &y) {
	  if (!p) return x = y = 0 void();
	  if (val[p] <= v) split(rs[p], v, rs[v = p], y);
	  else split(ls[p], v, x, ls[y = p]);
	  push(p); 
  }
  ```


- 同样的，给定 $v$，对于当前节点 $p$，如果 $v\leq sz_{ls_{p}}$，那么 $p$ 和整个 $rs_{p}$ 的子树都应该被分到 $T_{y}$，向$ls_{p}$ 递归即可。
  
  代码实现：
  
  ```cpp
  void split(int p, int v, int &x, int &y) {
	  if (!p) return x = y = 0, void();
	  if (v <= sz[ls[x]]) split(ls[p], v, x, ls[y = p]);
	  else split(rs[p], v - sz[ls[p]] - 1, rs[x = p], y);
	  push(x); 
  }
  ```

##### 合并

像极了线段树的分裂和合并。

首先，合并的两棵树 $T_{x}$ 和 $T_{y}$ 需要满足对于任意的 $i\in T_{x},j\in T_{y}$，都有 $val_{i}<val_{j}$。假设当前我们要合并 $x,y$ 两个节点：

- 如果 $r d_{x}> r d_{y}$，那么 $x$ 的优先级更高。因此 $x$ 应该是 $y$ 的父亲。而根据二叉平衡树的性质，因为 $val_{x}< val_{y}$，所以 $y$ 是 $x$ 的右儿子。 故调用 $rs_{x}\leftarrow \text{merge}(rs_{x},y)$ 即可。
- 反之亦然，直接调用 $ls_{y}\leftarrow \text{merge}(x,ls_{y})$。
- 递归边界：$x,y$ 中至少有一个为空，此时我们采用类似线段树合并的 Trick，直接返回 $x \text{ or } y$ 即可。

代码实现：

```cpp
int merge(int x, int y) {
	if (!x || !y) return x | y;
	if (rd[x] < rd[y]) return ls[y] = merge(x, ls[x]), push(y), y;
	return rs[x] = merge(rs[x], y), push(x), x;
}
```


#### 功能实现

##### 插入

插入一个数 $v$，只需要按照 $v-1$ 的权值分裂成两棵树 $T_{x},T_{y}$，再 $root= \text{merge}(\text{merge}(x,\text{newnode}(v)))$ 即可。

```cpp
void insert(int v) {
	int x = 0, y = 0;
	split(R, v - 1, x, y), R = merge(merge(x, nd(v)), y);
}
```

##### 删除

删除一个数 $v$，先用 $v$ 按照权值分裂成两棵树 $T_{x},T_{z}$，再用 $v-1$ 按照权值将 $T_{x}$ 分裂成两棵树 $T_{x},T_{y}$，这时 $T_{y}$ 中的元素都是 $v$，我们只需删掉一个，故直接把左右节点合并即可。最后全部合并回来。

```cpp
void del(int v) {
	int x = 0, y = 0, z = 0;
	split(R, v, x, z), split(x, v - 1, x, y);
	R = merge(merge(x, y = merge(ls[y], rs[y])), z);
}
```

##### 第 k 大

查找第 k 大的数：假设当前遍历到了节点 $p$，若 $k\leq sz_{ks_{p}}$，则向左儿子递归；若 $k=sz_{ls_{p}}+1$ 则返回 $val_{p}$，否则向右儿子递归。

```cpp
int kth(int k) {
	int p = R;
	while (1) {
		if (k <= sz[ls[p]]) p = ls[p];
		else if (k == sz[ls[p]]) return val[p];
		else k -= sz[ls[p]] + 1, p = rs[p];
	} 
}
```

##### 前驱 / 后继

和查第 k 大类似。

```cpp
int pre(int v) {
	int p = R, ans = 0;
	while (1) {
		if (!p) return ans;
		else if (v <= val[p]) p = ls[p];
		else ans = val[p], p = rs[p];
	}
}
int suc(int v) {
	int p = R, ans = 0;
	while (1) {
		if (!p) return ans;
		else if (v >= val[p]) p = rs[p];
		else ans = val[p], p = ls[p];
	}
}
```

##### 排名

查询 $v$ 的排名：用 $v-1$ 按照排名将权值分裂成 $T_{x},T_{y}$，那么答案为 $sz_{x}+1$。最后合并。

```cpp
int rnk(int v) {
	int x = 0, y = 0, ans;
	split(R, v - 1, x, y), ans = sz[x] + 1;
	return R = merge(x, y), ans;
}
```

##### 区间翻转

平衡树维护区间，那么每个节点存储的就是对应位置的值，而他的中序遍历就是整个区间。

只要将要翻转的区间分裂出来，打上标记再合并即可。参考文艺平衡树。


[模板题](https://www.luogu.com.cn/problem/P3369)。代码：

```cpp
  
#include <bits/stdc++.h>
using namespace std;

const int N = 1e5+5;
const int inf = 1e9+7;

int R, node, ls[N], rs[N], val[N], rd[N], sz[N];
void push(int x) {
	sz[x] = sz[ls[x]] + sz[rs[x]] + 1;
}

void spl(int p, int v, int &x, int &y) {
	if (!p) return x = y = 0,void();
	if (val[p] <= v) spl(rs[p], v, rs[x = p],y);
	else spl(ls[p], v, x, ls[y = p]);
	push(p);
}
int mer(int x, int y) {
	if(!x || !y) return x | y;
	if(rd[x] < rd[y]) return ls[y] = mer(x, ls[y]), push(y), y;
	return rs[x] = mer(rs[x], y), push(x), x;
}
int nd(int v) {
	int x = ++node;
	val[x] = v, rd[x] = rand(), sz[x] = 1;
	return x;
}
void ins(int v) {
	int x = 0,y = 0;
	spl(R, v - 1, x, y),R = mer(mer(x, nd(v)), y);
}
void del(int v) {
	int x = 0, y = 0, z = 0;
	spl(R, v, x, z), spl(x, v - 1, x, y);
	R = mer(mer(x, y = mer(ls[y], rs[y])), z);
}
int kth(int k) {
	int p = R;
	while(1){
		if (k <= sz[ls[p]]) p = ls[p];
		else if (k == sz[ls[p]] + 1) return val[p];
		else k -= sz[ls[p]] + 1, p = rs[p];
	}
}
int pre(int v) {
	int p = R,ans = 0;
	while(1){
		if(!p) return ans;
		else if (v <= val[p]) p = ls[p];
		else ans = val[p], p = rs[p];
	}
}
int suc(int v) {
	int p = R, ans = 0;
	while(1){
		if(!p) return ans;
		else if (v >= val[p]) p = rs[p];
		else ans = val[p], p = ls[p];
	}
}
int rnk(int v) {
	int x = 0, y = 0, ans = 0;
	spl(R, v - 1, x, y), ans = sz[x] + 1;
	return R = mer(x, y), ans;
}

int n, m;
int main(){
	cin >> n;
	for (int i = 1;i <= n;i++) {
		int op, x; cin >> op >> x;
		if (op == 1) ins(x);
		if (op == 2) del(x);
		if (op == 3) cout << rnk(x) << endl;
		if (op == 4) cout << kth(x) << endl;
		if (op == 5) cout << pre(x) << endl;
		if (op == 6) cout << suc(x) << endl;
	}
	return 0;
}
```