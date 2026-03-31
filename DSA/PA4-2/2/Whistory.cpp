#include <cstdio>
#include <cstring>

template <typename T>
struct Cleaner
{
    static void clean(T x){};
};
template <typename T>
struct Cleaner<T*>
{
    static void clean(T* x){if (x) delete x;}
};
template <typename T>
void release(T x){Cleaner<T>::clean(x);}

// 元组模板类
template <typename T1, typename T2>
struct Tuple
{
    T1 elem_1;
    T2 elem_2;

    // 默认构造
    Tuple(T1 e1 = T1(), T2 e2 = T2()) : elem_1(e1), elem_2(e2){};
    // 复制构造
    Tuple(const Tuple<T1, T2>& t) : elem_1(t.elem_1), elem_2(t.elem_2){};

    // 重载比较运算符
    bool operator< (const Tuple<T1, T2>& t) const
    {
        if (elem_1 == t.elem_1) return (elem_2 < t.elem_2);
        else return (elem_1 < t.elem_1);
    }
    bool operator> (const Tuple<T1, T2>& t) const
    {
        if (elem_1 == t.elem_1) return (elem_2 > t.elem_2);
        else return (elem_1 > t.elem_1);
    }
    bool operator<= (const Tuple<T1, T2>& t) const
    {
        if (elem_1 == t.elem_1) return (elem_2 <= t.elem_2);
        else return (elem_1 < t.elem_1);
    }
    bool operator>= (const Tuple<T1, T2>& t) const
    {
        if (elem_1 == t.elem_1) return (elem_2 >= t.elem_2);
        else return (elem_1 > t.elem_1);
    }
    bool operator== (const Tuple<T1, T2>& t) const
    {
        if ((elem_1 == t.elem_1) && (elem_2 == t.elem_2)) return true;
        return false;
    }
    bool operator!= (const Tuple<T1, T2>& t) const
    {
        if ((elem_1 == t.elem_1) && (elem_2 == t.elem_2)) return false;
        return true;
    }
};

// 二叉树的节点结构体
template <typename T>
struct binode
{
    T data; // 数据
    binode<T> *parent; // 父节点位置
    binode<T> *lc, *rc; // 子节点位置

    int height; // 高度
    int size; // 以自身为根的子树规模
    bool color; // 节点颜色，红0黑1，仅在红黑树中维护

    // 默认构造函数
    binode() : parent(NULL), lc(NULL), rc(NULL), height(0), size(1), color(false){};
    // 初始化构造函数
    binode(T e, binode<T> *parent = NULL, binode<T> *lc = NULL, binode<T> *rc = NULL, int height = 0, int size = 1, bool color = false)
        : data(e), parent(parent), lc(lc), rc(rc), height(height), size(size), color(color){};

    // 插入左孩子，返回左孩子的位置
    // 此处不负责维护
    binode<T>* insert_lc(const T& e){return lc = new binode(e, this);}
    // 插入右孩子，返回右孩子的位置
    // 此处不负责维护
    binode<T>* insert_rc(const T& e){return rc = new binode(e, this);}

    // 返回中序遍历意义下当前节点的直接后继
    // 实际上是搜索最左的右后代，然后搜索最左的右祖先
    binode<T>* succ()
    {
        binode<T> *x = this;
        if (has_rc())
        {
            x = rc;
            while (x -> has_lc()) x = x -> lc;
        }
        else
        {
            while (x -> is_rc()) x = x -> parent;
            x = x -> parent;
        }
        return x;
    }
    // 返回中序遍历意义下当前节点的直接前驱
    // 实际上是搜索最右的左后代，然后搜索最右的左祖先
    binode<T>* pred()
    {
        binode<T> *x = this;
        if (has_lc())
        {
            x = lc;
            while (x -> has_rc()) x = x -> lc;
        }
        else
        {
            while (x -> is_lc()) x = x -> parent;
            x = x -> parent;
        }
        return x;
    }

    // 中序遍历
    // 范围为以本节点为根的子树
    template <typename VST>
    void trav_in(const VST& visit)
    {
        binode<T> *x = this;
        while (x -> has_lc()) x = x -> lc; // 转移到中序遍历起点处
        while (x)
        {
            visit(x -> data);
            x = x -> succ();
        }
    }

    //是否为根
    bool is_root(){return !parent;}
    //是否有左孩子
    bool has_lc(){return lc;}
    //是否有右孩子
    bool has_rc(){return rc;}
    //是否为左孩子
    bool is_lc(){return (!is_root()) && (this == parent -> lc);}
    //是否为右孩子
    bool is_rc(){return (!is_root()) && (this == parent -> rc);}

    //返回兄弟
    binode<T>* sibling()
    {
        if (is_root()) return NULL;
        return is_lc() ? parent -> rc : parent -> lc;
    }
    //返回舅舅
    binode<T>* uncle()
    {
        if (is_root()) return NULL;
        return sibling(parent);
    }
};

// 二叉树模板类
template <typename T>
class Bitree
{
private:
    // 递归统计后代总数
    // 效率较低，慎用，建议改用维护的size值
    // 中序遍历实例
    int cal_size(binode<T> *x)
    {
        int re0 = 1;
        if (x -> has_lc()) re0 += cal_size(x -> lc);
        if (x -> has_rc()) re0 += cal_size(x -> rc);
        return re0;
    }

    // remove()中使用的递归删除操作
    // 返回删除的节点数
    // 后序遍历实例
    int removeAt(binode<T> *x)
    {
        if (!x) return 0; // 递归基
        if (x -> is_root()){_root = NULL;} // 若删除根，将根置空
        int n = 1 + removeAt(x -> lc) + removeAt(x -> rc);
        release(x -> data); release(x);
        return n;
    }

protected:
    int _size; // 树的规模
    binode<T> *_root; // 根节点
    binode<T> *_head; // 保护节点

    // 空树高度保护（-1）
    // 在红黑树中需要重写
    virtual int stature(binode<T> *x){return ((x) ? x -> height : -1);}

    // 空树规模保护
    int scale(binode<T> *x){return ((x) ? x -> size : 0);}

    // 更新节点x的高度和子树规模
    // 勤奋策略，及时更新
    // 根据具体树的种类需要重写
    virtual void update(binode<T> *x)
    {
        int hi_max = (stature(x -> lc) > stature(x -> rc)) ? stature(x -> lc) : stature(x -> rc);
        x -> height = hi_max + 1;
        x -> size = scale(x -> lc) + scale(x -> rc) + 1;
    }
    // 更新节点x及祖先的高度和子树规模
    void updateAbove(binode<T> *x)
    {
        while (x)
        {
            update(x);
            x = x -> parent;
        }
    }

    // 交换节点数据
    // 需要构造临时变量，存在优化空间
    void swap(binode<T> *x_a, binode<T> *x_b)
    {
        T temp = x_a -> data;
        x_a -> data = x_b -> data;
        x_b -> data = temp;
    }

    // 返回x的来自父亲的引用
    // 根节点默认返回NULL
    binode<T>*& from(binode<T>* x)
    {
        if (x -> is_root()) return _head -> rc;
        else return (x -> is_lc()) ? (x -> parent -> lc) : (x -> parent -> rc);
    }

public:
    // 默认构造函数
    Bitree() : _size(0), _root(NULL){_head = new binode<T>();};
    // 析构函数
    ~Bitree()
    {
        if (!empty()) remove(_root);
        release(_head -> data); release(_head);
    }

    // 报告当前树的规模
    int size(){return _size;}
    // 获取树根
    binode<T>* root(){return _root;}
    // 判断树是否为空
    bool empty(){return !_root;}

    // 插入根节点
    // 返回指向新插入节点的指针
    binode<T>* insert(const T& e)
    {
        if (empty())
        {
            _size = 1;
            _root = new binode<T>(e);
            _head -> rc = _root;
            return _root;
        }
        else return _root;
    }
    // 插入新节点作为左孩子
    // 返回指向新插入节点的指针
    binode<T>* insert(const T& e, binode<T> *x)
    {
        if (!(x -> has_lc()))
        {
            _size++;
            x -> insert_lc(e);
            updateAbove(x);
            return x -> lc;
        }
        else return x;
    }
    // 插入新节点作为右孩子
    // 返回指向新插入节点的指针
    binode<T>* insert(binode<T> *x, const T& e)
    {
        if (!(x -> has_rc()))
        {
            _size++;
            x -> insert_rc(e);
            updateAbove(x);
            return x -> rc;
        }
        else return x;
    }

    // 递归删除x处的节点及其后代
    // 返回删除节点的数量
    int remove(binode<T> *x)
    {
        from(x) = NULL; // 与父节点切断
        updateAbove(x -> parent);
        int n = removeAt(x); _size -= n;
        return n;
    }

    //从根节点开始，作中序遍历
    template <typename VST>
    void trav_in(const VST& visit){if (!empty()) _root -> trav_in(visit);}
};

// 二叉搜索树模板类
template <typename T>
class BST : protected Bitree<T>
{
protected:
    binode<T> *_hot; // 游标，总是指向命中节点的父亲

    // 为节点连接左子树
    void attach_l(binode<T> *tree, binode<T> *p){p -> lc = tree; if (tree) tree -> parent = p;}
    // 为节点连接右子树
    void attach_r(binode<T> *p, binode<T> *tree){p -> rc = tree; if (tree) tree -> parent = p;}

    // 3+4重整
    // 返回重整后子树的根节点
    binode<T>* connect_34(binode<T> *a, binode<T> *b, binode<T> *c, binode<T> *T0, binode<T> *T1, binode<T> *T2, binode<T> *T3)
    {
        attach_l(T0, a); attach_r(a, T1);
        Bitree<T>::update(a);
        attach_l(T2, c); attach_r(c, T3);
        Bitree<T>::update(c);
        b -> lc = a; a -> parent = b;
        b -> rc = c; c -> parent = b;
        Bitree<T>::update(b);
        return b;
    }

    // 旋转操作
    // 返回旋转后子树的根节点位置
    binode<T>* rotateAt(binode<T>* v)
    {
        binode<T> *p = v -> parent; // 父
        binode<T> *g = p -> parent; // 祖父
        if (p -> is_lc())
        {
            if (v -> is_lc()) // zig-zig
            {
                p -> parent = g -> parent;
                if (g -> is_root()) Bitree<T>::_root = p; // 若基于根旋转，需重设根的位置
                return connect_34(v, p, g, v -> lc, v -> rc, p -> rc, g -> rc);
            }
            else // zig-zag
            {
                v -> parent = g -> parent;
                if (g -> is_root()) Bitree<T>::_root = v; // 若基于根旋转，需重设根的位置
                return connect_34(p, v, g, p -> lc, v -> lc, v -> rc, g -> rc);
            }
        }
        else
        {
            if (v -> is_rc())//zag-zag
            {
                p -> parent = g -> parent;
                if (g -> is_root()) Bitree<T>::_root = p; // 若基于根旋转，需重设根的位置
                return connect_34(g, p, v, g -> lc, p -> lc, v -> lc, v -> rc);
            }
            else//zag-zig
            {
                v -> parent = g -> parent;
                if (g -> is_root()) Bitree<T>::_root = v; // 若基于根旋转，需重设根的位置
                return connect_34(g, v, p, g -> lc, v -> lc, v ->rc, p -> rc);
            }
        }
    }

    // 删除操作
    // 返回删除后接替者的位置
    binode<T>* removeAt(binode<T>*& x)
    {
        binode<T> *w = x; // 实际被删除的节点
        binode<T> *succ = NULL; // 实际被删除节点的接替
        if (!(x -> has_lc())){x = x -> rc; succ = x;}
        else if (!(x -> has_rc())){x = x -> lc; succ = x;}
        else
        {
            w = w -> succ();
            Bitree<T>::swap(x, w);
            binode<T> *u = w -> parent;
            succ = w -> rc;
            ((u == x) ? u -> rc : u -> lc) = succ; // 需考虑u==x的特殊情况
        }
        _hot = w -> parent;
        if (succ) succ -> parent = _hot;
        if (w -> is_root()) // 若根节点被删除，需重设根的位置
        {
            Bitree<T>::_root = succ;
            Bitree<T>::_head -> rc = succ;
        }
        release(w -> data); release(w);
        return succ;
    }

    // 可重查找方法
    // 总是会向下查找，直到x指向空
    // 指向值不大于e的最后一个节点
    // 若需要允许关键码可重复，请将接口中调用的search方法改为本方法
    binode<T>*& get(const T& e)
    {
        // 特判退化情况
        if (Bitree<T>::empty())
        {
            _hot = NULL;
            return Bitree<T>::_head -> rc;
        }
        _hot = Bitree<T>::_root;
        while (1)
        {
            binode<T>*& x = (e < (_hot -> data)) ? (_hot -> lc) : (_hot -> rc); // 二分搜索，左小右大
            if (!x) return x;
            _hot = x;
        }
    }

public:
    // 返回游标
    binode<T>* hot(){return _hot;}

    // 循秩访问方法
    // 将节点按中序排列为一个向量，获得向量中秩为r的节点的位置
    binode<T>* rfind(int r)
    {
        if (Bitree<T>::empty()) return NULL;
        binode<T> *x = Bitree<T>::_root;
        while (1)
        {
            int mid = Bitree<T>::scale(x -> lc);
            if (r == mid) return x;
            else if (r < mid) x = x -> lc;
            else{x = x -> rc; r -= mid + 1;}
        }
    }

    // 查找方法
    // 采用二分搜索，返回目标节点位置的引用
    // 需根据BST类型的不同重写
    virtual binode<T>*& search(const T& e)
    {
        // 特判退化情况
        if (Bitree<T>::empty() || e == Bitree<T>::_root -> binode<T>::data)
        {
            _hot = NULL;
            return Bitree<T>::_head -> rc;
        }
        _hot = Bitree<T>::_root;
        while (1)
        {
            binode<T>*& x = (e < (_hot -> data)) ? (_hot -> lc) : (_hot -> rc); // 二分搜索，左小右大
            if (!x || e == (x -> data)) return x;
            _hot = x;
        }
    }

    // 插入方法
    // 返回新插入节点的位置
    // 需根据BST类型的不同重写
    virtual binode<T>* insert(const T& e)
    {
        binode<T>*& x = search(e);
        if (!x) // 仅在关键码不重复时进行插入
        {
            x = new binode<T>(e, _hot);
            if (Bitree<T>::empty()) Bitree<T>::_root = x;
            Bitree<T>::_size++;
            Bitree<T>::updateAbove(x);
        }
        return x;
    }

    // 删除方法
    // 返回布尔量，提示是否成功删除了节点
    // 需根据BST类型的不同重写
    virtual bool remove(const T& e)
    {
        binode<T>*& x = search(e);
        if (!x) return false;
        removeAt(x);
        Bitree<T>::_size--;
        Bitree<T>::updateAbove(_hot);
        return true;
    }
};

// AVL树模板类
template<typename T>
class AVLtree : protected BST<T>
{
private:
    // 平衡因子
    int balFac(binode<T> *x){return (Bitree<T>::stature(x -> lc) - Bitree<T>::stature(x -> rc));}
    // AVL平衡条件
    bool AVLbalanced(binode<T> *x){return ((-2 < balFac(x)) && (balFac(x) < 2));}

    // 平衡调整的辅助函数
    // 返回x的更高的孩子的位置
    // 若孩子等高，返回同侧孩子
    binode<T>* child_taller(binode<T> *x)
    {
        int hi_lc = Bitree<T>::stature(x -> lc);
        int hi_rc = Bitree<T>::stature(x -> rc);
        if (hi_lc > hi_rc) return x -> lc;
        else if (hi_lc < hi_rc) return x -> rc;
        else
        {
            if (x -> is_lc()) return x -> lc;
            else return x -> rc;
        }
    }

public:
    // 查找方法不变
    binode<T>*& search(const T& e){return BST<T>::search(e);}

    // 重写插入方法
    // 返回新插入节点的位置
    binode<T>* insert(const T& e)
    {
        binode<T>*& x = BST<T>::get(e);
        if (x) return x;
        binode<T> *xx = x = new binode<T>(e, BST<T>::_hot);
        if (Bitree<T>::empty()) Bitree<T>::_root = x;
        Bitree<T>::_size++;

        for (binode<T> *g = BST<T>::_hot; g; g = g -> parent)
        {
            if (!AVLbalanced(g))
            {
                binode<T>*& r = Bitree<T>::from(g);
                r = BST<T>::rotateAt(child_taller(child_taller(g)));
                Bitree<T>::updateAbove(g);
                break;
            }
            else Bitree<T>::update(g);
        }
        return xx;
    }

    // 重写删除方法
    // 返回布尔量，提示是否成功删除了节点
    bool remove(binode<T> *p)
    {
        if (!p) return false;
        binode<T>*& x = Bitree<T>::from(p);
        BST<T>::removeAt(x);
        Bitree<T>::_size--;

        for (binode<T> *g = BST<T>::_hot; g; g = g -> parent)
        {
            if (!AVLbalanced(g)) Bitree<T>::from(g) = BST<T>::rotateAt(child_taller(child_taller(g)));
            Bitree<T>::update(g);
        }
        return true;
    }
};

// 对模式串构建Bad Charactor Shift表
// 画家算法
int* buildBC(char *P)
{
    int *bc = new int[256]; // 字符集更大的时候需要考虑使用Bitmap
    for (int j = 0; j < 256; j++) bc[j] = -1;
    for (int m = strlen(P), j = 0; j < m; j++) bc[(int)P[j]] = j;
    return bc;
}

// 字符串匹配算法，返回是否匹配成功
// BM算法
// 可使用GS表进一步优化
bool match_BM(char *P, char *T)
{
    int *bc = buildBC(P);
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
    return !(strlen(T) < i + strlen(P));
}

// 散列函数，采用多项式法
int encode(char s[])
{
    int n = strlen(s);

    // 最小表示法
    int i = 0, j = 1, k = 0;
    while((i < n) && (j < n) && (k < n))
    {
        int t = s[(i + k) % n] - s[(j + k) % n] ;
        if (t == 0) k++;
        else
        {
            if (t > 0) i += k + 1;
            else j += k + 1;
            if(i == j) j++;
            k = 0;
        }
    }
    int start =  (i < j) ? i : j;

    int re0 = 0;
    for (int i = 0; i < n; i++)
    {
        re0 = (re0 << 5) | (re0 >> 27);
        re0 += s[(i + start) % n];
    }
    return re0;
}

char words[16384][2048]; // 词表
AVLtree<Tuple<int, int>> dict; // 词语字典：hash-词语id

int main()
{
    int n, m;
    scanf("%d %d", &n, &m);

    for (int k = 0; k < m; k++)
    {
        bool isfound = false;
        scanf("%s", words[k]);
        int hash = encode(words[k]);
        binode<Tuple<int, int>> *x = dict.insert(Tuple<int, int>(hash, k));
        binode<Tuple<int, int>> *xx = x -> pred();

        char T[(n << 1) + 1]; T[n << 1] = '\0';
        for (int j = 0; j < n; j++) T[j] = T[n + j] = words[(x -> data).elem_2][j];

        while ((xx) && ((xx -> data).elem_1 == hash))
        {
            if (match_BM(words[(xx -> data).elem_2], T))
            {
                printf("%d\n", (xx -> data).elem_2 + 1);
                isfound = true; break;
            }
            else xx = xx -> pred();
        }
        if (!isfound) printf("0\n");
        if (isfound) dict.remove(x);
    }
}
