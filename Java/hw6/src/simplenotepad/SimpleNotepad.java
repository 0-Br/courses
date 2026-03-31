package simplenotepad;

import java.io.*;
import java.nio.file.*;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class SimpleNotepad extends JFrame
{
    public SimpleNotepad()
    {
        setTitle("SimpleNotepad");
        setSize(600, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        JMenuBar menuBar = new JMenuBar();
        JMenu fileMenu = new JMenu("File");
        menuBar.add(fileMenu);
        JMenuItem openItem = new JMenuItem("Open");
        JMenuItem saveItem = new JMenuItem("Save");
        fileMenu.add(openItem);
        fileMenu.add(saveItem);
        setJMenuBar(menuBar);

        JPanel panel_c = new JPanel(new BorderLayout());
        JPanel panel_s = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        add(panel_c, BorderLayout.CENTER);
        add(panel_s, BorderLayout.SOUTH);

        JTextArea textarea = new JTextArea();
        textarea.setLineWrap(true);
        JScrollPane sp = new JScrollPane(textarea);
        panel_c.add(sp, BorderLayout.CENTER);

        JLabel label = new JLabel();
        label.setText("刘滨瑞's notepad");
        panel_s.add(label);

        openItem.addActionListener(new ActionListener()
            {
                public void actionPerformed(ActionEvent e)
                {
                    try
                    {
                        JFileChooser filechooser = new JFileChooser();
                        filechooser.setDialogTitle("打开");
                        int returnValue = filechooser.showOpenDialog(null);
                        if (returnValue == JFileChooser.APPROVE_OPTION)
                        {
                            File file = filechooser.getSelectedFile();
                            String mtype = Files.probeContentType(file.toPath());
                            if (mtype != null && mtype.equals("text/plain"))
                            {
                                BufferedReader br = new BufferedReader(new FileReader(file));
                                String line = br.readLine();
                                while (line != null)
                                {
                                    textarea.append(line);
                                    line = br.readLine();
                                }
                                br.close();
                            }
                        }
                    }
                    catch (IOException exception){};
                }
            });

        saveItem.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                try
                {
                    JFileChooser filechooser = new JFileChooser();
                    filechooser.setDialogTitle("保存");
                    int returnValue = filechooser.showSaveDialog(null);
                    if (returnValue == JFileChooser.APPROVE_OPTION)
                    {
                        File file = filechooser.getSelectedFile();
                        String mtype = Files.probeContentType(file.toPath());
                        if (mtype != null && mtype.equals("text/plain"))
                        {
                            BufferedWriter bw = new BufferedWriter(new FileWriter(file));
                            bw.write(textarea.getText());
                            bw.close();
                        }
                    }
                }
                catch (IOException exception){};
            }
        });
    }

    public static void main(String[] args)
    {
        SimpleNotepad mainGUI = new SimpleNotepad();
        mainGUI.setVisible(true);
    }
}