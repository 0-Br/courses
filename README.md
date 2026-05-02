# 课程作业合集

本仓库收录本科及研究生阶段的课程编程作业、实验报告与项目代码，涵盖计算机科学、地球科学、物理实验与工程力学等学科方向，涉及 Python、C++、Fortran、Java、SQL 等多种编程语言。

## 目录

| 目录 | 课程 | 语言 | 内容 |
|------|------|------|------|
| [DL](#dl) | 深度学习 | Python | CNN · MLP · RNN · GNN · Diffusion · GAN · Transformer |
| [DSA](#dsa) | 数据结构与算法 | C++ | 编程作业 × 12 · 实验 × 3 · 课程评测工具 |
| [Fortran](#fortran) | Fortran 程序设计 | Fortran | 数值方法 · MPI/OpenMP 并行计算 · Jacobi 求解器 |
| [Java](#java) | Java 程序设计 | Java | OOP · GUI · 网络编程 · 多线程 |
| [ML](#ml) | 机器学习 | Python | SGD · SVM · 决策树 · 梯度提升 · 强化学习 |
| [人智导](#人智导) | 人工智能导论 | Python | 博弈搜索 · 主题模型 · 图像分类 · 情感分析 |
| [大数据](#大数据) | 大数据技术 | Python | Jupyter notebook 数据分析实验 × 3 |
| [实验](#实验) | 物理与工程实验 | Python | 物理实验数据分析 × 11 |
| [数值](#数值) | 数值方法 | Python | 线性方程组求解 · 插值方法 |
| [数据库](#数据库) | 数据库技术 | SQL / VC++ / Delphi | SQL 查询 · 数据库应用开发 × 3 |
| [河川](#河川) | 河川水文学 | Python / LaTeX | 水文计算 × 4 |
| [海气](#海气) | 海洋-大气相互作用 | Python | 气候指数分析 · Hadley 环流 |
| [程设P](#程设p) | Python 程序设计 | Python | GUI 绘图 · OJ 算法题 × 28 |

---

## DL

深度学习课程，3 次大作业。

| 作业 | 主题 | 内容 |
|------|------|------|
| HW1 | 网络基础 | CNN 图像分类、MLP 时序预测（ETTh1 数据集） |
| HW2 | 序列与图模型 | RNN/LSTM 序列建模、GNN 图分类（Cora 数据集） |
| HW3 | 生成模型 | Diffusion 扩散模型（DDPM/DDIM 采样、分类器引导生成）、GAN、Transformer |

每次作业含 LaTeX 实验报告。模型权重（约 18.9 GB）已移至本地存档。

## DSA

数据结构与算法课程。12 个编程作业（PA）和 3 个实验（Lab），每题附有题目说明、C++ 实现和报告。

**编程作业：**

| 编号 | 题目 | 核心数据结构/算法 |
|------|------|-----------------|
| PA1-1 | Alarm | 二分查找、几何判定 |
| PA2-1 | Unrolled List | 块状链表，O(√n) 操作 |
| PA2-2 | Battery | 队列管理 |
| PA2-3 | Build | 多叉树、层序遍历 |
| PA3-1 | kth | 快速选择 |
| PA3-2 | Magician | 高级算法 |
| PA4-1 | Process Schedule | 进程调度 |
| PA4-2 | Q&A / Whistory | 多文件类设计、字符串算法 |
| PA4-3 | Count Simple | 组合计数 |

**实验：**

| 编号 | 主题 | 内容 |
|------|------|------|
| Lab2 | 决策树 | ID3（信息增益）与 CART（基尼系数），准确率约 76.5% |
| Lab3 | 平衡搜索树 | AVL 树与 Splay 树性能对比（随机/聚簇/顺序访问） |
| Lab4 | 字符串匹配 | KMP、Trie、Aho-Corasick 自动机 |

各 PA 目录下的 `checkit/` 为课程提供的自动评测工具。

## Fortran

Fortran 程序设计课程，覆盖基础语法、数值计算与并行编程。

**数值方法（`Numerical_Methods/`）：** 二分法、Newton 法、割线法、Lagrange 与 Newton 插值、Gauss-Jordan 消元、LU 分解、行列式计算、数值积分。

**并行计算：**
- `MPI/`：点对点通信、集合通信（Broadcast / Gather / Scatter）、域分解 Jacobi 迭代、Monte Carlo 求 π，分初/中/高级三个阶段。
- `OpenMP/`：线程并行、私有/共享变量、混合并行 π 计算。

**`Jacobi_2D/`：** 二维 Jacobi 迭代求解器，支持多进程域分解（N ∈ {1,2,4,8}，网格 S ∈ {64,128,256}），附加速比与并行效率分析报告。

另含 10 次常规作业（`hw1`–`hw10`）和编译产物（`bin/`）。

## Java

Java 程序设计课程，7 次作业，覆盖 OOP 核心特性。

| 作业 | 主题 | 内容 |
|------|------|------|
| hw1 | OOP 基础 | Complex（复数）、Rational（有理数）、TicTacToe |
| hw2 | 类设计 | Date、HugeInteger（大整数运算）、SavingsAccount |
| hw3 | 继承与多态 | Shape 层次结构（Circle / Rectangle / Square） |
| hw4 | 文件与异常 | FileSearcher、自定义异常、CSV 数据读取 |
| hw5 | GUI 图形 | ColorWord、DrawArc（Swing/AWT） |
| hw6 | GUI 应用 | SimpleNotepad 文本编辑器 |
| hw7 | 网络与线程 | Client-Server 游戏、线程安全 TicketPool |

## ML

机器学习课程，4 次作业。

| 作业 | 主题 | 内容 |
|------|------|------|
| HW1 | 线性模型 | SGD（L2 正则化、特征归一化）、SVM |
| HW2 | 进阶方法 | 理论推导（仅报告） |
| HW3 | 集成学习 | 决策树（熵 / 回归）、梯度提升机（L2 / Logistic 损失） |
| HW4 | 强化学习 | SARSA、Q-Learning、REINFORCE、TD Actor-Critic |

HW4 含训练历史缓存（`.npy`），用于复现奖励曲线。

## 人智导

人工智能导论课程，3 个项目覆盖搜索、学习与推理三大范式。

**搜索（`search/`）：** 五子棋 AI，实现 Minimax（α-β 剪枝）、截断搜索（启发式评估函数）、MCTS（UCB1）和 AlphaZero 变体。评估函数基于棋形模式加权（活二/三/四、冲三/四）和中心距离偏置。

**学习（`learn/`）：** 图像纹理分析（p3）、MNIST 手写数字分类（p4，MLP 实现）、文本情感分类（p5）。

**推理（`reasoning/`）：** LDA 主题模型，变分 EM 算法，中文分词与停用词处理，主题数 K ∈ {5, 10, 20}，以困惑度评估模型质量。

## 大数据

大数据技术课程，3 次 Jupyter notebook 实验（`hw2`–`hw4`），涉及大规模数据处理与分析。原始数据文件 HadISST.nc（213 MB）已移至本地存档。

## 实验

物理与工程实验课程，11 个实验的数据分析脚本。

| 类别 | 实验 |
|------|------|
| 电磁学 | 霍尔实验（5 组）、同轴电缆、无线传输 |
| 光学 | 偏振实验、塞曼实验、迈克耳孙干涉 |
| 热学 | 热导实验 |
| 力学 | 摩擦系数实验（3 组） |
| 材料 | 混凝土强度、混凝土抗弯、混凝土配置（C40 计算书） |

分析工具以 Python 脚本和 Jupyter notebook 为主，使用 NumPy/SciPy/Matplotlib 进行数据拟合与可视化。

## 数值

数值方法课程，2 次作业。

- **hw1**：线性方程组求解——迭代法（Gauss-Seidel、Jacobi、SOR）、LU 分解、LDL^T 分解。
- **hw2**：插值方法——三次样条插值、抛物线插值。

## 数据库

数据库技术课程，3 个开发实验，各含 Markdown 和 PDF 格式报告。

- **SQL 实验**：DDL/DML 全流程（建表、约束、索引、视图），11 类复杂查询（聚合、子查询、连接、模式匹配）。
- **VC++ 开发实验**：基于 ODBC 的 Windows 数据库应用。
- **Delphi 开发实验**：可视化数据库应用开发。

## 河川

河川水文学课程，4 次作业。以 Python 进行水文计算（Newton-Raphson 迭代求解水深等），LaTeX 撰写技术报告。

## 海气

海洋-大气相互作用课程，3 次作业。

- **HW2**：大气-海洋指数基础分析。
- **HW3**：Niño 3.4 指数分析（ERSSTv5 观测 1854–2020、CESM1 模式输出），El Niño/La Niña 位相识别。
- **HW5**：Hadley 环流经向扩展分析。

NetCDF 气候数据（约 1 GB）已移至本地存档。

## 程设P

Python 程序设计课程。

**课程作业：**
- **HW1**：tkinter GUI——小猪佩奇绘图（AutoCAD 坐标提取 + Photoshop 取色）、冬奥知识问答系统。
- **HW2**：素数计数算法对比与性能分析。

**在线评测（OJ1–OJ7，共 28 题）：** 覆盖 Fibonacci 数列、BST 操作、字符串处理、进制转换、哈希查询、Morse 编码、排列组合、分数运算类、日期类等。
