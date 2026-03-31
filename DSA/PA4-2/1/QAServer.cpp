#include "QAServer.h"
#include <cstring>

// 对模式串构建Bad Charactor Shift表
// 画家算法
int* build_BC(char *P)
{
    int *bc = new int[256]; // 字符集更大的时候需要考虑使用Bitmap
    for (int j = 0; j < 256; j++) bc[j] = -1;
    for (int m = strlen(P), j = 0; j < m; j++) bc[(int)P[j]] = j;
    return bc;
}

// 字符串匹配算法，返回最终的匹配位置
// BM算法
// 可使用GS表进一步优化
int match_BM(char *P, char *T)
{
    int *bc = build_BC(P);
    int n = strlen(T), i = 0;
    int m = strlen(P);
    while (n >= i + m)
    {
        int j = m - 1;
        while (P[j] == T[i + j]) if (--j < 0) break;
        if (j < 0) break;
        else i += (1 > (j - bc[(int)T[i + j]])) ? 1 : (j - bc[(int)T[i + j]]);
    }
    delete[] bc;
    return i;
}

int GetAnswer(char* text, char* question)
{
    int re0 = match_BM(question, text);
    if (strlen(text) >= re0 + strlen(question)) return re0;
    else return strlen(text);
}
