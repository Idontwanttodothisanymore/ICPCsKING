---
tags:
  - 数据结构
  - 分治
  - 计数
  - 模板
status: 完成
---
> 陌上花开，可缓缓归矣。

CDQ 分治是 IOI 金牌得主陈丹琦提出的一种分治思想，主要用来解决三维偏序、DP 优化、动态转静态的问题。

##### 三维偏序

> 给定 $n$ 个三元组 $(a,b,c)$，对于所有的 $i$，求 满足 $a_{j}\leq a_{i} \wedge b_{j}\leq b_{i} \wedge c_{j}\leq c_{i}$ 的 $j$ 的个数。

CDQ 分治的核心是用不同的逻辑一层层的筛选符合要求的点。

首先将所有元素按照 $a$ 升序排列，这样考虑小于 $i$ 的元素是否满足后两个性质即可，以排序剥开了第一个限制。然后是本算法的核心：使用 CDQ 分治和 BIT 处理第二层和第三层。我们的目标是找到所有满足 $b_{j}\leq b_{i}$ 的 $j$，并把它丢到 BIT 里面以进行最后一次的筛选。

具体而言，为了保证递归树的 $\log$ 深度取 $mid=\frac{l+r}{2}$，随后先递归 CDQ 处理左右两个区间内部的偏序对，然后左右两半分别按 $b$ 排序。用左指针、右指针来遍历这两个区间，因为区间内部的偏序对已经统计，这一轮中只统计左指针属于 $l\sim mid$ 和右指针属于 $mid+1\sim r$ 且满足后两个要求的点。$b_i\leq b_{j}$ 时，把 $c_{i}$ 丢到权值 BIT，然后查询 $c\leq c_{j}$ 的 $c$ 的数量并累计到答案。统计完这一层所有跨中点的贡献后，需要把 BIT 清零，避免残留的数据污染其他递归层的计算。排序时间 $n \log n$，BIT 的查询 $\log n$，总计 $\Theta(n\log^2n)$。

注意到 CDQ 递归的过程中和归并排序很相似，如果将归并的过程内嵌到 CDQ 的递归中可以把复杂度做到 $\Theta(n \log n)$。我这里就不写了。~~没什么用这东西，一般都不卡。~~

当出现三元组相同时，应该进行去重操作，将多个三元组合并成一个，并记录出现次数。

[模版题](https://www.luogu.com.cn/problem/P3810)，代码：

```cpp
#include <bits/stdc++.h>
// #define int long long
using namespace std;
using ll = long long;
using pii = pair<int,int>;
using ull = unsigned long long;

int const N = 2e5 + 10, mod = 1e9 + 7, inf = 0x7fffffff;
int tr[N], k;

void add(int x, int v) { for (; x <= k; x += x & -x) tr[x] += v; }
int  ask(int x) { int r = 0; for (; x; x -= x & -x) r += tr[x]; return r; }

int n;
struct T{
    int a, b, c, cnt, ans;
}e[N];

bool cmp(const T &x, const T &y) {
    return x.b < y.b;
}

void cdq(int l, int r) {
    if (l == r) return;
    int mid = (l + r) >> 1;
    cdq(l, mid); cdq(mid + 1, r);
    sort(e + l, e + mid + 1, cmp);
    sort(e + mid + 1, e + r + 1, cmp);
    int i = l;
    for (int j = mid + 1; j <= r;++j) {
        while (i <= mid && e[i].b <= e[j].b) {
            add(e[i].c, e[i].cnt), i++;
        }
        e[j].ans += ask(e[j].c);
    }
    for (int t = l;t < i;++t) add(e[t].c, -e[t].cnt);
}

void Main(){
    cin >> n >> k;
    for (int i = 1;i <= n;++i) cin >> e[i].a >> e[i].b >> e[i].c;
    sort(e + 1, e + n + 1, [](T a, T b) {
        if (a.a != b.a) return a.a < b.a;
        if (a.b != b.b) return a.b < b.b;
        return a.c < b.c;
    });
    int m = 0;
    for (int i = 1;i <= n;) {
        int j = i;
        while (j <= n && e[j].a == e[i].a && e[i].b == e[j].b && e[i].c == e[j].c) j++;
        e[++m] = {e[i].a, e[i].b, e[i].c, j - i, 0};
        i = j;
    }    
    cdq(1, m);
    static int res[N];
    for (int i = 1;i <= m;++i) res[e[i].ans + e[i].cnt - 1] += e[i].cnt; // 奇妙的去重 trick
    for (int i = 0;i < n;++i) cout << res[i] << endl;
}
signed main() {
    // freopen("cpp.in", "r", stdin);
    // freopen("cpp.out", "w", stdout);
    int T = 1;
    // cin >> e;
    while(T--) Main();
    return 0;
}
```

##### CDQ 分治优化 DP

**[P4093 序列](https://www.luogu.com.cn/problem/P4093)**

> 可以把一个指定的元素换成指定的另一个值。求在一个最长子序列的长度，使其在随意执行上述操作的时候依然不下降。

考虑序列 dp 的常见 trick，设 $dp_{i}$ 为强制选 $a_{i}$ 时最长符合要求子序列的长度。有以下转移：

$$
dp_{i}= \begin{cases}
1\\ \max (dp_{j}+1,1) & j<i\wedge\max(a_{j})\leq a_{i}\wedge a_{j}\leq\min(a_{i})
\end{cases}
$$

第二部分的转移正好和 CDQ 处理的三元偏序很像，只有最后一步统计的时候从统计个数变成了求 $\max$，于是可以采取类似的想法来解决问题。

注意这里的 dp 刚需前缀，所以不能先递归两遍的 CDQ 在处理跨区间的，必须 **左 + 垮区间 + 右** 的顺序。另外双指针排第二维的时候一边是 $\max(a_{j})$ 一边是 $a_{i}$，所以不能通过归并排序处理，必须要显式的排序。

##### 动态转静态

**[P3157 动态逆序对](https://www.luogu.com.cn/problem/P3157)**

> 按顺序将序列中的一些元素删去，求所有时间内的逆序对的数量。

对于一个逆序对 $(u,v)$，如果 $u$ 和 $v$ 中的一个被删去，那么他的贡献的消失了。换言之，记 $u_{t},v_{t}$ 为他们被删掉的时间，其只会在 $t\leq \min(u_{t}, v_{t})$ 时贡献答案。

因此对于每个元素，记录其位置 $pos$，删除的时间 $t$，其值 $v$。对于 $1\sim m$ 的每个 $t$，满足：
$$
\min(t_{i},t_{j})\geq t \wedge \begin{cases}
v_{i}<v_{j} & pos_{i}>pos_{j}\\v_{i}>v_{j} &pos_{i}<pos_{j}
\end{cases}
$$
的 $(i,j)$ 数量就是答案。

将分支拆开，就是两个 CDQ 分治的标准结构。先考虑第一种情况，即：
$$
\min(t_{i},t_{j})\geq t\wedge v_{i}<v_{j}\wedge pos_{i}>pos_{j}
$$
$\min(t_{i},t_{j})\geq t$ 并不是一个合法的偏序维度，不能直接用 CDQ， 但是考虑一整个过程，删除一个元素 $i$ 后只会影响满足 $t_{j} \geq t_i\wedge v_{i}<v_{j} \wedge pos_{i}>pos_{j}$ 的元素。 而这就是合法的偏序维度了。简而言之，我们通过把视角从时间转化到了元素上，从而得到了一个容易计算的式子。

然后考虑第二种情况，聪明的你一定发现了只要把元素和下标左右翻转一下他的要求就和第一维一样了！这样就不用写两遍的 CDQ 了，只需要翻转后再调用函数就好了。

