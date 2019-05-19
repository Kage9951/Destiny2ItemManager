import csv


class Armor:
    def __init__(self):
        self.perks = []
        self.name = ''
        self.total_rec_perks = 0

    def Check_Perks(self, perk):
        for x in self.perks:
            if perk.lower() == x.lower():
                return 1
        return 0

    def Print_RecPerks(self, perks):
        print(f" -{self.name}")
        for perk in perks:
            if self.Check_Perks(perk.perk):
                print(f"    {perk.perk}")


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
    def __init__(self, p, m):
        self.perk = p
        self.total = 0
        self._min = 1
        self._item = {}
        for x in ['Hunter', 'Warlock', 'Titan']:
            for y in ['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor']:
                self._item.update({f'{x}-{y}': 0})
        self._item.update({'Hunter-Hunter Cloak': 0,
                           'Warlock-Warlock Bond': 0,
                           'Titan-Titan Mark': 0
                           })

    def Update(self, armor):
        temp = armor.Check_Perks(self.perk)
        self._item[f"{armor.equippable}-{armor.type}"] += temp
        self.total += temp

    def Get_Item_Status(self, key):
        return self._item[key] < self._min


# Get data from CSVs
# Get Armor from CSV
armor = []
with open('Destiny_Item_Manager/destinyArmor.csv') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        if (row[4] != 'Exotic'):
            arm = Armor()
            arm.name = row[0]
            arm.hash = row[1]
            arm.id = row[2]
            arm.tag = row[3]
            arm.tier = row[4]
            arm.type = row[5]
            arm.equippable = row[6]
            arm.power = row[7]
            arm.masterworkType = row[8]
            arm.masterworkTier = row[9]
            arm.mobility = row[18]
            arm.recovery = row[19]
            arm.resilience = row[20]
            arm.notes = row[21]
            for x in range(22, len(row)):
                arm.perks.append(row[x].replace('*', ''))

            if arm.tag not in ['Tag', 'favorite']:
                arm.tag = None
            armor.append(arm)

# Get Perk Sets from CSV
perk_sets = []
with open('Destiny_Item_Manager/Perk_Sets.csv') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        if row[0][0] != '#':
            perk_sets.append(PerkSets(row))
perks = []
# Get Perks from CSV
with open('Destiny_Item_Manager/RecommendedPerks.csv') as csvfile:
    data = csv.reader(csvfile)
    for row in data:
        if row[0][0] != '#':
            perks.append(Perk(row[0], int(row[1])))

# Update Existing Favorites
for arm in armor:
    if arm.tag == 'favorite':
        for perk in perks:
            perk.Update(arm)

# Find Perks
count = 0
# Find Perk Sets
maxLen = 0
for perk_set in perk_sets:
    if len(str(perk_set._perks)) > maxLen:  # Getting max length for formatting purposes
        maxLen = len(str(perk_set._perks))
    for arm in armor:
        if perk_set.Check(arm.perks):
            arm.tag = 'favorite'
            count += 1
            for perk in perks:
                perk.Update(arm)

maxLength = 0
# Find Keeps
for perk in perks:
    print(f"\n{perk.perk}")
    # Find Total Rec Perks for armor with current perk
    for arm in armor:
        if arm.tag != 'Tag':
            arm.total_rec_perks = 0
            if arm.Check_Perks(perk.perk) and perk.Get_Item_Status(f"{arm.equippable}-{arm.type}"):
                for p in perks:
                    if arm.Check_Perks(p.perk):
                        arm.total_rec_perks += 1

    #Dict to put in the top pieces of armor
    #by most number of recommended perks
    topArmor = {}
    for x in ['Hunter', 'Warlock', 'Titan']:
        for y in ['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor']:
            topArmor.update({f'{x}-{y}': Armor()})
    topArmor.update({'Hunter-Hunter Cloak': Armor(),
                     'Warlock-Warlock Bond': Armor(),
                     'Titan-Titan Mark': Armor()
                     })

    # Get most rec perks
    for arm in armor:
        if arm.tag != 'Tag':
            if arm.total_rec_perks > topArmor[f"{arm.equippable}-{arm.type}"].total_rec_perks:
                topArmor[f"{arm.equippable}-{arm.type}"] = arm

    for key in topArmor:
        if topArmor[key].name != '':
            topArmor[key].tag = 'keep'
            count += 1
            for p in perks:
                p.Update(topArmor[key])
            topArmor[key].Print_RecPerks(perks)

# Print Perk Sets
for perk_set in perk_sets:
    x = maxLen - len(str(perk_set._perks))
    print(f"{perk_set._perks}{' '*x} || {perk_set._count}")

# Print Perks
for perk in perks:
    if perk.total != 0:
        z = maxLength - len(perk.perk)
        print(f"\n{perk.perk} - {perk.total}")
        for x in ['Hunter', 'Warlock', 'Titan']:
            for y in ['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor']:
                key = f"{x}-{y}"
                if perk._item[key]:
                    print(f" {key}:{perk._item[key]}")

            if x == 'Hunter':
                key = f"{x}-Hunter Cloak"
                if perk._item[key]:
                    print(f" {key}:{perk._item[key]}")
            elif x == 'Warlock':
                key = f"{x}-Warlock Bond"
                if perk._item[key]:
                    print(f" {key}:{perk._item[key]}")
            elif x == 'Titan':
                key = f"{x}-Titan Mark"
                if perk._item[key]:
                    print(f" {key}:{perk._item[key]}")

# Export CSV
with open('Destiny_Item_Manager/DestinyArmorExport.csv', 'w') as csvfile:
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

print(f"\nTotal Tagged Armor: {count}")
