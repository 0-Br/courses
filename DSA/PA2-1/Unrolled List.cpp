#include <cstdio>
const int M = 4096;
//You can modify the value of M
//Design testcases to select the best M for your code.

struct Node
{
    Node *pred, *succ;
    int data[M + 1];//数据区，出于保护考虑，容量设为M+1
    unsigned int _node_size;

    Node(){_node_size = 0;}
    Node(unsigned int size_in, int *data_in)
    {
        _node_size = size_in;
        for (unsigned int i = 0; i < size_in; i++) data[i] = data_in[i];
    }

    //插入后继节点，返回指向新增节点的指针
    Node* insert_s(unsigned int size, int *data)
    {
        Node *oldsucc = succ;
        succ = new Node(size, data);
        succ -> succ = oldsucc;
        succ -> pred = this;
        succ -> succ -> pred = succ;
        return succ;
    }

    //在节点内增加元素
    //若节点已满，将本节点均分为两节点
    void append(unsigned int r, int e)
    {
        if (_node_size < M)
        {
            _node_size++;
            for (unsigned int i = _node_size - 1; i > r; i--) data[i] = data[i - 1];
            data[r] = e;
        }
        else if (_node_size == M)
        {
            for (unsigned int i = M; i > r; i--) data[i] = data[i - 1];
            data[r] = e;
            int newdata[M + 1];unsigned int mid = M / 2 + 1;
            _node_size = mid;
            for (unsigned int i = mid; i < M + 1; i++) newdata[i - mid] = data[i];
            insert_s(M + 1 - mid, newdata);
        }
        else printf("Error!");
    }

    int remove(unsigned int r)
    {
        _node_size--;
        int oldelem = data[r];
        for (unsigned int i = r; i < _node_size; i++) data[i] = data[i + 1];
        return oldelem;
    }
};

struct UnrolledList
{
    unsigned int _list_size;
    Node *header, *trailer;

    UnrolledList()
    {
        _list_size = 0;
        header = new Node;
        trailer = new Node;
        header -> pred = NULL;
        header -> succ = trailer;
        trailer -> succ = NULL;
        trailer -> pred = header;
        int data[M + 1];
        header -> insert_s(0, data);
    }

    Node* cursor(unsigned int& rank, Node *p)
    {
        p = p -> succ;
        while ((rank > (p -> _node_size)))
        {
            rank -= (p -> _node_size);
            p = p -> succ;
        }
        return p;
    }

    void insert(unsigned int position, int value)
    {
        if ((position < 0) || (position > _list_size)) position = _list_size;
        Node *c = cursor(position, header);
        c -> append(position, value);
        _list_size++;
    }
    void remove(unsigned int position)
    {
        if ((position < 0) || (position >= _list_size)) return;
        Node *c = cursor(position, header);
        if (c -> _node_size == position)
        {
            position = 0;
            c = c -> succ;
        }
        c -> remove(position);
        _list_size--;
        if (c -> _node_size == 0)
        {
            c -> pred = c -> succ -> pred;
            c -> succ = c -> pred -> succ;
        }
    }
    int query(unsigned int position)
    {
        if ((position < 0) || (position >= _list_size)) return -1;
        Node *c = cursor(position, header);
        if (c -> _node_size == position)
        {
            c = c -> succ;
            position = 0;
        }
        return c -> data[position];
    }
};

enum OperationType
{
    NOT_USED,
    INSERT,
    DELETE,
    QUERY
};

int main(){
    // you should not modify the main function
    int num_of_operation;
    scanf("%d", &num_of_operation);
    int type_of_operation, argument1, argument2;
    UnrolledList a_list;
    for(int operation_id = 0; operation_id < num_of_operation; operation_id++)
    {
        scanf("%d%d%d", &type_of_operation, &argument1, &argument2);
        if (type_of_operation == INSERT)
        {
            a_list.insert(argument1,argument2);
        }
        else if (type_of_operation == DELETE)
        {
            // argument2 is 0 and should be ignored
            a_list.remove(argument1);
        }
        else if (type_of_operation == QUERY)
        {
            // argument2 is 0 and should be ignored
            printf("%d\n", a_list.query(argument1));
        }
        else
        {
            printf("Invalid Operation");
            return 0;
        }
    }
    return 0;
}