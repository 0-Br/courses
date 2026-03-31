#include <cstdio>

#define DEFAULT_CAPACITY 1024//默认初始容量设为1024
#define Rank unsigned int//秩为无符号整型

template <typename T>
class Vector
{
private:
    Rank _size;//数据规模
    Rank _capacity;//数据容量
    T *_elem;//数据储存区

protected:
    //复制数组区间[lo, hi)
    void copyfrom(const T *source, Rank lo, Rank hi)
    {
        _size = hi - lo;
        if (((hi - lo) << 1) > DEFAULT_CAPACITY) _capacity = ((hi - lo) << 1);
        else _capacity = DEFAULT_CAPACITY;
        _elem = new T[_capacity];
        for (Rank i = 0; i < hi - lo; i++) _elem[i] = source[lo + i];
    }

    //加倍扩容算法
    void expand()
    {
        if (_size < _capacity) return;
        T *oldelem = _elem;
        _capacity <<= 1;
        _elem = new T[_capacity];
        for (Rank i = 0; i < _size; i++) _elem[i] = oldelem[i];
        delete[] oldelem;
    }
    //收缩算法
    void shrink()
    {
        if ((DEFAULT_CAPACITY << 1) > _capacity) return;
        if ((_size << 2) > _capacity) return;//以25%为界决定是否收缩
        T *oldElem = _elem;
        _capacity >>= 1;
        _elem = new T[_capacity];
        for (Rank i = 0; i < _size; i++ ) _elem[i] = oldElem[i];
        delete[] oldElem;
    }

    //归并算法
    void merge(Rank lo, Rank mid, Rank hi)
    {
        Rank i = 0, j = 0, k = 0;
        T *A = _elem + lo;
        Rank lb = mid - lo;
        T *B = new T[lb];
        for (Rank i = 0;i < lb; i++) B[i] = A[i];
        Rank lc = hi - mid;
        T *C = _elem + mid;

        while ((j < lb) && (k < lc)) A[i++] = (B[j] <= C[k]) ? B[j++] : C[k++];
        while (j < lb) A[i++] = B[j++];
        delete[] B;
    }

public:
    //构造一个容量为c的未初始化向量，若不指定c则默认为DEFAULT_CAPACITY
    Vector(Rank c = DEFAULT_CAPACITY)
    {
        _size = 0;
        _capacity = c;
        _elem = new T[_capacity];
    }
    //构造一个规模为s的向量，并全部初始化为e
    Vector(Rank s, T e)
    {
        _size = s;
        if ((s << 1) > DEFAULT_CAPACITY) _capacity = (s << 1);
        else _capacity = DEFAULT_CAPACITY;
        _elem = new T[_capacity];
        for (Rank i = 0; i < s; i++) _elem[i] = e;
    }
    //基于数组区间[lo, hi)构造一个向量
    Vector(const T* source, Rank lo, Rank hi){copyfrom(source, lo, hi);}
    //基于向量区间[lo, hi)构造一个向量
    Vector(const Vector<T>& source, Rank lo, Rank hi){copyfrom(source._elem, lo, hi);}
    //复制向量
    Vector(const Vector<T>& source){copyfrom(source._elem, 0, source._size);}

    //析构函数
    ~Vector(){delete[] _elem;}

    //报告当前向量的规模
    Rank size() const{return _size;}
    //报告当前向量的容量
    Rank capacity() const{return _capacity;}

    //重载[]运算符，按mod取秩
    T& operator[] (Rank r)
    {
        while (r < 0) r += _size;
        while (r >= _size) r -= _size;
        return _elem[r];
    }
    //重载[]运算符，只读，按mod取秩
    const T& operator[] (Rank r) const
    {
        while (r < 0) r += _size;
        while (r >= _size) r -= _size;
        return _elem[r];
    }

    //插入操作，在秩r位置插入元素e，已有元素依次后移
    //从后往前操作，减小空间复杂度
    void insert(Rank r, T const& e)
    {
        expand();
        for (Rank i = _size; i > r; i--) _elem[i] = _elem[i - 1];
        _elem[r] = e;
        _size++;
    }

    //区间删除操作，删除[lo, hi)间的元素，已有元素依次前移
    void remove(Rank lo, Rank hi)
    {
        if (lo == hi) return;//处理退化情况
        while (hi < _size)
        {
            _elem[lo] = _elem[hi];
            lo++;hi++;
        }
        _size = lo;
        shrink();
    }
    //单元素删除操作，返回被删除的元素，已有元素依次前移
    T remove(Rank r)
    {
        T e = _elem[r];
        remove(r, r + 1);
        shrink();
        return e;
    }

    //只允许对递增向量使用
    //去除向量中所有重复的元素，返回删除的元素个数
    //采用双指针法提高效率
    Rank uniquify()
    {
        Rank i = 0;
        Rank oldsize = _size;
        for (Rank j = 1; j < _size; j++)
        {
            if (_elem[i] != _elem[j])
            {
                i++;
                _elem[i] = _elem[j];
            }
        }
        _size = i + 1;
        shrink();
        return (oldsize - _size);
    }

    //只允许对递增向量使用
    //二分查找，在[lo, hi)中搜索值target，返回其秩
    //默认为在向量整体中查找
    //若不存在target，返回向左最近的元素的秩
    //若存在多个target，返回最右的一个的秩
    Rank binsearch(T const& target, Rank lo, Rank hi) const
    {
        while (lo < hi)
        {
            Rank mid = (hi + lo) >> 1;
            if (target < _elem[mid]) hi = mid;
            else lo = mid;
        }
        return lo;
    }
    Rank binsearch(T const& target) const
    {
        Rank lo = 0;Rank hi = _size;
        while (hi - lo > 1)
        {
            Rank mid = (hi + lo) >> 1;
            if (target < _elem[mid]) hi = mid;
            else lo = mid;
        }
        return lo;
    }

    //归并排序算法
    void mergeSort(Rank lo, Rank hi)
    {
        if (hi - lo < 2) return;
        Rank mid = (lo + hi) / 2;
        mergeSort(lo, mid);mergeSort(mid, hi);
        merge(lo, mid, hi);
    }
};

struct node
{
    int lo, hi;//节点区间：[Vs[lo], Vs[hi])；注意左闭右开
    node *parent;//父节点位置
    node *lc, *rc;//子节点位置
    int mc;//归并计数
    int mid;//中心分割点

    //构造函数
    node(int lo, int hi, node *parent = NULL):lo(lo), hi(hi), parent(parent), lc(NULL), rc(NULL), mc(0){mid = (hi + lo) / 2;}

    //对半分裂自身区间，得到子节点
    void split()
    {
        if (hi - lo > 1)
        {
            lc = (mid > lo) ? new node(lo, mid, this) : NULL;
            rc = (hi > mid) ? new node(mid, hi, this) : NULL;
        }
        else
        {
            lc = NULL;
            rc = NULL;
        }
    }
};

class Stree
{
private:
    node* _root;

    //递归，初始化
    void init(node *x)
    {
        x -> split();
        if (x -> lc) init(x -> lc);
        if (x -> lc) init(x -> rc);
    }

    //递归，添加线段并更新计数
    void add(int begin, int end, node *x)
    {
        if ((begin <= (x -> lo)) && ((x -> hi) <= end))
        {
            (x -> mc)++;
            return;
        }
        if ((x -> lc) && (begin < x -> mid)) add(begin, end, x -> lc);
        if ((x -> rc) && (x -> mid < end)) add(begin, end, x -> rc);
    }

public:
    //构造函数
    Stree(int min, int max)
    {
        _root = new node(min, max);
        init(_root);
    }

    //添加一条线段，更新计数
    void insertS(int begin, int end){add(begin, end, _root);}

    //查询
    int calculate(int itv)
    {
        node* x = _root;
        int re0 = 0;
        while (x)
        {
            re0 += x -> mc;
            if (itv < x -> mid) x = x -> lc;
            else x = x -> rc;
        }
        return re0;
    }
};

bool array_op[320000];
int array_lo[320000];
int array_hi[320000];
int array_q[320000];
Vector<int> Vs;//区间点集

int main()
{
    int n, m;
    scanf("%d %d", &n, &m);

    //数据输入
    int len_H = 0, len_Q = 0;
    for (int i = 0; i < m; i++)
    {
        char op;
        scanf("\n%c", &op);
        if (op == 'H')
        {
            array_op[i] = true;
            scanf("%d %d", &array_lo[len_H], &array_hi[len_H]);;
            array_lo[len_H]--;
            Vs.insert(Vs.size(), array_lo[len_H]);
            Vs.insert(Vs.size(), array_hi[len_H]);
            len_H++;
        }
        if (op == 'Q')
        {
            array_op[i] = false;
            scanf("%d", &array_q[len_Q]);
            array_q[len_Q]--;
            len_Q++;
        }
    }
    Vs.insert(Vs.size(), 0);
    Vs.insert(Vs.size(), __INT_MAX__);
    Vs.mergeSort(0, Vs.size());
    Vs.uniquify();

    Stree* pt = new Stree(0, Vs.size() - 1);

    int i_H = 0, i_Q = 0;
    for (int i = 0; i < m; i++)
    {
        if (array_op[i])
        {
            int begin = Vs.binsearch(array_lo[i_H]);
            int end = Vs.binsearch(array_hi[i_H]);
            pt -> insertS(begin, end);
            i_H++;
        }
        else
        {
            int itv = Vs.binsearch(array_q[i_Q]);
            printf("%d\n", pt -> calculate(itv));
            i_Q++;
        }
    }

    return 0;
}