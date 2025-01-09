class Student:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.ratings = {}
        self.debts = []

    def add_rating(self, discipline, rating):
        self.ratings[discipline] = rating

    def add_debt(self, debt):
        self.debts.append(debt)
