package complex;

public class Complex
{
    double realPart, imaginaryPart;
    public Complex(double real, double imag)
    {
        realPart = real;
        imaginaryPart = imag;
    }

    public String toString()
    {
        String re0 = "";
        if (imaginaryPart == 0) re0 = String.format("%.3f", realPart);
        else if (realPart == 0) re0 = String.format("%.3f", imaginaryPart) + "i";
        else
        {
            re0 = String.format("%.3f", realPart);
            if (imaginaryPart > 0) re0 += "+";
            re0 += String.format("%.3f", imaginaryPart) + "i";
        }
        return re0;
    }

    public Complex add(Complex b)
    {
        return new Complex(this.realPart + b.realPart, this.imaginaryPart + b.imaginaryPart);
    }
    public Complex sub(Complex b)
    {
        return new Complex(this.realPart - b.realPart, this.imaginaryPart - b.imaginaryPart);
    }
    public Complex mul(Complex b)
    {
        double newreal = this.realPart * b.realPart - this.imaginaryPart * b.imaginaryPart;
        double newimag = this.realPart * b.imaginaryPart + this.imaginaryPart * b.realPart;
        return new Complex(newreal, newimag);
    }
    public Complex div(Complex b)
    {
        double newreal = this.realPart * b.realPart + this.imaginaryPart * b.imaginaryPart;
        double newimag = this.imaginaryPart * b.realPart - this.realPart * b.imaginaryPart;
        double den = b.realPart * b.realPart + b.imaginaryPart * b.imaginaryPart;
        return new Complex(newreal / den, newimag / den);
    }
}