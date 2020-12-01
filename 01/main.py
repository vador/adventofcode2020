from loadValues import LoadValues

lv = LoadValues()
expenses = lv.list_to_intlist()

print(expenses)

exp_set = set(expenses)

while len(exp_set)>0:
    first = exp_set.pop()

    rest = 2020 - first

    if (rest in exp_set):
        print(first, rest, first*rest)

