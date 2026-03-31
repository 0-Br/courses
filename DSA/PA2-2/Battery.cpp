#include <cstdio>
#define Rank unsigned int//秩为无符号整型

//列表的节点结构体
template <typename T>
struct node
{
    T data;//数据
    node<T> *pred;//指向前驱
    node<T> *succ;//指向后继

    //默认构造函数
    node(){};
    //节点的初始化构造函数，默认前后均为NULL
    node(T e, node<T> *p = NULL, node<T> *s = NULL):data(e), pred(p), succ(s){};

    //插入前驱，返回一个指向插入前驱的指针
    node<T>* insert_p(const T& e)
    {
        node<T> *oldpred = pred;
        pred = new node<T>(e);
        pred -> pred = oldpred;
        pred -> succ = this;
        pred -> pred -> succ = pred;
        return pred;
    }
    //插入后继，返回一个指向插入后继的指针
    node<T>* insert_s(const T& e)
    {
        node<T> *oldsucc = succ;
        succ = new node<T>(e);
        succ -> succ = oldsucc;
        succ -> pred = this;
        succ -> succ -> pred = succ;
        return succ;
    }
};

template <typename T>
class List
{
private:
    Rank _size;//数据规模
    node<T> *header, *trailer;//头尾哨兵

protected:
    //构造时的初始化函数，将得到一个只有头尾哨兵的列表
    void init()
    {
        _size = 0;
        header = new node<T>;
        trailer = new node<T>;
        header -> pred = NULL;
        header -> succ = trailer;
        trailer -> succ = NULL;
        trailer -> pred = header;
    }

public:
    //（仅测试，在T为long long时可用）打印列表
    void print() const
    {
        printf("[");
        node<T> *p = first();
        for (Rank i = 0; i < _size; i++)
        {
            printf("%d, ", (int)(p -> data));
            p = p -> succ;
        }
        printf("]\n");
    }

    //报告当前列表的规模
    Rank size() const{return _size;}
    //返回首位指针
    node<T>* first() const{return header -> succ;}
    //返回末位指针
    node<T>* last() const{return trailer -> pred;}
    //判断列表是否为空
    bool empty() const{return !_size;}

    //获得一个指向秩为r的元素的指针，按mod取秩
    //效率不高，慎用
    node<T>* gp(Rank r) const
    {
        while (r < 0) r += _size;
        while (r >= _size) r -= _size;
        node<T> *p = first();
        for (Rank i = 0; i < r; i++) p = p -> succ;
        return p;
    }

    //交换p，q指向的元素值，复杂度较插入低
    void exchange(node<T> *p, node<T> *q)
    {
        T temp = q -> data;
        q -> data = p -> data;
        p -> data = temp;
    }

    //插入操作，在p处插入元素e，已有元素依次后移，默认在末尾插入
    //返回指向新插入元素的指针
    //常数时间教大，建议仅在增加节点时使用
    node<T>* insert(const T& e, node<T> *p)
    {
        _size++;
        return (p -> insert_p(e));//前插入
    }
    node<T>* insert(const T& e)
    {
        node<T> *p = trailer;
        _size++;
        return (p -> insert_p(e));//前插入
    }

    //单元素删除操作，删除p指向的元素，返回被删除的元素
    T remove(node<T> *p)
    {
        _size--;
        T e = p -> data;
        p -> pred -> succ = p -> succ;
        p -> succ -> pred = p -> pred;
        delete p;
        return e;
    }
    //区间删除操作，删除[p, p + r)间的元素
    void remove(node<T> *p, Rank r)
    {
        _size -= r;
        node<T> *endp = p;
        for (Rank i = 0; i < r; i++) endp = endp -> succ;
        p -> pred -> succ = endp;
        endp -> pred = p -> pred;
        endp = endp -> pred;
        for (Rank i = 0; i < r; i++)
        {
            node<T> *tempp = p;
            p = p -> succ;
            delete tempp;
        }
    }

    //列表清空
    //返回列表清空前的规模
    Rank clear()
    {
        Rank oldsize = _size;
        remove(first(), _size);
        return oldsize;
    }

    //构造一个空列表
    List(){init();}
    //构造一个列表，规模为s，全部初始化为e
    List(Rank s, T e)
    {
        init();
        for (Rank i = 0; i < s; i++) insert(e);
    }
    //基于数组区间[lo, hi)构造一个列表
    List(const T *source, Rank lo, Rank hi)
    {
        init();
        for (Rank i = lo; i < hi; i++) insert(source[i]);
    }
    //基于列表区间[p, p + n)构造一个列表
    List(node<T> *p_source, Rank n)
    {
        init();
        for (Rank i = 0; i < n; i++)
        {
            insert(p_source -> data);
            p_source = p_source -> succ;
        }
    }
    //复制列表
    List(const List<T>& source)
    {
        init();
        node<T> *p_source = source.first();
        for (Rank i = 0; i < source._size; i++)
        {
            insert(p_source -> data);
            p_source = p_source -> succ;
        }
    }

    //析构函数
    ~List()
    {
        clear();
        delete header;
        delete trailer;
    }

    //重载[]运算符
    T& operator[] (Rank r){return gp(r) -> data;}
    //重载[]运算符，只读
    const T& operator[] (Rank r) const{return gp(r) -> data;}

    //在区间[p, p + n)中查找元素target，返回指向该元素的指针
    //默认在列表全体中查找，此情况效率较高（常数），可优化
    //若有多个目标，返回最后一个，若查找失败，返回NULL
    node<T>* find(const T& target, node<T> *p, Rank n) const
    {
        node<T> *re0 = NULL;
        for (Rank i = 0; i < n; i++)
        {
            if (p -> data == target) re0 = p;
            p = p -> succ;
        }
        return re0;
    }
    node<T>* find(const T& target) const
    {
        node<T> *p = last();
        for (Rank i = 0; i < _size; i++)
        {
            if (p -> data == target) return p;
            p = p -> pred;
        }
        return NULL;
    }

    //选取区间[p, p + n)中最大的元素，返回指向该处的指针
    node<T>* selectMax(node<T> *p, Rank n) const
    {
        node<T> *pMax = p;
        for (Rank i = 1; i < n; i++)
        {
            p = p -> succ;
            if ((p -> data) >= (pMax -> data)) pMax = p;
        }
        return pMax;
    }

    //列表去重，返回删除的元素个数
    Rank deduplicate()
    {
        Rank oldsize = _size;
        node<T> *p = last();
        for (Rank r = 0; p != header; p = p -> pred)
        {
            if (node<T> *q = find(p -> data, p -> succ, r)) remove(q);
            else r++;
        }
        return oldsize - _size;
    }

    //有序列表查找，不能使用二分查找加速
    //默认在列表全体中查找，此情况效率较高（常数），可优化
    //返回不大于目标的最靠后元素的指针
    node<T>* search(const T& target, node<T> *p, Rank n) const
    {
        node<T> *re0 = NULL;
        for (Rank i = 0; i < n; i++)
        {
            if (p -> data <= target)
            {
                re0 = p;
                p = p -> succ;
            }
            else return re0;
        }
        return NULL;
    }
    node<T>* search(const T& target) const
    {
        node<T> *p = last();
        if (target > p -> data) return NULL;
        for (Rank i = 0; i < _size; i++)
        {
            if (p -> data <= target) return p;
            p = p -> pred;
        }
        return NULL;
    }

    //有序列表去重，返回删除的元素个数
    //采用检查临近元素的方法，可优化
    Rank uniquify()
    {
        if (_size < 2) return 0;//排除平凡情况
        Rank oldsize = _size;
        node<T> *p = first();
        node<T> *q;
        while (1)
        {
            q = p -> succ;
            if (trailer == q) break;
            if ((p -> data) != (q -> data)) p = q;
            else remove(q);
        }
        return oldsize - _size;
    }

    //选择排序算法
    //对[p, p + r)间的元素排序，修改原值
    void selectionSort(node<T> *p, Rank n)
    {
        node<T> *tail = p;
        for (Rank i = 1; i < n; i++) tail = tail -> succ;
        while (1 < n)
        {
            node<T> *pMax = selectMax(p, n);
            exchange(pMax, tail);
            tail = tail -> pred;
            n--;
            print();
        }
    }
};

//基于列表和堆实现的队列
template <typename T>
class Queue:public List<T>
{
private:
    //维护两个列表，分别记录到队尾的最大值的位置和长度信息
    List<T> pair_p;
    List<Rank> pair_r;

public:
    //构建一个空队列
    Queue(){};

    //入队
    void enqueue(const T& e)
    {
        node<T> *pp = pair_p.insert(e);
        node<Rank> *pr = pair_r.insert(1);
        node<Rank> *endr = pr;
        pp = pp -> pred;
        pr = pr -> pred;
        while (((pp -> data) < e) && ((pp -> pred) != NULL))
        {
            pp = pp -> pred;
            pr = pr -> pred;
            pair_p.remove(pp -> succ);
            (endr -> data) += pair_r.remove(pr -> succ);
        }
        List<T>::insert(e);
    }
    //出队
    T dequeue()
    {
        (pair_r.first() -> data)--;
        if (pair_r.first() -> data == 0)
        {
            pair_p.remove(pair_p.first());
            pair_r.remove(pair_r.first());
        }
        return List<T>::remove(List<T>::first());
    }
    //访问队首，为只读接口
    const T& front() const
    {
        return (List<T>::first() -> data);
    }
    //获取队列中的最大元素，只读
    const T& getMax() const
    {
        return (pair_p.first() -> data);
    }
};

int nothave(int t1, int t2)
{
    if (t1 == 0) return ((t2 == 1) ? 2 : 1);
    if (t1 == 1) return ((t2 == 2) ? 0 : 2);
    if (t1 == 2) return ((t2 == 0) ? 1 : 0);
    return -1;
}

int main()
{
    Queue<int> stores[3];//记录充电宝id的队列

    int n;//初始桌上的充电宝个数
    scanf("%d", &n);
    for (int i = 0; i < n; i++)
    {
        int t1, t2;
        scanf("%d %d", &t1, &t2);
        stores[nothave(t1, t2)].enqueue(i + 1);
    }

    int m;//事件数
    int backnum = 0;//回归的充电宝数
    scanf("%d", &m);
    for (int i = 0; i < m; i++)
    {
        int op;
        scanf("%d", &op);
        if (op == 0)//归还充电宝
        {
            backnum++;
            int t1, t2;
            scanf("%d %d", &t1, &t2);
            stores[nothave(t1, t2)].enqueue(n + backnum);
        }
        if (op == 1)//借用充电宝
        {
            int tx;
            scanf("%d", &tx);
            int minid = __INT_MAX__;int s = 3;
            for (int i = 0; i < 3; i++)
            {
                if ((i == tx) || (stores[i].empty())) continue;
                if (minid > stores[i].front())
                {
                    minid = stores[i].front();
                    s = i;
                }
            }
            if (s == 3) printf("%d\n", -1);
            else printf("%d\n", stores[s].dequeue());
        }
    }
    return 0;
}