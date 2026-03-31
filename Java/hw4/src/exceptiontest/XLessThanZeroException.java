package exceptiontest;

public class XLessThanZeroException extends Exception
{
    public double y;
    public XLessThanZeroException(double y_in)
    {
        super();
        y = y_in;
    }
    public String getInfo()
    {
        return (String.valueOf(y) + " is too small");
    }
}