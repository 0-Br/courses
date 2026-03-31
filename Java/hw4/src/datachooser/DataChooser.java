package datachooser;

import java.io.*;
import java.util.*;

public class DataChooser
{
    public static void choose(String inputFile, String outputFile)
    {
        try
        {
            Scanner input = new Scanner(new File(inputFile));
            int index = 0;
            File output = new File(outputFile);
            PrintStream out = new PrintStream(output);
            if (input.hasNextLine())
            {
                Scanner label = new Scanner(input.nextLine());
                label.useDelimiter(",");
                while (label.hasNext())
                {
                    String temps = label.next();
                    if (temps.equals("Department")) break;
                    index++;
                }
            }
            out.println("Department");
            while (input.hasNextLine())
            {
                Scanner row = new Scanner(input.nextLine());
                row.useDelimiter(",");
                String info = row.next();
                for (int i = 0; i < index; i++)
                {
                    info = row.next();
                }
                out.println(info);
            }
            out.close();
        }
        catch (FileNotFoundException e)
        {
            System.out.println("路径错误");
        }
    }
}