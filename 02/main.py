from loadValues import LoadValues

lv = LoadValues()
database = lv.get_rules()

print database


def check_rule_1star(rule, password):
    (letter, (qmin, qmax)) = rule

    counter = password.count(letter)
    if (counter >= qmin and counter <= qmax):
        return True
    else:
        return False


def check_rule_2star(rule, password):
    (letter, (pos1, pos2)) = rule

    res1 = password[pos1 - 1] == letter
    res2 = password[pos2 - 1] == letter
    return res1 ^ res2


cnt = 0

for (rule, password) in database:
    res = check_rule_1star(rule, password)
    if res:
        cnt += 1
    print (rule, password, res)

print("Nb :", cnt)

cnt = 0

for (rule, password) in database:
    res = check_rule_2star(rule, password)
    if res:
        cnt += 1
    print (rule, password, res)

print("Nb :", cnt)
