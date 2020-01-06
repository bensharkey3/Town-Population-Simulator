import random
import pandas as pd
import matplotlib
%matplotlib inline


class Person:
    def __init__(self, ID, parent_ID):
        self.ID = ID
        self.parent_ID = parent_ID
        self.DOB = year
        self.DOD = None
        
    @property
    def age(self):
        if self.DOD != None:
            return self.DOD - self.DOB
        else:
            return year - self.DOB
        
    @property
    def productive_output(self):
        if self.DOD != None:
            return 0
        else:
            return productive_output_at_age[self.age]
        
    @property
    def productive_usage(self):
        if self.DOD != None:
            return 0
        else:
            return 0.25

    def reproduce(self):
        '''Person object has a baby, baby is stored as a new Person in obj_list'''
        ID = obj_list[-1].ID + 1
        parent_ID = self.ID
        obj_list.append(Person(ID, parent_ID))

        
def productivity():
    '''creates productive_output_at_age dict'''
    r1 = list(range(0,16))
    l1 = [0.0625]*15
    lr1 = [r1*l1 for r1,l1 in zip(r1,l1)]
    r2 = list(reversed(range(0,35)))
    l2 = [0.0286]*34
    lr2 = [r2*l2 for r2,l2 in zip(r2,l2)]
    prodout = [0]*15 + lr1 + [1]*11 + lr2 + [0]*46
    productive_output_at_age = dict(zip(list(range(0,121)), prodout))
    return productive_output_at_age


def probabilities(prob_baby_scale_factor=1):
    '''creates probability dicts'''
    # probability of dying at age dict
    prob = [0.01] * 1 + [0.001] * 40 + [0.002] * 10 + [0.008] * 10 + [0.012] * 10 + [0.025] * 10 + [0.05] * 5 + [0.1] * 5 + [0.2] * 5 + [0.25] * 15 + [0.35] * 6 + [0.5] * 3 + [1] * 1
    prob_death_at_age = dict(zip(list(range(0,121)), prob))
    # probability of having a baby at age dict     # min age=18, max age=40
    prob = [0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.13, 0.155, 0.165, 0.172, 0.175, 0.172, 0.165, 0.155, 0.13, 0.1, 0.075, 0.05, 0.04, 0.03, 0.02, 0.01]
    prob_baby_at_age = dict(zip(list(range(0,121)), [0]*18 + prob + [0]*80))
    # scaling probability of having a baby at age dict
    prob_baby_at_age.update((x , y*prob_baby_scale_factor) for x, y in prob_baby_at_age.items())
    return prob_death_at_age, prob_baby_at_age



# run simulation
print('Welcome to the game!')
input('Press enter to continue:  ')


# initialise the first 10 person objects
year = 0
p0 = Person(0,None)
p1 = Person(1,None)
p2 = Person(2,None)
p3 = Person(3,None)
p4 = Person(4,None)
p5 = Person(5,None)
p6 = Person(6,None)
p7 = Person(7,None)
p8 = Person(8,None)
p9 = Person(9,None)
obj_list = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9]


# initialise the record keeping list of dicts
statslist = [{'year': 0, 'population': len(obj_list), 'born': 0, 'died': 0,'average age':round(sum(i.age for i in obj_list) / len(obj_list)), 'productive output': 0, 'productive usage': 0}]


playing = 'y'

while playing == 'y':
    
    # add years
    yearsadd = int(input('Run for how many more years? (enter between 1-50 years):  '))
    prob_baby_scale_factor = float(input('Enter growth factor (enter between 0-1):  '))
    endyear = year + yearsadd
    
    # return probabilities and productivity from function
    prob_death_at_age, prob_baby_at_age = probabilities(prob_baby_scale_factor)
    productive_output_at_age = productivity()
    
    print('prob baby scale factor {}'.format(prob_baby_scale_factor))
    print('prob baby at age 28 {}'.format(prob_baby_at_age[28]))
    

    while year < endyear:
        year += 1

        ## people that died in the year
        # create a list of only living people. excludes those that have a DOD
        obj_list_alive = [x for x in obj_list if x.DOD == None]

        # did the person die? if so update DOD to the current year
        prob_death_obj = [prob_death_at_age[x] for x in [i.age for i in obj_list_alive]]
        died_in_year_bool = [x > y for x, y in zip(prob_death_obj, [random.random() for i in obj_list_alive])]
        died_in_year_obj = [x for x, y in zip(obj_list_alive, died_in_year_bool) if y == True]
        for obj in died_in_year_obj: obj.DOD = year

        # update list of only living people. excludes those that have a DOD
        obj_list_alive = [x for x in obj_list if x.DOD == None]
            
            
        ## people that had babies in the year
        # did the person have a baby? if so run reproduce method
        prob_baby_obj = [prob_baby_at_age[x] for x in [i.age for i in obj_list_alive]]
        baby_in_year_bool = [x > y for x, y in zip(prob_baby_obj, [random.random() for i in obj_list_alive])]
        baby_in_year_obj = [x for x, y in zip(obj_list_alive, baby_in_year_bool) if y == True]
        for i in baby_in_year_obj[:len(baby_in_year_obj)]:
            i.reproduce()
        
        # update list of only living people. excludes those that have a DOD
        obj_list_alive = [x for x in obj_list if x.DOD == None]
        
        
        # write stats for the year to output table
        # anything that needs to be done at the end of each year, do here
        print('year: {}, population: {}, born {}, died {}, productive output {}, productive usage {}'.format(year, len(obj_list_alive), len(baby_in_year_obj), len(died_in_year_obj), round(sum(i.productive_output for i in obj_list_alive)), round(sum(i.productive_usage for i in obj_list_alive))))
        dictyr = {'year': year, 'population': len(obj_list_alive), 'born': len(baby_in_year_obj), 'died': len(died_in_year_obj), 'average age':round(sum(i.age for i in obj_list_alive) / len(obj_list_alive)), 'productive output': round(sum(i.productive_output for i in obj_list_alive)), 'productive usage': round(sum(i.productive_usage for i in obj_list_alive))}
        statslist.append(dictyr)
        
    # enter end of period stats here
    # anything that needs to be done at the end of each run period, do here
    print('Statistics at the end of year {}'.format(year))
    df = pd.DataFrame(statslist)
    df = df[['year', 'population', 'born', 'died', 'average age', 'productive output', 'productive usage']]
    df[['population', 'born', 'died']].plot()
    df[['productive output', 'productive usage']].plot()
    df[['average age']].plot()

    
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
            
            
## TO DO
# charts on current pop, born, died, average age, % in age demographic bins
# excess productive output creates extra productive capacity
# shortage of productive output creates declining population
# exit game once population == 0
# display charts at the end of each cycle
# add average age
# create horizontal bar chart to show demographic distribution
