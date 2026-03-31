package drawarc;

import java.awt.*;
import javax.swing.*;

public class DrawArc extends JFrame
{
    public DrawArc()
    {
        super("DrawArc");
        setSize(600, 600);
        setResizable(false);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
    }

    public void paint(Graphics g)
    {
        super.paint(g);
        g.setColor(Color.GREEN);
        g.fillRect(295, 200, 10, 360);
        g.setColor(Color.BLUE);
        g.fillArc(160, 60, 280, 280, 30, 30);
        g.fillArc(160, 60, 280, 280, 120, 30);
        g.fillArc(160, 60, 280, 280, 210, 30);
        g.fillArc(160, 60, 280, 280, 300, 30);
        g.setColor(Color.BLACK);
        g.setFont(new Font("Times New Roman", Font.PLAIN, 24));
        g.drawString("Welcome to Java world", 20, 500);
    }

    public static void main(String[] args)
    {
        DrawArc maingui = new DrawArc();
        maingui.setVisible(true);
    }
}
