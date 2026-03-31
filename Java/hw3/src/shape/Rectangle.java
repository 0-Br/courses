package shape;

public class Rectangle extends Shape
{
    public double h, w;

    public Rectangle(){};
    public Rectangle(double height, double width)
    {
        super();
        h = height;
        w = width;
    }
    public Rectangle(double height, double width, String color)
    {
        super(color);
        h = height;
        w = width;
    }

    public double getHeight()
    {
        return h;
    }
    public double getWidth()
    {
        return w;
    }
    public void setHeight(double height)
    {
        h = height;
    }
    public void setWidth(double width)
    {
        w = width;
    }

    public double getArea()
    {
        return (h * w);
    }
    public double getPerimeter()
    {
        return (2 * (h + w));
    }
    public String toString()
    {
        return ("Rectangle" + "(" + c + ")");
    }
}