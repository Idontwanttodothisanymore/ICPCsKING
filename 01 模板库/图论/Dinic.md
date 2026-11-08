---
tags: [图论, 模板, 网络流]
status: 完成
---

# Dinic

> 复杂度：一般图 $O(n^2 m)$，二分图单位容量 $O(m \sqrt n)$。
> 必须：当前弧优化 + 分层 BFS；边数 ×2（反向边），`tot` 从 1 起使反向边为 `i^1`。

```cpp
#include <bits/stdc++.h>
using namespace std;
const int N = 1e5 + 10, M = 2e6 + 10;
struct Dinic {
    struct E { int to, next; long long cap; } e[M];
    int head[N], dep[N], cur[N], tot = 1, S, T;
    void init(){ memset(head, -1, sizeof head); tot = 1; }
    void addE(int u, int v, long long c){
        e[++tot] = {v, head[u], c}; head[u] = tot;
        e[++tot] = {u, head[v], 0}; head[v] = tot;  // 反向边
    }
    bool bfs(){
        memset(dep, -1, sizeof dep);
        queue<int> q; q.push(S); dep[S] = 0;
        while(!q.empty()){
            int u = q.front(); q.pop();
            for(int i = head[u]; i != -1; i = e[i].next){
                int v = e[i].to;
                if(dep[v] == -1 && e[i].cap > 0){
                    dep[v] = dep[u] + 1;
                    if(v == T) return true;
                    q.push(v);
                }
            }
        }
        return dep[T] != -1;
    }
    long long dfs(int u, long long in){
        if(u == T) return in;
        long long used = 0;
        for(int &i = cur[u]; i != -1; i = e[i].next){   // 当前弧
            int v = e[i].to;
            if(dep[v] == dep[u] + 1 && e[i].cap > 0){
                long long f = dfs(v, min(in - used, e[i].cap));
                if(f > 0){
                    e[i].cap -= f; e[i ^ 1].cap += f; used += f;
                    if(used == in) break;
                }
            }
        }
        return used;
    }
    long long run(int s, int t){
        S = s; T = t; long long ans = 0;
        while(bfs()){
            memcpy(cur, head, sizeof cur);
            ans += dfs(S, (1ll << 60));
        }
        return ans;
    }
} D;
int main(){
    int n, m, s, t; scanf("%d%d%d%d", &n, &m, &s, &t);
    D.init();
    for(int i = 0; i < m; i++){ int u,v; long long c; scanf("%d%d%lld",&u,&v,&c); D.addE(u,v,c); }
    printf("%lld\n", D.run(s, t));
    return 0;
}
```

> [!tip] 待补（用到再拷）
> - 费用流（SSP + SPFA / Dijkstra+势）
> - 上下界可行流、最大点权独立集封装

相关：[[网络流]]
