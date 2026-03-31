package test;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Polygon;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JPanel;

public class HexagonAnimation extends JPanel {

    private Polygon hexagon; // 六边形对象
    private int side; // 六边形的边长
    private int shrink; // 六边形缩小的速度
    private JButton button; // 按钮对象

    public HexagonAnimation() {
        side = 100; // 初始边长为100
        shrink = 1; // 每次缩小1个像素
        setPreferredSize(new Dimension(500, 500)); // 设置面板大小
        createHexagon(); // 创建六边形
        button = new JButton("开始动画"); // 创建按钮
        button.addActionListener(new ButtonListener()); // 为按钮添加事件监听器
        add(button); // 将按钮添加到面板中
    }

    @Override
    public void paintComponent(Graphics g) {
        super.paintComponent(g);
        g.fillPolygon(hexagon); // 填充六边形
        animate();
    }

    private void createHexagon() {
        hexagon = new Polygon(); // 初始化六边形对象
        for (int i = 0; i < 6; i++) { // 添加六个顶点
            hexagon.addPoint((int) (250 + side * Math.cos(i * Math.PI / 3)), // x坐标
                    (int) (250 + side * Math.sin(i * Math.PI / 3))); // y坐标
        }
    }

    private void animate() {
        if (side > 0) { // 如果边长大于0，就缩小六边形
            side -= shrink; // 边长减少
            createHexagon(); // 重新创建六边形
            repaint(); // 重新绘制画面
        }
    }

    private class ButtonListener implements ActionListener { // 按钮事件监听器类

        @Override
        public void actionPerformed(ActionEvent e) { // 当按钮被点击时执行的方法
            side = 100;
            repaint(); // 调用动画方法
        }
    }

    public static void main(String[] args) {
        JFrame frame = new JFrame("Hexagon Animation"); // 创建窗口对象
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // 设置关闭窗口时退出程序
        frame.add(new HexagonAnimation()); // 添加面板对象到窗口中
        frame.pack(); // 调整窗口大小以适应内容
        frame.setLocationRelativeTo(null); // 设置窗口居中显示
        frame.setVisible(true); // 设置窗口可见
    }
}