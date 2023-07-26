import random
import os
import time

#TO-DO list: easy
### add monster list action, so that player can check which monsters they've fought and which attacks worked/failed
### * this list should be presented in 2 columns, the monsters they've seen in the current level on the left, and the monsters of previous levels on the right
### * under each name or to the right of the name, print either "s" or whatever is the correct attack, or "*not m" or whatever attack they've tried.
###    if they've made 2 incorrect attacks, it's obviously the third one, so in the monster list, don't say "*not m" and "*not b", just say "s" 
### animate the screen so the dungeon doesn't move around all the time
#TO-DO list: difficult
### actually put the game in a window with graphics (pygame or pyqt)
### get a website to display all players' usernames who have gotten a perfect 30,000 score
###     * if I do this, I need to add some kind of blacklist filter for the player's name
###     * in addition, I would need to check the game file to make sure the player didn't cheat
###     * it might be okay to have duplicates, but since it's not a leaderboard, 
###        it might just make more sense to tell the player their name is already in the hall of fame,
###         BUT... I think the hall of fame will show your character's race and class as well, so you could have Jeremy the Orc Knight and Jeremy the Elf Witch, etc

endGame = 11
filler = '='

classlist = ['fighter', 'spell-slinger', 'dark-knight', 'knight', 'thief', 'bard', 'duelist', 'wizard', 'witch', 'shinobi']
raceList = ['elf', 'dwarf', 'human', 'orc']
#note: if you add a boss to the monsters list that is technically plural, add their name to the plurs list in main, just before the levelUp function call
monList = [
    ["a ghost", "a death vulture", "a goblin", "a zombie", "an ogre", "a Troll", "a Saber Leopard", "a Wraith"],
    ["a ghoul", "an oozing mass", "an orc fighter", "a banshee", "a giant", "an Orc Commander", "a Cyclops", "a Witch"],
    ["a troll", "a stone golum", "an orc archer", "a hag", "a saber leopard", "a Giant Snake", "an Ettin", "a Necromancer"],
    ["a werewolf", "a young dragon", "an orc shaman", "an orc duelist", "a shadow tiger", "a Frost Giant", "a Griffin", "a Rock Giant"],
    ["a flame elemental", "an ettin", "an ancient draugr", "an undead horde", "a poltergeist", \
        "the Orc Squadron", "the Dragon", "the Army of Sorcerers"],
    ["a spriggan warlord", "a griffin", "a monstrous owlbear", "a water elemental", "a phoenix", "a frost giant", "a manticore", \
        "a necromancer", "a storm wizard", "a giant snake", "the Feral Werewolf", "the Royal Griffin", "the Vampire"],
    ["a basilisk", "a squadron of orcs", "a drider", "a persistent phantom", "an eldritch monstrocity", "a dragon", "a war sloth", \
        "an army of sorcerers", "a flying octopus", "an old griffin", "the Horde of Trolls", "the Elder Dragon", "the Mindflayer"],
    ["a hound of Topedus", "a feral werewolf", "a wight stalker", "a royal griffin", "a graveknight", "a stone dragon", "a beholder", \
        "a shadow serpent", "an uthul", "an orc warg rider", "the Werewolf Pack", "the Ancient Wyrm", "the Vampire Lord"],
    ["a moonflower", "a mindflayer", "a mohrg spawn", "a warg captain", "a hellcat", "a horde of trolls", "a blade mantis", 
        "a king shadow serpent", "a jabberwock", "a lich", "Topedus the Mouse God", "the Sea Monster", "the Arch Demon"],
    ["a pit fiend", "an undead army", "a harpy queen", "a mind flayer overlord", "a void worm", "a werewolf pack", \
        "an ifrit", "a vampire lord", "a wendigo", "a sea monster", "Okesh, the Orc World Eater", "Toroloth, the Calamity Dragon", \
            "Vuen, the Elder Goddess of Death"]
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
        #final score, decreases by 50 per wrong attack, increases by 1000 per level up (x2 in normal mode, x3 in hard mode)
        self.finscore = 0
        #player's kill count, this is your xp (monster essenses), which count up until you reach the goal or camp, it modifies how much you heal when you camp or flee
        self.killCount = 0
        #determines the width of the dungeon
        self.killGoal = 5
        #determine the size of wizard explosions
        self.expwidth = 4
        self.exheight = 1
        #strings used to add modifiers to your character
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

    #print the player's score, name, level, race, class, a health bar, and their numeric HP/maxHP
    def printHP(self):
        print("\nScore:", self.finscore)
        race = ''
        for char in range(len(self.race)):
            if char == 0:
                race += self.race[char].upper()
            else:
                race += self.race[char]
        pclass = ''
        for char in range(len(self.pclass)):
            if char == 0:
                pclass += self.pclass[char].upper()
            else:
                pclass += self.pclass[char]
        suf = 'th'
        if self.level == 1:
            suf = 'st'
        elif self.level == 2:
            suf = 'nd'
        elif self.level == 3:
            suf = 'rd'
        print(self.name, "[", str(self.level) + suf, "Level", race, pclass, "] :")
        HP = self.HP / self.maxHP * 80
        print("HP: [", end='')
        for i in range(80):
            if i < HP:
                print("=", end='')
            else:
                print("-", end='')
        print("]", str(self.HP) + '/' + str(self.maxHP))
        return
    
    #The player has either reached endgame, or chose to end the game early, printing their final score
    def gameOver(self):
        if (self.level != endGame):
            print("  _________________________________________________________________")
            print(" /                                                                 \\")
            print("|                                                                   |")
            print("|                             Game  Over...                         |")
            print("|                                                                   |")
            print(" \\_________________________________________________________________/")
        else:
            os.system("color 0A")
            print("  _________________________________________________________________")
            print(" /                                                                 \\")
            print("|                                                                   |")
            print("|                             You  win!                             |")
            print("|                                                                   |")
            print(" \\_________________________________________________________________/")
        print()
        print("YOUR FINAL SCORE:", self.finscore)
        return
    
    #the player heals a significant amount of HP, this can go beyond their maxHP, if they died, the dungeon gets re-built, 
    ## otherwise, it just resets
    def rest(self, scorehit):
        self.finscore -= scorehit * self.diffRating
        self.HP += self.killCount * 6 * self.level
        if (self.HP < self.maxHP):
            self.HP = self.maxHP
        self.killCount = 0
        flag = 0

        if (self.pclass == 'witch'):
            self.classKit1 = self.maxh
            self.classKit2 = self.maxk
        
        elif (self.pclass == 'bard'):
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
        
        elif (self.pclass == 'duelist'):
            self.classKit1 = 2 * self.level
            if (self.race == 'elf'):
                self.classKit1 += 1
    
        elif (self.pclass == 'shinobi'):
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
        
        elif (self.pclass == 'wizard'):
            if (scorehit == 1000):
                self.classKit1 = 2 + self.level
                self.classKit2 = 1
                if (self.level > 6):
                    self.classKit2 += 1
                if (self.race == 'elf'):
                    self.classKit1 += 1
            else:
                flag = 1
        
        elif (self.pclass == 'knight'):
            if self.increase == 'p':
                self.classKit1 = 1
                if (self.race == 'elf'):
                    self.classKit1 += 1
            else:
                self.classKit2 = 1
                if (self.race == 'elf'):
                    self.classKit2 += 1

        elif (self.pclass == 'thief'):
            self.classKit1 = self.level
            if (self.race == 'elf'):
                self.classKit1 += 1

        if (scorehit != 1000):
            print("You flee the dungeon and rest,\n using your monster essenses to regain your strength...")
        else:
            print("And, it appears the dungeon has shifted...")

        if (flag):
            print("Your spell slots do not regenerate, unfortunately...\n")
        
        return 

    #the intro sequence gets all the customizable character information from the player, 
    # doesn't allow them to enter options that don't exist
    def intro(self):
        print("Welcome to...")
        time.sleep(3)
        print("Matthew Walters' original game...")
        time.sleep(3)
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|                         Dungeon  Crawl!!!                         |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        
        time.sleep(3)

        difficulty = ''
        while (difficulty != 'easy' and difficulty != 'medium' and difficulty != 'hard'):
            print("Choose a difficulty: (easy, medium, hard)")
            difficulty = input()
            print()
        if difficulty == 'easy':
            self.diffRating = 1
        elif difficulty == 'medium':
            self.diffRating = 2
        else:
            self.diffRating = 3
        print("Greetings traveler...")
        print("What is your name?")
        self.name = input()
        print()

        while (self.race not in raceList):
            print("What are you? (dwarf, elf, orc, human)")
            self.race = input()
            print()
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
    
        return

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
            print(" (Enter h outside of combat),\n and one lethal poison (enter k during a fight).\n")
            print("These potion refill when you rest.\n")
        
        elif (self.pclass == 'bard'):
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
            print("As a bard, you get to choose what weapon type you enhance each level.")
            print("Choose one now...(s/b/m)")
            while (self.strongAttack != 's' and self.strongAttack != 'b' and self.strongAttack != 'm'):
                self.strongAttack = input()
                print()
            if (self.race != 'elf'):
                print("Once per level, outside of combat,\n you may choose to change your enhanced weapon type by entering 'b'\n")
            else:
                print("Twice per level, outside of combat,\n you may choose to change your enhanced weapon type by entering 'b'\n")
        
        elif (self.pclass == 'duelist'):
            self.strongAttack = 's'
            self.classKit1 = 2
            if (self.race == 'elf'):
                self.classKit1 += 1
            print("As a duelist, you are skilled with a sword,\n and can counter enemies for a chance to take no damage.")
            print("To counter attack, enter c during a fight.\n")
        
        elif (self.pclass == 'shinobi'):
            self.strongAttack = 'b'
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
            print("As a shinobi, you are skilled with a bow,\n and can always escape a fight back to the entrance of the dungeon (enter e during a fight).")
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
            print("As a wizard, you have a few spells you can use,\n and two types of spells slots, high slots and low slots")
            print("You can cast Fire Ball (enter f during a fight),\n expending one of", self.classKit1, "low spell slots that don't regenerate until you level up.\n")
            print("You can also use Invisibility (enter i during a fight),\n or Explosion (enter e outside of combat), expending one of", self.classKit2, "high spell slots\n")
        
        elif (self.pclass == 'knight'):
            self.increase = 'p'
            self.strongAttack = 's'
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
            self.maxHP += 4
            self.HP = self.maxHP
            print("As a knight, you are very hardy, you have a little more HP than other classes,\n and you are much stronger with a sword\n")
            if (self.race != 'elf'):
                print("Once per rest, you can power attack your enemy (enter p during a fight), ", end='')
            else:
                print("Twice per rest, you can power attack your enemy (enter p during a fight), ", end='')
            print("taking more damage,\n but you will progress more than one space in the direction you were moving.\n")

        elif (self.pclass == 'thief'):
            self.strongAttack = 'b'
            self.classKit1 = 1
            if (self.race == 'elf'):
                self.classKit1 += 1
                print("As a thief, you are skilled with a bow and hard to detect,\n twice per rest, you can sneak attack an enemy, taking zero damage in the fight\n")
            else:
                print("As a thief, you are skilled with a bow and hard to detect,\n once per rest, you can sneak attack an enemy, taking zero damage in the fight\n")
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
    
        print("Dungeons will look something like this:")
        print("[X] [X] [X] [O] [-]")
        print("[-] [-] [#] [-] [-]")
        print("[-] [-] [-] [-] [-]")
        print("  X : a room where you have already been, and killed the monster")
        print("  O : where you are currently")
        print("  - : a space you have yet to explore")
        print("  # : a space that cannot be entered, it is an obsticle in your path\n")
        print("the final boss of each floor will be found somewhere along the furthest column to the right,\n and you will start in the top left corner of the dungeon\n")
        print("   you -> [O] [-] [#] [-] [-] <- boss?")
        print("          [-] [-] [-] [-] [-] <- boss?\n")
        print("In order to level up and move on to the next floor of the dungeon, defeat the boss on the other end\n")
        print("Each time you enter a space you have not previously explored,\n you will be faced by some sort of monster that you must fight\n")
        print("In a fight, you can use a sword (Enter s), a bow (Enter b), or magic (Enter m);")
        print(" each monster is specifically weak to one of these.\n")
        print("You may flee to the entrance of the dungeon,\n regaining your HP and class abilities, by entering f outside of combat.\n")
        print("Outside of a fight,\n you may enter i to see what items and abilities you have collected on your adventure!\n")
        print("u makes you go up, d makes you go down, r makes you go right, and l makes you go left\n")
        print("In the dungeon, you can make camp (enter c outside of combat) to regain some HP before continuing on.\n")
        print("You must flee to regain the supplies to make camp again\n")
        print("Enter q to quit\n")
        return
    
    #levelUp means that you finished the floor and go to the next one, your maxHP increases, and HP is set to it,
    # your classKit1 or 2 items are scaled to your level, and you are reminded about them, and how many times you can use them
    def levelUp(self):
        #typical boost for all classes
        self.maxHP += 25
        self.killGoal += 2
        self.killCount = 0
        self.finscore += 1000 * self.diffRating
        self.level += 1
        self.potion = True
        
        #since the player has won the game, no need to tell them that theorhetically they could have more skill uses than before.
        if (self.level == endGame):
            return

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

        #wait until you get your race/class bonus/penalty before setting HP to max
        self.HP = self.maxHP

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
                print()
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
                print(bv[bindex], "per rest, you can war cry, restoring your strength.")
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
                print()
                if (self.increase not in choices):
                    print("That's not one of your options...")
            if (self.increase == 'h'):
                self.maxh += 1
            else:
                self.maxk += 1
            self.classKit1 = self.maxh
            self.classKit2 = self.maxk
            print("You now have", self.classKit1, "potions, and", self.classKit2, "poisons.")
        
        return

    #this happens when the player's HP hit's zero, they can continue, hurting their score; or end the game, calling gameover
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
            print()
        if (gameState == 'n'):
            self.gameOver()
            return 1
        else:
            self.killCount = 0
            print("You revive at the beginning of this floor,\n but you have lost all of your monster essences.")
            self.rest(1000)
            return 0

class monster:
    def __init__(self):
        self.damage = 0
        self.name = ''
        self.weakness = ''
        self.bossType = 0

    #there will only be one monster object, 
    # the game loop will call "m = monsterLibrary(level, damage)" for every room the player enters, 
    #  using the damage of that space to generate the monster,
    ### the bossType variable ensures that you do not encounter the monster you were told to defeat at the beginning of the level, until you reach the final space
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
            boss = random.randint(0,2)
            while (boss == bossType):
                boss = random.randint(0,2)
            jindex += boss
        elif damage == 100:
            damage = 10
            jindex += bossType
        self.damage = damage
        self.name = monList[index][jindex]
        self.weakness = weakList[index][jindex]

        return isBoss

#buildDungeon uses the player's info to generate a new floor of the dungeon, 
# it's just a 2D array of integers, used by monsterLibrary to identify the creature
def buildDungeon(pc):
    # Dungeon Key:
    ### Regular Monster [int from 1 to 10]
    ### Dead Monster    [int from -1 to -10]
    ### Obsticle        [-50]
    ### Boss Monster    [100]
    dungeon = []
    for i in range(0, pc.level + 1):
        b = []
        for j in range(0, pc.killGoal):
            b.append(random.randint(1,10))
        dungeon.append(b)
    dungeon[0][0] = -1
    #make one random square at the end of the level into a boss
    num = random.randint(1, pc.level)
    dungeon[num][pc.killGoal - 1] = 100
    #randomly generate obsticles in the dungeon, don't allow them to form on the left column, right column, or bottom row
    for i in range(0, int(pc.level/2) + 1):
        for j in range(0, pc.level):
            dungeon[j][random.randint(1,pc.killGoal-2)] = -50

    return dungeon

#When the player flees the dungeon, I'd rather they encounter the same monsters in the same order, as if they respawned,
# instead of resetting the dungeon completely, including re-structuring the obsticles
def resetDungeon(pc, dungeon):
    for i in range(0, pc.level + 1):
        for j in range(0, pc.killGoal):
            if (i != 0 or j != 0):
                if (dungeon[i][j] < 0 and dungeon[i][j] != -50):
                    dungeon[i][j] *= -1
    return dungeon

#this just takes the dungeon and describes to the player where they are, 
# where they've been, where they can't go (obsticles), but doesn't identify monsters
def printDungeon(dungeon, row, col, level, killGoal):
    for i in range(0, level + 1):
        for j in range(0, killGoal):
            print("[", end='')
            if i == row and j == col:
                print("O", end='')
            elif dungeon[i][j] == -50:
                print("#", end='')
            elif dungeon[i][j] < 0:
                print("X", end='')
            else:
                print("-", end='')
            print("] ", end='')
        print()
    return

#this takes the player's position in the dungeon and their class (pclass) to determine which actions they can take outside of combat,
# it returns a list of possible inputs that will be accepted in the game loop, as well as printing those same inputs to the screen
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

#this does the same thing as getOptions, but for combat, asking the player which attack they'd like to use,
# since each class works differently, it has to be able to print a lot of different options,
#  it also set's boss monster's damage to 15, instead of 10, this is for balance, since bosses didn't really deal enough damage
def preAttack(pc, m):
    if (m.damage == 10):
        m.damage = 15
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

#this calculates how much damage the player takes based on the game's difficulty level, 
# the monster's power level, the player's attack choice, what upgrades they've received so far, and they're race and class benefits
def calcDamage(pc, m, attackType, upgrades):
    damage = m.damage
    if pc.diffRating == 1:
        damage -= 2
    elif pc.diffRating == 3:
        damage += 2
    
    if damage <= 0:
        damage = 1

    if (pc.race == "dwarf"):
        damage /= 2
    if (pc.name == "Topedus"):
        damage = 0

    #if the attack is not a class ability, just one of (s/b/m)
    if attackType in basics:
        #if the attack is the correct one for what the monster is weak to
        if m.weakness == attackType:
            damage /= 2
            print("It's super effective!\n")
            if pc.strongAttack == attackType:
                damage /= 2
            elif pc.strongAttack2 == attackType:
                damage /= 2
            #the upgraded weapons only affect damage if they are the right weapon to use, otherwise it would be a bit silly
            if (upgrades[basics.index(attackType) + 3] == 1):
                damage /= 2
            if (upgrades[basics.index(attackType) + 3] == 3):
                damage /= 8
        else:
            print("Not very effective...\n")
            pc.finscore -= 50 * pc.diffRating
    else:
        #this is fireball for the wizard
        if (attackType == 'f'):
            damage /= 8
            if (upgrades[3] == 1 and upgrades[4] == 1 and upgrades[5] == 1 and pc.level > 4):
                damage /= 4
            if ((upgrades[3] == 3 or upgrades[4] == 3 or upgrades[5] == 3) and pc.level > 7):
                damage /= 8
            print("You cast Fire Ball!\n")
            pc.classKit1 -= 1
            print("Spell slots remaining:", pc.classKit1)
        #this is invisibility for the wizard
        elif (attackType == 'i'):
            damage = 0
            print("You cast Invisibility!\n")
            pc.classKit2 -= 1
            print("High spell slots remaining:", pc.classKit2)
        #this is the thief's sneak attack
        elif (attackType == 'h'):
            pc.classKit1 -= 1
            damage = 0
            print("You sneak attack the monster!\n")
            print("You can sneak attack", pc.classKit1, "more monsters.")
        #this is the knight's power attack
        elif (attackType == 'p'):
            print("You plow through several monsters!\n")
            pc.classKit1 -= 1
            pc.killCount += pc.level
            damage -= pc.level
            print("You can power attack", pc.classKit1, "more monsters.")
        #this is the witch's poison attack, or the shinobi's assassination attack, both have the same effect on the monster's damage
        elif (attackType == 'k'):
            damage /= 8
            if (pc.pclass == "witch"):
                pc.classKit2 -= 1
                print("You poison the monster!\n")
                print("Poison remaining:", pc.classKit2)
            elif (pc.pclass == "shinobi"):
                pc.classKit1 -= 1
                print("You assassinate the monster!\n")
                print("You can stealth attack", pc.classKit1, "more monsters.")
        #this is the duelist's counter attack, it has a random chance to fail, but only from level 3 onwards. 
        # Level 3 is the point where you are most likely to fail your counter attack, since it is based on a 1 in [player's level] chance of failure
        elif (attackType == 'c'):
            chance = random.randint(0,pc.level - 1)
            if (chance != 2):
                damage = 0
                print("You counter attack the monster!\n")
                pc.classKit1 -= 1
                print("You can counter", pc.classKit1, "more monsters.")
            else:
                print("You failed to counter the monster!\n")
                if (upgrades[3] == 1 and upgrades[4] == 1 and upgrades[5] == 1 and pc.level > 4):
                    damage /= 4
                else:
                    damage /= 2
        #this is the shinobi's escape move, which pulls them out of combat, but resets the dungeon, like when you flee
        if attackType == 'e' and pc.pclass == 'shinobi':
            damage = 0
            print("Using your escape rope, ", end='')
            pc.rest(100)
    
    #damage is not allowed to go negative and thus heal the player
    if (damage < 0):
        damage = 0
    
    return int(damage)

#discovery is used to give the player a boost when they defeat a boss,
# they receive one of three legendary weapons, which further reduce damage when that weapon is the right choice,
#  these also effect certain class's abilities, like the wizard's fireball, which is more effective if you have all 3 artifacts
def discovery(upgrades):
    flag = 2
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
    elif (upgrades[1] == 1 and upgrades[4] != 1):
        upgrades[4] = 1
        upgrades[1] = 0
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|             You have discovered the Bow of Heroes!!!              |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
    elif (upgrades[2] == 1 and upgrades[5] != 1):
        upgrades[5] = 1
        upgrades[2] = 0
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|             You have discovered the Staff of Argon!!!             |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
    else:
        flag = 0
    return flag, upgrades

#bigDiscovery is similar to discovery, but these items are much more beneficial, and are limited to 1 per game on hard mode, 
# but you can get 2 of them on medium mode, and all 3 in easy mode
def bigDiscovery(upgrades):
    flag = 1
    if (upgrades[0] == 3 and upgrades[3] != 3):
        upgrades[3] = 3
        upgrades[0] = 0
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|       You have discovered Getauskaath, the Phalanx Render!!!      |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
    elif (upgrades[1] == 3 and upgrades[4] != 3):
        upgrades[4] = 3
        upgrades[1] = 0
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|         You have discovered Orokriegr, the God Hunter!!!          |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
    elif (upgrades[2] == 3 and upgrades[5] != 3):
        upgrades[5] = 3
        upgrades[2] = 0
        print("  _________________________________________________________________")
        print(" /                                                                 \\")
        print("|                                                                   |")
        print("|      You have discovered Throshfrein, the Catalyst of Doom!!!     |")
        print("|                                                                   |")
        print(" \\_________________________________________________________________/")
        print()
    else:
        flag = 0
    return flag, upgrades

#this function is used when the player has a healing ability and uses it, or when they decide to camp,
# it is less effective than fleeing, but doesn't destroy your progress
### camping is also more effective allowing the player to heal all the way to double their maxHP, unlike class abilities
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

#powerAttack is used by the knight class, pushing the player further into the dungeon, as long as they don't hit an obsticle
# they will continue in the direction of their previous move, it is generally most effective when moving to the right
def powerAttack(dungeon, move, level, killGoal, row, col):
    for step in range(0, level):
        dungeon[row][col] *= -1
        if (row > 0 and move == 'u'):
            if (dungeon[row - 1][col] != -50):
                row -= 1
        elif (row < level and move == 'd'):
            if (dungeon[row + 1][col] != -50):
                row += 1
        elif (col < killGoal - 1 and move == 'r'):
            if (dungeon[row][col + 1] != -50):
                col += 1
        elif (col > 0 and move == 'l'):
            if (dungeon[row][col - 1] != -50):
                col -= 1

    return dungeon, row, col

#inventory shows the player which weapon is their most effective, whether they've collected legendary weapons,
# if they've camped or not this level, and how many uses they have for their class abilities
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
    if (upgrades[3] == 1):
        print("  the Sword of Destiny", end='')
    elif (upgrades[3] == 3):
        print("  Getauskaath, the Phalanx Render", end='')
    elif (pc.strongAttack == 's' or pc.strongAttack2 == 's'):
        print("  a good sword", end='')
    else:
        print("  a sword", end='')    
    if (pc.pclass == "bard" and pc.strongAttack == 's'):
        print("(enhanced)")
    else:
        print()
    #Bow stuffs
    if (upgrades[4] == 1):
        print("  the Bow of Heroes", end='')
    elif (upgrades[4] == 3):
        print("  Orokriegr, the God Hunter", end='')
    elif (pc.strongAttack == 'b' or pc.strongAttack2 == 'b'):
        print("  a longbow", end='')
    else:
        print("  a bow", end='')
    if (pc.pclass == "bard" and pc.strongAttack == 'b'):
        print("(enhanced)")
    else:
        print()
    #Magic stuffs
    if (upgrades[5] == 1):
        print("  the Staff of Argon", end='')
    elif (upgrades[5] == 3):
        print("  Throshfrein, the Catalyst of Doom", end='')
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

#this function could use player and dungeon information to carry out the wizard's explosion ability,
# but I really just wanted to get the massive text block out of the main function
def explode():
    print("  _________________________________________________________________")
    print(" /                                                                 \\")
    print("|                                                                   |")
    print("|                             EXPLOSION!                            |")
    print("|                                                                   |")
    print(" \\_________________________________________________________________/")
    print()

#colorScreen is used to call the color function in the command prompt, at first, the screen is black with green letters,
# at level 5+, the letters are yellow, at 8+, the letters are purple. Originally they were red, but the letters turn red on player death, so 
#  it felt like you died when actually you were just leveling up to 8 or higher, so they became purple to prevent this confusion.
def colorScreen(level):
    if level >= 8:
            os.system("color 0D")
    elif level >= 5:
        os.system("color 0E")
    else:
        os.system("color 0A")

#here's the actual game, it is structured in this way:
### forEach level from 1 to endGame:
###     build the dungeon
###     determine the boss
###     while player is not at the boss
###         printHP
###         printDungeon
###         ask player for next action
###         if they move, move them
###             if space not negative (dead), reveal the monster
###             player chooses attack type or class ability
###             calculate damage
###         if they don't move, handle the action and restart While loop
###         if  : player dies, continue screen, 
###             if they choose to continue, restart For loop (player's level stays the same), decrease player's score, 
###             else print score and end game
###         else: multiply space by -1, manage magic items, increase killcount, restart While loop
###     end while
###     if we got here, they already fought the boss
###     player's level += 1
###     since they level up, increase maxHP, set HP to max, handle other levelUp bonuses, reset position to [0][0], restart For loop
### end for
def main():
    #set color to black with green characters
    os.system("color 0A")
    #initialize all of our variables, including the player
    pc = player()
    m = monster()
    disc = 0
    upgrades = [0,0,0,0,0,0]
    row = 0
    col = 0
    
    #big bits of text, character creation, description of the game's processes
    pc.intro()
    pc.setup()

    counter = 1
    if (pc.diffRating == 2):
        counter += 1
    elif (pc.diffRating == 1):
        counter += 2

    for level in range(1, endGame):
        colorScreen(level)
        #set up for discovering legendary weapons, specifically once per floor if requirements are met
        if (disc != 4):
            disc = 0
        #build the level with random numbers
        dungeon = buildDungeon(pc)
        #determine the boss type, so that you can tell the player their intended final fight for the level,
        ## plus, if they find a boss monster (space == 10) prior to the final fight (space == 100), then force it to not be the same as the final fight
        bossType = random.randint(0,2)
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
                print()
                if (gameState not in options):
                    print("You can't do that...")
                    reloop += 1
                    break
            #resets the loop, so they don't lose track of the dungeon if they accidentally mistype
            if (reloop):
                continue

            #the player is using a move action, thus moving to a new room, and possibly starting Combat 
            if (gameState in moves):
                move = gameState
                if (gameState == 'u'):
                    row -= 1
                elif (gameState == 'd'):
                    row += 1
                elif (gameState == 'l'):
                    col -= 1
                elif (gameState == 'r'):
                    col += 1
                #if they've already killed a monster in a particular room, reset the loop, because the rest of this loop is Combat
                if (dungeon[row][col] < 0 and dungeon[row][col] != -50):
                    print("The monster here is already dead.")
                    continue
                #if the monster is not dead, look it up, prepare for battle!
                #check if the monster is the boss, for the while loop, so they can level up
                isBoss = m.monsterLibrary(level, dungeon[row][col], bossType)
                #check if the monster is any type of boss, so we can handle item discovery
                if (m.damage == 10) and disc == 0:
                    #this is the first level of weapon upgrades, these can be found as early as level 1
                    if(m.weakness == 's' and upgrades[3] == 0):
                        upgrades[0] = 1
                        disc = 1
                    elif (m.weakness == 'b' and upgrades[4] == 0):
                        upgrades[1] = 1
                        disc = 1
                    elif (m.weakness == 'm' and upgrades [5] == 0):
                        upgrades[2] = 1
                        disc = 1
                    
                    #this is the second level of weapon upgrades, the player can only receive 1 or 2 of them if playing in hard or medium mode, respectively.
                    # They are only accessible at level 7 and up, and decrease damage significantly more than their predecessors.
                    if (level >= 7):
                        if (m.weakness == 's' and upgrades[3] == 1):
                            disc = 3
                            upgrades[0] = 3
                        elif (m.weakness == 'b' and upgrades[4] == 1):
                            disc = 3
                            upgrades[1] = 3
                        elif (m.weakness == 'm' and upgrades[5] == 1):
                            disc = 3
                            upgrades[2] = 3

                #get player's attack/class ability options
                options = preAttack(pc, m)
                gameState = ''
                #get player's input for their attack
                while (gameState not in options):
                    gameState = input()
                    print()
                    if (gameState not in options):
                        print("You can't do that...")
                
                #handle power attack's movement
                if gameState == 'p':
                    dungeon, row, col = powerAttack(dungeon, move, level, pc.killGoal, row, col)
                
                #calculate damage to deal to the player, according to the monster and player's decision
                damage = calcDamage(pc, m, gameState, upgrades)
                
                #this is for the shinobi's escape, it resets the dungeon, obsticles and all, 
                # unless I add some functionality to buildDungeon, so I can reset the dead to their original monsters, but not move the obsticles around
                if (gameState == 'e'):
                    upgrades[0] = 0
                    upgrades[1] = 0
                    upgrades[2] = 0
                    if (disc != 4):
                        disc = 0
                    row = 0
                    col = 0
                    dungeon = resetDungeon(pc, dungeon)
                    continue
                
                #actually deal the damage to the player
                print("You take", damage, "damage.")
                pc.HP -= damage
                
                #without this, you never saw how close you might have come to dying vs. the boss, so the extra print is nice
                if (isBoss):
                    pc.printHP()
                
                ### The Player Has Died
                if (pc.HP <= 0):
                    isBoss = False
                    os.system("color 0C")
                    quitter = pc.youDied()
                    if (quitter):
                        return
                    colorScreen(level)
                    row = 0
                    col = 0
                    dungeon = buildDungeon(pc)
                    continue
                
                ### The Player has not died, thus defeating the monster, now they take damage and maybe discover items
                dungeon[row][col] *= -1
                pc.killCount += 1
                print("You now have", pc.killCount, "monster essenses.")
                if (disc == 1):
                    disc, upgrades = discovery(upgrades)
                if (disc == 3):
                    flag, upgrades = bigDiscovery(upgrades)
                    if (flag != 0):
                        counter -= 1
                        if (counter <= 0):
                            disc = 4
            
            #the player did not make a move action, handle the action, combat will not occur this iteration
            else:
                #this is the flee action, they reset their position and all monsters respawn.
                # fleeing is preferable to dying, but it still hurts the player's score, in addition, you can heal beyond your max health,
                #  there is actually no limit to how high your health can get when you flee, 
                #   just in case the only path through the dungeon is unachievable with max health.
                if (gameState == 'f'):
                    row = 0
                    col = 0
                    dungeon = resetDungeon(pc, dungeon)
                    pc.rest(200)
                
                #this is not like fleeing, does not hurt your score, but can only be done a certain number of times per level, and only by some player classes
                elif (gameState == 'w' or gameState == 'c' or gameState == 'h'):
                    heal(pc, gameState)
                
                #this shows the player's inventory, and reminds them of the current Boss monster they are going after
                elif (gameState == 'i'):
                    inventory(pc, upgrades)
                    m.monsterLibrary(level, 100, bossType)
                    print("\nRemember, to complete this floor of the dungeon, you must defeat", m.name + "!")
                
                #this is the bard's skill to change their strong attack, they generally can only do this once per level
                elif (gameState == 'b'):
                    pc.classKit1 -= 1
                    print("Which attack type do you wish to enhance? (s/b/m)")
                    pc.strongAttack = ''
                    while (pc.strongAttack not in basics):
                        pc.strongAttack = input()
                        print()
                        if (pc.strongAttack not in basics):
                            print("You can't do that...")

                #this is the wizard's explosion skill, it kills a large number of enemies to the player's right, it cannot kill the boss monster,
                # it also does not destroy obsticles in the dungeon
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
                
                #this is how you quit the game, it makes sure the player actually wants to quit before it ends the game.
                elif (gameState == 'q'):
                    print("ARE YOU SURE??? (y/n)")
                    gameState = ''
                    while (gameState != 'y' and gameState != 'n'):
                        gameState = input()
                        print()
                        if (gameState != 'y' and gameState != 'n'):
                            print("You can't do that...")
                    if (gameState == 'y'):
                        pc.gameOver()
                        return
                    
        #if you got to the boss, level up here
        # but first, if the boss is plural, say they used the souls of them, not the soul of them
        plurs = ["the Army of Sorcerers", "the Horde of Trolls", "the Werewolf Pack", "the Orc Squadron"]
        soul = "soul"
        if (m.name in plurs):
            soul += 's'
        print("You use the", soul, "of", m.name, "to grow stronger", end='')
        if (level + 1 == endGame):
            print(", and become the most powerful creature in the world!!!")
        else:
            print('.')
        row = 0
        col = 0
        if (disc != 4):
            disc = 0
        pc.levelUp()

    #if you reach this point, you won! and the game will end after showing you your score
    pc.gameOver()
    return

if __name__ == "__main__":
    main()