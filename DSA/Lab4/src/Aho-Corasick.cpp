#include <cstdio>
#include <cstring>
#include <vector>
#include <queue>

struct node
{
    char c;
    node* fail;
    node* father;
    node* childs[26];
    int depth;

    bool is_end = false;
    int num = 0;

    node() : c('\0'), fail(NULL), father(NULL), depth(-1){for (int i = 0; i < 26; i++) childs[i] = NULL;}
    node(char c, node *father) : c(c), fail(NULL), father(father)
    {
        for (int i = 0; i < 26; i++) childs[i] = NULL;
        depth = (father -> depth) + 1;
    }

    // 检查是否有字符为c的子节点
    bool check(char c){return (childs[c - 97] ? true : false);}
    bool update(){if (is_end) num++; return is_end;}

    // 返回字符为c的子节点的位置
    node* next(char c){return childs[c - 97];}
    // 插入字符为c的子节点
    node* insert(char c){return childs[c - 97] = new node(c, this);}
};

class acm
{
public:
    node *root = new node();
    std::vector<node*> patterns;

    void insert(char *P)
    {
        node *p = root;
        for (int i = 0; i < (int)strlen(P); i++)
        {
            if (!(p -> check(P[i]))) p -> insert(P[i]);
            p = p -> next(P[i]);
        }
        p -> is_end = true;
        patterns.push_back(p);
    }

    void buildF()
    {
        std::queue<node*> Q;
        for (int i = 0; i < 26; i++)
        {
            if (root -> childs[i]) Q.push(root -> childs[i]);
        }
        while (!Q.empty())
        {
            node *p = Q.front(); Q.pop();
            for (int i = 0; i < 26; i++)
            {
                if (p -> childs[i]) Q.push(p -> childs[i]);
            }
            if (!(p -> father -> fail)){p -> fail = root; continue;}
            node *x = p -> father -> fail;
            while (x)
            {
                if (x -> check(p -> c)){p -> fail = x -> next(p -> c); break;}
                x = x -> fail;
            }
            if (!(p -> fail)) p -> fail = root;
        }
    }

    void search(char *T)
    {
        int n = strlen(T), i = 0; // 文本串长度和当前比对位置
        bool is_end = false;
        node *p = root;
        while (i < n)
        {
            if (p -> check(T[i])){p = p -> next(T[i]); i++;}
            else if (is_end){i -= (p -> depth); is_end = false; p = root;}
            else p = p -> fail;
            if (!p){i++; if (is_end) i -= (1 + p -> depth); p = root;}
            if (p -> update()) is_end = true;
        }
    }
};

char Ps[65536][2048];
char T[134217728];

int main()
{
    acm t;

    int m; scanf("%d", &m);
    for (int i = 0; i < m; i++) scanf("%s", Ps[i]);
    for (int i = 0; i < m; i++) t.insert(Ps[i]);
    t.buildF();

    scanf("%s", T);
    t.search(T);

    for (int i = 0; i < m; i++) printf("%d\n", t.patterns[i] -> num);

    return 0;
}
