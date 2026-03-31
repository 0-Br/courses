package filesearcher;

import java.io.*;

public class FileSearcher
{
    public static int search(String inputFile, String keyword)
    {
        try
        {
            BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(inputFile), "GBK"));
            String line = br.readLine();
            int re0 = 0;
            while (line != null)
            {
                re0 += count(line, keyword);
                line = br.readLine();
            }
            br.close();
            return re0;
        }
        catch (FileNotFoundException e)
        {
            System.out.println("路径错误");
            return -1;
        }
        catch (IOException e)
        {
            System.out.println("输入输出错误");
            return -1;
        }
    }
    private static int count(String line, String keyword)
    {
        int re0 = 0;
        keyword = keyword.toLowerCase();
        String temp = "";int r = 0;
        while (r < line.length())
        {
            if (Character.isLetter(line.charAt(r)) || Character.isDigit(line.charAt(r))) temp += line.charAt(r);
            else
            {
                temp = temp.toLowerCase();
                if (temp.equals(keyword)) re0++;
                temp = "";
            }
            r++;
        }
        temp = temp.toLowerCase();
        if (temp.equals(keyword)) re0++;
        return re0;
    }
}