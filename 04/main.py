from loadValues import LoadValues
from passport import Passport

lv = LoadValues()
lv.strip_lines()
passports = (lv.passportlist_parse())

cnt = 0
for passportfields in passports:
    passport = Passport()
    passport.set_fields(passportfields)
    res = passport.isvalid_passport()
    if res:
        cnt += 1

print(cnt)

##
