import sys
sys.path.append('../fashion-mnist/utils')
from sklearn.neural_network import MLPClassifier
import os
import glob
from sklearn.externals import joblib
import mnist_reader
import numpy as np
from scipy.misc import imread

train_new = True

classifier_path = 'classifiers'
classifier_description_file = 'description.txt'
unlabeled_data_path = 'unlabeled_data/*.bmp'
data_base_path = os.path.join('..', 'fashion-mnist', 'data', 'fashion')
new_file_index = len(os.listdir(classifier_path)) + 1
load_file_index = None

label_map = ['T-shirt/top', 'Trouser',
             'Pullover', 'Dress', 'Coat',
             'Sandal', 'Shirt', 'Sneaker',
             'Bag', 'Ankle boot']

if train_new:
    X_train, y_train = mnist_reader.load_mnist(data_base_path, kind='train')
    X_test, y_test = mnist_reader.load_mnist(data_base_path, kind='t10k')

    X_train = X_train / 255.0
    X_test = X_test / 255.0

    layers = (32, 32, 32)
    activation = 'relu'
    clf = MLPClassifier(max_iter=200,
                        hidden_layer_sizes=layers, random_state=1, activation=activation, tol=10e-6, verbose=True)

    clf.fit(X_train, y_train)

    score = clf.score(X_test, y_test)
    print(score)
    clf_file = os.path.join(classifier_path, 'classifier_{}.pkl'.format(new_file_index))
    joblib.dump(clf, clf_file)
    with open(classifier_description_file, 'a') as f:
        f.write("{} {} iterations {} score {} layers {} activation {} loss {} best loss\n".format(clf_file, clf.n_iter_, score, layers, activation, clf.loss_, clf.best_loss_))
else:
    clf = joblib.load(os.path.join(classifier_path, 'classifier_{}.pkl'.format(load_file_index if load_file_index is not None else new_file_index - 1)))

for file in glob.glob(unlabeled_data_path):
    bla = imread(file, mode='L')
    X = np.reshape(bla, (1,28*28)) / 255.0
    result = clf.predict(X)
    print("Image {} is predicted as {}={}".format(file, result, label_map[int(result)]))
