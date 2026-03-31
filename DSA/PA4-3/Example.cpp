#include <cstdio>
#include <cstdlib>

inline void swap(int &a, int &b)
{
    int c = a;
    a = b;
    b = c;
}

int data[500000];
int buffer[500000];
unsigned long long count = 0;
int n, LIMIT;

void insertionSort(int array[], int L, int R)
{
    for(int i = L + 1; i < R; ++i)
    {
        for(int j = i; j > L; --j)
        {
            if(array[j] < array[j - 1])
            {
                swap(array[j], array[j - 1]);
                count++;
            }
            else break;
        }
    }
}

void quicksort(int array[], int buffer[], int L, int R) // stable + inplace  + O(n)?
{
    if (R - L <= LIMIT) // 在LIMIT = 1时等价于直接返回
    {
        insertionSort(array, L, R); // merge sort to calculate how many swaps happened
        return;
    }
    count += (R - L) * 2;
    int pivot = array[L];
    int k = L;
    for (int i = L + 1; i < R; ++i)
    {
        if (array[i] < pivot)
        {
            buffer[k] = array[i];
            k++;
        }
    }
    int mid = k;
    buffer[mid] = pivot;
    k++;
    for (int i = L + 1; i < R; ++i)
    {
        if (array[i] >= pivot)
        {
            buffer[k] = array[i];
            k++;
        }
    }
    for (int i = L; i < R; ++i)
    {
        array[i] = buffer[i];
    }
    quicksort(array, buffer, L, mid);
    quicksort(array, buffer, mid + 1, R);
}

int main()
{
    scanf("%d %d", &n, &LIMIT); // LIMIT = 1
    for (int i = 0; i < n; ++i)
    {
        scanf("%d", &data[i]);
    }
    quicksort(data, buffer, 0, n);
    for (int i = 0; i < n - 1; ++i)
    {
        if (data[i] > data[i + 1]) printf("%d failed", i);
    }
    printf("%llu\n", count);
    return 0;
}