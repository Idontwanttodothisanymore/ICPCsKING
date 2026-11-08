---
tags: [图论, 模板, 最短路]
status: 完成
---

# Dijkstra（优先队列）

> 复杂度：$O(m \log n)$。**非负边权**；负权用 SPFA / Bellman-Ford。

```cpp
#include <bits/stdc++.h>
using namespace std;
const int N = 1e5 + 10, M = 2e5 + 10;
const long long INF = 4e18;
struct Edge { int to, w; };
vector<Edge> g[N];
long long dis[N];
void dijkstra(int s, int n){
    priority_queue<pair<long long,int>, vector<pair<long long,int>>, greater<>> pq;
    fill(dis, dis + n + 1, INF);
    dis[s] = 0; pq.emplace(0, s);
    while(!pq.empty()){
        auto [d, u] = pq.top(); pq.pop();
        if(d != dis[u]) continue;               // 懒删除
        for(auto &e : g[u]){
            if(dis[e.to] > d + e.w){
                dis[e.to] = d + e.w;
                pq.emplace(dis[e.to], e.to);
            }
        }
    }
}
int main(){
    int n, m, s; scanf("%d%d%d", &n, &m, &s);
    for(int i = 0; i < m; i++){ int u,v,w; scanf("%d%d%d",&u,&v,&w); g[u].push_back({v,w}); }
    dijkstra(s, n);
    for(int i = 1; i <= n; i++) printf("%lld ", dis[i] == INF ? -1 : dis[i]);
    return 0;
}
```

> [!tip] 相关板子
> - SPFA（判负环、负权）：Bellman-Ford 队列优化
> - Floyd（全源，$O(n^3)$）
> - 次短路 / k 短路（堆 + 分支删除）

相关：[[图论]]、[[网络流]]
