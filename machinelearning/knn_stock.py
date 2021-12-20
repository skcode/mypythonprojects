# Data Manipulation
import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
# Plotting graphs
import matplotlib.pyplot as plt
#from pandas.plotting import register_matplotlib_converters
# Machine learning libraries
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Data fetching



#register_matplotlib_converters()
# Read the data from Yahoo
stock='BTC-USD'
start_date = '2010-01-01'
end_date = '2021-12-31'

df = data.DataReader(stock, 'yahoo', start_date, end_date)
#df= pdr.get_data_yahoo(stock, '2012-01-01', '2017-01-01')

df = df.dropna()
df = df[['Open', 'High', 'Low','Close']]
df.head()
# Predictor variables
df['Open-Close']= 100*(df.Open -df.Close)/df.Open
df['High-Low']  = 100*(df.High - df.Low)/df.Low
df['LastReturn']  = 100*(df.Close - df.Close.shift(1))/df.Close.shift(1)
df['LastReturn2']  = 100*(df.Close.shift(1) - df.Close.shift(2))/df.Close.shift(2)
df['LastReturn3']  = 100*(df.Close.shift(2) - df.Close.shift(3))/df.Close.shift(3)
df =df.dropna()
X= df[['Open-Close', 'High-Low','LastReturn','LastReturn2','LastReturn3']]
X.head()
# Target variable
Y= np.where(df['Close'].shift(-1)>df['Close']*1.00,1,0)#1 quando supera dell'% il g precedente
# Splitting the dataset
#75 / 25 train test split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=0,train_size=0.80,test_size=0.20)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.25, random_state=0)
#split_percentage = 0.7
#split = int(split_percentage*len(df))

#X_train = X[:split]
#Y_train = Y[:split]

#X_test = X[split:]
#Y_test = Y[split:]


# we must apply the scaling to the test set that we computed for the training set
from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
X_val = scaler.transform(X_val)

# Instantiate KNN learning model(k=15)
best=[-1,-1,-1]
for i in range(10,300):
  knn = KNeighborsClassifier(n_neighbors=i)

  # fit the model
  knn.fit(X_train, Y_train)

  # Accuracy Score
  accuracy_train = accuracy_score(Y_train, knn.predict(X_train))
  accuracy_test = accuracy_score(Y_val, knn.predict(X_val))
  if accuracy_test>best[2]:
    best=[i,accuracy_train,accuracy_test]
  #print('k=',i)
  #print ('Train_data Accuracy: %.2f' %accuracy_train)
  #print ('Test_data Accuracy: %.2f' %accuracy_test)
print('best:',best)
print('test set accuracy:',accuracy_score(Y_test, knn.predict(X_test)))

knn = KNeighborsClassifier(n_neighbors=best[0])

# fit the model
knn.fit(X_train, Y_train)
# Predicted Signal
df=df[-len(X_test):]
df['Predicted_Signal'] = knn.predict(X_test)

# SPY Cumulative Returns
df['stock_returns'] = np.log(df['Close']/df['Close'].shift(1))
Cumulative_SPY_returns = df[:]['stock_returns'].cumsum()*100

# Cumulative Strategy Returns
df['Startegy_returns'] = df['stock_returns']* df['Predicted_Signal'].shift(1)
Cumulative_Strategy_returns = df[:]['Startegy_returns'].cumsum()*100

# Plot the results to visualize the performance

plt.figure(figsize=(10,5))
plt.plot(Cumulative_SPY_returns, color='r',label = 'stock Returns')
plt.plot(Cumulative_Strategy_returns, color='g', label = 'Strategy Returns')
plt.legend()
plt.show()