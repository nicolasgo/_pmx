'''confusion matrix related files
   created by Robert Kruhlak
'''
## use floating point division always (ie matlab, python 3.x)
from __future__ import division

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt

def confusion_matrices( results_dict):
    '''generate a dict of confusion matrices from
       Inputs: result_dict, dict with algorithm keys, and values are 
                           y_array, list/array of category arrays
                           result_array, list/array of run_cv results
    '''
    
    confusion_matrices = { key : confusion_matrix(*values) 
                           for key, values in results_dict.items() }
    
    print(confusion_matrices)
    for title, cm in confusion_matrices.items():
        # Show confusion matrix in a separate window
        plt.matshow(cm)
        plt.title('Confusion matrix: {0}'.format(title))
        plt.colorbar()
        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.show()
