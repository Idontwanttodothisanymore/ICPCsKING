---
tags: [数据结构, 模板]
status: 骨架
---

# 树状数组（BIT）

> 复杂度：单次 $O(\log n)$。单点加区间和 / 区间加单点查（差分）/ 区间加区间和（双 BIT）。
> 注意：只能维护前缀和意义下可减的信息；求逆元版用于值域计数。

```cpp
/*

 @Author: CreeperOI
 @Problem: Luogu_P_3369
 @Start Time: 2024-04-01 19:54
 @Finish Time: 2024-04-01

*/
#include <bits/stdc++.h>
// #define int long long
using namespace std;

// const int mod = 1e9 + 7;

// ------------------------- templates above -------------------------

int const N = 5e5 + 10;

int s[N], a[N], c[N], n, m;

int lowbit(int x){
    return x & -x;
}

void modify(int x, int d){
    s[x] += d;
    for (int i = x;i <= n;i += lowbit(i)) c[i] += d;
}

int query(int x){
    int ans = 0;
    for (int i = x;i > 0;i -= lowbit(i))
        ans += c[i];
    return ans;
}

void mian(){
    cin >> n >> m;
    for (int i = 1;i <= n;++i) cin >> s[i];
    for (int i = 1;i <= n;++i)
        for (int j = i - lowbit(i) + 1;j <= i;++j) c[i] += s[j];
    while (m--){
        int op, x, y;
        cin >> op >> x >> y;
        if (op == 1) modify(x, y);
        else cout << query(y) - query(x - 1) << endl;
    }
}
signed main() {
    // freopen("cpp.in", "r", stdin);
    // freopen("cpp.out", "w", stdout);
    ios::sync_with_stdio(0), cin.tie(0), cout.tie(0);
    int T = 1;
    while(T--) mian();
    cerr << 1e3 * clock() / CLOCKS_PER_SEC << " ms\n";
    return 0;
}

```

> [!todo] 待补
> - [ ] 单点改区间和代码
> - [ ] 区间改区间和（两个 BIT）代码
> - [ ] 值域 BIT 求逆序对

相关：[[线段树]]
