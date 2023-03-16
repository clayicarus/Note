### bfs

```cpp
#include <iostream>
#include <vector>
#include <queue>
using namespace std;

vector<vector<int>> *pm;
const vector<vector<int>> dir {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

int bfs(const pair<int, int> &p, const pair<int, int> &b)  
{
    auto &mat = *pm;
    int m_i = mat.size();
    int m_j = mat.front().size();
    
    vector status(m_i, vector(m_j, vector(m_i, vector<int>(m_j))));
    
    queue<pair<pair<int, int>, pair<int, int>>> q;
    q.emplace(p, b);
    int step = 0;
    while(!q.empty()) {
        auto sz = q.size();
        while(sz--) {
            const auto [p_c, b_c] = q.front();
            q.pop();
            status[p_c.first][p_c.second][b_c.first][b_c.second] = true;
            if(mat[b_c.first][b_c.second] == 'E') {
                return step;
            }
            for(const auto &d : dir) {
                pair<int, int> p_n = { p_c.first + d[0], p_c.second + d[1] };
                pair<int, int> b_n = b_c;
                if(p_n == b_c) {
                    b_n.first += d[0];
                    b_n.second += d[1];
                }
                if(p_n.first < 0 || p_n.second < 0 || b_n.first < 0 || b_n.second < 0
                    || p_n.first == m_i || p_n.second == m_j || b_n.first == m_i || b_n.second == m_j
                    || status[p_n.first][p_n.second][b_n.first][b_n.second]) 
                    continue;
                if(mat[b_n.first][b_n.second] != '#' && mat[p_n.first][p_n.second] != '#')
                    q.emplace(p_n, b_n);
            }
        }
        ++step;
    }
    return -1;
}

int main() {
    int n, m;
    cin >> n >> m;
    int pi, pj, bi, bj;
    vector<vector<int>> mat(n, vector<int>(m));
    for(int i = 0; i < n; ++i) {
        string s;
        cin >> s;
        for(int j = 0; j < m; ++j) {
            mat[i][j] = s[j];
            if(mat[i][j] == 'S') {
                pi = i;
                pj = j;
            }
            if(mat[i][j] == '0') {
                bi = i;
                bj = j;
            }
        }
    }

    pm = &mat;
    cout << bfs({pi, pj}, {bi, bj}) << '\n';
    
    return 0;
}

```



