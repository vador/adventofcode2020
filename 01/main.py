from loadValues import LoadValues

lv = LoadValues()
expenses = lv.list_to_intlist()

print(expenses)


year = 2020

for i in range(len(expenses)):
    basis = expenses[i]
    exp_set = set(expenses)
    exp_set.remove(basis)
    howmuch = year - basis
    while len(exp_set)>0:
        first = exp_set.pop()

        rest = howmuch - first

        if (rest in exp_set):
            print(basis, first, rest, first*rest*basis)

