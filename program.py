# importing required packages
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn import metrics
from sklearn.model_selection import train_test_split


# importing data as DataFrame
df = pd.read_csv("train.csv")
#print("Initial shape of train-test data: ",df.shape,'\n') 
#print("The list of columns in DataFrame: ",list(df),'\n')


"""
                DATA PREPROCESSING
"""

# changing the type of the CoapplicantIncome values
for i in df['CoapplicantIncome']:
    df['CoapplicantIncome'].replace([i], int(i))


# Credit_History setting nan to 2.0
l1=[]
for i in df['Credit_History']:
    if i==1.0 or i==0.0:
        l1.append(i)
    else:
        l1.append(2.0)
l1=pd.DataFrame(l1)
l1.columns=['Credit_History']
df.update(l1) 


keys={} # contains all the keys generated by below function
# function to replace string values to numeric for traiing 
def numberRep(s):
    ul=[ x for x in df[s].unique()]
    d={x: ul.index(x) for x in ul}
    keys[s]=d
    l1=[]
    for i in df[s]:
        l1.append(ul.index(i))
    l1=pd.DataFrame(l1)
    l1.columns=[s]
    df.update(l1)
    
numberRep('Gender')
numberRep('Married')
numberRep('Education')
numberRep('Self_Employed')
numberRep('Dependents')
numberRep('Property_Area')
numberRep('Loan_Status')


# Deleting rows with empty LoanAmount or Loan_Amount_term values
df.dropna(subset=['LoanAmount','Loan_Amount_Term'], inplace=True)
#print("Shape of DataFrame after preprocessing: ",df.shape,'\n')        


"""
                TRAINING & TESTING DECISION TREE MODEL
"""

# defining input and output to train model
fdf=df[df.columns[1:12]]
X=fdf.to_numpy()
Y=df['Loan_Status'].to_numpy()
X=X.astype('int') # god knows why, it was giving TypeError without this
Y=Y.astype('int') # same as above

#spliting data to train and test sets
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.4, random_state=1)


'''  Traiing model   '''
# defining Decision Tree classifier 
dtc = tree.DecisionTreeClassifier()

# fitting classifier with x_train as input and y_train as output
dtc= dtc.fit(x_train, y_train)


'''  testing accuracy of model   '''
# storing model's output in y_pred
y_pred = dtc.predict(x_test)

# checking model's ouput accuracy 
print('\n',"The Accuracy of trained model: ",metrics.accuracy_score(y_test, y_pred),'\n')


"""
                USING THE MODEL TO PREDICT LOAN APPROVAL
"""

# importing DATA file
df = pd.read_csv("test.csv")
cdf=df # making a copy of the DataFrame
#print("The shape of Input DataFrame: ",df.shape, '\n')
#print("The list of columns in Input DataFrame: ",list(df), '\n')


''' preprocessing input data '''
# changing the type of the CoapplicantIncome values
for i in df['CoapplicantIncome']:
    df['CoapplicantIncome'].replace([i], int(i))

 # Credit_History setting nan to 2.0
l1=[]
for i in df['Credit_History']:
    if i==1.0 or i==0.0:
        l1.append(i)
    else:
        l1.append(2.0)
l1=pd.DataFrame(l1)
l1.columns=['Credit_History']
df.update(l1) 

 # replace string values to numeric
def useNumberRep(k):
    for i in k:
        if i=="Loan_Status":
            continue
        d=k[i]
        l1=[]
        for j in df[i]:
            l1.append(d[j])
        l1=pd.DataFrame(l1)
        l1.columns=[i]
        df.update(l1)
        
useNumberRep(keys)
    
# Deleting rows with empty LoanAmount or Loan_Amount_term values
df.dropna(subset=['LoanAmount','Loan_Amount_Term'], inplace=True)
#print("The shape of Input DataFrame after preprocessing: ",df.shape,'\n') 

# defining input
fdf=df[df.columns[1:12]]
X=fdf.to_numpy()
X=X.astype('int')


''' Predicting output '''
# storing model's output in y_pred
y_pred = dtc.predict(X)

print("The Output of the model for the Input DataFrame: ",y_pred, '\n')
d=keys["Loan_Status"]
print("Output key: ",d,'\n')


''' Exporting data with Loan_Status column '''
cdf.dropna(subset=['LoanAmount','Loan_Amount_Term'], inplace=True)
inv_d = {v: k for k, v in d.items()}
l1=[]
for i in y_pred:
    l1.append(inv_d[i])
cdf["Loan_Status"]=l1

# creating a csv file with the Loan Approval Status  
cdf.to_csv('output.csv')
print("The output is stored in 'output.csv' file.")

