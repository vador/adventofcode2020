from loadValues import LoadValues

import re

lv = LoadValues()
lv.strip_lines()
passports = (lv.passportlist_parse())


class Passport:
    fields = None
    passport_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    compulsory_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    def __init__(self):
        self.fields = {}

    def set_fields(self, fields):
        self.fields = fields

    def isvalid_passport(self):
        for k in self.compulsory_keys:
            if k not in self.fields.keys():
                return False
        res = self.are_passportkeys_valid()
        if res == True:
            print (self.fields['pid'])
        return res

    def are_passportkeys_valid(self):
        byr = int(self.fields['byr'])
        if (byr < 1920 or byr > 2002):
            return False
        iyr = int(self.fields['iyr'])
        if (iyr < 2010 or iyr > 2020):
            return False
        eyr = int(self.fields['eyr'])
        if (eyr < 2020 or eyr > 2030):
            return False
        ecl = self.fields['ecl']
        if ecl not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
            return False
        pid = self.fields['pid']
        if not re.match('^\d{9}$', pid):
            return False
        hgt = self.fields['hgt']
        h_unit = hgt[-2:]
        h_val = int(hgt[:-2])
        if h_unit == "in" and (h_val < 59 or h_val > 76):
            return False
        if h_unit == "cm" and (h_val < 150 or h_val > 193):
            return False
        if h_unit != "cm" and h_unit != "in":
            return False
        hcl = self.fields['hcl']
        if not re.match('^#[0-9a-f]{6}$', hcl):
            return False
        return True


cnt = 0
for passportfields in passports:
    passport = Passport()
    passport.set_fields(passportfields)
    res = passport.isvalid_passport()
    if res:
        cnt += 1

print(cnt)

##
