obj_list = []

class Person:
    def __init__(self, ID, parent_ID):
        self.ID = ID
        self.parent_ID = parent_ID

    def reproduce(self):
        '''Person object has a baby, baby is stored as a new Person in obj_list'''
        ID = obj_list[-1].ID + 1
        parent_ID = self.ID
        return obj_list.append(Person(ID, parent_ID))