import random


class Person:
    def __init__(self, ID, parent_ID):
        self.ID = ID
        self.parent_ID = parent_ID
        self.DOB = year
        self.DOD = None
        
    @property
    def age(self):
        if self.DOD == None:
            return year - self.DOB
        else:
            return self.DOD - self.DOB

    def reproduce(self):
        '''Person object has a baby, baby is stored as a new Person in obj_list'''
        ID = obj_list[-1].ID + 1
        parent_ID = self.ID
        obj_list.append(Person(ID, parent_ID))

        
def productivities():
    '''creates productivity dicts'''
    # create productive output by age dict
    r1 = list(range(1,16))
    l1 = [0.0625]*15
    lr1 = [r1*l1 for r1,l1 in zip(r1,l1)]
    r2 = list(reversed(range(1,35)))
    l2 = [0.0286]*34
    lr2 = [r2*l2 for r2,l2 in zip(r2,l2)]
    prodout = [0]*14 + lr1 + [1]*11 + lr2 + [0]*46
    productive_output_at_age = dict(zip(list(range(1,121)), prodout))
    # create productive usage by age dict
    productive_usage_at_age = dict(zip(list(range(1,121)), [0.25]*120))
    return productive_output_at_age, productive_usage_at_age


def probabilities(prob_baby_scale_factor=1):
    '''creates probability dicts'''
    # probability of dying at age dict
    prob = [0.01] * 1 + [0.001] * 40 + [0.002] * 10 + [0.008] * 10 + [0.012] * 10 + [0.025] * 10 + [0.05] * 5 + [0.1] * 5 + [0.2] * 5 + [0.25] * 15 + [0.35] * 6 + [0.5] * 3 + [1] * 1
    prob_death_at_age = dict(zip(list(range(0,121)), prob))
    # probability of having a baby at age dict     # min age=18, max age=40
    prob = [0.01, 0.02, 0.03, 0.04, 0.05, 0.075, 0.1, 0.13, 0.155, 0.19, 0.215, 0.215, 0.19, 0.155, 0.13, 0.1, 0.075, 0.05, 0.04, 0.03, 0.02, 0.01, 0.01]
    prob_baby_at_age = dict(zip(list(range(0,121)), [0]*18 + prob + [0]*80))
    # scaling probability of having a baby at age dict
    prob_baby_at_age.update((x , y*prob_baby_scale_factor)for x, y in prob_baby_at_age.items())
    return prob_death_at_age, prob_baby_at_age



# run simulation
print('Welcome to the game!')
input('Press enter to continue:  ')

# initialise the first person object
obj_list = []
year = 0
p0 = Person(0,None)
obj_list.append(p0)

playing = 'y'

while playing == 'y':
    # add years
    yearsadd = int(input('Run for how many more years? (enter between 1-50 years):  '))
    endyear = year + yearsadd

    while year < endyear:
        year += 1

        ## people that died in the year
        # return probabilities from function
        prob_death_at_age, prob_baby_at_age = probabilities()

        # create a list of only living people. excludes those that have a DOD
        obj_list_alive = [x for x in obj_list if x.DOD == None]

        # did the person die? if so update DOD to the current year
        prob_death_obj = [prob_death_at_age[x] for x in [i.age for i in obj_list_alive]]
        died_in_year_bool = [x > y for x, y in zip(prob_death_obj, [random.random() for i in obj_list_alive])]
        died_in_year_obj = [x for x, y in zip(obj_list_alive, died_in_year_bool) if y == True]
        for obj in died_in_year_obj: obj.DOD = year

        # update list of only living people. excludes those that have a DOD
        obj_list_alive = [x for x in obj_list if x.DOD == None]
        
        # for all people objects currently created, run the reproduce method
        for i in obj_list_alive[:len(obj_list_alive)]:
            i.reproduce()
        
        # write stats for the year to output table
        # anything that needs to be done at the end of each year, do here
        print('year: {}, population: {}'.format(year, len(obj_list_alive)))

        
    # enter end of period stats here
    # anything that needs to be done at the end of each run period, do here
    print('Statistics at the end of year {}'.format(year))

    
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
