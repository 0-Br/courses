package ticket;

public class TicketPool
{
    private static int rest;
    TicketPool(int trest)
    {
        rest = trest;
    }

    public int getRest()
    {
        int trest = rest;
        try
        {
            Thread.sleep((int)(Math.random() * 20));
        }
        catch (Exception e)
        {
            System.out.println(e);
        }
        return trest;
    }

    public void reduceRest(int delta)
    {
        try
        {
            Thread.sleep((int)(Math.random() * 20));
        }
        catch (Exception e)
        {
            System.out.println(e);
        }
        rest -= delta;
    }
}

class Ticket extends Thread
{
    public TicketPool ticketpool;
    public int treq;
    public Ticket(TicketPool tpl, int t)
    {
        ticketpool = tpl;
        treq = t;
    }

    public void run()
    {
        synchronized(ticketpool)
        {
            int rest = ticketpool.getRest();
            if (rest < treq) treq = rest;
            ticketpool.reduceRest(treq);
        }
    }

    public int getObtained()
    {
        return treq;
    }
}