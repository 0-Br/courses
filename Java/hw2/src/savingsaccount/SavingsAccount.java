package savingsaccount;

public class SavingsAccount
{
    public static double rate = 0.01;
    public static void modifyInterestRate(double interestRate)
    {
        rate = interestRate;
    }

    double save;
    public SavingsAccount(double savings)
    {
        save = savings;
    }

    public double calculateMonthlyInterest()
    {
        double interests;
        interests = save * (Math.pow((1 + rate), (1.0 / 12)) - 1);
        save += interests;
        return interests;
    }
}