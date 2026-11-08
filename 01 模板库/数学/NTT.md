---
tags: [数学, 模板, 多项式]
status: 完成
---
> 复杂度：$O(n \log n)$。仅支持模数 $998244353$（$119 \times 2^{23}+1$，原根 3），长度上限 $2^{23}$。
> 用法：`conv(a, b)` 返回多项式 $a \times b$ 的系数（`poly` 即 `vector<int>`），传入时下标即次数。
> 注意：需要精确卷积长度，函数内部已按 `need` 裁剪；系数先对 MOD 取模再传入。

```cpp
// NTT: MOD=998244353, G=3
#include <bits/stdc++.h>

using namespace std;
using ll = long long;
using poly = vector<int>;

const int MOD = 998244353, G = 3;

int qpow(int a, int e) {
    int r = 1;
    for (; e; e >>= 1, a = (ll)a * a % MOD)
        if (e & 1) r = (ll)r * a % MOD;
    return r;
}

void ntt(poly &a, bool inv) {
    int n = a.size();
    for (int i = 1, j = 0; i < n; i++) {
        int b = n >> 1;
        for (; j & b; b >>= 1) j ^= b;
        j ^= b;
        if (i < j) swap(a[i], a[j]);
    }
    for (int len = 2; len <= n; len <<= 1) {
        int w = qpow(G, (MOD - 1) / len);
        if (inv) w = qpow(w, MOD - 2);
        for (int i = 0; i < n; i += len) {
            int cur = 1;
            for (int j = 0; j < len / 2; j++) {
                int u = a[i + j], v = (ll)a[i + j + len / 2] * cur % MOD;
                a[i + j] = (u + v) % MOD;
                a[i + j + len / 2] = (u - v + MOD) % MOD;
                cur = (ll)cur * w % MOD;
            }
        }
    }
    if (inv) {
        int ni = qpow(n, MOD - 2);
        for (int &x : a) x = (ll)x * ni % MOD;
    }
}

poly conv(poly a, poly b) {
    int sz = 1, need = a.size() + b.size() - 1;
    while (sz < need) sz <<= 1;
    a.resize(sz); b.resize(sz);
    ntt(a, 0); ntt(b, 0);
    for (int i = 0; i < sz; i++) a[i] = (ll)a[i] * b[i] % MOD;
    ntt(a, 1);
    a.resize(need);
    return a;
}

```