# Dungeon-Crawl
in order to play this game, all you need is a c++ compiler, and a terminal  
to compile it, run "g++ -o game game.cpp"  

to play, "./game"  
if your terminal supports the "color" command, it will turn black with green characters  

Gameplay  
  In this game, you are fighting to get to and defeat the boss of level 10 of the dungeon.  To do so, you fight monsters,  
    You will have 3 attack options, s (sword), b (bow), and m (magic), each monster has a weakness, and if you choose the right weapon,  
    you will take less damage than you would using the other 2 attack types.  
  You are trying to reach to final boss of the dungeon.  To do so, fight your way from the left side to the right side of the dungeon,  
    and somewhere along the far side, is the boss of this level.  When you defeat the boss, you level up, and find yourself on a different, and bigger,  
    floor.  
  Dungeons will look something like this:  
	[X] [X] [X] [O] [-]  
	[-] [-] [#] [-] [-]  
	[-] [-] [-] [-] [-]  
	X : a room where you have already been, and killed the monster  
	O : where you are currently  
	- : a space you have yet to explore  
	# : a space that cannot be entered, it is an obstacle in your path  
	the final boss of each floor will be found somewhere along the furthest column to the right, and you will start in the top left corner of the dungeon  
	you -> [O] [-] [#] [-] [-] <- boss?  
	       [-] [-] [-] [-] [-] <- boss?  
 
  Outside of combat, you have lots of options, which will look something like this:  
  "How do you wish to proceed? (u/l/d/r/f/c/i/q)"  
  u - up         (go up, fight a monster if its not already dead)  
  l - left       (go left)  
  d - down       (go down)  
  r - right      (go right)  
  f - flee       (send your character back to the top left of the floor, all enemies respawn, you regain health based on how many monster essenses you have)  
  c - camp       (spend your monster essenses to regain a smaller amount of health than if you had fled, but you don't reset the floor)  
  i - inventory  (check your inventory, as you can receive special weapons that reduce damage even further when they are the right attack, and your class items)  
  q - quit       (quit the game, there is no save feature at this time, you will lose all progress if you confirm the quit action)  
  
Note: flee and camp can increase your health beyond the listed maximum, since the floor may be unbeatable without more health than you start with...  
However, camp can only increase your health to double your maximum, while flee is uncapped  
  
Starting the Game  
  At the start, you are asked for your choice of difficulty, this will modify monster damage  
  then your name, give it a name  
  Then, you are asked for your fantasy race, (Dwarf, Orc, Elf, Man)  
  Dwarfs take less damage when they attack correctly, but gain less health per level up than men and orcs  
  Orcs begin the game with more health than other classes, and gain more health per level up  
  Elves receive 1 more of certain class items/skill uses than other races, but also gain less health per level up than men and orcs  
  Men have no bonuses, but also no drawbacks  
  
Speaking of Classes  
  There are 10 different classes, with different abilities  
  Each class begins with one weapon that reduces damage more than the others do, if the monster is weak to that weapon  

The "easy" classes actually have 2 weapons that are better than average  
  Fighter: strong with Swords and Bows  
  Spell-Slinger: strong with Bows and Magic  
  Dark-Knight: strong with Swords and Magic  
  
Each class beyond this point has class items or skills that are restored when they level up or flee.  
  
The "moderate" classes have one class item or skill, that gets better as they level up, and one single stronger weapon  
  Knight: strong with Swords, and begin the game with Power Attack, but can switch to war cry or back to power attack during level ups  
    Power Attack - When you are in combat, whichever direction you stepped into this room,  
      you will continue and kill every monster for a few rooms (increasing with level),  
      however, you take increased damage than you would from the monster normally, this is recommended only to be used on the weaker monsters of the floor.  
    War Cry - This skill heals you much like camping does, it does not reset the floor, nor your location (but you can only heal up to your maximum HP, not more)  
      however, it does not expend your monster essenses like camping does.  
      
  Thief: strong with Bows, and begin the game with 1 Sneak Attack, with which you take no damage when killing the enemy,  
      you gain one more sneak attack per level and, elves begin the game with 2.  
  
  Bard: Bards actually choose which weapon they are strong with, and can change it once per level up,  
      and their strong weapon reduces damage much more than other classes.  
  
  Duelist: strong with Swords, and have a high number of Counter Attacks, 2 x your level (+1 for elves) 
      Counter Attack: You have a chance to negate the damage of an attack, but if it fails, you only reduce the damage slightly.  
          Your chances of countering your opponent get higher with your level as well.  
      
The "advanced" classes have multiple class items/abilities  
  Wizard: strong with magic, and have 2 types of spell slots.  Low spell slots can be used to cast 'fireball'  
      in combat to reduce damage similarly to choosing the correct attack type, and High spell slots (only increased at level 6) are used for 'invisibility'  
      in combat, to reduce damage to 0, or to cast 'explosion' outside of combat, killing a large square of enemies all at once, but only enemies to your right,  
      and not including the boss of the floor.  This square increases in size at level 5 and 8.  
      
  Witch: strong with magic, and have healing potions, and deadly poisons.  Using poison in combat reduce the damage you take, similar to choosing the correct attack type,  
      and healing potions heal you (no more than your maximum health) based on your monster essenses, without spending them.  
      On level up, you choose to increase the quantity of either potions or poisons by 1.  
        
  Shinobi: strong with bows, can use Stealth Attack, which reduces damage, similar to choosing the correct attack type, with increased number of uses each level up,  
      shinobi can also flee in combat.  This resets the floor, but it means you won't die when encountering a monster you know will kill you.  
        
I hope you enjoy my game, there is a score system, based on difficulty, how many levels you beat, and how many wrong attacks you use.  
The maximum score is 30,000 but don't worry, it's not easy, I haven't received a perfect score with every class yet either.
