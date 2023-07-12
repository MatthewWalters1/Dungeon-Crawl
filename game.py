import numpy as np
import os

filler = '='
classlist = ['fighter', 'spell-slinger', 'dark-knight', 'knight', 'thief', 'bard', 'duelist', 'wizard', 'witch', 'shinobi']
monList = [
    ["a ghost", "a death vulture", "a goblin", "a zombie", "an ogre", "a Troll", "a Saber Leopard", "a Wraith"],
    ["a ghoul", "an oozing mass", "an orc fighter", "a banshee", "a giant", "an Orc Commander", "a Cyclops", "a Witch"],
    ["a troll", "a stone golum", "an orc archer", "a hag", "a saber leopard", "a Giant Snake", "an Ettin", "a Necromancer"],
    ["a werewolf", "a young dragon", "an orc shaman", "an orc duelist", "a shadow tiger", "a Frost Giant", "a Griffin", "a Rock Giant"],
    ["a flame elemental", "an ettin", "an ancient draugr", "an undead horde", "a poltergeist", "the Orc Squadron", "the Dragon", "the Army of Sorcerers"],
    ["a spriggan warlord", "a griffin", "a monstrous owlbear", "a water elemental", " a phoenix", "a frost giant", "a manticore", "a necromancer", \
        "a storm wizard", "a giant snake", "the Feral Werewolf", "the Royal Griffin", "the Vampire"],
    ["a bog hatcher", "a squadron of orcs", "a drider", "a persistent phantom", "a gogiteth", "a dragon", "a nilith", "an army of sorcerers", \
        "a shoggti", "an old griffin", "the Horde of Trolls", "the Elder Dragon", "the Mindflayer"],
    ["a hound of Topedus", "a feral werewolf", "a wight stalker", "a royal griffin", "a graveknight", "a stone dragon", "a grothlut", \
        "a shadow serpent", "an uthul", "an orc warg rider", "the Werewolf Pack", "the Ancient Wyrm", "the Vampire Lord"],
    ["a moonflower", "a mindflayer", "a mohrg spawn", "a warg captain", "a hellcat", "a horde of trolls", "a irlgaunt", "a king shadow serpent", \
        "a jabberwock", "a lich", "Topedus the Mouse God", "the Sea Monster", "the Arch Demon"],
    ["a pit fiend", "an undead army", "a harpy queen", "a mind flayer overlord", "a void worm", "a werewolf pack", "an ifrit", "a vampire lord", "an erlking", \
        "a sea monster", "the Orc World Eater", "the Calamity Dragon", "the Elder Goddes of Death"]
]
weakList = [
    ['m', 'b', 's', 'b', 's', 's', 'b', 'm'],
    ['b', 'm', 's', 'm', 'b', 's', 'b', 'm'],
    ['s', 'm', 'b', 'm', 'b', 's', 'b', 'm'],
    ['s', 'b', 'm', 's', 'b', 's', 'b', 'm'],
    ['m', 'b', 's', 'b', 'm', 's', 'b', 'm'],
    ['s', 'b', 's', 'm', 'm', 's', 'b', 'm', 'm', 's', 's', 'b', 'm'],
    ['b', 's', 's', 'm', 'm', 'b', 's', 'm', 'b', 'b', 's', 'b', 'm'],
    ['s', 's', 'b', 'b', 'm', 'm', 'b', 's', 'm', 'b', 's', 'b', 'm'],
    ['s', 'm', 'b', 'b', 's', 's', 's', 's', 'b', 'm', 's', 'b', 'm'],
    ['m', 'b', 'b', 'm', 's', 's', 'm', 'm', 'm', 'b', 's', 'b', 'm']
]
moves = ['u', 'd', 'l', 'r']
basics = ['s', 'b', 'm']

class player:
    def __init__(self):
        #player's remaining HP
        self.HP = 25
        #player's maximum HP
        self.maxHP = 25
        #player's level
        self.level = 1
        #player's one time heal per floor
        self.potion = True
        #final score, decreases by 100 per wrong attack, increases by 1000 per level up (x2 in normal mode, x3 in hard mode)
        self.finscore = 10000
        #player's kill count, this is your xp (monster essenses), which count up until you reach the goal or camp, it modifies how much you heal when you camp or flee
        self.killCount = 0
        #the level to reach for the game to end
        self.endgame = 11
        #determines the width of the dungeon
        self.killGoal = 5
        #determine the size of wizard explosions
        self.expwidth = 4
        self.exheight = 1
        #strings used to add modifiers to your character
        self.difficulty = ''
        self.diffRating = 0
        self.pclass = ''
        self.race = ''
        self.name = ''
        #strings and numerics used for class abilities
        self.strongAttack = ''
        self.strongAttack2 = ''
        self.increase = ''
        self.classKit1 = 0
        self.classKit2 = 0
        self.maxh = 0
        self.maxk = 0

    def printHP(self):
        score = self.finscore - (10000 - 1000*(self.level - 1))
        score *= self.diffRating
        print("Score:", score)
        print(self.name, "[" + str(self.level) + "] :", end='')
        HP = self.HP / self.maxHP * 80
        print("[", end='')
        for i in range(80):
            if i < HP:
                print("=", end='')
            else:
                print("-", end='')
        print("]", str(self.HP) + '/' + str(self.maxHP))
    
    def gameOver(self):
        score = self.finscore - (10000 - 1000*(self.level - 1))
        score *= self.diffRating
        if (self.level != 10):
            print("  _________________________________________________________________")
            print(" /                                                                 \\")
            print("|                                                                   |")
            print("|                             Game  Over...                         |")
            print("|                                                                   |")
            print(" \\_________________________________________________________________/")
        else:
            print("  _________________________________________________________________")
            print(" /                                                                 \\")
            print("|                                                                   |")
            print("|                             You  win!                             |")
            print("|                                                                   |")
            print(" \\_________________________________________________________________/")
        print()
        print("YOUR FINAL SCORE:", score)
        return
    
    def rest(self, scorehit):
        self.finscore -= scorehit
        self.HP += self.killCount * 6 * self.level
        if (self.HP < self.maxHP):
            self.HP = self.maxHP
        self.killCount = 0

        if (scorehit != 1000):
            print("You flee the dungeon and rest, using your monster essenses to regain your strength...")
        print("But, the dungeon has shifted") 

    #the intro sequence gets all the customizable character information from the player, doesn't allow them to enter options that don't exist
    def intro(self):
        while (self.difficulty != 'easy' and self.difficulty != 'medium' and self.difficulty != 'hard'):
            print("Choose a difficulty: (easy, medium, hard)")
            self.difficulty = input()
        if self.difficulty == 'easy':
            self.diffRating = 1
        elif self.difficulty == 'medium':
            self.diffRating = 2
        else:
            self.diffRating = 3
        print("Greetings traveler...")
        print("What is your name?")
        self.name = input()
        print()

        while (self.race != 'dwarf' and self.race != 'elf' and self.race != 'orc' and self.race != 'man'):
            print("What are you? (dwarf, elf, orc, man)")
            self.race = input()
        if (self.race == 'orc'):
            self.maxHP += 4
            self.HP = self.maxHP
        print()
        
        while (self.pclass not in classlist):
            print("What is your class? (easy: fighter, spell-slinger, dark-knight)")
            print("                    (moderate: knight, thief, bard, duelist)")
            print("                    (advanced: wizard, witch, shinobi)")
            self.pclass = input()
        print()

    #setup is huge, it has to give you different sets of items and describe to the player what they can do during the game, 
    # some of these can probably be condensed, but it would also require conditions for what to print out, so be careful in doing that
    def setup(self):
        if (self.pclass == 'witch'):
            self.strongAttack = 'm'
            self.classKit1 = 1
            self.classKit2 = 1
            self.maxh = 1
            self.maxk = 1
            print("As a witch, you have ", end='')
            if (self.race == 'elf'):
                self.classKit1 += 1
                self.maxh += 1
                print("two healing potions", end='')
            else:
                print("one healing potion", end='')
            print(" (Enter h outside of combat), and one lethal poison (enter k during a fight).\n")
            print("These potion refill when you rest.\n")
        
        elif (self.pclass == 'bard'):
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
            print("As a bard, you get to choose what weapon type you enhance each level.")
            print("Choose one now...(s/b/m)")
            while (self.strongAttack != 's' and self.strongAttack != 'b' and self.strongAttack != 'm'):
                self.strongAttack = input()
            if (self.race != 'elf'):
                print("Once per level, outside of combat, you may choose to change your enhanced weapon type by entering 'b'\n")
            else:
                print("Twice per level, outside of combat, you may choose to change your enhanced weapon type by entering 'b'\n")
        
        elif (self.pclass == 'duelist'):
            self.strongAttack = 's'
            self.classKit1 = 2
            if (self.race == 'elf'):
                self.classKit1 += 1
            print("As a duelist, you are skilled with a sword, and can counter enemies for a chance to take no damage.")
            print("To counter attack, enter c during a fight.\n")
        
        elif (self.pclass == 'shinobi'):
            self.strongAttack = 'b'
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
            print("As a shinobi, you are skilled with a bow, and can always escape a fight back to the entrance of the dungeon (enter e during a fight).")
            print("To use your shinobi escape, you are required to rest.")
            if (self.race != 'elf'):
                print("Once per rest, you can stealth attack an enemy (enter k during a fight) to mitigate damage.\n")
            else:
                print("Twice per rest, you can stealth attack an enemy (enter k during a fight) to mitigate damage.\n")
        
        elif (self.pclass == 'wizard'):
            self.strongAttack = 'm'
            self.classKit1 = 2
            self.classKit2 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
            print("As a wizard, you have a few spells you can use, and two types of spells slots, high slots and low slots")
            print("You can cast Fire Ball (enter f during a fight) expending one of", self.classKit1, "low spell slots that don't regenerate until you level up.\n")
            print("You can also use Invisibility (enter i during a fight), or Explosion (enter e outside of combat), expending one of", self.classKit2, "high spell slots\n")
        
        elif (self.pclass == 'knight'):
            self.increase = 'p'
            self.strongAttack = 's'
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
            self.maxHP += 4
            self.HP = self.maxHP
            print("As a knight, you are very hardy, you have a little more HP than other classes, and you are much stronger with a sword\n")
            if (self.race != 'elf'):
                print("Once per rest, you can power attack your enemy (enter p during a fight), ", end='')
            else:
                print("Twice per rest, you can power attack your enemy (enter p during a fight), ", end='')
            print("taking more damage, but you will progress more than one space in the direction you were moving.\n")

        elif (self.pclass == 'thief'):
            self.strongAttack = 'b'
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
                print("As a thief, you are skilled with a bow and hard to detect, twice per rest, you can sneak attack an enemy, taking zero damage in the fight\n")
            else:
                print("As a thief, you are skilled with a bow and hard to detect, once per rest, you can sneak attack an enemy, taking zero damage in the fight\n")
            print("To sneak attack, enter h during a fight.\n")
        
        elif (self.pclass == 'spell-slinger'):
            self.strongAttack = 'b'
            self.strongAttack2 = 'm'
            print("As a spell-slinger, you are quite skilled with magic attacks and a bow.\n")
        
        elif (self.pclass == 'fighter'):
            self.strongAttack = 's'
            self.strongAttack2 = 'm'
            print("As a fighter, you are quite skilled with sword and bow.\n")

        elif (self.pclass == 'dark-knight'):
            self.strongAttack = 's'
            self.strongAttack2 = 'm'
            print("As a dark-knight, you are quite skilled with the sword and magic attacks.\n")
    
    def levelUp(self):
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|                             Level Up!                             |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
        
        ### bv is for better voice, I'm trying to avoid saying something can be done "one times", instead saying it can be done once or twice per rest
        bv = ['Once', 'Twice']
        bindex = 0

        self.level += 1
        self.potion = True

        ### HP stuff
        #class bonus/penalty
        if (self.pclass == "knight"):
            self.maxHP += (2 * self.level)
        elif (self.pclass == "wizard"):
            self.maxHP -= (2 * self.level)
        
        #race bonus/penalty
        if (self.race == "orc"):
            self.maxHP += (2 * self.level)
        elif (self.race == "elf" or self.race == "dwarf"):
            self.maxHP -= (2 * self.level)

        #typical boost for all classes
        self.maxHP += 25
        self.HP = self.maxHP
        self.killGoal += 2
        self.killCount = 0

        ### class kit stuff
        #wizard
        if (self.pclass == "wizard"):
            self.classKit1 = 2 + self.level
            if (self.level == 5 or self.level == 8):
                self.expwidth += 2
                self.exheight += 1
            if (self.level > 6):
                self.classKit2 = 2
            else:
                self.classKit2 = 1
            if (self.race == "elf"):
                self.classKit1 += 1
            print("Spell slots remaining:", self.classKit1)
            print("High  slots remaining:", self.classKit2)
        #thief
        elif (self.pclass == "thief"):
            self.classKit1 = self.level
            if (self.race == "elf"):
                self.classKit1 += 1
            print("Now you can sneak attack", self.classKit1, "monsters.")
        #knight
        elif (self.pclass == "knight"):
            if (self.increase != "w"):
                print("Would you like to keep power attack? Or switch to war cry? (p/w)")
            else:
                print("Would you like to keep war cry? Or switch to power attack? (p/w)")
            choices = ['w','p']
            self.increase = ''
            while (self.increase not in choices):
                self.increase = input()
                if (self.increase not in choices):
                    print("That's not one of your options...")
            if (self.increase == "p"):
                self.classKit1 = 1
                self.classKit2 = 0
                if (self.race == "elf"):
                    self.classKit1 += 1
                    bindex += 1
                print(bv[bindex], "per rest, you can power attack monsters, pushing further into the dungeon.")
            else:
                self.classKit1 = 0
                self.classKit2 = 1
                if (self.race == "elf"):
                    self.classKit2 += 1
                print("per rest, you can war cry, restoring your strength.")
        #bard
        elif (self.pclass == "bard"):
            self.classKit1 = 1
            if (self.race == "elf"):
                self.classKit1 += 1
                bindex += 1
            print(bv[bindex], "per rest, you can enhance one of your weapons outside of combat.")
        #duelist
        elif (self.pclass == "duelist"):
            self.classKit1 = 2 * self.level
            if (self.race == "elf"):
                self.classKit1 += 1
            print("You can now counter", self.classKit1, "more monsters.")
        #shinobi
        elif (self.pclass == "shinobi"):
            self.classKit1 = 1
            if (self.race == "elf"):
                self.classKit1 += 1
            print(bv[bindex], "per rest, you can stealth attack monsters, reducing damage in combat.")
        #witch
        elif (self.pclass == "witch"):
            choices = ['h','k']
            self.increase = ''
            print("Would you like to increase your Potions(h) or Poisons(k)?")
            while (self.increase not in choices):
                self.increase = input()
                if (self.increase not in choices):
                    print("That's not one of your options...")
            if (self.increase == 'h'):
                self.maxh += 1
            else:
                self.maxk += 1
            self.classKit1 = self.maxh
            self.classKit2 = self.maxk
            print("You now have", self.classKit1, "potions, and", self.classKit2, "poisons.")

    def youDied(self):
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|                             You  Died                             |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
        print("Continue? (y/n)")
        gameState = ''
        while (gameState != 'y' and gameState != 'n'):
            gameState = input()
        if (gameState == 'n'):
            self.gameOver()
            return 1
        else:
            self.killCount = 0
            print("You revive at the beginning of this floor, but you have lost all of your monster essences.")
            self.rest(1000)
            return 0

class monster:
    def __init__(self):
        self.damage = 0
        self.name = ''
        self.weakness = ''
        self.bossType = 0

    #there will only be one monster object, the game loop will call "m = monsterLibrary(level, damage)" for every room the player enters, using the damage of the monster
    def monsterLibrary(self, level, damage, bossType):
        index = level - 1
        jindex = damage
        isBoss = False
        if jindex == 100:
            isBoss = True
            jindex = 10
            if level <= 5:
                jindex = 5
        if level <= 5 and damage != 100:
            jindex = int(jindex/2)
        if damage == 10:
            boss = np.random.randint(0,3)
            while (boss == bossType):
                boss = np.random.randint(0,3)
            jindex += boss
        elif damage == 100:
            damage = 10
            jindex += bossType
        self.damage = damage
        self.name = monList[index][jindex]
        self.weakness = weakList[index][jindex]

        return isBoss


def buildDungeon(pc):
    # Dungeon Key:
    ### Regular Monster [int from 1 to 10]
    ### Obsticle        [-50]
    ### Boss Monster    [100]
    dungeon = []
    for i in range(0, pc.level + 1):
        b = []
        for j in range(0, pc.killGoal):
            b.append(np.random.randint(1,11))
        dungeon.append(b)
    dungeon[0][0] = -1
    #make one random square at the end of the level into a boss
    num = np.random.randint(1, pc.level + 1)
    dungeon[num][pc.killGoal - 1] = 100
    #randomly generate obsticles in the dungeon, don't allow them to form on the left column, right column, or bottom row
    for i in range(0, int(pc.level/2) + 1):
        for j in range(0, pc.level):
            dungeon[j][np.random.randint(1,pc.killGoal-1)] = -50

    return dungeon

def printDungeon(dungeon, row, col, level, killGoal):
    for i in range(0, level + 1):
        for j in range(0, killGoal):
            print("[", end='')
            if i == row and j == col:
                print("O", end='')
            elif dungeon[i][j] == -50:
                print("#", end='')
            elif dungeon[i][j] == -1:
                print("X", end='')
            else:
                print("-", end='')
            print("] ", end='')
        print()
    return

def getOptions(pc, row, col, dungeon):
    print("How would you like to proceed? (", end='')
    options = []
    if (row > 0 and dungeon[row - 1][col] != -50):
        print("u/", end='')
        options.append('u')
    if (col > 0 and dungeon[row][col - 1] != -50):
        print("l/", end='')
        options.append('l')
    if (row < pc.level and dungeon[row + 1][col] != -50):
        print("d/", end='')
        options.append('d')
    if (col < pc.killGoal - 1 and dungeon[row][col + 1] != -50):
        print("r/", end='')
        options.append('r')
    print("f/", end='')
    options.append('f')
    if (pc.pclass == "knight" and pc.increase == "w" and pc.classKit2 > 0):
        print("w/", end='')
        options.append('w')
    elif (pc.pclass == "bard" and pc.classKit1 > 0):
        print("b/", end='')
        options.append('b')
    elif (pc.pclass == "wizard" and pc.classKit2 > 0):
        print("e/", end='')
        options.append('e')
    elif (pc.pclass == "witch" and pc.classKit1 > 0):
        print("h/", end='')
        options.append('h')
    if (pc.potion == True):
        print("c/", end='')
        options.append('c')
    print("i/q)")
    options.append('i')
    options.append('q')

    return options

def preAttack(pc, m, disc, upgrades):
    m.damage = m.damage * 2 * pc.level
    print("It's", m.name, end='')
    cap = False
    for c in m.name:
        if c.isupper():
            cap = True
            break
    if (cap):
        print("!")
    else:
        print(".")

    print("How do you attack? (s/b/m", end='')
    options = ['s', 'b', 'm']
    if (pc.classKit1 > 0):
        if (pc.pclass == "wizard"):
            print("/f", end='')
            options.append('f')
        elif (pc.pclass == "thief"):
            print("/h", end='')
            options.append('h')
        elif (pc.pclass == "knight"):
            print("/p", end='')
            options.append('p')
        elif (pc.pclass == "shinobi"):
            print("/k", end='')
            options.append('k')
        elif (pc.pclass == "dualist"):
            print("/c", end='')
            options.append('c')
    if (pc.classKit2 > 0):
        if (pc.pclass == "wizard"):
            print("/i", end='')
            options.append('i')
        if (pc.pclass == "witch"):
            print("/k", end='')
            options.append('k')
    if (pc.pclass == "shinobi"):
        print("/e", end='')
        options.append('e')
    print(")")
    return options

def calcDamage(pc, m, attackType, upgrades):
    damage = m.damage
    if pc.difficulty == 'easy':
        damage -= 2
    elif pc.difficulty == 'hard':
        damage += 2
    
    if damage <= 0:
        damage = 1

    if (pc.race == "dwarf"):
        damage /= 2
    if (pc.name == "Topedus"):
        damage = 0

    if attackType in basics:
        if m.weakness == attackType:
            damage /= 2
            print("\nIt's super effective!\n")
            if pc.strongAttack == attackType:
                damage /= 2
            elif pc.strongAttack2 == attackType:
                damage /= 2
        else:
            print("Not very effective...\n")
            pc.finscore -= 50
        if (upgrades[basics.index(attackType) + 3] == 1):
            damage /= 2
    else:
        if (attackType == 'f'):
            damage /= 8
            if (upgrades[3] == 1 and upgrades[4] == 1 and upgrades[5] == 1 and pc.level > 4):
                damage /= 4
            print("You cast Fire Ball!\n")
            pc.classKit1 -= 1
            print("Spell slots remaining:", pc.classKit1)
        elif (attackType == 'i'):
            damage = 0
            print("You cast Invisibility\n")
            pc.classKit2 -= 1
            print("High spell slots remaining:", pc.classKit2)
        elif (attackType == 'h'):
            pc.classKit1 -= 1
            damage = 0
            print("\nYou sneak attack the monster!")
            print("You can sneak attack", pc.classKit1, "more monsters.")
        elif (attackType == 'p'):
            print("\nYou rush the monster!")
            pc.classKit1 -= 1
            killCount += pc.level
            damage -= pc.level
            print("You can power attack", pc.classKit1, "more monsters.")
        elif (attackType == 'k'):
            damage /= 8
            if (pc.pclass == "witch"):
                pc.classKit2 -= 1
                print("\nYou poison the monster!")
                print("Poison remaining:", pc.classKit2)
            elif (pc.pclass == "shinobi"):
                pc.classKit1 -= 1
                print("You assassinate the monster!")
                print("You can stealth attack", pc.classKit1, "more monsters.")
        elif (attackType == 'c'):
            chance = np.random.randint(0,pc.level)
            if (chance != 2):
                damage = 0
                print("You counter attack the monster!")
                pc.classKit1 -= 1
                print("You can counter", pc.classKit1, "more monsters.")
            else:
                print("You failed to counter the monster!")
                if (upgrades[3] == 1 and upgrades[4] == 1 and upgrades[5] == 1 and pc.level > 4):
                    damage /= 4
                else:
                    damage /= 2
        if attackType == 'e' and pc.pclass == 'shinobi':
            damage = 0
            print("Using your escape rope, ", end='')
            pc.rest(100)
    
    if (damage < 0):
        damage = 0
    
    return int(damage)

def discovery(upgrades):
    flag = False
    if (upgrades[0] == 1 and upgrades[3] != 1):
        upgrades[3] = 1
        upgrades[0] = 0
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|            You have discovered the Sword of Destiny!!!            |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
    elif (upgrades[0] == 1 and upgrades[3] == 1):
        flag = True
    elif (upgrades[1] == 1 and upgrades[4] != 1):
        upgrades[4] = 1
        upgrades[1] = 0
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|                You discovered the Bow of Heroes!!!                |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
    elif (upgrades[1] == 1 and upgrades[4] == 1):
        flag = True
    elif (upgrades[2] == 1 and upgrades[5] != 1):
        upgrades[5] = 1
        upgrades[2] = 0
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|                You discovered the Staff of Argon!!!               |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
    elif (upgrades[2] == 1 and upgrades[5] == 1):
        flag = True
    return flag, upgrades

def heal(pc, gameState):
    pc.HP += (pc.killCount * 4 * pc.level)
    power = 1
    if (gameState == 'c'):
        power = 2
        pc.potion = False
        print("You set up camp and consume your monster essenses, regaining your strength.")
    elif (gameState == 'w'):
        pc.classKit2 -= 1
        print("You let out a bellowing warcry that restores your strength!")
        print("\nYou can war cry", pc.classKit2, "more times.")
    elif (gameState == 'h'):
        pc.classKit1 -= 1
        print("You drink a healing Potion!")
        print("Potions remaining:", pc.classKit1)
    if (pc.HP > (power * pc.maxHP)):
        pc.HP = power * pc.maxHP
    print("HP is", pc.HP)

def inventory(pc, upgrades):
    print("You have...")
    #Potion
    if (pc.potion):
        print("  camping supplies")
    else:
        print("  no camping supplies")
    #Experience Points
    print(" ", pc.killCount, "monster essenses")
    #Sword stuffs
    if (upgrades[3]):
        print("  the Sword of Destiny", end='')
    elif (pc.strongAttack == 's' or pc.strongAttack2 == 's'):
        print("  a good sword", end='')
    else:
        print("  a sword", end='')    
    if (pc.pclass == "bard" and pc.strongAttack == 's'):
        print("(enhanced)")
    else:
        print()
    #Bow stuffs
    if (upgrades[4]):
        print("  the Bow of Heroes", end='')
    elif (pc.strongAttack == 'b' or pc.strongAttack2 == 'b'):
        print("  a longbow", end='')
    else:
        print("  a bow", end='')
    if (pc.pclass == "bard" and pc.strongAttack == 'b'):
        print("(enhanced)")
    else:
        print()
    #Magic stuffs
    if (upgrades[5]):
        print("  the Staff of Argon", end='')
    elif (pc.strongAttack == 'm' or pc.strongAttack2 == 'm'):
        print("  a powerful magic staff", end='')
    else:
        print("  a somewhat magic stick", end='')
    if (pc.pclass == "bard" and pc.strongAttack == 'm'):
        print("(enhanced)")
    else:
        print()
    #individual Class stuffs
    if (pc.pclass == "knight"):
        if (pc.increase == "w"):
            print(" ", pc.classKit2, "war cries")
        else:
            print(" ", pc.classKit1, "power attacks")
    elif (pc.pclass == "thief"):
        print(" ", pc.classKit1, " poison darts for sneak attacks")
    elif (pc.pclass == "wizard"):
        print(" ", pc.classKit1, "spell slots")
        print(" ", pc.classKit2, "high slots")
    elif (pc.pclass == "witch"):
        print(" ", pc.classKit1, "healing potions")
        print(" ", pc.classKit2, "poisons")
    elif (pc.pclass == "shinobi"):
        print(" ", pc.classKit1, " kunai for assassinations")
    elif (pc.pclass == "duelist"):
        print(" ", pc.classKit1, " counter attacks")
    elif (pc.pclass == "bard"):
        print(" ", pc.classKit1, "enhancing performances")

    return

def explode():
    print("  _________________________________________________________________")
    print(" /                                                                 \\")
    print("|                                                                   |")
    print("|                             EXPLOSION!                            |")
    print("|                                                                   |")
    print(" \\_________________________________________________________________/")
    print()
    
def bigOutput():
    print("Dungeons will look something like this:")
    print("[X] [X] [X] [O] [-]")
    print("[-] [-] [#] [-] [-]")
    print("[-] [-] [-] [-] [-]")
    print("  X : a room where you have already been, and killed the monster")
    print("  O : where you are currently")
    print("  - : a space you have yet to explore")
    print("  # : a space that cannot be entered, it is an obsticle in your path\n")
    print("the final boss of each floor will be found somewhere along the furthest column to the right, and you will start in the top left corner of the dungeon\n")
    print("   you -> [O] [-] [#] [-] [-] <- boss?")
    print("          [-] [-] [-] [-] [-] <- boss?\n")
    print("In order to level up and move on to the next floor of the dungeon, defeat the boss on the other end\n")
    print("Each time you enter a space you have not previously explored, you will be faced by some sort of monster that you must fight\n")
    print("In a fight, you can use a sword (Enter s), a bow (Enter b), or magic (Enter m);")
    print(" each monster is specifically weak to one of these.\n")
    print("You may flee to the entrance of the dungeon, regaining your HP and class abilities, by entering f outside of combat.\n")
    print("Outside of a fight, you may enter i to see what items and abilities you have collected on your adventure!\n")
    print("u makes you go up, d makes you go down, r makes you go right, and l makes you go left\n")
    print("In the dungeon, you can make camp (enter c outside of combat) to regain some HP before continuing on,\n")
    print("you must flee to regain the supplies to make camp again\n")
    print("Enter q to quit\n")
    return

def main():
    #set color to black with green characters
    os.system("color 0A")
    #initialize all of our variables, including the player
    pc = player()
    m = monster()
    disc = False
    upgrades = [0,0,0,0,0,0]
    row = 0
    col = 0
    
    #big bits of text, character creation, description of the game's processes
    pc.intro()
    pc.setup()
    bigOutput()

    #gameplay loop structure
    ### forEach level:
    ###     build the dungeon
    ###     determine the boss
    ###     while player is not at the boss
    ###         printHP
    ###         printDungeon
    ###         ask player for next action
    ###         if they move, move them
    ###             if space != -1 (dead), reveal the monster
    ###             player chooses attack type or class ability
    ###             calculate damage
    ###         if they don't move, handle the action and restart While loop
    ###         if  : player dies, continue screen, 
    ###             if they choose to continue, restart For loop (player's level stays the same), decrease player's score, 
    ###             else print score and end
    ###         else: set current space to -1, manage magic items, increase killcount, restart While loop
    ###     end while
    ###     if we got here, they already fought the boss
    ###     player's level += 1
    ###     since they level up, increase maxHP, set HP to max, reset position to [0][0], restart For loop

    for level in range(1,pc.endgame):
        #set up for discovering legendary weapons, specifically once per floor if requirements are met
        disc = False        
        #build the level with random numbers
        dungeon = buildDungeon(pc)
        #determine the boss type, so that you can tell the player their intended final fight for the level,
        ## plus, if they find a boss monster (space == 10) prior to the final fight (space == 100), then force it to not be the same as the final fight
        bossType = np.random.randint(0,3)
        m.monsterLibrary(level, 100, bossType)
        print("To defeat the dungeon, traverse this floor and defeat", m.name + '!')
        isBoss = False
        while (isBoss == False):
            pc.printHP()
            printDungeon(dungeon, row, col, level, pc.killGoal)
            #prints the list of possible inputs for the player, and if player's input is not in that list, then remind them they can't do that, and ask again
            options = getOptions(pc, row, col, dungeon)
            gameState = ''
            reloop = 0
            while (gameState not in options):
                gameState = input()
                if (gameState not in options):
                    print("You can't do that...")
                    reloop += 1
                    break
            #resets the loop, so they don't lose track of the dungeon if they accidentally mistype
            if (reloop):
                continue

            #the player is using a move action, thus moving to a new room, and possibly starting Combat 
            if (gameState in moves):
                if (gameState == 'u'):
                    row -= 1
                elif (gameState == 'd'):
                    row += 1
                elif (gameState == 'l'):
                    col -= 1
                elif (gameState == 'r'):
                    col += 1
                #if they've already killed a monster in a particular room, don't continue the loop, because the rest of this loop is Combat
                if (dungeon[row][col] == -1):
                    print("The monster here is already dead.")
                    continue
                #if they have not killed the monster, look it up, prepare for battle!
                #check if the monster is the boss, for the while loop, so they can level up
                isBoss = m.monsterLibrary(level, dungeon[row][col], bossType)
                #check if the monster is any type of boss, so we can handle item discovery
                if (m.damage == 10 or m.damage == 100) and disc != True:
                    if(m.weakness == 's' and upgrades[3] != 1):
                        upgrades[0] = 1
                        disc = True
                    elif (m.weakness == 'b' and upgrades[4] != 1):
                        upgrades[1] = 1
                        disc = True
                    elif (m.weakness == 'm' and upgrades [5] != 1):
                        upgrades[2] = 1
                        disc = True
                options = preAttack(pc, m, disc, upgrades)
                gameState = ''
                while (gameState not in options):
                    gameState = input()
                    if (gameState not in options):
                        print("You can't do that...")
                
                damage = calcDamage(pc, m, gameState, upgrades)
                #this is for the shinobi's escape, it resets the dungeon, obsticles and all, 
                # unless I add some functionality to buildDungeon, so I can reset the dead to their original monsters, but not move the obsticles around
                if (gameState == 'e'):
                    upgrades[0] = 0
                    upgrades[1] = 0
                    upgrades[2] = 0
                    disc = False
                    row = 0
                    col = 0
                    dungeon = buildDungeon(pc)
                    continue
                print("You take", damage, "damage.")
                pc.HP -= damage
                if (isBoss):
                    pc.printHP()
                
                ### The Player Has Died
                if (pc.HP <= 0):
                    quitter = pc.youDied()
                    if (quitter):
                        return
                    row = 0
                    col = 0
                    dungeon = buildDungeon(pc)
                    continue
                
                ### The Player has not died, thus defeating the monster, now they take damage and maybe discover items
                dungeon[row][col] = -1
                pc.killCount += 1
                print("You now have", pc.killCount, "monster essenses.")
                if (disc == True):
                    disc, upgrades = discovery(upgrades)
            else:
                if (gameState == 'f'):
                    row = 0
                    col = 0
                    dungeon = buildDungeon(pc)
                    pc.rest(200)
                
                elif (gameState == 'w' or gameState == 'c' or gameState == 'h'):
                    heal(pc, gameState)
                
                elif (gameState == 'i'):
                    inventory(pc, upgrades)
                
                elif (gameState == 'b'):
                    pc.classKit1 -= 1
                    print("Which attack type do you wish to enhance? (s/b/m)")
                    pc.strongAttack = ''
                    while (pc.strongAttack not in basics):
                        pc.strongAttack = input()
                
                elif (gameState == 'e'):
                    explode()
                    pc.classKit2 -= 1
                    if (col < pc.killGoal - 1 and row >= 0 and row <= pc.level):
                        for i in range((row - pc.exheight), (row + pc.exheight + 1)):
                            for j in range(col + 1, col + pc.expwidth):
                                if (i <= pc.level and i >= 0 and j < pc.killGoal and j >= 0):
                                    if (dungeon[i][j] != 100 and dungeon[i][j] != -50):
                                        dungeon[i][j] = -1
                                        pc.killCount += 1
                
                elif (gameState == 'q'):
                    print("ARE YOU SURE??? (y/n)")
                    gameState = ''
                    while (gameState != 'y' and gameState != 'n'):
                        gameState = input()
                    if (gameState == 'y'):
                        pc.gameOver()
                        return
                    
        #if you got to the boss, level up here
        #For this print, I want the bosses to have a "singular/plural" flag, so it says "the souls of", not just "the soul of", better voice and all that...
        print("You use the soul of", m.name, "to grow stronger.")
        row = 0
        col = 0
        disc = False
        pc.levelUp()

    pc.gameOver()

    return

if __name__ == "__main__":
    main()