import csv


class Armor:
    def __init__(self):
        self.perks = []

    def Check_Perks(self, perk):
        for x in self.perks:
            if perk in x:
                return True
        return False


class PerkSets:
    def __init__(self, x):
        self._perks = x
        self._count = 0

    def Check(self, perks):
        _perk_found = []
        for perk in self._perks:
            if perk in perks:
                _perk_found.append(True)
            else:
                _perk_found.append(False)

        if False in _perk_found:
            return False
        else:
            self._count += 1
            return True


class Perk:
    def __init__(self, p):
        self.perk = p
        self._item = {}
        for x in ['hunter', 'warlock', 'titan']:
            for y in ['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor']:
                self._item.update({f'{x}-{y}': False})
        self._item.update({'hunter-Hunter Cloak': False,
                           'warlock-Warlock Bond': False,
                           'titan-Titan Mark': False
                           })

    def Update(self, armor):
        for arm in armor:
            if arm.tag not in [None, 'Tag'] and self._item[f"{arm.equippable}-{arm.type}"] == 0:
                self._item[f"{arm.equippable}-{arm.type}"] = arm.Check_Perks(
                    self.perk)

    def Get_Item_Status(self, key):
        return self._item[key]


# Get data from CSVs
# Get Armor from CSV
armor = []
with open('destinyArmor.csv') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        arm = Armor()
        arm.name = row[0]
        arm.hash = row[1]
        arm.id = row[2]
        arm.tag = None
        arm.tier = row[4]
        arm.type = row[5]
        arm.equippable = row[6]
        arm.power = row[7]
        arm.masterworkType = row[8]
        arm.masterworkTier = row[9]
        arm.owner = row[10]
        arm.locked = row[11]
        arm.equipped = row[12]
        arm.year = row[13]
        arm.season = row[14]
        arm.event = row[15]
        arm.dtrrating = row[16]
        arm.reviews = row[17]
        arm.mobility = row[18]
        arm.recovery = row[19]
        arm.resilience = row[20]
        arm.notes = row[21]
        for x in range(22, len(row)):
            arm.perks.append(row[x].replace('*', ''))
        armor.append(arm)
armor[0].tag = 'Tag'

# Get Perk Sets from CSV
perk_sets = []
with open('Perk_Sets.csv') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        if row[0][0] != '#':
            perk_sets.append(PerkSets(row))

perks = []
# Get Perks from CSV
with open('RecommendedPerks.csv') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        if row[0][0] != '#':
            perks.append(Perk(row[0]))

# Find Perks

# Find Perk Sets
maxLen = 0
for perk_set in perk_sets:
    if len(str(perk_set._perks)) > maxLen:  # Getting max length for formatting purposes
        maxLen = len(str(perk_set._perks))
    for arm in armor:
        if perk_set.Check(arm.perks):
            arm.tag = 'favorite'

maxLength = 0
# Update perks found/Find Keeps
for perk in perks:
    perk.Update(armor)
    if len(perk.perk) > maxLength:  # Getting max length for formatting purposes
        maxLength = len(perk.perk)
    for arm in armor:
        if arm.tag == None:
            if arm.Check_Perks(perk.perk) and perk.Get_Item_Status(f"{arm.equippable}-{arm.type}") == False:
                arm.tag = 'keep'

# Print Perk Sets
for perk_set in perk_sets:
    x = maxLen - len(str(perk_set._perks))
    print(f"{perk_set._perks}{' '*x} || {perk_set._count}")
# Print Perks
for perk in perks:
    perk.Update(armor)
    z = maxLength - len(perk.perk)
    print(f"\n{perk.perk}{' '*z}")
    for x in ['hunter', 'warlock', 'titan']:
        for y in ['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor']:
            key = f"{x}-{y}"
            if perk._item[key]:
                print(f"{key}:{perk._item[key]}")
        if x == 'hunter':
            key = f"{x}-Hunter Cloak"
            if perk._item[key]:
                print(f"{key}:{perk._item[key]}")
        elif x == 'warlock':
            key = f"{x}-Warlock Bond"
            if perk._item[key]:
                print(f"{key}:{perk._item[key]}")
        elif x == 'titan':
            key = f"{x}-Titan Mark"
            if perk._item[key]:
                print(f"{key}:{perk._item[key]}")

# Export CSV
with open('DestinyArmorExport.csv', 'w') as csvfile:
    data = csv.writer(csvfile)
    for arm in armor:
        data.writerow([arm.name,
                       arm.hash,
                       arm.id,
                       arm.tag,
                       arm.tier,
                       arm.type,
                       arm.equippable,
                       arm.power,
                       arm.masterworkType,
                       arm.masterworkTier,
                       arm.owner,
                       arm.locked,
                       arm.equipped,
                       arm.year,
                       arm.season,
                       arm.event,
                       arm.dtrrating,
                       arm.reviews,
                       arm.mobility,
                       arm.recovery,
                       arm.resilience,
                       arm.notes,
                       arm.perks[0],
                       arm.perks[1],
                       arm.perks[2],
                       arm.perks[3],
                       arm.perks[4],
                       arm.perks[5],
                       arm.perks[6],
                       arm.perks[7],
                       arm.perks[8],
                       arm.perks[9],
                       arm.perks[10]])
