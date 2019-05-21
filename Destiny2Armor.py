import csv
import os


class Armor:
    def __init__(self):
        self.perks = []  # Array to store perks
        self.name = ''  # init with blank name
        self.total_rec_perks = 0  # Total amount of Rec perks

    def Check_Perks(self, perk):
        for x in self.perks:  # Loop through perks on armor
            if perk.lower() == x.lower():  # If matches input
                return 1  # return true
        return 0  # Otherwise return false

    def Get_Total_Rec_Perks(self, perks):
        for perk in perks:  # Loop through array of perks from input
            if self.Check_Perks(perk.perk):  # Check for a match
                self.total_rec_perks += perk.weight  # increase total by weight
                # Adding a weight system to Rec Perks
                # Ex. Remote Connection, Pump Action has a weight of 2
                #    Precision Weapon Targeting, Ashes to Assets has a weight of 1
                #    Add the weight to self.total_rec_perks to prioritize what perks are wanted
                #    So a helm with Remote Connection, Pump Action is better than a helm with Remote Connection, Ashes to Assets

    def Print_RecPerks(self, perks):  # Just a function to print out armor and its rec perks
        print(f" -{self.equippable}: {self.name}")
        for perk in perks:
            if self.Check_Perks(perk.perk):
                print(f"    {perk.perk}")


class PerkSets:  # Allows for Custom Perks sets. May be replaced by weight system.
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
    def __init__(self, p, m, w):
        self.perk = p
        self.total = 0
        self._min = 1
        self.weight = w
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


os.chdir(os.path.dirname(__file__))
# Get data from CSVs
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
            perks.append(Perk(row[0], int(row[1]), int(row[2])))
# Get Armor from CSV
armor = []
with open('destinyArmor.csv') as csvfile:
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
            arm.Get_Total_Rec_Perks(perks)
            armor.append(arm)

# Update Existing Favorites
for arm in armor:
    if arm.tag == 'favorite':
        for perk in perks:
            perk.Update(arm)

# Find Perks
maxLength = 0
# Find Keeps
for perk in perks:
    print(f"\n{perk.perk}")

    topArmor = {}
    for x in ['Hunter', 'Warlock', 'Titan']:
        for y in ['Helmet', 'Gauntlets', 'Chest Armor', 'Leg Armor']:
            topArmor.update({f'{x}-{y}': [Armor()]})
    topArmor.update({'Hunter-Hunter Cloak': [Armor()],
                     'Warlock-Warlock Bond': [Armor()],
                     'Titan-Titan Mark': [Armor()]
                     })

    # Get armor with most rec perks for the current perk and add to the dict
    for arm in armor:
        if arm.tag != 'Tag':  # Exclue header row
            if arm.Check_Perks(perk.perk):  # Check if current perk is on armor
                key = f'{arm.equippable}-{arm.type}'  # Create dict key
                # if more rec perks then
                if arm.total_rec_perks > topArmor[key][0].total_rec_perks:
                    topArmor[key] = []
                    topArmor[key].append(arm)  # replace current piece
                elif arm.total_rec_perks == topArmor[key][0].total_rec_perks:
                    topArmor[key].append(arm)

    for key in topArmor:
        for arm in topArmor[key]:
            if arm.name != '':
                arm.tag = 'keep'
                for p in perks:
                    p.Update(arm)
                arm.Print_RecPerks(perks)

# Find Perk Sets
maxLen = 0
for perk_set in perk_sets:
    if len(str(perk_set._perks)) > maxLen:  # Getting max length for formatting purposes
        maxLen = len(str(perk_set._perks))
    for arm in armor:
        if perk_set.Check(arm.perks):
            arm.tag = 'favorite'
            for perk in perks:
                perk.Update(arm)

# Print Perk Sets
for perk_set in perk_sets:
    x = maxLen - len(str(perk_set._perks))
    print(f"{perk_set._perks}{' '*x} || {perk_set._count}")

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

count = 0
for arm in armor:
    if arm.tag in ['favorite', 'keep']:
        count += 1

print(f"\nTotal Tagged Armor: {count}")
