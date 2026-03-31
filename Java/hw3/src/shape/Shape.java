package shape;

public abstract class Shape
{
    public String c;
    public boolean iscolored;

    public Shape()
    {
        c = "#";
        iscolored = false;
    }
    public Shape(String color)
    {
        c = color;
        iscolored = true;
    }

    public String getColor()
    {
        if (!iscolored) return "#";
        else return c;
    }
    public void setColor(String color)
    {
        iscolored = true;
        c = color;
    }
    public boolean isFilled()
    {
        return iscolored;
    }

    public abstract double getArea();
    public abstract double getPerimeter();
    public abstract String toString();
}