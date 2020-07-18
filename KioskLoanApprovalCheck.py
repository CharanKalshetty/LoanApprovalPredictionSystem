# packages
import pickle
from trainmodel import keys
import pandas as pd


# importing trained model
filename = 'finalized_model1.sav'
lrc = pickle.load(open(filename, 'rb'))
filename = 'finalized_model2.sav'
dtc = pickle.load(open(filename, 'rb'))


def removeNan(d):
    lk=[i for i in d]
    for i in d.keys():
        if type(i)==float:
            j=lk.index(i)
            lk[j]="Other"
    lv=[i for i in d.values()]
    for i in range(0,len(lk)):
        print(lk[i],": ",lv[i])
    return lk,lv
  

"""
             INPUTING
 """
 
x1=[]
x2=[]
print("Loan Approval Check",'\n')
print("=====================", '\n')

# Gender
d=keys['Gender']
print('Gender / Sex ')
print('-------------')
lk,lv=removeNan(d)
x2.append(int(input("Enter the number corresponding to your answer: ")))
print('\n')

# Marital Status
d=keys['Married']
print('Married')
print('-------')
lk,lv=removeNan(d)
x2.append(int(input("Enter the number corresponding to your answer: ")))
print('\n')

# number of dependents
d=keys['Dependents']
print('Number of Dependents')
print('--------------------')
lk,lv=removeNan(d)
x2.append(int(input("Enter the number corresponding to your answer: ")))
print('\n')

# Education
d=keys['Education']
print('Education')
print('---------')
lk,lv=removeNan(d)
x2.append(int(input("Enter the number corresponding to your answer: ")))
print('\n')

# Self Employed
d=keys['Self_Employed']
print('Self Employed')
print('-------------')
lk,lv=removeNan(d)
x2.append(int(input("Enter the number corresponding to your answer: ")))
print('\n')

# Applicant Income
print('Applicant Income')
print('----------------')
x1.append(int(input("Enter the Applicant's per month Income: ")))
print('\n')

# Coapplicant Income
print('Coapplicant Income')
print('------------------')
x1.append(int(input("Enter Co-Applicant's per month Income: ")))
print('\n')

# Loan Amount
print('Loan Amount')
print('-----------')
x1.append(int(input("Enter the Loan mount in thousands (eg: 20, means 20 thousands): ")))
print('\n')

# Loan Amount Term
print('Loan Amount Term')
print('----------------')
x1.append(int(input("Enter the Term of the Loan in months: ")))
print('\n')

# Credit History
print('Credit History')
print('--------------')
print("meets guidelines: 1")
print("does not meet guidelines: 0")
x2.append(int(input("Enter the number corresponding to your answer: ")))
print('\n')

# Property Area
d=keys['Property_Area']
print('Property Area')
print('-------------')
lk,lv=removeNan(d)
x2.append(int(input("Enter the number corresponding to your answer: ")))
print('\n')


"""
                    PREDICTING
"""

X1=[]
X2=[]
X1.append(x1)
X1=pd.DataFrame(X1)
X1=X1.to_numpy()
X1=X1.astype(int)
X2.append(x2)
X2=pd.DataFrame(X2)
X2=X2.to_numpy()
X2=X2.astype(int)
y1=lrc.predict(X1)
y2=dtc.predict(X2)
y=[]
for i in range(0,len(y1)):
    y.append(y1[i] or y2[i])
d={v: k for k, v in keys['Loan_Status'].items()}
print("Loan Approved: ",d[y[0]])
