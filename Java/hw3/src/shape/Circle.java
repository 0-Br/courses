package shape;

public class Circle extends Shape
{
    public double r;

    public Circle(){};
    public Circle(double radius)
    {
        super();
        r = radius;
    }
    public Circle(double radius, String color)
    {
        super(color);
        r = radius;
    }

    public double getRadius()
    {
        return r;
    }
    public void setRadius(double radius)
    {
        r = radius;
    }

    public double getArea()
    {
        return (Math.PI * r * r);
    }
    public double getPerimeter()
    {
        return (Math.PI * r * 2);
    }
    public String toString()
    {
        return ("Circle" + "(" + c + ")");
    }
}