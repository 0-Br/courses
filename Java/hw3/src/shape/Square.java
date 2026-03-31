package shape;

public class Square extends Rectangle
{
    public Square(){};
    public Square(double a)
    {
        super(a, a);
    }
    public Square(double a, String color)
    {
        super(a, a, color);
    }

    public double getSide()
    {
        if (h == w) return h;
        else return -1;
    }
    public void setSide(double a)
    {
        h = a;
        w = a;
    }

    public double getArea()
    {
        if (h == w) return (h * w);
        else return -1;
    }
    public double getPerimeter()
    {
        if (h == w) return (4 * h);
        else return -1;
    }
    public String toString()
    {
        if (h == w) return ("Square" + "(" + c + ")");
        else return "not match!";
    }
}