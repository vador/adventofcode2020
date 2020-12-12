import logging
import re

logger = logging.getLogger(__name__)


class Passport:
    fields = None
    passport_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid', 'cid']
    compulsory_keys = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

    def __init__(self):
        self.fields = {}

    def set_fields(self, fields):
        self.fields = fields
        logger.debug("Creating passport :" + str(self.fields))

    def isvalid_passport(self):
        res = self.are_compulsory_keys_present()
        if res:
            res = self.are_passportkeys_valid()
        return res

    def are_compulsory_keys_present(self):
        res = True
        for k in self.compulsory_keys:
            if k not in self.fields.keys():
                res = False
        return res

    def are_passportkeys_valid(self):
        pass_keys = ('byr', 'iyr', 'eyr', 'ecl', 'pid', 'hgt', 'hcl')
        byr = int(self.fields['byr'])
        iyr = int(self.fields['iyr'])
        eyr = int(self.fields['eyr'])
        ecl = self.fields['ecl']
        pid = self.fields['pid']
        hgt = self.fields['hgt']
        hcl = self.fields['hcl']
        detail = {'byr': Passport.validate_byr(byr),
                  'iyr': Passport.validate_iyr(iyr),
                  'eyr': Passport.validate_eyr(eyr),
                  'ecl': Passport.validate_ecl(ecl),
                  'pid': Passport.validate_pid(pid),
                  'hgt': Passport.validate_hgt(hgt),
                  'hcl': Passport.validate_hcl(hcl)}
        res = all(detail.values())
        logger.debug("Validation :" + str(res) + str(detail))

        return res

    @staticmethod
    def validate_hcl(hcl):
        return re.match('^#[0-9a-f]{6}$', hcl) is not None

    @staticmethod
    def validate_hgt(hgt):
        res = True
        if len(hgt) <= 2:
            return False
        h_unit = hgt[-2:]
        h_val = int(hgt[:-2])
        if h_unit != "cm" and h_unit != "in":
            res = False
        if h_unit == "in" and (h_val < 59 or h_val > 76):
            res = False
        if h_unit == "cm" and (h_val < 150 or h_val > 193):
            res = False

        return res

    @staticmethod
    def validate_pid(pid):
        return re.match('^\d{9}$', pid) is not None

    @staticmethod
    def validate_ecl(ecl):
        return ecl in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

    @staticmethod
    def validate_eyr(eyr):
        return 2020 <= eyr <= 2030

    @staticmethod
    def validate_iyr(iyr):
        return 2010 <= iyr <= 2020

    @staticmethod
    def validate_byr(byr):
        return 1920 <= byr <= 2002
