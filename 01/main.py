from loadValues import LoadValues

lv = LoadValues()
expenses = lv.list_to_intlist()

print(expenses)


year = 2020

while (len(expenses)>0):
    first = expenses.pop()
    exp_set = set(expenses)
    rest = year - first
    while len(exp_set)>0:
        second = exp_set.pop()

        third = rest - second

        if (third in exp_set):
            print(first, second, third, second * third * first)

