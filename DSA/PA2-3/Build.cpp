#include <cstdio>

#define DEFAULT_CAPACITY 16//默认初始容量设为8
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

    //重载==运算符
    bool operator== (const Vector<T>& V) const
    {
        if (_size != V._size) return false;
        else
        {
            for (Rank i = 0; i < V._size; i++)
            {
                if (_elem[i] != V._elem[i]) return false;
            }
            return true;
        }
    }
    //重载!=运算符
    bool operator!= (const Vector<T>& V) const
    {
        if (_size != V._size) return true;
        else
        {
            for (Rank i = 0; i < V._size; i++)
            {
                if (_elem[i] != V._elem[i]) return true;
            }
            return false;
        }
    }

    //重载<运算符，只允许对有序向量使用，先大即大，先长即大
    bool operator< (const Vector<T>& V) const
    {
        if (_size < V._size) return true;
        if (_size > V._size) return false;
        for (Rank i; (i < _size) && (i < V._size); i++)
        {
            if (_elem[i] < V._elem[i]) return true;
            if (_elem[i] > V._elem[i]) return false;
        }
        if (_size == V._size) return false;
    }
    //重载>运算符，只允许对有序向量使用，先大即大，先长即大
    bool operator> (const Vector<T>& V) const
    {
        if (_size > V._size) return true;
        if (_size < V._size) return false;
        for (Rank i; (i < _size) && (i < V._size); i++)
        {
            if (_elem[i] > V._elem[i]) return true;
            if (_elem[i] < V._elem[i]) return false;
        }
        if (_size == V._size) return false;
    }

    //重载+运算符，只允许对两相同规模的向量使用
    Vector<T> operator+ (const Vector<T>& V) const
    {
        T* array = new T[_size];
        for (Rank i; i < _size; i++) array[i] = _elem[i] + V._elem[i];
        Vector<T> newV(array, 0, _size);
        return newV;
    }
    //重载-运算符，只允许对两相同规模的向量使用
    Vector<T> operator- (const Vector<T>& V) const
    {
        T* array = new T[_size];
        for (Rank i; i < _size; i++) array[i] = _elem[i] - V._elem[i];
        Vector<T> newV(array, 0, _size);
        return newV;
    }

    //重载+=运算符
    void operator+= (const Vector<T>& V)
    {
        for (Rank i; i < _size; i++) _elem[i] += V._elem[i];
    }
    //重载-=运算符
    void operator-= (const Vector<T>& V)
    {
        for (Rank i; i < _size; i++) _elem[i] -= V._elem[i];
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

    //顺序查找，在[lo, hi)中搜索值target，返回其秩
    //默认为在向量整体中查找
    //若不存在target，返回0
    //若存在多个target，返回最右的一个的秩
    Rank find(T const& target) const
    {
        Rank lo = 0, hi = _size;
        while (hi > lo)
        {
            hi--;
            if (_elem[hi] == target) return hi;
        }
        return 0;
    }
    Rank find(T const& target, Rank lo, Rank hi) const
    {
        while (hi > lo)
        {
            hi--;
            if (_elem[hi] == target) return hi;
        }
        return 0;
    }

    //去除向量中所有重复的元素，返回删除的元素个数
    Rank deduplicate()
    {
        Rank oldsize = _size;
        for (Rank i = 1; i < _size;)
        {
            if ((find(_elem[i], 0, i) == 0) && (_elem[i] != _elem[0])) i++;
            else remove(i);
        }
        shrink();
        return (oldsize - _size);
    }

    //向量反序，修改原向量值
    void reverse()
    {
        for(Rank i = 0; i < _size / 2; i++)
        {
            T temp = _elem[i];
            _elem[i] = _elem[_size - i - 1];
            _elem[_size - i - 1] = temp;
        }
    }

    //返回向量的逆序对数量，若为0则说明向量是递增向量
    Rank checkorder() const
    {
        if (_size == 1) return 0;
        Rank re0 = 0;
        for (Rank i = 0; i < _size - 1; i++)
        {
            if (_elem[i] > _elem[i + 1]) re0++;
        }
        return re0;
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
    //
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
};

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

struct treenode
{
    int data = 0;
    treenode *parent = NULL;
    Vector<treenode*> childs;

    void add_child(treenode *x)
    {
        x -> parent = this;
        childs.insert(childs.size(), x);
    }
};

int main()
{
    int N;scanf("%d", &N);
    treenode *treenodes = new treenode[N];
    for (int i = 0; i < N; i++)
    {
        treenodes[i].data = i + 1;
        int num;scanf("%d", &num);
        for (int j = 0; j < num; j++)
        {
            int id;scanf("%d", &id);
            treenodes[i].add_child(&treenodes[id - 1]);
        }
    }
    Queue<treenode*> q;
    q.enqueue(&treenodes[0]);
    while (!q.empty())
    {
        treenode *x = q.dequeue();
        printf("%d\n", x -> data);
        for (int i = 0; i < (int)((x -> childs).size()); i++) q.enqueue(x -> childs[i]);
    }
    delete[] treenodes;
    return 0;
}