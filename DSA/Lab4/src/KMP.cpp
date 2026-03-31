#include <cstdio>
#include <cstring>

// 检查字符串是否匹配成功
bool is_match(char *P, char *T, int i){return (strlen(T) >= i + strlen(P));}

// 对模式串P构建next表
int* build_Next(char *P)
{
    int m = strlen(P), j = 0;
    int *next = new int[m + 1];
    int t = next[0] = -1; // next表首项必然为-1
    while (j < m)
    {
        if ((t < 0) || (P[t] == P[j]))
        {
            if (P[++t] != P[++j]) next[j] = t; // 避免重复犯错
            else next[j] = next[t];
        }
        else t = next[t];
    }
    return next;
}

// 字符串匹配算法，返回最终的匹配位置
// KMP算法
int match_KMP(char *P, char *T)
{
    int num = 0;
    int *next = build_Next(P);
    int n = strlen(T), i = 0; // 文本串长度和当前比对位置
    int m = strlen(P), j = 0; // 模式串长度和当前比对位置
    while (i < n)
    {
        if ((j < 0) || T[i] == P[j]){i++; j++;}
        else j = next[j]; // 文本串始终不回退
        if (j == m){num++; j = next[j];}
    }
    delete[] next;
    return num;
}

char Ps[65536][2048];
char T[134217728];

int main()
{
    int m; scanf("%d", &m);
    for (int i = 0; i < m; i++) scanf("%s", Ps[i]);

    scanf("%s", T);

    for (int i = 0; i < m; i++) printf("%d\n", match_KMP(Ps[i], T));

    return 0;
}
