package hugeinteger;

public class HugeInteger
{
    int[] array;
    int len;
    public HugeInteger(long i)
    {
        array = new int[128];
        for (int j = 0; j < 128; j++) array[j] = 0;
        if (i == 0){len = 1;return;}
        int j = 0;
        while (i > 0)
        {
            array[j] = (int)(i % 10);
            i /= 10;j++;
        }
        len = j;
    }
    public HugeInteger(String s)
    {
        array = new int[128];
        for (int j = 0; j < 128; j++) array[j] = 0;
        len = s.length();
        for (int j = 0; j < len; j++)
        {
            array[j] = Integer.parseInt(s.substring(len - j - 1, len - j));
        }
    }

    public String toString()
    {
        String re0 = "";
        for (int j = 0; j < len; j++)
        {
            re0 += Integer.toString(array[len - j - 1]);
        }
        return re0;
    }

    public void add(HugeInteger b)
    {
        for (int j = 0; j < 128; j++)
        {
            array[j] += b.array[j];
            if (array[j] >= 10)
            {
                array[j] -= 10;
                array[j + 1] += 1;
            }
        }
        int j = 127;
        while ((array[j] == 0) && (j > 0)) j--;
        len = j + 1;
    }

    public int compareTo(HugeInteger o)
    {
        if (len < o.len) return -1;
        if (len > o.len) return 1;
        for (int j = len - 1; j >= 0; j--)
        {
            if (array[j] < o.array[j]) return -1;
            if (array[j] > o.array[j]) return 1;
        }
        return 0;
    }
    public int compareTo(long o)
    {
        HugeInteger oo = new HugeInteger(o);
        if (len < oo.len) return -1;
        if (len > oo.len) return 1;
        for (int j = len - 1; j >= 0; j--)
        {
            if (array[j] < oo.array[j]) return -1;
            if (array[j] > oo.array[j]) return 1;
        }
        return 0;
    }
}