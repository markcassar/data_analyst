import numpy
import pandas
import statsmodels.api as sm
from patsy import dmatrices
from sklearn import linear_model, svm

def custom_heuristic(file_path):
    '''
    You are given a list of Titantic passengers and their associated
    information. More information about the data can be seen at the link below:
    http://www.kaggle.com/c/titanic-gettingStarted/data

    For this exercise, you need to write a custom heuristic that will take
    in some combination of the passenger's attributes and predict if the passenger
    survived the Titanic diaster.

    Can your custom heuristic beat 80% accuracy?
    
    The available attributes are:
    Pclass          Passenger Class
                    (1 = 1st; 2 = 2nd; 3 = 3rd)
    Name            Name
    Sex             Sex
    Age             Age
    SibSp           Number of Siblings/Spouses Aboard
    Parch           Number of Parents/Children Aboard
    Ticket          Ticket Number
    Fare            Passenger Fare
    Cabin           Cabin
    Embarked        Port of Embarkation
                    (C = Cherbourg; Q = Queenstown; S = Southampton)
                    
    SPECIAL NOTES:
    Pclass is a proxy for socioeconomic status (SES)
    1st ~ Upper; 2nd ~ Middle; 3rd ~ Lower

    Age is in years; fractional if age less than one
    If the age is estimated, it is in the form xx.5

    With respect to the family relation variables (i.e. SibSp and Parch)
    some relations were ignored. The following are the definitions used
    for SibSp and Parch.

    Sibling:  brother, sister, stepbrother, or stepsister of passenger aboard Titanic
    Spouse:   husband or wife of passenger aboard Titanic (mistresses and fiancees ignored)
    Parent:   mother or father of passenger aboard Titanic
    Child:    son, daughter, stepson, or stepdaughter of passenger aboard Titanic
    
    Write your prediction back into the "predictions" dictionary. The
    key of the dictionary should be the passenger's id (which can be accessed
    via passenger["PassengerId"]) and the associating value should be 1 if the
    passenger survvied or 0 otherwise. 

    For example, if a passenger is predicted to have survived:
    passenger_id = passenger['PassengerId']
    predictions[passenger_id] = 1

    And if a passenger is predicted to have perished in the disaster:
    passenger_id = passenger['PassengerId']
    predictions[passenger_id] = 0
    
    You can also look at the Titantic data that you will be working with
    at the link below:
    https://www.dropbox.com/s/r5f9aos8p9ri9sa/titanic_data.csv
    '''

    predictions = {}
    df = pandas.read_csv(file_path)
    age_med = numpy.median(df['Age'])
    fare_med = numpy.median(df['Fare'])
    df['Gender'] = df['Sex'].map( {'female':0, 'male':1} )
    
    median_ages = numpy.zeros( (2,3) )

    for i in range(0,2):
        for j in range(0,3):
            median_ages[i,j] = df[ (df['Gender'] == i) & (df['Pclass'] == j + 1) ]['Age'].dropna().median()

    df['AgeFill'] = df['Age']   


    for i in range(0,2):
        for j in range(0,3):
            df.loc[ (df['Age'].isnull() ) & (df['Gender'] == i) & 
                        (df['Pclass'] == j + 1), 'AgeFill'] = median_ages[i,j]

    df['AgeFillPclass'] = df['AgeFill'] * df['Pclass']

    vars = [ 'Gender','Pclass', 'Fare', 'SibSp', 'AgeFillPclass']

#    clf = svm.SVC()
#    clf.fit(df[vars], df['Survived'])
    
    for passenger_index, passenger in df.iterrows():
        passenger_id = passenger['PassengerId']
#        predictions[passenger_id] = (clf.predict(passenger[vars]))
        if ((passenger['Sex'] == 'female') \
                & ((passenger['Pclass'] ==1) | (passenger['Pclass'] == 2))):
            predictions[passenger_id] = 1
        elif ((passenger['Sex'] == 'female') & (passenger['Pclass'] == 3) & ((passenger['SibSp'] + \
               passenger['Parch']) == 0) ): 
            predictions[passenger_id] = 1
        elif ( ("Dr" in passenger['Name']) | ('Master' in passenger['Name']) ):
            predictions[passenger_id] = 1
        else:
            predictions[passenger_id] = 0
         
    return predictions