#include<stdio.h>

template <typename T> class Vector
{
protected:
    int _size;//数据规模
    int _capacity;//数据容量
    T* _elem;//数据储存区

    //复制数组区间[lo, hi])
    void copyfrom(T const* source, int lo, int hi)
    {
        _size = 0;
        _capacity = 2 * (hi - lo);
        _elem = new T[_capacity];
        for (int i = 0; i < hi - lo; i++){_elem[i] = source[lo + i];_size++;}
    }

    //加倍扩容算法
    void expand()
    {
        if (_size < _capacity) return;
        T* oldelem = _elem;
        _elem = new T[_capacity * 2];
        for (int i = 0; i < _size; i++){_elem[i] = oldelem[i];}
        delete[] oldelem;
    }

public:
    //构造一个容量为c的未初始化向量
    Vector(int c)
    {
        _size = 0;
        _capacity = c;
        _elem = new T[_capacity];
    }
    //构造一个规模为s的向量，并全部初始化为v
    Vector(int s, T v)
    {
        _size = s;
        _capacity = 2 * s;
        _elem = new T[_capacity];
        for (int i = 0; i < s; i++){_elem[i] = v;}
    }
    //基于数组区间[lo, hi)构造一个向量
    Vector(T const* source, int lo, int hi){copyfrom(source, lo, hi);}

    //析构函数
    ~Vector(){delete[] _elem;}

    //重载[]运算符，区分const
    T& operator[](int r){return _elem[r];}
    const T& operator[](int r) const{return _elem[r];}

    //报告当前向量的规模
    int size(){return _size;}
    //报告当前向量的容量
    int capicity(){return _capacity;}

    //只允许对有序向量使用
    //使用二分查找，在向量中搜索值target，返回其秩
    //若不存在target，返回向左最近的元素的秩
    //若存在多个target，返回最右的一个的秩
    int binsearch(T target)
    {
        int lo = 0;
        int hi = _size;
        while (hi - lo > 1)
        {
            int mid = lo + (hi - lo) / 2;
            if (target < _elem[mid]) hi = mid;
            else lo = mid;
        }
        return lo;
    }
};

int main()
{
    int n, m;
    scanf("%d %d", &n, &m);
    Vector<long long> x_lines(n);
    Vector<long long> y_lines(n);
    Vector<int> results(m);
    for (int i = 0; i < n; i++){scanf("%lld %lld", &x_lines[i], &y_lines[i]);}
    for (int i = 0; i < m; i++)
    {
        long long x, y;
        scanf("%lld %lld", &x, &y);
        if (x_lines[0] * y + y_lines[0] * x < x_lines[0] * y_lines[0])
        {
            results[i] = 0;
            continue;
        }
        //二分查找
        int lo = 0;int hi = n;
        while (hi - lo > 1)
        {
            int mid = lo + (hi - lo) / 2;
            if (x_lines[mid] * y + y_lines[mid] * x < x_lines[mid] * y_lines[mid]) hi = mid;
            else lo = mid;
        }
        results[i] = lo + 1;
    }
    for (int i = 0; i < m; i++) printf("%d\n", results[i]);
    return 0;
}