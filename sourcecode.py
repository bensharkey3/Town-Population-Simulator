import pandas as pd
import numpy as np
import matplotlib as plt
import random
import os

print('Welcome to the game!')
input('Press enter to continue:  ')
print('')
print('- This is a population simulator for a fictional town.')
print('- The town starts with 20 people. With each year that passes, babies will be born and people will die.')
print('- Females can have a baby at any age between 18 and 40, but are most likely to give birth a in their late 20s.')
print('- People can die at any age, but more likely as they get older.')
print('- Names will be randomly assigned based on names in USA datasets.')
print('- Surnames are inherited from the mother.')
print('')
print('loading...')

# read in surnames from data source
# snlist = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/most-common-name/surnames.csv', nrows=20)['name'].tolist()
snlist = ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER', 'DAVIS', 'GARCIA', 'RODRIGUEZ', 'WILSON', 'MARTINEZ', 'ANDERSON', 'TAYLOR', 'THOMAS', 'HERNANDEZ', 'MOORE', 'MARTIN', 'JACKSON', 'THOMPSON', 'WHITE']

# read in first names from data source
fnlistcsv = pd.read_csv('https://raw.githubusercontent.com/MatthiasWinkelmann/firstname-database/master/firstnames.csv', delimiter=';')

# select only relevent data
fnlist = fnlistcsv
fnlist = fnlist[fnlist['U.S.A.'].notnull()][['name', 'gender', 'U.S.A.']].rename(columns={'U.S.A.':'Freq'})
fnlist['Freq'] = fnlist['Freq'].astype(int)

# clean gender values
fnlist.replace({'1F': 'F', '?F': 'F', '1M': 'M', '?M': 'M'}, inplace=True)
fnlist = fnlist[fnlist['gender'].isin(['F', 'M'])]

# apply factors to 'Freq' column to represent popularity
fnlist['Freq'] = (10-(fnlist[['Freq']]*-1+1))**3
fnlistm = fnlist[fnlist['gender'] == 'M'].sort_values('Freq', ascending=False).reset_index(drop=True)
fnlistf = fnlist[fnlist['gender'] == 'F'].sort_values('Freq', ascending=False).reset_index(drop=True)
fnlistm = fnlistm.reindex(fnlistm.index.repeat(fnlistm['Freq']))['name'].tolist()
fnlistf = fnlistf.reindex(fnlistf.index.repeat(fnlistf['Freq']))['name'].tolist()

town = input('Enter the name of your town:  ')

FirstName = []
for i in range(20):
    FirstName.append(random.choice(fnlistf))

MiddleName = []
for i in range(20):
    MiddleName.append(random.choice(fnlistf))
    
# create dataframe
data = {'FirstName':FirstName, 'MiddleName':MiddleName, 'Surname':snlist, 'Sex':'F', 'YearBorn':list(range(0,20))}
df = pd.DataFrame(data)

# add columns
year = 19
df['YearDeceased'] = np.nan
df['CurrentYear'] = year
df['Age'] = (df[['CurrentYear','YearDeceased']].min(axis=1) - df['YearBorn']).astype(int)
df['ParentID'] = np.nan
df['Generation'] = 1
df['NoOfChildren'] = 0

# probability of dying at age
# manually enter probablities
prob = [0.001] * 40 + [0.002] * 10 + [0.008] * 10 + [0.012] * 10 + [0.025] * 10 + [0.05] * 5 + [0.1] * 5 + [0.2] * 5 + [0.25] * 15 + [0.35] * 6 + [0.5] * 3 + [1] * 1
data = {'Age':list(range(1,121)), 'Prob':prob} 
probdeath = pd.DataFrame(data)

# probability of having a baby at age
# min age=18, max age=40. manually enter probablities
# rapid growth
data = {'Age':list(range(18,40)), 'Prob':[0.02, 0.04, 0.06, 0.08, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.4, 0.35, 0.3, 0.25, 0.2, 0.15, 0.1, 0.08, 0.06, 0.04, 0.02]} 
probbabyRG = pd.DataFrame(data)
# neutral growth
data = {'Age':list(range(18,40)), 'Prob':[0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.13, 0.155, 0.19, 0.215, 0.215, 0.19, 0.155, 0.13, 0.1, 0.075, 0.05, 0.04, 0.03, 0.02, 0.01]} 
probbabyNU = pd.DataFrame(data)
# moderate decline
data = {'Age':list(range(18,40)), 'Prob':[0.007, 0.015, 0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.12, 0.16, 0.21, 0.21, 0.16, 0.12, 0.1, 0.07, 0.05, 0.04, 0.03, 0.02, 0.015, 0.007]} 
probbabyMD = pd.DataFrame(data)

playing = 'y'

while playing == 'y':

    # add years
    yearsadd = int(input('Run for how many more years? (enter between 1-50 years):  '))
    probbabyint = int(input('At what population growth rate? (1=rapid growth, 2=neutral, 3=moderate decline):  '))

    if probbabyint == 1:
        probbaby = probbabyRG
    elif probbabyint == 2:
        probbaby = probbabyNU
    elif probbabyint == 3:
        probbaby = probbabyMD
    else:
        print('incorrect input!')
    
    endyear = year + yearsadd

    while year < endyear:
        year += 1
        df['CurrentYear'] = year
        df['Age'] = np.where(df['YearDeceased'].isnull(), (df['CurrentYear'] - df['YearBorn']), (df['YearDeceased'] - df['YearBorn'])).astype(int)

        # did anyone die? if so enter in YearDeceased
        temp1 = df[df['YearDeceased'].isnull()].reset_index().merge(probdeath).set_index('index')[['Prob']]
        temp1['rand'] = [random.random() for i in temp1.index]
        temp1['YearDeceased1'] = np.where(temp1['rand'] < temp1['Prob'], year, np.nan)
        temp1.drop(columns={'Prob', 'rand'}, inplace=True)
        df = pd.concat([df, temp1], axis=1)
        df['YearDeceased'] = np.where(df['YearDeceased'].isnull() == True, df['YearDeceased1'], df['YearDeceased'])
        df.drop(columns={'YearDeceased1'}, inplace=True)

        # did anyone have a baby? if so enter new row for each
        babies = df[(df['YearDeceased'].isnull()) & (df['Sex'] == 'F')].reset_index().merge(probbaby, on='Age').set_index('index')
        lst = []
        for i in range(babies.shape[0]):
            lst.append(random.random())
        babies['rand'] = lst
        babies['baby?'] = babies['Prob'] > babies['rand']
        babies = babies[babies['baby?']][['Surname', 'Generation']]
        babies['Generation'] += 1

        babies = babies.reset_index().rename(columns={'index':'ParentID'})

        if len(babies) > 0:
            Sex = []
            for i in range(babies.shape[0]):
                Sex.append(random.choice(['F', 'M']))
            babies['Sex'] = Sex

            MFirstName = []
            for i in range(babies.shape[0]):
                MFirstName.append(random.choice(fnlistm))
            babies['MFirstName'] = MFirstName

            MMiddleName = []
            for i in range(babies.shape[0]):
                MMiddleName.append(random.choice(fnlistm))
            babies['MMiddleName'] = MMiddleName

            FFirstName = []
            for i in range(babies.shape[0]):
                FFirstName.append(random.choice(fnlistf))
            babies['FFirstName'] = FFirstName

            FMiddleName = []
            for i in range(babies.shape[0]):
                FMiddleName.append(random.choice(fnlistf))
            babies['FMiddleName'] = FMiddleName

            babies['FirstName'] = np.where(babies['Sex'] == 'F', babies['FFirstName'], babies['MFirstName'])
            babies['MiddleName'] = np.where(babies['Sex'] == 'F', babies['FMiddleName'], babies['MMiddleName'])
            babies.drop(columns={'MFirstName', 'MMiddleName', 'FFirstName', 'FMiddleName'}, inplace=True)

            babies['YearBorn'] = year
            babies['YearDeceased'] = np.nan
            babies['CurrentYear'] = year
            babies['Age'] = 0
            babies['NoOfChildren'] = 0

            babies = babies[['FirstName', 'MiddleName', 'Surname', 'Sex', 'YearBorn', 'YearDeceased', 'CurrentYear', 'Age', 'ParentID', 'Generation', 'NoOfChildren']]
            df = pd.concat([df, babies]).reset_index(drop=True)
            childadd = babies['ParentID'].tolist()
            df['NoOfChildren'] = np.where(df.index.isin(childadd) == True, 1, 0) + df['NoOfChildren']

    csvfileloc = '{}\\TheTownOf{}.csv'.format(os.getcwd(), town)
    df.to_csv(csvfileloc, index=False)
    
    print('')
    print('--------------------------------------------------')
    title = 'Statistics for {} at the end of year {}'.format(town, year)
    print(title)
    print('--------------------------------------------------')
    print('')
    print('Current population: ')
    print(len(df[df['YearDeceased'].isnull()]))
    print('')
    print('All people that ever lived: ')
    print(len(df))
    print('')
    print('A randomly selected living person:')
    alive = df[df['YearDeceased'].isnull()].index.tolist()
    print(df.iloc[random.choice(alive)])
    print('')
    print('Average age: ')
    print(df[df['YearDeceased'].isnull()]['Age'].mean())
    print('')
    print('Average age at death: ')
    print(df[df['YearDeceased'].notnull()]['Age'].mean())
    print('')
    print('Record for oldest person:')
    print(df['Age'].max())
    print('')
    print('Record for most children:')
    print(df[df['NoOfChildren'] == df['NoOfChildren'].max()])
    print('')
    print('Most popular surnames:')
    print(df.groupby('Surname').count()['FirstName'].sort_values(ascending=False))
    print('')
    print('Number of babies born in each year:')
    print(df.groupby('YearBorn')['FirstName'].count().plot())
    print('')
    print('Any duplicate names?')
    temp2 = df.groupby(['FirstName', 'MiddleName', 'Surname']).count().sort_values(by='Sex', ascending=False)[['Sex']].reset_index()
    if len(temp2[temp2['Sex'] > 1]) == 0:
        print('none, everyone has a unique name so far!')
    else:
        print(temp2[temp2['Sex'] > 1].rename(columns={'Sex': 'Count'}))
    print('')
    
    while True:
        playagain = str(input('Keep going? (enter y or n):  '))
        if playagain == 'n':
            input('Thanks for playing! - press enter to exit')
            playing = 'n'
            break
        elif playagain =='y':
            playing = 'y'
            break
        else:
            print('invalid response, please enter y or n')
    

    
# TO DO:
# introduction and explanation text
# add population vs time chart
# try except to validate user input
# figure out how to get charts to show
# add in NoOfGrandchildren
# add in written personal bio
# age demographics histogram by bins
# select birthrate option (rapid growth, moderate growth, stable, rapid contraction, high contraction)
# option to add in an immigrant (female only), enter name and age
# add a file that records aggregated data for each year, population etc
# annual  productivity
# limit list of duplicate names
# clear output after each cycle
# family tree