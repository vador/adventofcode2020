from loadValues import LoadValues

import re

lv = LoadValues()
lv.strip_lines()
passports = (lv.passportlist_parse())

passport_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
compulsory_key = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']


def isvalid_passport(passport):
    for k in compulsory_key:
        if k not in passport.keys():
            return False
    res = are_passportkeys_valid(passport)
    if res == True:
        print (passport['pid'])
    return res


def are_passportkeys_valid(passport):
    byr = int(passport['byr'])
    if (byr < 1920 or byr > 2002):
        return False
    iyr = int(passport['iyr'])
    if (iyr < 2010 or iyr > 2020):
        return False
    eyr = int(passport['eyr'])
    if (eyr < 2020 or eyr > 2030):
        return False
    ecl = passport['ecl']
    if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False
    pid = passport['pid']
    if not re.match('^\d{9}$', pid):
        return False
    hgt = passport['hgt']
    h_unit = hgt[-2:]
    h_val = int(hgt[:-2])
    if h_unit == "in" and (h_val < 59 or h_val > 76):
        return False
    if h_unit == "cm" and (h_val < 150 or h_val > 193):
        return False
    if h_unit != "cm" and h_unit != "in":
        return False
    hcl = passport['hcl']
    if not re.match('^#[0-9a-f]{6}$', hcl):
        return False
    return True


cnt = 0
for passport in passports:
    res = isvalid_passport(passport)
    if res:
        cnt += 1

print(cnt)

##
