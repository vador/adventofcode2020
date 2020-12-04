from loadValues import LoadValues
from passport import Passport

lv = LoadValues()
lv.strip_lines()
passports = (lv.passportlist_parse())

cntstar1 = 0
cntstar2 = 0

for passportfields in passports:
    passport = Passport()
    passport.set_fields(passportfields)
    if passport.are_compulsory_keys_present():
        cntstar1 += 1
    if passport.isvalid_passport():
        cntstar2 += 1

print(cntstar1, cntstar2)

##
