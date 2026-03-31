#include <cstdio>
#include <cmath>
#include <set>
#include <sys/timeb.h>

#define AREA_SIZE 3//标签的可取值数量
#define ATTRI_MAX 64//最大属性数
#define EXAMPLE_MAX 4096//最大实例数

//计算信息熵
double cal_entropy(int num_labels[])
{
    int total = 0;
    for (int i = 0; i < AREA_SIZE; i++) total += num_labels[i];
    double re0 = 0.0;
    for (int i = 0; i < AREA_SIZE; i++)
    {
        if (num_labels[i])
        {
            double p = (double)num_labels[i] / (double)total;
            re0 += -p * log2(p);
        }
    }
    return re0;
}

//计算基尼系数
double cal_gini(int num_labels[])
{
    int total = 0;
    for (int i = 0; i < AREA_SIZE; i++) total += num_labels[i];
    double re0 = 1.0;
    if (!total) return 0.0;
    for (int i = 0; i < AREA_SIZE; i++)
    {
        double p = (double)num_labels[i] / (double)total;
        re0 -= p * p;
    }
    return re0;
}

struct example
{
    int dimension;//维度
    int data[ATTRI_MAX];//数据
    int label;//标签值，为[0, AREA_SIZE)间的一个值
    void init(int d, const int data_in[], int label_in)
    {
        dimension = d;
        for (int i = 0; i < d; i++) data[i] = data_in[i];
        label = label_in;
    }
};

struct node
{
    std::set<int> attributes;//尚可用于分类的属性
    int attribute = -1;//本节点用于分类的属性
    int dimension = -1;//维度
    int num;//实例数量
    example* examples[EXAMPLE_MAX];//实例
    int areas[AREA_SIZE];//值域
    node *lc, *rc;

    node()
    {
        num = 0;
        for (int i = 0; i < AREA_SIZE; i++) areas[i] = 0;
        lc = NULL;rc = NULL;
    }

    //添加一条实例数据
    void append(example* new_example)
    {
        dimension = new_example -> dimension;
        examples[num] = new_example;
        num++;
        areas[new_example -> label]++;
    }

    //计算以“attri”属性分类的ID3算法IG
    double cal_IG_ID3(int attri)
    {
        int l_num = 0, r_num = 0;
        int l_areas[AREA_SIZE] = {0};
        int r_areas[AREA_SIZE] = {0};
        for (int i = 0; i < num; i++)
        {
            if ((examples[i] -> data)[attri])
            {
                l_num++;
                l_areas[examples[i] -> label]++;
            }
            else
            {
                r_num++;
                r_areas[examples[i] -> label]++;
            }
        }
        return (cal_entropy(areas)
            - cal_entropy(l_areas) * ((double)l_num / (double)num)
            - cal_entropy(r_areas) * ((double)r_num / (double)num));
    }

    //计算以“attri”属性分类的CART算法IG
    //定义CART算法的IG为1-基尼系数，此后统一取IG最大
    double cal_IG_CART(int attri)
    {
        int l_num = 0, r_num = 0;
        int l_areas[AREA_SIZE] = {0};
        int r_areas[AREA_SIZE] = {0};
        for (int i = 0; i < num; i++)
        {
            if ((examples[i] -> data)[attri])
            {
                l_num++;
                l_areas[examples[i] -> label]++;
            }
            else
            {
                r_num++;
                r_areas[examples[i] -> label]++;
            }
        }
        return (1.0
            - cal_gini(l_areas) * ((double)l_num / (double)num)
            - cal_gini(r_areas) * ((double)r_num / (double)num));
    }

    //检查是否满足终止条件，满足则返回决策结果，不满足则返回0
    int check()
    {
        //为空，无法判断，默认取最后一类为决策结果
        if (!num) return AREA_SIZE;

        //无可用于分类的属性，作最大投票
        if (attributes.empty())
        {
            int re0;
            int label_max = -1;
            for (int i = 0; i < AREA_SIZE; i++)
            {
                if (areas[i] > label_max)
                {
                    re0 = i;
                    label_max = areas[i];
                }
            }
            return (re0 + 1);
        }

        //所有数据标签相同，直接返回决策结果
        int temp = 0;int re0;
        for (int i = 0; i < AREA_SIZE; i++)
        {
            if (areas[i])
            {
                temp++;
                re0 = i;
            }
        }
        if (temp == 1) return (re0 + 1);

        return 0;
    }

    //决策函数，根据输入实例输出决策结果
    //递归
    int decide(const example& x)
    {
        if (attribute == -1) return check();
        else
        {
            if (x.data[attribute]) return lc -> decide(x);
            else return rc -> decide(x);
        }
    }

    //ID3算法决策树生成函数，默认左1右0
    //递归
    void build_ID3()
    {
        lc = new node();
        rc = new node();
        int attri_best;
        double IG_max = -10.0;
        for (int i = 0; i < dimension; i++)
        {
            if (attributes.count(i))
            {
                double IG = cal_IG_ID3(i);
                if (IG > IG_max)
                {
                    attri_best = i;
                    IG_max = IG;
                }
            }
        }
        attribute = attri_best;

        (lc -> attributes) = attributes;
        (lc -> attributes).erase(attri_best);
        (rc -> attributes) = attributes;
        (rc -> attributes).erase(attri_best);
        for (int i = 0; i < num; i++)
        {
            if ((examples[i] -> data)[attri_best]) lc -> append(examples[i]);
            else rc -> append(examples[i]);
        }

        if (!(lc -> check())) lc -> build_ID3();
        if (!(rc -> check())) rc -> build_ID3();
    }

    //CART算法决策树生成函数，默认左1右0
    //递归
    void build_CART()
    {
        lc = new node();
        rc = new node();
        int attri_best;
        double IG_max = -10.0;
        for (int i = 0; i < dimension; i++)
        {
            if (attributes.count(i))
            {
                double IG = cal_IG_CART(i);
                if (IG > IG_max)
                {
                    attri_best = i;
                    IG_max = IG;
                }
            }
        }
        attribute = attri_best;

        (lc -> attributes) = attributes;
        (lc -> attributes).erase(attri_best);
        (rc -> attributes) = attributes;
        (rc -> attributes).erase(attri_best);
        for (int i = 0; i < num; i++)
        {
            if ((examples[i] -> data)[attri_best]) lc -> append(examples[i]);
            else rc -> append(examples[i]);
        }

        if (!(lc -> check())) lc -> build_CART();
        if (!(rc -> check())) rc -> build_CART();
    }
};

int main()
{
    //训练数据、测试数据的绝对路径
    FILE *file_train = fopen("C:\\Users\\Binrui_Liu\\OneDrive\\Cloud\\Codes\\DSA\\Lab2\\data\\data_train.in", "r");
    FILE *file_test = fopen("C:\\Users\\Binrui_Liu\\OneDrive\\Cloud\\Codes\\DSA\\Lab2\\data\\data_test.in", "r");
    if (!file_train || !file_test)
    {
        printf("File not found!");
        return 0;
    }

    int n_train, m_train, n_test, m_test;
    fscanf(file_train, "%d %d", &n_train, &m_train);
    fscanf(file_test, "%d %d", &n_test, &m_test);
    if (m_train - m_test)
    {
        printf("Attribute not match!");
        return 0;
    }

    int buf[ATTRI_MAX + 1];
    example *set_train = new example[n_train];
    example *set_test = new example[n_test];

    for (int i = 0; i < n_train; i++)
    {
        for (int j = 0; j <= m_train; j++) fscanf(file_train, "%d", &buf[j]);
        set_train[i].init(m_train, buf, buf[m_test] - 1);
    }
    for (int i = 0; i < n_test; i++)
    {
        for (int j = 0; j <= m_test; j++) fscanf(file_test, "%d", &buf[j]);
        set_test[i].init(m_test, buf, buf[m_test] - 1);
    }
    fclose(file_train);
    fclose(file_test);

    node *root_ID3 = new node();
    node *root_CART = new node();
    for (int i = 0; i < n_train; i++)
    {
        root_ID3 -> append(&set_train[i]);
        root_CART -> append(&set_train[i]);
    }
    for (int i = 0; i < m_train; i++)
    {
        (root_ID3 -> attributes).insert(i);
        (root_CART -> attributes).insert(i);
    }


    timeb start, end;

    ftime(&start);
    root_ID3 -> build_ID3();
    ftime(&end);
    printf("ID3算法已完成决策树构建！用时：%dms\n", end.millitm - start.millitm);
    ftime(&start);
    root_CART -> build_CART();
    ftime(&end);
    printf("CART算法已完成决策树构建！用时：%dms\n", end.millitm - start.millitm);

    //结果输出路径
    FILE *output_ID3 = fopen("C:\\Users\\Binrui_Liu\\OneDrive\\Cloud\\Codes\\DSA\\Lab2\\data\\result_ID3.out", "w");
    int num_correct_ID3 = 0;
    for (int i = 0; i < n_test; i++)
    {
        int re0 = root_ID3 -> decide(set_test[i]);
        fprintf(output_ID3, "%d\n", re0);
        if (set_test[i].label + 1 == re0) num_correct_ID3++;
    }
    fclose(output_ID3);

    //结果输出路径
    FILE *output_CART = fopen("C:\\Users\\Binrui_Liu\\OneDrive\\Cloud\\Codes\\DSA\\Lab2\\data\\result_CART.out", "w");
    int num_correct_CART = 0;
    for (int i = 0; i < n_test; i++)
    {
        int re0 = root_CART -> decide(set_test[i]);
        fprintf(output_CART, "%d\n", re0);
        if (set_test[i].label + 1 == re0) num_correct_CART++;
    }
    fclose(output_ID3);

    printf("complete\n");
    printf("ID3 accuracy:%f\n", (double)num_correct_ID3 / (double)n_test);
    printf("CART accuracy:%f\n", (double)num_correct_CART / (double)n_test);

    delete[] set_train;
    delete[] set_test;
    delete root_ID3;
    delete root_CART;
    return 0;
}