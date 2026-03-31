package date;

public class Date
{
    private int ex_month(String s_month)
    {
        if (s_month.equals("Jan.")) return 1;
        else if (s_month.equals("Feb.")) return 2;
        else if (s_month.equals("Mar.")) return 3;
        else if (s_month.equals("Apr.")) return 4;
        else if (s_month.equals("May.")) return 5;
        else if (s_month.equals("Jun.")) return 6;
        else if (s_month.equals("Jul.")) return 7;
        else if (s_month.equals("Aug.")) return 8;
        else if (s_month.equals("Sept.")) return 9;
        else if (s_month.equals("Oct.")) return 10;
        else if (s_month.equals("Nov.")) return 11;
        else if (s_month.equals("Dec.")) return 12;
        else return -1;
    }

    int day, month, year;
    public Date(String s)
    {
        int loc_0 = s.indexOf('.');
        int loc_1 = s.indexOf(',');
        String s_day = s.substring(loc_0 + 1, loc_1);
        String s_month = s.substring(0, loc_0 + 1);
        String s_year = s.substring(loc_1 + 1);
        day = Integer.parseInt(s_day);
        month = ex_month(s_month);
        year = Integer.parseInt(s_year);
    }
    public Date(String m, int d, int y)
    {
        day = d;
        month = ex_month(m);
        year = y;
    }
    public Date(int d, int m, int y)
    {
        day = d;
        month = m;
        year = y;
    }

    public String toString()
    {
        return String.format("%d/%d/%d", year, month, day);
    }
}