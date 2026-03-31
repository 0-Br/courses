package shape;

public class Shapes
{
    Shape[] s;
    public Shapes(Shape[] ss)
    {
        s = ss;
    }

    public double getArea()
    {
        double sum = 0;
        for (int i = 0; i < s.length; i++) sum += s[i].getArea();
        return sum;
    }

    public double getFilledArea()
    {
        double sum = 0;
        for (int i = 0; i < s.length; i++)
        {
            if (s[i].isFilled()) sum += s[i].getArea();
        }
        return sum;
    }

    public String toString()
    {
        String re0 = "[";
        for (int i = 0; i < s.length - 1; i++)
        {
            re0 += s[i].toString();
            re0 += ",";
        }
        re0 += s[s.length - 1].toString();
        re0 += "]";
        return re0;
    }
}