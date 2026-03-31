from sklearn.metrics import roc_auc_score
import data
import numpy as np


def get_roc_auc_score(y_true, y_probs):
    '''
    Uses roc_auc_score function from sklearn.metrics to calculate the micro ROC AUC score for a given y_true and y_probs.
    '''

    NoFindingIndex = data.all_classes.index('No Finding')

    class_roc_auc_list = []
    useful_classes_roc_auc_list = []

    for i in range(y_true.shape[1]):
        class_roc_auc = roc_auc_score(y_true[:, i], y_probs[:, i])
        class_roc_auc_list.append(class_roc_auc)
        if i != NoFindingIndex:
            useful_classes_roc_auc_list.append(class_roc_auc)
    print('class_roc_auc_list: ', class_roc_auc_list)
    useful_classes = [x for x in data.all_classes if x != 'No Finding']
    print('useful_classes_roc_auc_list', {useful_classes[i]: x for i, x in enumerate(useful_classes_roc_auc_list)})

    return np.mean(np.array(useful_classes_roc_auc_list))
