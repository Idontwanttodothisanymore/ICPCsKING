---
tags:
  - 数据结构
  - 笔记
  - 树上启发式
status: 完成
---
树上每个节点 $v$ 都要回答一个关于**它子树内所有节点**的统计问题，例如"子树里出现次数最多的颜色是哪种""子树里有多少种不同颜色"。

朴素做法是对每个 $v$ 遍历整个子树，最坏(链)是 $\Theta(n^2)$。DSU on tree 把它降到 $\Theta(n\log n)$。

**[模版题 CF 600 E Lomsat gelral](https://codeforces.com/contest/600/problem/E)**

> 给一个根节点为 $1$ 的树，每个节点上有一个颜色。求所有子树中最多的颜色的编号之和（如果有多个颜色数量并列最多，把编号加起来）

存一个 `cnt[x]` 表示颜色 $x$ 出现次数，`maxx` 表示目前的数量最多的颜色的数量，`sum` 表示目前最多的颜色的编号和。

如果树是一条链，那么这是容易的，因为可以直接从下到上扫，依次更新我们所需要的数据。当情况更一般的时候，我们可以稍微暴力一点，也就是通过上面的想法计算树中的重链，对于其他的轻儿子，直接暴力的处理就好了。

这就是启发式合并的树上版本了。具体地：

1. 先递归处理所有**轻儿子**，处理完后**清空**数据结构（轻儿子的信息不保留）；
2. 再递归处理**重儿子**，处理完后**保留**数据结构(此时里面已经装着重儿子子树的全部信息)；
3. 把 $v$ 自己，以及所有轻儿子子树里的节点,**逐个加进**数据结构；
4. 此时数据结构恰好是 $v$ 的整棵子树，回答 $v$ 的询问；
5. 如果 $v$ 本身是其父亲的轻儿子，就把整个子树**清空**；否则保留。

和启发式合并的对应关系:重儿子的信息就是"大集合"，原地保留不用搬；轻儿子子树就是"小集合"，逐个搬进来。

##### 复杂度分析

数一个节点 $u$ 被"暴力加入"多少次。只有当 $u$ 位于某个祖先 $v$ 的**轻儿子子树**里时， $u$ 才会在处理 $v$ 时被加一次。

从 $u$ 往根走，每经过一条**轻边**，子树大小至少翻倍（轻儿子的子树大小不超过父亲子树的一半）。所以从 $u$ 到根最多经过 $\log_2 n$ 条轻边，即 $u$ 最多被加 $\Theta(\log n)$ 次。总代价 $\Theta(n\log n)$。

##### 代码实现

```cpp
#include <bits/stdc++.h>
#define int long long
using namespace std;

using ll = long long;
using pii = pair<int,int>;
using ull = unsigned long long;

int const N = 2e5 + 10, mod = 1e9 + 7, inf = 0x7fffffff;
int n, m, k, a[N], son[N], sz[N], cnt[N], sum, maxx, big, ans[N];
vector<int> e[N];

void dfs1(int x, int lst) { // 算重儿子
    sz[x] ++;
    int mx = 0;
    for (auto i : e[x]) {
        if (i == lst) continue;
        dfs1(i, x);
        sz[x] += sz[i];
        if (sz[i] > mx) {
            mx = sz[i];
            son[x] = i;
        }
    }
} 

void add(int x, int lst, int d) { // 将以 x 为节点的子树中所有的颜色的cnt +1 / -1
    cnt[a[x]] += d;
    if (d == 1) {
        if (cnt[a[x]] > maxx) maxx = cnt[a[x]], sum = a[x];
        else if (cnt[a[x]] == maxx) sum += a[x];
    }
    for (int i : e[x]) if (i != lst && i != big) add(i, x, d);
}

void dfs2(int x, int lst, bool keep) { 
    for (auto i : e[x]) if (i != son[x] && i != lst) dfs2(i, x, 0); // 算轻儿子
    if (son[x]) dfs2(son[x], x, 1), big = son[x]; // big 表示当前在处理的重儿子
    add(x, lst, 1);
    ans[x] = sum;
    big = 0;
    if (!keep) add(x, lst, -1), sum = maxx = 0;
}

void Main(){
    cin >> n;
    for (int i = 1;i <= n;++i) cin >> a[i];
    for (int i = 1;i <= n - 1;++i) {
        int x, y;
        cin >> x >> y;
        e[x].push_back(y);
        e[y].push_back(x);
    }
    dfs1(1, 0);
    dfs2(1, 0, 1);
    for (int i = 1;i <= n;++i) cout << ans[i] << ' ';
}
signed main() {
    // freopen("cpp.in", "r", stdin);
    // freopen("cpp.out", "w", stdout);
    int T = 1;
    // cin >> T;
    while(T--) Main();
    return 0;
}
```

`add` 里跳过 `big` 是关键:重儿子的信息已经在 `cnt` 里了,不能重复加。

- [x] 洛谷 U41492 树上数颜色（模板）
- [x] 洛谷 P4755 Beautiful Pair（启发式合并 + 值域计数）
- [ ] CF 600E Lomsat gelral（子树众数之和，最经典入门）
- [ ] CF 208E Blood Cousins（树上 k 级祖先 + 表兄弟计数


相关：[[线段树合并]]、[[CDQ 分治]]、[[树链剖分]]
