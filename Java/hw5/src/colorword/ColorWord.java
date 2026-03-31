package colorword;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class ColorWord extends JFrame
{
    public ColorWord()
    {
        setSize(600, 200);
        setResizable(false);
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setLayout(new GridLayout(3, 1));

        JPanel p_up = new JPanel();
        JPanel p_down = new JPanel(new FlowLayout(FlowLayout.LEFT));
        add(p_up);
        add(p_down);

        ButtonGroup group = new ButtonGroup();
        JRadioButton rb0 = new JRadioButton("red");
        JRadioButton rb1 = new JRadioButton("blue");
        JRadioButton rb2 = new JRadioButton("black");

        group.add(rb0);
        group.add(rb1);
        group.add(rb2);
        p_up.add(rb0);
        p_up.add(rb1);
        p_up.add(rb2);
        rb2.setSelected(true);

        JLabel l = new JLabel("Welcome to Java world");
        l.setHorizontalAlignment(JLabel.LEFT);
        l.setVerticalAlignment(JLabel.TOP);
        l.setFont(new Font("Gothic", Font.BOLD, 24));
        p_down.add(l);

        rb0.addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent e)
                {
                    l.setForeground(Color.RED);
                }
            });
        rb1.addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent e)
                {
                    l.setForeground(Color.BLUE);
                }
            });
        rb2.addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent e)
                {
                    l.setForeground(Color.BLACK);
                }
            });
    }

    public static void main(String[] args)
    {
        ColorWord maingui = new ColorWord();
        maingui.setVisible(true);
    }
}
