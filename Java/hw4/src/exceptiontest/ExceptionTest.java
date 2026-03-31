package exceptiontest;

public class ExceptionTest
{
    public int getFirstValidInt()
    {
        while(true)
        {
            try
            {
                return Test.readInt();
            }
            catch (NumberFormatException e){};
        }
    }

    public double getX(double y)
    throws XLessThanZeroException, XGreaterThanOneException
    {
        double x = Math.log(y);
        if (x < 0) throw new XLessThanZeroException(y);
        if (x > 1) throw new XGreaterThanOneException();
        return x;
    }
}