import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.manifold import TSNE
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
from sklearn import tree
import matplotlib.pyplot as plt
import pandas

data = pandas.read_csv("IFI6057_hw2017_data.txt")

#print(np.array(data.drop("Result", axis=1)), np.array(data["Result"]))
#print()

features = np.array(data.drop("Result", axis=1))
classes = np.array(data["Result"])

clf = tree.DecisionTreeClassifier()
clf.fit(features, classes)

wrong_count = 0
for i, row in enumerate(features):
    prediction = clf.predict(row.reshape(1, -1))
    if prediction != [classes[i]]:
        #print("Failed", i, "features", row, "predicted", prediction[0], "but expected", classes[i])
        wrong_count += 1

#print("Total", len(features), "wrong", wrong_count, "correct", len(features) - wrong_count, "p", (len(features) - wrong_count) / len(features))
#print()

columns = ['method', 'mean', 'std']

#print("Initial")
scores = cross_val_score(clf, features, classes, cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
result = pandas.DataFrame([['initial', scores.mean(), scores.std() * 2]], columns=columns)

#print("Maximizing")
#print("balanced")
grouped_data = data.groupby('Result')
balanced_data = grouped_data.apply(lambda x: x.sample(n=int(min(len(x), grouped_data.size().min()))))
#print(balanced_data.groupby(['Result'], axis=0).size())
balanced_features = np.array(balanced_data.drop("Result", axis=1))
balanced_classes = np.array(balanced_data["Result"])
clf = tree.DecisionTreeClassifier()
scores = cross_val_score(clf, balanced_features, balanced_classes, cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
result = result.append(pandas.DataFrame([['balanced', scores.mean(), scores.std() * 2]], columns=columns))


#X_embedded = TSNE().fit_transform(balanced_features)
#plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=balanced_classes)
#plt.subplot(121)

#print("with PCA & balance")
pca = PCA()
pca.fit(balanced_features)
pca_features_transformed = pca.transform(balanced_features)
#plt.scatter(pca_features_transformed[:, 0], pca_features_transformed[:, 1], c=balanced_classes)
#plt.subplot(122)

#plt.show()
clf = tree.DecisionTreeClassifier()
scores = cross_val_score(clf, pca_features_transformed, balanced_classes, cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
result = result.append(pandas.DataFrame([['PCA&balanced', scores.mean(), scores.std() * 2]], columns=columns))


#print("with PCA")
pca = PCA()
pca.fit(features)
pca_features_transformed = pca.transform(features)
clf = tree.DecisionTreeClassifier()
scores = cross_val_score(clf, pca_features_transformed, classes, cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
result = result.append(pandas.DataFrame([['PCA', scores.mean(), scores.std() * 2]], columns=columns))

#print("with Feature Selection")
p = 0.7
fs = VarianceThreshold(threshold=p*(1-p))
fs.fit(features)
fs_features_transformed = fs.transform(features)
clf = tree.DecisionTreeClassifier(max_depth=7)
scores = cross_val_score(clf, fs_features_transformed, classes, cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
result = result.append(pandas.DataFrame([['Feature Selection', scores.mean(), scores.std() * 2]], columns=columns))

#print("with Feature Selection & balance")
fs = VarianceThreshold(threshold=p*(1-p))
fs.fit(balanced_features)
fs_features_transformed = fs.transform(balanced_features)
clf = tree.DecisionTreeClassifier(max_depth=7)
scores = cross_val_score(clf, fs_features_transformed, balanced_classes, cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
result = result.append(pandas.DataFrame([['Feature Selection & balance', scores.mean(), scores.std() * 2]], columns=columns))

#print('manually removing features')
#print(balanced_data.groupby(['Result'], axis=0).size())
rem_features = np.array(data.drop("Result", axis=1)
                        .drop("popUpWidnow", axis=1)
                        .drop("age_of_domain", axis=1)
                        .drop("having_IP_Address", axis=1))
clf = tree.DecisionTreeClassifier()
scores = cross_val_score(clf, rem_features, classes, cv=5)
#print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))
result = result.append(pandas.DataFrame([['manual mod features', scores.mean(), scores.std() * 2]], columns=columns))

print(result)
