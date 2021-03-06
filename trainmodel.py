# importing required packages
import pandas as pd
from sklearn import tree 
from sklearn.linear_model import LogisticRegression 
from sklearn import metrics
from sklearn.model_selection import train_test_split
import pickle


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
                TRAINING & TESTING MACHINE LEARNING MODEL
"""

# defining input and output to train model
fdf=df[df.columns[1:12]]
fdf1=fdf[fdf.columns[5:9]]
my_cols=list(fdf.columns)
for i in fdf1.columns:
    my_cols.remove(i)
fdf2=fdf[my_cols]
X1=fdf1.to_numpy()
X2=fdf2.to_numpy()
Y=df['Loan_Status'].to_numpy()
X1=X1.astype('int') 
X2=X2.astype('int') 
Y=Y.astype('int') 

#spliting data to train and test sets
x1_train, x1_test, y1_train, y1_test = train_test_split(X1, Y, test_size=0.3, random_state=1)
x2_train, x2_test, y2_train, y2_test = train_test_split(X2, Y, test_size=0.3, random_state=1)


'''  Traiing model   '''
# defining classifier models
dtc = tree.DecisionTreeClassifier()
lrc=LogisticRegression()


# fitting classifiers with x_train as input and y_train as output
lrc= lrc.fit(x1_train, y1_train)
dtc= dtc.fit(x2_train, y2_train)


'''  testing accuracy of model   '''
# storing model's output
y1_pred = lrc.predict(x1_test)
y2_pred = dtc.predict(x2_test)
Y1_pred = lrc.predict(X1)
Y2_pred = dtc.predict(X2)
Y_pred=[]
for i in range(0,len(Y1_pred)):
   Y_pred.append(Y1_pred[i] or Y2_pred[i])


# checking model's ouput accuracy 
print('\n',"The Accuracy of regression model for test data: ",metrics.accuracy_score(y1_test, y1_pred),'\n')
print('\n',"The Accuracy of decision tree model for test data: ",metrics.accuracy_score(y2_test, y2_pred),'\n')

print('\n',"The Accuracy of regression model for entire train.csv data: ",metrics.accuracy_score(Y, Y1_pred),'\n')
print('\n',"The Accuracy of decision tree model for entire train.csv data: ",metrics.accuracy_score(Y, Y2_pred),'\n')

print('\n',"The Accuracy of both models combined for entire train.csv  data: ",metrics.accuracy_score(Y, Y_pred),'\n')



'''
                USING THE MODEL TO PREDICT LOAN APPROVAL
'''

# importing DATA file
df = pd.read_csv("predict.csv")
cdf=df.copy() # making a copy of the DataFrame
#print("The shape of Input DataFrame: ",df.shape, '\n')
#print("The list of columns in Input DataFrame: ",list(df), '\n')


''' preprocessing input data '''
def preprocessInput(df):
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
    fdf1=fdf[fdf.columns[5:9]]
    my_cols=list(fdf.columns)
    for i in fdf1.columns:
        my_cols.remove(i)
    fdf2=fdf[my_cols]
    X1=fdf1.to_numpy()
    X2=fdf2.to_numpy()
    return X1, X2

X1, X2 = preprocessInput(df)


''' Predicting output '''
# storing model's output
y1_pred = lrc.predict(X1)
y2_pred = dtc.predict(X2)
y_pred=[]
for i in range(0,len(y1_pred)):
   y_pred.append(y1_pred[i] or y2_pred[i])

# preparing DataFrame with both input and output
d=keys["Loan_Status"]
''' Exporting data with Loan_Status column '''
cdf.dropna(subset=['LoanAmount','Loan_Amount_Term'], inplace=True)
inv_d = {v: k for k, v in d.items()}
l1=[]
for i in y_pred:
    l1.append(inv_d[i])
cdf["Loan_Status"]=l1

# creating a csv file with the Loan Approval Status  
cdf.to_csv('output.csv')
print("The output of 'predict.csv' is stored in 'output.csv' file.")


# exporting the trained models
filename1 = 'finalized_model1.sav'
filename2 = 'finalized_model2.sav'
pickle.dump(lrc, open(filename1, 'wb'))
pickle.dump(dtc, open(filename2, 'wb'))
