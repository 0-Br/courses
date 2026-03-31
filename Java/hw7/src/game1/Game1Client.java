package game1;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class Game1Client
{
    public String host_server;
    public int port_server;
    public Socket client;

    public Game1Client(String host, int port)
    {
        host_server = host;
        port_server = port;
    }

    public int run()
    {
        try
        {
            client = new Socket(host_server, port_server);
            Scanner reader = new Scanner(
                new BufferedReader(new InputStreamReader(client.getInputStream())));
            BufferedWriter writer =
                new BufferedWriter(new OutputStreamWriter(client.getOutputStream()));

            writer.write("hello");
            writer.newLine();
            writer.flush();

            int lower_bound = reader.nextInt();
            int upper_bound = reader.nextInt() + 1;
            int limit = reader.nextInt();
            reader.nextLine();

            int mid;
            while (limit > 0)
            {
                limit--;
                mid = (lower_bound + upper_bound) / 2;
                writer.write(String.format("%d", mid));
                writer.newLine();
                writer.flush();

                String signal = reader.nextLine();
                if (signal.equals("Correct!"))
                {
                    reader.nextLine();
                    client.close();
                    reader.close();
                    writer.close();
                    return mid;
                }
                if (signal.equals("<")) lower_bound = mid;
                if (signal.equals(">")) upper_bound = mid;
            }
            return -1;
        }
        catch (Exception e)
        {
            return -1;
        }
    }
}
