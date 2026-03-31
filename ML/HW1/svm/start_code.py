import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from time import time
from tqdm import trange

# 固定随机数种子
np.random.seed(42)


def load_text_dataset(filename, positive='joy', negative='sadness'):
    """
    从文件filename读入文本数据集
    """
    data = pd.read_csv(filename)
    is_positive = data.Emotion == positive
    is_negative = data.Emotion == negative
    data = data[is_positive | is_negative]
    X = data.Text  # 输入文本
    y = np.array(data.Emotion == positive) * 2 - 1  # 1: positive, -1: negative
    return X, y

def vectorize(train, test):
    """
    将训练集和验证集中的文本转成向量表示

    Args：
        train - 训练集，大小为 num_instances 的文本数组
        test - 测试集，大小为 num_instances 的文本数组
    Return：
        train_normalized - 向量化的训练集 (num_instances, num_features)
        test_normalized - 向量化的测试集 (num_instances, num_features)
    """
    tfidf = TfidfVectorizer(stop_words='english', use_idf=True, smooth_idf=True)
    train_normalized = tfidf.fit_transform(train).toarray()
    test_normalized = tfidf.transform(test).toarray()
    return train_normalized, test_normalized

def linear_svm_subgrad_descent(X, y, alpha=0.05, lambda_reg=0.0001, num_iter=60000, batch_size=1):
    """
    线性SVM的随机次梯度下降

    参数：
        X - 特征向量，数组大小 (num_instances, num_features)
        y - 标签向量，数组大小 (num_instances)
        alpha - 浮点数。梯度下降步长，可自行调整为默认值以外的值或扩展为步长策略
        lambda_reg - 正则化系数，可自行调整为默认值以外的值
        num_iter - 要运行的迭代次数，可自行调整为默认值以外的值
        batch_size - 批大小，可自行调整为默认值以外的值

    返回：
        theta_hist - 参数向量的历史，大小的 2D numpy 数组 (num_iter+1, num_features)
        loss_hist - 小批量损失函数的历史，数组大小(num_iter)
    """
    num_instances, num_features = X.shape[0], X.shape[1]
    theta_hist = np.zeros((num_iter + 1, num_features))  # Initialize theta_hist
    theta_hist[0] = theta = np.zeros(num_features)  # Initialize theta
    loss_hist = np.zeros(num_iter)  # Initialize loss_hist

    # 3.4.1
    for epoch in trange(num_iter):
        # 取batch，允许样本重复
        batch_ids = np.random.randint(0, num_instances, size=batch_size)
        X_batch = X[batch_ids]
        y_batch = y[batch_ids]
        # 计算次梯度
        y_pred = X_batch @ theta
        gradient = lambda_reg * theta - (np.sum((y_batch[:, None] * X_batch)[np.maximum(0, 1 - y_batch * y_pred) > 0], axis=0) / batch_size)
        # 更新与记录
        loss_hist[epoch] = (np.linalg.norm(theta) ** 2) * lambda_reg / 2 + np.mean(np.maximum(0, 1 - y_batch * y_pred))
        theta = theta - alpha * gradient
        theta_hist[epoch + 1] = theta
    return theta_hist, loss_hist

def linear_svm_subgrad_descent_lambda(X, y, lambda_reg=0.0001, num_iter=60000, batch_size=1):
    """
    线性SVM的随机次梯度下降;在lambda-强凸条件下有理论更快收敛速度的算法
    该函数每次迭代的梯度下降步长已由算法给出，无需自行调整

    参数：
        X - 特征向量，数组大小 (num_instances, num_features)
        y - 标签向量，数组大小 (num_instances)
        lambda_reg - 正则化系数，可自行调整为默认值以外的值
        num_iter - 要运行的迭代次数，可自行调整为默认值以外的值
        batch_size - 批大小，可自行调整为默认值以外的值

    返回：
        theta_hist - 参数向量的历史，大小的 2D numpy 数组 (num_iter+1, num_features)
        loss hist - 小批量损失函数的历史，数组大小(num_iter)
    """
    num_instances, num_features = X.shape[0], X.shape[1]
    theta_hist = np.zeros((num_iter + 1, num_features))  # Initialize theta_hist
    theta_hist[0] = theta = np.zeros(num_features)  # Initialize theta
    loss_hist = np.zeros(num_iter)  # Initialize loss_hist

    smooth_theta_hist = np.zeros((num_iter + 1, num_features))
    smooth_theta_hist[0] = smooth_theta = np.zeros(num_features)
    smooth_loss_hist = np.zeros(num_iter)

    # 3.4.3
    for epoch in trange(num_iter):
        # 取batch，允许样本重复
        batch_ids = np.random.randint(0, num_instances, size=batch_size)
        X_batch = X[batch_ids]
        y_batch = y[batch_ids]
        # 计算次梯度
        y_pred = X_batch @ theta
        gradient = lambda_reg * theta - (np.sum((y_batch[:, None] * X_batch)[np.maximum(0, 1 - y_batch * y_pred) > 0], axis=0) / batch_size)
        # 更新与记录
        loss_hist[epoch] = (np.linalg.norm(theta) ** 2) * lambda_reg / 2 + np.mean(np.maximum(0, 1 - y_batch * y_pred))
        theta = theta - gradient / (lambda_reg * (epoch + 1)) # 强凸情况下的学习率调整策略
        theta_hist[epoch + 1] = theta

        smooth_y_pred = X_batch @ smooth_theta
        smooth_loss_hist[epoch] = (np.linalg.norm(smooth_theta) ** 2) * lambda_reg / 2 + np.mean(np.maximum(0, 1 - y_batch * smooth_y_pred))
        smooth_theta = np.mean(theta_hist[0 : epoch + 2], axis=0)
        smooth_theta_hist[epoch + 1] = smooth_theta

    return theta_hist, loss_hist, smooth_loss_hist # 额外实现了取权重平均为输出的算法

def kernel_svm_subgrad_descent(X, y, alpha=0.1, lambda_reg=1, num_iter=1000, batch_size=1):
    """
    Kernel SVM的随机次梯度下降

    参数：
        X - 特征向量，数组大小 (num_instances, num_features)
        y - 标签向量，数组大小 (num_instances)
        alpha - 浮点数。初始梯度下降步长
        lambda_reg - 正则化系数
        num_iter - 遍历整个训练集的次数（即次数）
        batch_size - 批大小

    返回：
        theta_hist - 参数向量的历史，大小的 2D numpy 数组 (num_iter+1, num_instances)
        loss hist - 正则化损失函数向量的历史，数组大小(num_iter,)
    """
    num_instances, num_features = X.shape[0], X.shape[1]
    theta = np.zeros(num_instances)  # Initialize theta
    theta_hist = np.zeros((num_iter+1, num_instances))  # Initialize theta_his
    loss_hist = np.zeros(num_iter)  # Initialize loss_hist

    # 3.4.4
    # 参考了《Understanding Machine Learning: From Theory to Algorithms》 16.3
    K, var = get_kernel(X, X)
    for epoch in trange(num_iter):
        gamma = theta / ((epoch + 1) * lambda_reg)
        batch_ids = np.random.randint(0, num_instances, size=batch_size)
        y_pred = K @ gamma
        mask = y * y_pred < 1
        for i in range(num_instances):
            if i not in batch_ids:
                mask[i] = False
        theta[mask] = theta[mask] + y[mask]
        theta_hist[epoch + 1] = theta
        theta_avg = np.mean(theta_hist[0: epoch + 2], axis=0)
        loss_hist[epoch] = (theta_avg.T @ K @ theta_avg) * lambda_reg / 2 + np.mean(np.maximum(0, 1 - y * K @ theta_avg))

        ''' 参考PPT实现的算法，但是不能收敛
        # 取batch，允许样本重复
        batch_ids = np.arange(num_instances)
        K_batch = K[batch_ids]
        y_batch = y[batch_ids]
        # 计算次梯度
        y_pred = K_batch @ theta
        gradient = lambda_reg * (K @ theta) - (np.sum((y_batch[:, None] * K_batch)[np.maximum(0, 1 - y_batch * y_pred) > 0], axis=0) / batch_size)
        # 更新与记录
        loss_hist[epoch] = (theta.T @ K @ theta) * lambda_reg / 2 + np.mean(np.maximum(0, 1 - y * y_pred))
        theta = theta - alpha * gradient
        theta_hist[epoch + 1] = theta
        '''

    return theta_hist, loss_hist

def get_kernel(X, Y, var=None):
    '''
    计算RBF核矩阵
    X: (Bx, d); Y: (By, d) -> (By, Bx)
    '''
    X_norm = np.sum(X * X, axis=1)
    Y_norm = np.sum(Y * Y, axis=1)
    D = X_norm[None, :] + Y_norm[:, None] - 2 * Y @ X.T
    if var is None:
        var = np.median(np.sqrt(np.abs(D)).reshape(-1)) ** 2
    return np.exp(-D / (2 * var)), var

def metrics(y, pred):
    '''评价指标计算'''
    TP = np.sum(np.ones_like(y)[(y >= 0) * (pred >= 0)])
    TN = np.sum(np.ones_like(y)[(y < 0) * (pred < 0)])
    FP = np.sum(np.ones_like(y)[(y < 0) * (pred >= 0)])
    FN = np.sum(np.ones_like(y)[(y >= 0) * (pred < 0)])
    accuracy = (TP + TN) / (TP + TN + FP + FN) # 准确率
    precision = (TP) / (TP + FP) # 精确率
    recall = (TP) / (TP + FN) # 召回率
    F1_score = (2 * precision * recall) / (precision + recall)
    return {'matrix': np.array([[TP, FP], [FN, TN]]), 'F1': F1_score, 'accuracy': accuracy, 'precision': precision, 'recall': recall}


def main():
    # 加载所有数据
    X_train, y_train = load_text_dataset("data_train.csv", "joy", "sadness")
    X_val, y_val = load_text_dataset("data_test.csv")
    print("Training Set Size: {} Validation Set Size: {}".format(len(X_train), len(X_val)))
    print("Training Set Text:", X_train, sep='\n')

    # 将训练集和验证集中的文本转成向量表示
    X_train_vect, X_val_vect = vectorize(X_train, X_val)
    X_train_vect = np.hstack((X_train_vect, np.ones((X_train_vect.shape[0], 1))))  # 增加偏置项
    X_val_vect = np.hstack((X_val_vect, np.ones((X_val_vect.shape[0], 1))))  # 增加偏置项

    # SVM的随机次梯度下降训练
    # 计算SVM模型在验证集上的准确率，F1-Score以及混淆矩阵

    # 3.4.2 调整超参数
    # 第一次调整，测试alpha
    '''
    hyper_params = ( # alpha, lambda_reg, num_iter, batch_size
                    (0.005, 0.0001, 60000, 1),   # 0.785890, 0.749819
                    (0.010, 0.0001, 60000, 1),   # 0.883436, 0.827910
                    (0.050, 0.0001, 60000, 1),   # 0.953988, 0.867679 # 较优
                    (0.100, 0.0001, 60000, 1),)  # 0.962883, 0.841649
    '''
    '''
    # 第二次调整，测试lambda_reg
    hyper_params = ( # alpha, lambda_reg, num_iter, batch_size
                    (0.050, 0.00005, 60000, 1),   # 0.957055, 0.858279
                    (0.050, 0.00010, 60000, 1),   # 0.953988, 0.867679 # 较优
                    (0.050, 0.00020, 60000, 1),   # 0.950307, 0.866233
                    (0.050, 0.00050, 60000, 1),)  # 0.942331, 0.857556
    '''
    '''
    # 第三次调整，测试batch_size
    hyper_params = ( # alpha, lambda_reg, num_iter, batch_size
                    (0.050, 0.00010, 60000, 1),    # 0.953988, 0.867679 # 较优
                    (0.050, 0.00010, 60000, 4),    # 0.957362, 0.863341
                    (0.050, 0.00010, 60000, 16),   # 0.958589, 0.864787
                    (0.050, 0.00010, 60000, 64),)  # 0.956748, 0.862617
    '''
    '''
    # 第四次调整，测试num_iter
    hyper_params = ( # alpha, lambda_reg, num_iter, batch_size
                    (0.050, 0.00010, 10000, 1),    # 0.876994, 0.814172
                    (0.050, 0.00010, 30000, 1),    # 0.935890, 0.859725
                    (0.050, 0.00010, 60000, 1),    # 0.953988, 0.867679 # 较优
                    (0.050, 0.00010, 100000, 1),)  # 0.967791, 0.866956
    '''
    '''
    for hp in hyper_params:
        print('*' * 100)
        print(hp)
        theta_hist, loss_hist = linear_svm_subgrad_descent(X_train_vect, y_train, *hp)
        print('accuracy (train): %f' % metrics(y_train, X_train_vect @ theta_hist[-1])['accuracy'])
        print('accuracy (valid): %f' % metrics(y_val, X_val_vect @ theta_hist[-1])['accuracy'])
    '''

    # 3.4.3 比较优化方法
    '''
    fig, ax = plt.subplots()
    theta_hist, loss_hist = linear_svm_subgrad_descent(X_train_vect, y_train, alpha=0.001, lambda_reg=0.001, batch_size=1, num_iter=3000)
    avg_loss_hist = []
    temp = []
    for i in range(loss_hist.shape[0]):
        temp.append(loss_hist[i])
        if i > 0 and i % 10 == 0:
            avg_loss_hist.append(np.min(temp))
            temp = []
    ax.plot(np.arange(len(avg_loss_hist)), avg_loss_hist, label="original (alpha = 0.05)")
    theta_hist, loss_hist = linear_svm_subgrad_descent(X_train_vect, y_train, alpha=0.001, lambda_reg=0.001, batch_size=1, num_iter=3000)
    avg_loss_hist = []
    temp = []
    for i in range(loss_hist.shape[0]):
        temp.append(loss_hist[i])
        if i > 0 and i % 10 == 0:
            avg_loss_hist.append(np.min(temp))
            temp = []
    ax.plot(np.arange(len(avg_loss_hist)), avg_loss_hist, label="original (alpha = 0.001)")
    theta_hist, loss_hist, smooth_loss_hist = linear_svm_subgrad_descent_lambda(X_train_vect, y_train, lambda_reg=0.001, batch_size=1, num_iter=3000)
    avg_loss_hist = []
    temp = []
    for i in range(loss_hist.shape[0]):
        temp.append(loss_hist[i])
        if i > 0 and i % 10 == 0:
            avg_loss_hist.append(np.min(temp))
            temp = []
    ax.plot(np.arange(len(avg_loss_hist)), avg_loss_hist, label="lambda")
    avg_loss_hist = []
    temp = []
    for i in range(smooth_loss_hist.shape[0]):
        temp.append(smooth_loss_hist[i])
        if i > 0 and i % 10 == 0:
            avg_loss_hist.append(np.min(temp))
            temp = []
    ax.plot(np.arange(len(avg_loss_hist)), avg_loss_hist, label="lambda_smooth")
    ax.set_title("Curve of Loss Function")
    ax.set_xlabel('Epoch/10')
    ax.set_ylabel('Loss')
    ax.legend()
    plt.savefig("Curve of Loss Function.png", dpi=400)
    '''

    # 3.4.4 核函数SVM
    '''
    print('*' * 100)
    K, var = get_kernel(X_train_vect, X_train_vect)
    KV, _ = get_kernel(X_train_vect, X_val_vect, var)
    '''
    '''
    # 第一次调整，测试batch_size
    for batch_size in (1, 4, 16, 64):
        theta_hist, loss_hist = kernel_svm_subgrad_descent(X_train_vect, y_train, lambda_reg=0.001, num_iter=1000, batch_size=batch_size) # alpha无效
        theta = np.mean(theta_hist, axis=0)
        print('accuracy (train): %f' % metrics(y_train, K @ theta)['accuracy'])
        print('accuracy (valid): %f' % metrics(y_val, KV @ theta)['accuracy'])
    '''
    '''
    # 第二次调整，测试lambda_reg
    for lambda_reg in (0.0001, 0.0005, 0.0010, 0.0050):
        theta_hist, loss_hist = kernel_svm_subgrad_descent(X_train_vect, y_train, lambda_reg=lambda_reg, num_iter=1000, batch_size=64) # alpha无效
        theta = np.mean(theta_hist, axis=0)
        print('accuracy (train): %f' % metrics(y_train, K @ theta)['accuracy'])
        print('accuracy (valid): %f' % metrics(y_val, KV @ theta)['accuracy'])
    '''
    '''
    # 第三次调整，测试num_iter
    for num_iter in (500, 1000, 2000, 5000):
        theta_hist, loss_hist = kernel_svm_subgrad_descent(X_train_vect, y_train, lambda_reg=0.001, num_iter=num_iter, batch_size=64) # alpha无效
        theta = np.mean(theta_hist, axis=0)
        print('accuracy (train): %f' % metrics(y_train, K @ theta)['accuracy'])
        print('accuracy (valid): %f' % metrics(y_val, KV @ theta)['accuracy'])
    '''

    # 3.4.5
    K, var = get_kernel(X_train_vect, X_train_vect)
    KV, _ = get_kernel(X_train_vect, X_val_vect, var)
    theta_hist, loss_hist = kernel_svm_subgrad_descent(X_train_vect, y_train, lambda_reg=0.001, num_iter=10000, batch_size=64) # alpha无效
    theta = np.mean(theta_hist, axis=0)
    print(metrics(y_train, K @ theta))
    print(metrics(y_val, KV @ theta))


if __name__ == '__main__':
    main()
