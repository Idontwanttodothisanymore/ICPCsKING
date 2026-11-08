---
tags: [图论, 模板, LCA]
status: 骨架
---
过去那些求 LCA 的方法都弱爆了！看我的 DFS 序！

DFS 序表示对一棵树进行深度优先搜索得到的节点序列，而 **时间戳** dfn 表示每个节点再 DFS 序中的位置。  

---

考虑树上的两个节点 $u, v$ 及其最近的公共祖先 $d$，在 DFS 遍历中， $d$ 没有在 $u,v$ 之间出现过。

DFS 序的性质：祖先先于后代遍历，即若 $u$ 是 $v$ 的祖先，则 $dfn_{u}<dfn_{v}$。

不妨设 $dfn_{u}<dfn_{v}$：

- 当 $u$ 不是 $v$ 的祖先时，DFS的顺序是 $d\to u\to d\to v$。因为到达 $u$ 在到达 $d$ 之后，到达 $v$ 在离开 $d$ 之前。这说明 $u,v$ 之间的所有点都在 $d$ 的子树内（不含 $d$）。 因此， $u\to v$ 中深度最小的点的父亲就是 $d$。
  
- 当 $u$ 是 $v$ 的祖先时，考虑将查询区间从 $[dfn_{u},dfn_{v}]$ 改成 $[dfn_{u}+1,dfn_{v}]$。这意味着我们查询 $u$ 的一个儿子和 $v$ 的 LCA，这将 case 2 转化成了 case 1，且不会影响 case 1 的答案。

综上，若 $u\neq v$，则他们的 LCA 等于 DFS 序上位置在 $[dfn_{u}+1,dfn_{v}]$ 的深度最小的任意节点的父亲。若 $u=v$，LCA 就等于 $u$ 这也是唯一需要特判的情况。

一种避免记录每个结点的父亲和深度的方法是直接在 ST 表的最底层记录父亲，比较时取时间戳较小的结点。因为时间戳最小的点一定是所关注的子树的根。如果你完全理解了 DFS 序求 LCA，自然能够理解这个技巧的正确性。

```cpp
  
#include <bits/stdc++.h>
using namespace std;
constexpr int N = 5e5 + 5;
int n, m, R, dn, dfn[N], mi[19][N];
vector<int> e[N];
int get(int x, int y) {
	return dfn[x] < dfn[y] ? x : y;
}
void dfs(int id, int f) {
	mi[0][dfn[id] = ++dn] = f;
	for (int it : e[id]) if (it != f) dfs(it, id); 
}
int lca(int u, int v) {
    if (u == v) return u;
    if ((u = dfn[u]) > (v = dfn[v])) swap(u, v);
    int d = __lg(v - u++);
    return get (mi[d][u], mi[d][v - (1 << d) + 1]);
}
int main() {
    scanf("%d %d %d", &n, &m, &R);
    for (int i = 2, u, v; i <= n; i++) {
        scanf("%d %d", &u, &v);
	    e[u].push_back(v), e[v].push_back(u);
	}
    dfs(R, 0);
    for (int i = 1; i <= __lg(n); i++)
	    for (int j = 1; j + (1 << i) - 1 <= n; j++)
		    mi[i][j] = get(mi[i - 1][j], mi[i - 1][j + (1 << i - 1)]);
	for (int i = 1, u, v; i <= m; i++) scanf("%d %d", &u, &v), printf("%d\n", lca(u, v));
    return 0;
}
```

> [!todo] 待补
> - [x] 倍增 LCA 代码
> - [x] 欧拉序 ST 表版
> - [ ] 树上差分用法

相关：[[树链剖分]]、[[图论]]
