import re 
from pathlib import Path

data_path = Path('./data')
test_data_path = data_path/'test_data.txt'
real_data_path = data_path/'data.txt'

FIELDS = {   
    'byr': 'Birth Year',
    'iyr': 'Issue Year',
    'eyr': 'Expiration Year',
    'hgt': 'Height',
    'hcl': 'Hair Color',
    'ecl': 'Eye Color',
    'pid': 'Passport ID',
    'cid': 'Country ID'
}

def valid_height(h):
    if h.endswith("cm"):
        return 150<=int(h[:-2])<=193
    if h.endswith("in"):
        return 59<=int(h[:-2])<=76

FIELD_VALID = {
    'byr': lambda n: 1920<=int(n)<=2002,
    'iyr': lambda n: 2010<=int(n)<=2020,
    'eyr': lambda n: 2020<=int(n)<=2030,
    'hgt': lambda h: valid_height(h),
    'hcl': lambda c: bool(re.findall(r"#[a-z\d]{6}", c)),
    'ecl': lambda c: c in ('amb','blu','brn','gry','grn','hzl','oth'),
    'pid': lambda pid: len(pid) == 9 and pid.isnumeric(),
    'cid': lambda _: True
}

CANMISS = ['cid']
CANTMISS = [k for k in FIELDS if not k in CANMISS]

def read_file(path):
    with open(path) as f:
        t = f.read()
    return t.split("\n\n")

def find_fields(entry):
    field_pats = [r"(%s):([^\s]+)[ \t\n]?"%f for f in FIELDS]
    fields = {}
    for fp in field_pats:
        res = re.search(fp, entry, flags=re.MULTILINE)
        if res:
            fields[res.group(1)] = res.group(2)

    return fields

def count_valid(passengers):
    is_valid = lambda p: all(k in p for k in CANTMISS)
    count = sum(is_valid(p) for p in passengers)
    return count

def count_valid2(passengers):
    is_valid = lambda p: all(k in p for k in CANTMISS) and \
                      all(FIELD_VALID[k](v) for k,v in p.items())
    count = sum(is_valid(p) for p in passengers)
    return count

def main():
    entries = read_file(real_data_path)
    passengers = [
        find_fields(entry) for entry in entries
        ]
    valid = count_valid2(passengers)
    print(valid)

if __name__ == "__main__":
    main()
