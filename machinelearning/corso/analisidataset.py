import numpy as np
import pandas as pd
import sklearn.metrics
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris_dataset = load_iris()
names = iris_dataset['target_names']
data = pd.DataFrame(data=iris_dataset['data'], columns=iris_dataset['feature_names'])
data = pd.concat([data, pd.DataFrame(data=iris_dataset['target'], columns=['species'])], axis=1)
print(data)

####prove
print(data.sample(frac=.8, random_state=0))
print([(lambda x: names[x])(x) for x in data.species.unique()])
mask = data['sepal length (cm)'] > data['sepal length (cm)'].mean()
print(data.where(data['sepal length (cm)'] > data['sepal length (cm)'].mean()).dropna())
print(data[mask])
prova = pd.DataFrame({'colore': ['giallo', 'rosso', 'verdone'], 'taglia': ['L', 'XL', 'S']})
print(prova)
prova = pd.get_dummies(prova, columns=['colore'])
prova['taglia'] = prova['taglia'].map({'S': 0, 'M': 1, 'L': 2, 'XL': 3})
print(prova)
####
# ora normalizzo i dati e trasformo in matrixi numpy
datacpy = data.sample(frac=1, random_state=0)  # faccio lo shuffle dei dati, randomizzando le posizioni
X = datacpy.drop(labels='species', axis=1)  # tolgo l'ultima colonna delle labels
Y = datacpy['species']
X_norm = (X - X.mean()) / X.std()
print(X_norm)
X_norm = np.array(X_norm)
Y = np.array(Y)
Y = Y.reshape(Y.shape[0], 1)
# split dataset
dslen = Y.shape[0]
train_pct, valid_pct, test_pct = 0.6, 0.2, 0.2
train_len = int(np.floor(train_pct * dslen))
valid_len = int(np.floor(valid_pct * dslen))
test_len = dslen - train_len - valid_len
print(train_len, valid_len, test_len)
X_train = X_norm[0:train_len]
X_val = X_norm[train_len:train_len + valid_len]
X_test = X_norm[train_len + valid_len:]
Y_train = Y[0:train_len]
Y_val = Y[train_len:train_len + valid_len]
Y_test = Y[train_len + valid_len:]
##

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score  # R2 è un MSE standardizzato, migliore quanto più si avvicina ad 1

#metodo minimi quadrati

#approssimazione lineare
lr = LinearRegression()
lr.fit(X_train, Y_train)
Y_pred = lr.predict(X_test)
print("MSE=", mean_squared_error(Y_test, Y_pred))
print("R2=", r2_score(Y_test, Y_pred))

from sklearn.preprocessing import PolynomialFeatures

# quadratica
poly = PolynomialFeatures(degree=2)
X2_train = poly.fit_transform(X_train)
X2_test = poly.fit_transform(X_test)
lr.fit(X2_train, Y_train)
Y_pred = lr.predict(X2_test)
print("MSE=", mean_squared_error(Y_test, Y_pred))
print("R2=", r2_score(Y_test, Y_pred))

# cubica
poly = PolynomialFeatures(degree=3)
X3_train = poly.fit_transform(X_train)
X3_test = poly.fit_transform(X_test)
lr.fit(X3_train, Y_train)
Y_pred = lr.predict(X3_test)
print("MSE=", mean_squared_error(Y_test, Y_pred))
print("R2=", r2_score(Y_test, Y_pred))

#KNN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
knn=KNeighborsClassifier(n_neighbors=10)
knn.fit(X_train,np.reshape(Y_train,newshape=(len(Y_train),)))
Y_pred=knn.predict(X_test)
print("accuracy: ",accuracy_score(y_true=Y_test,y_pred=Y_pred))

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
n_clusters=3
kmeans=KMeans(n_clusters=n_clusters)
kmeans.fit(X_train)
kmeans.predict(X_test)
labels_k = kmeans.labels_
score_k = silhouette_score(X_train, labels_k)
print("Tested kMeans with k = %d\tSS: %5.4f" % (n_clusters, score_k))
