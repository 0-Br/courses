package rational;

public class Rational
{
    private int gcd(int a, int b)
    {
        if (b == 0) return a;
        else return gcd(b, a % b);
    }

    int numerator, denominator;
    public Rational(int num, int den)
    {
        int temp = gcd(num, den);
        numerator = num / temp;
        denominator = den / temp;
    }

    public String toString()
    {
        if (denominator == 1) return String.format("%d", numerator);
        else return String.format("%d", numerator) + "/" + String.format("%d", denominator);
    }
    public double toDouble()
    {
        return (double)numerator / denominator;
    }

    public void add(Rational b)
    {
        int tempnum = this.numerator * b.denominator + this.denominator * b.numerator;
        int tempden = this.denominator * b.denominator;
        int temp = gcd(tempnum, tempden);
        this.numerator =  tempnum / temp;
        this.denominator = tempden / temp;
    }
    public void sub(Rational b)
    {
        int tempnum = this.numerator * b.denominator - this.denominator * b.numerator;
        int tempden = this.denominator * b.denominator;
        int temp = gcd(tempnum, tempden);
        this.numerator =  tempnum / temp;
        this.denominator = tempden / temp;
    }
    public void mul(Rational b)
    {
        int tempnum = this.numerator * b.numerator;
        int tempden = this.denominator * b.denominator;
        int temp = gcd(tempnum, tempden);
        this.numerator =  tempnum / temp;
        this.denominator = tempden / temp;
    }
    public void div(Rational b)
    {
        int tempnum = this.numerator * b.denominator;
        int tempden = this.denominator * b.numerator;
        int temp = gcd(tempnum, tempden);
        this.numerator =  tempnum / temp;
        this.denominator = tempden / temp;
    }
}