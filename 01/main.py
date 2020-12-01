from loadValues import LoadValues

lv = LoadValues()
expenses = lv.list_to_intlist()

print(expenses)


year = 2020

while (len(expenses)>0):
    basis = expenses.pop()
    exp_set = set(expenses)
    howmuch = year - basis
    while len(exp_set)>0:
        first = exp_set.pop()

        rest = howmuch - first

        if (rest in exp_set):
            print(basis, first, rest, first*rest*basis)

