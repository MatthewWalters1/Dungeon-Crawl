#include <iostream>
#include <cstdlib>
#include <time.h>
#include <string>
#include <iomanip>
#include <vector>
using namespace std;

    //future goals:

struct player {
	//the remaining HP of the player
	int HP;
	//the maximum HP of the player
	int maxHP;
	//these vary between classes, but they are the resourses expended to use class abilities
	int classKit1;
	//some classes have a 2nd resourse also to be expended
	int classKit2;
	//for witches almost exclusively, this is the max number of healing potions
	int maxh;
	//for witches almost exclusively, this is the max number of poisons (which reduce monster damage significantly)
	int maxk;
	//this is the player's level, which controls the damage of enemies, how much the player heals on rest or flee, and the height of the dungeon
	int level;
	//this is your final score, it increases by 1,000 per level up (x2 in normal mode, x3 in hard mode) and decreases by 100 per wrong attack type, and 1,000 per death(also x2 in normal, x3 in hard)
	int finScore;
	//this is the height of the wizard's explosion spell, it is increased with expwidth at level 5 and 8
	int exheight;
	//this is the width of the wizard's explosion spell, it can be increased at level 5 and 8
	int expwidth;
	//this is the player's class, which determines their abilities and sometimes their HP increases on level ups
	string character;
	//this is the player's race, it changes how the player's HP increases per level, elves also get an extra classKit use, and dwarves reduce monster damage a little more
	string race;
	//this is the best attack type of the player's class, if it's the right move, it reduces monster damage significantly
	char strongAttack;
	//the simple classes have a second attack type that is just as good as the first strongAttack
	char strongAttack2;
	//this is used during level-ups, some classes can choose to upgrade one skill or another
	string increase;
	//this is the player's chosen name, if it is "Topedus" the player cannot take damage
	string cname;
	//this is the game difficulty, easy reduces monster damage, hard increases monster damage, and medium and hard give a better final score than easy
	string difficulty;
};

struct monster {
	//this is the base damage a monster will deal to the player, which is modified by many variables
	int damage;
	//this is the name of the creature that the player sees, so they can guess what attack type is the best to use
	string type;
	//this is the attack type the player should use to take the least amount of damage
	char bestAttack;
};
class cell {
	public:
		int x;
		int y;
};
//this function prints the players name and their HP in a fun visual
void printHP(char &filler, player &pc);
//this function activates if the player survives fighting a boss, in which they will get a stronger weapon(once per weapon type)
void discovery(bool &sod, bool &boh, bool &soa, bool &sodestiny, bool &boheroes, bool &soargon);
//this function shows the player the remaining uses of their class abilities, their monster essenses, and whether they can camp or not
void inventory(bool &potion, int &killCount, bool &sodestiny, bool &boheroes, bool &soargon, player &pc);
//this function activates when the player says flee, they lose their xp for the current level and heal a certain amount 
//based on their kill count. ||**Their HP can get higher than their maxHP and that is ok**||
void rest(int &killCount, int &killGoal, char &filler, vector<vector<int> > &dungeon, player &pc, monster &m);
//this function restores player HP when they use healing classKit abilities or their potions (resting), this cannot exceed double the player's HP
void heal(int &killCount, player &pc, char &filler);
//this function happens when the player reaches the current kill goal, in which they will start fighting higher damage monsters, but the player also has better stats
void levelUp(vector<vector<int> > &dungeon, int &killGoal, char &filler, player &pc, monster &m, int &flor, int &pos);
//this function starts off the game, asking for difficulty, race, class. and then gives you your abilities based on your class
void intro(player &pc);
//this function literally makes a list(a vector) of random numbers(ints) 
void buildDungeon(vector<vector<int> > &dungeon, int &killGoal, monster &m, player &pc);
//for easy mode, the dungeon is sorted from easiest to hardest
void ins(vector<int> &dungeon, int killGoal);
//this function sets up discovery for rare weapons, and shows the extra class abilities for those who can do more than s,b,m
void preAttack(monster &m, bool &disc, bool &sodestiny, bool &sod, bool &boheroes, bool &boh, bool &soargon, bool &soa, player &pc);
//this function uses a bunch of variables based on your class, race, level, rare weapons and attack type to determine the damage dealt (this might need balancing)
void damageCalc(char &attackType, bool &disc, bool &sod, bool &soa, bool &boh, bool &sodestiny, bool &boheroes, bool &soargon, int &killCount, int &killGoal, monster &m, player &pc);
//this function uses the vector made in buildDungeon to establish the rest of the variables for the monster you are about to face
void monsterLibrary(player &pc, monster &m, int newNum = 3);
//this function provides a 2d dungeon layout for the rest of the game
char killed(vector<vector<int> > &dead, int &flor, int &pos, int &a, int &b) {
	char k;
	if (a == flor && b == pos) {
		k = 'O';
	}
	else if (dead[a][b] == 100) {
		k = '#';
	}
	else if (dead[a][b] > 0) {
		k = 'X';
	}
	else if (dead[a][b] <= 0) {
		k = '-';
	}
	return k;
}
int main() {
	//this sets the terminal color to green on black for the start of the game
	system("color 0A");
	//this is the player object, made up of variables listed in the player class above
	player pc;
	pc.HP = 25;
	pc.maxHP = 25;
	pc.level = 1;
	//this is the player's one healing potion they receive per level, some classes have abilities to heal in other ways as well
	bool potion = true;
	//this is the monster object, built in monsterLibrary based off of the damage integer in the dungeon vector
	monster m;
	//this variable is used for the discovery of rare weapons
	bool disc = false;
	//this variable tells the system the player should discover the sword of destiny at the end of the loop
	bool sod = false;
	//this variable tells the system the player should discover the bow of heroes at the end of the loop
	bool boh = false;
	//this variable tells the system the player should discover the staff of argon at the end of the loop
	bool soa = false;
	//this variable tells the system the player has the sword of destiny
	bool sodestiny = false;
	//this variable tells the system the player has the bow of heroes
	bool boheroes = false;
	//this variable tells the system the player has the staff of argon
	bool soargon = false;
	pc.finScore = 10000;
	//this is your xp, (monster essenses) which count up until you reach the goal or camp, and modify how much you heal when fleeing or camping
	int killCount = 0;
	//this is the level you must reach in order to see ("you win")
	int endgame = 11;
	//this determines the width of the dungeon 
	int killGoal = 5;
	//this is the input for whether to move, rest, heal, or check inventory
	char gameState;
	//this is the row in the dungeon
	int flor = 0;
	//this is the column in the dungeon
	int pos = 0;
	//this is the attack used by the player
	//string attackType;
	char attackType;
	//this fills out the HP bar with whatever symbol you want
	char filler = '=';
	//this is the boss required to beat the level you're on
	string bossType;
	//this matrix holds the damage value of the monster in each room
	vector<vector<int> > dungeon;
	pc.expwidth = 4;
	pc.exheight = 1;
	//this vector is pushed into the dead vector of vectors when resetting it
	vector<int> rooms;
	//this matrix is used to indicate whether a room has a living monster, an obstacle, and the final boss of the dungeon
	vector<vector<int> > dead;
	//this matrix is used to hold the positions of the obsticles if the same dungeon has to be reset, since you want the obsticles to stay where they were
	vector<vector<bool> > obst;
	//this vector is pushed into the obst vector of vectors when resetting it
	vector<bool> R;
	for (flor = 0;flor <= pc.level;flor++) {
		for (pos = 0;pos < killGoal;pos++) {
			rooms.push_back(0);
		}
		dead.push_back(rooms);
		rooms.clear();
	}
	flor = 0;
	pos = 0;
	srand(time(NULL));
	intro(pc);
	cout << "Dungeons will look something like this:\n";
	cout << "[X] [X] [X] [O] [-]\n";
	cout << "[-] [-] [#] [-] [-]\n";
	cout << "[-] [-] [-] [-] [-]\n";
	cout << "  X : a room where you have already been, and killed the monster\n";
	cout << "  O : where you are currently\n";
	cout << "  - : a space you have yet to explore\n";
	cout << "  # : a space that cannot be entered, it is an obsticle in your path\n\n";
	cout << "the final boss of each floor will be found somewhere along the furthest column to the right, and you will start in the top left corner of the dungeon\n\n";
	cout << "   you -> [O] [-] [#] [-] [-] <- boss?\n";
	cout << "          [-] [-] [-] [-] [-] <- boss?\n\n";
	cout << "In order to level up and move on to the next floor of the dungeon, defeat the boss on the other end\n\n";
	cout << "Each time you enter a space you have not previously explored, you will be faced by some sort of monster that you must fight\n\n";
	cout << "In a fight, you can use a sword (Enter s), a bow (Enter b), or magic (Enter m);";
	cout << " each monster is specifically weak to one of these.\n\n";
	cout << "You may flee to the entrance of the dungeon, regaining your HP and class abilities, by entering f outside of combat.\n\n";
	cout << "Outside of a fight, you may enter i to see what items and abilities you have collected on your adventure!\n\n";
	cout << "u makes you go up, d makes you go down, r makes you go right, and l makes you go left\n\n";
	cout << "In the dungeon, you can make camp (enter c outside of combat) to regain some HP before continuing on,\n\n";
	cout << "you must flee to regain the supplies to make camp again\n\n";
	cout << "Enter q to quit\n\n";
	printHP(filler, pc);
	
	dead[0][0] = 1;
	buildDungeon(dungeon, killGoal, m, pc); 
	//this makes the monster at the end of each level into a boss
	int num = rand() % pc.level + 1;
	//this sets a specific boss out of three to make the boss at the end of the level, it will not appear anywhere else in the dungone
	int newNum = rand() % 3;
	//this is used in random number generation
	int rando = 0;
	dungeon[num][killGoal - 1] = 10;
	dead[num][killGoal - 1] = -50;
	for (int i = 0;i < pc.level;i++) {
		dead[i][(rand()%(killGoal-2)) + 1] = 100;
	}
	for (flor = 0;flor <= pc.level;flor++) {
		for (pos = 0;pos < killGoal + 1;pos++) {
			if (dead[flor][pos] == 100) {
				R.push_back(true);
			}
			else {
				R.push_back(false);
			}
		}
		obst.push_back(R);
		R.clear();
	}
	flor = 0;
	pos = 0;
	m.damage = 10;
	monsterLibrary(pc, m, newNum);
	bossType = m.type;
	//this checks if the player is level 5
	bool check5 = false;
	//this checks if the player is level 8
	bool check8 = false;
	cout << "To defeat the dungeon, first traverse this floor and defeat" << bossType << '\n';
	while (pc.level < endgame) {
		if (pc.level > 8 && check8 == false) { 
			check8 = true;
			system("color 0D"); //set terminal color to purple on black for the last 2 levels (red on black is too much like dying)
		}
		else if (pc.level > 4 && check5 == false) { 
			check5 = true;
			system("color 0E"); //set terminal color to yellow on black for the slightly harder middle levels
		}
		for (int j = 0;j <= pc.level;j++) {	
			for (int i = 0;i < killGoal;i++) {
				cout << "[" << killed(dead, flor, pos, j, i) << "] "; 
			}
			cout << '\n';
		}
		cout << "How do you wish to proceed? (";
		if (flor > 0 && dead[flor - 1][pos] != 100) {
			cout << "u/";
		}
		if (pos > 0 && dead[flor][pos - 1] != 100) {
			cout << "l/";
		}
		if (flor < pc.level && dead[flor + 1][pos] != 100) {
			cout << "d/";
		}
		if (pos < killGoal - 1 && dead[flor][pos + 1] != 100) {
			cout << "r/";
		}
		cout << "f";
		if (pc.character == "knight" && pc.increase == "w" && pc.classKit2 > 0) {
			cout << "/w";
		}
		if (pc.character == "bard" && pc.classKit1 > 0) {
			cout << "/b";
		}
		if (pc.character == "wizard" && pc.classKit2 > 0) {
			cout << "/e";
		}
		if (pc.character == "witch" && pc.classKit1 > 0) {
			cout << "/h";
		}
		if (potion == true) {
			cout << "/c";
		}
		cout << "/i/q)" << '\n';
		do {
			cin >> gameState;
		}while (gameState != 'r' && gameState != 'h' && gameState != 'i' && gameState != 'w' && gameState != 'b' && gameState != 'u' && gameState != 'd' && 
				gameState != 'l' && gameState != 'f' && gameState != 'q' && gameState != 'c' && gameState != 'e');
			if (gameState != 'f' && gameState != 'h' && gameState != 'i' && gameState != 'w' && gameState != 'b' && gameState != 'q' && gameState != 'c' && gameState != 'e') {
				if (gameState == 'u' && flor > 0 && dead[flor - 1][pos] != 100) {
					flor -= 1;
				}
				else if (gameState == 'd' && flor < pc.level && dead[flor + 1][pos] != 100) {
					flor += 1;
				}
				else if (gameState == 'r' && pos < killGoal - 1 && dead[flor][pos + 1] != 100) {
					pos += 1;
				}
				else if (gameState == 'l' && pos > 0 && dead[flor][pos - 1] != 100) {
					pos -= 1;
				}
				else {
					cout << "You can't do that\n";
					continue;
				}
				if (dead[flor][pos] > 0) {
					cout << "The monster here is already dead\n";
					continue;
				}
				m.damage = dungeon[flor][pos];
				if (dead[flor][pos] == -50) {
					monsterLibrary(pc, m, newNum);
				}
				else {
					monsterLibrary(pc, m);
				}
				if (dead[flor][pos] != -50 && m.type == bossType) {
					//this condition stops the final boss of each level from popping up before 
					//the player gets to the end of the level
					//it has to reset to 10 since being a boss sets it to 15 in monsterLibrary
					m.damage = 10;
					rando = newNum;
					while (rando == newNum) {
						rando = rand() % 3;
					}
					monsterLibrary(pc, m, rando);
					m.damage = 15;
				}
				preAttack(m, disc, sodestiny, sod, boheroes, boh, soargon, soa, pc);			
				//here, we ignore the line the user entered, so if they accidentally enter 'rrrs' or something, 
				//their 's' command won't automatically be their attack type before they even know what the monster is
				cin.ignore(INT_MAX, '\n');
				cin >> attackType;
				bool check = false;
				//this makes sure only proper inputs are allowed for attacktypes, so users don't accidentally enter something they didn't want to for attacks
				while (check == false) {
					check = true;
					while (attackType != 'h' && attackType != 'f' && attackType != 'p' && attackType != 'e' && attackType != 's' && 
					attackType != 'b' && attackType != 'm' && attackType != 'k' && attackType != 'i' && attackType != 'c') {
						cout << "That's not a valid attack type\n";
						cin >> attackType;
					}
					if ((attackType == 'f' && pc.character != "wizard") || (attackType == 'p' && pc.character != "knight") || (attackType == 'k' && 
						(pc.character != "witch" && pc.character != "shinobi")) || (attackType == 'e' && pc.character != "shinobi") || 
						(attackType == 'h' && pc.character != "thief") || (attackType == 'i' && pc.character != "wizard") || (attackType == 'c' && pc.character != "duelist")) {
							check = false;
					}
					else if (attackType == 'f' || attackType == 'p' || attackType == 'h' || attackType == 'c') {
						if (pc.classKit1 == 0) {
							check = false;
						}
					}
					else if (attackType == 'k') {
						if (pc.character == "witch" && pc.classKit2 == 0) {
							check = false;
						}
						else if (pc.character == "shinobi" && pc.classKit1 == 0) {
							check = false;
						}
					}
					else if (attackType == 'i') {
							if (pc.classKit2 == 0) {
							check = false;
						}
					}
					if (check == true) break;
					cin.ignore(1);
					if (check == false) attackType = 'a';
				}			
				if (((attackType == 'f' && pc.character == "wizard") || (attackType == 'p' && pc.character == "knight")) && pc.classKit1 < 1) {
					m.damage = dungeon[flor][pos];
					monsterLibrary(pc, m);
					preAttack(m, disc, sodestiny, sod, boheroes, boh, soargon, soa, pc);
					cin >> attackType;
				}
				damageCalc(attackType, disc, sod, soa, boh, sodestiny, boheroes, soargon, killCount, killGoal, m, pc);
				
				if (pc.character == "shinobi" && attackType == 'e') {
					rooms.clear();
					//this vector of cells stores the obsticles in the dungeon, so when it is reset during a shinobi escape, the obsticles remain
					vector<cell> bob;
					//this is a cell for the bob vector
					cell borsch;
					for (int i = 0;i < dead.size();i++) {
						for (int j = 0;j < dead[i].size();j++) {
							if (dead[i][j] == 100) {
								borsch.x = i;
								borsch.y = j;
								bob.push_back(borsch);
							}
						}
					}
					dead.clear();
					for (flor = 0;flor <= pc.level;flor++) {
						for (pos = 0;pos < killGoal;pos++) {
							rooms.push_back(0);
						}
						dead.push_back(rooms);
					}
					dead[0][0] = 1;
					for (int i = 0;i < bob.size();i++) {
						dead[bob[i].x][bob[i].y] = 100;
					}
					flor = 0;
					pos = 0;
					num = rand() % pc.level + 1;
					dungeon[num][killGoal - 1] = 10;
					dead[num][killGoal - 1] = -50;
					potion = true;
					killCount = 0;
					continue;
				}
				if (m.damage < 0) {
					m.damage = 1;
				}
				if (pc.cname == "Topedus") {
					m.damage = 0;
				}
				if (pc.character == "bard" && attackType == pc.strongAttack && m.bestAttack == attackType) {
					m.damage /= 4;
				}
				cout << "You take " << m.damage << " damage..." << '\n' << '\n';
				dead[flor][pos] += 1;
				pc.HP -= m.damage;
				if (pc.character == "knight" && attackType == 'p' && pc.increase == "p") {
					int z;
					if (gameState == 'u') {
						for (z = 0;z <= pc.level;z++) {
							if (flor > 0 && dead[flor - 1][pos] != 100 && dead[flor - 1][pos] != -50) {
								flor -= 1;
								dead[flor][pos] = 10;
								killCount++;
							}
						}
					}
					else if (gameState == 'd') {
						for (z = 0;z <= pc.level;z++) {
							if (flor < pc.level && dead[flor + 1][pos] != 100 && dead[flor + 1][pos] != -50) {
								flor += 1;
								dead[flor][pos] = 10;
								killCount++;
							}
						}
					}
					else if (gameState == 'r') {
						for (z = 0;z <= pc.level;z++) {
							if (pos < (killGoal - 1) && dead[flor][pos + 1] != 100 && dead[flor][pos + 1] != -50) {
								pos += 1;
								dead[flor][pos] = 10;
								killCount++;
							}
						}
					}
					else {
						for (z = 0;z <= pc.level;z++) {
							if (pos > 0 && dead[flor][pos - 1]) {
								pos -= 1;
								dead[flor][pos] = 10;
								killCount++;
							}
						}
					}
				}
				printHP(filler, pc);
				killCount += 1;
				if (pc.HP <= 0) {
					system("color 0C");
						cout << "  _________________________________________________________________\n";
						cout << " /                                                                 \\\n"; 
						cout << "|                                                                   |\n";
						cout << "|                             You  Died                             |\n";
						cout << "|                                                                   |\n";
						cout << "|___________________________________________________________________|\n";
					cout << "Continue? (y/n)\n";
					do {
						cin >> gameState;
					}while (gameState != 'y' && gameState != 'n');
					if (gameState == 'y') {
						pc.finScore -= 1000;
						killCount = 0;
						disc = false;
						sod = false;
						boh = false;
						soa = false;
						rooms.clear();
						dead.clear();
						for (flor = 0;flor <= pc.level;flor++) {
							for (pos = 0;pos < killGoal;pos++) {
								rooms.push_back(0);
							}
							dead.push_back(rooms);
							rooms.clear();
						}
						for (flor = 0;flor <= pc.level;flor++) {
							for (pos = 0;pos < killGoal;pos++) {
								if (obst[flor][pos] == true) {
									dead[flor][pos] = 100;
								}
							}
						}
						flor = 0;
						pos = 0;
						dead[0][0] = 1;
						dead[num][killGoal - 1] = -50;
						rest(killCount, killGoal, filler, dungeon, pc, m);
						if (pc.level < 5) {
							system("color 0A");
						}
						else if (pc.level < 9) {
							system("color 0E");
						}
						potion = true;
						pc.HP = pc.maxHP;
						cout << "You revive at your camp, but you have lost all of your monster essences\n";
						continue;
					}
						cout << "  _________________________________________________________________\n";
						cout << " /                                                                 \\\n"; 
						cout << "|                                                                   |\n";
						cout << "|                             Game  Over...                         |\n";
						cout << "|                                                                   |\n";
						cout << "|___________________________________________________________________|\n";
					if (pc.finScore < 0) {
						pc.finScore = 0;
					}
					pc.finScore -= (1000 * (endgame - pc.level));
					if (pc.difficulty == "medium") {
						pc.finScore *= 2;
					}
					else if (pc.difficulty == "hard") {
						pc.finScore *= 3;
					}
					cout << "YOUR FINAL SCORE: " << pc.finScore << '\n';
					return 0;
				}
				discovery(sod, boh, soa, sodestiny, boheroes, soargon);
				cout << "You now have " << killCount << " monster essenses.\n" << '\n';
			}
			else if (gameState == 'q') {
				cout << "ARE YOU SURE??? (y/n)\n";
				do {
					cin >> gameState;
				}while (gameState != 'y' && gameState != 'n');
				if (gameState == 'y') {
					break;
				}
			}
			else if (gameState == 'i') {
				inventory(potion, killCount, sodestiny, boheroes, soargon, pc);
				cout << "  Remember, to level up, you must kill" << bossType << '\n';
			}
			else if (gameState == 'e' && pc.character == "wizard" && pc.classKit2 > 0) {
				cout << "  _________________________________________________________________\n";
				cout << " /                                                                 \\\n"; 
				cout << "|                                                                   |\n";
				cout << "|                             EXPLOSION!                            |\n";
				cout << "|                                                                   |\n";
				cout << "|___________________________________________________________________|\n";
				pc.classKit2 -= 1;
				cout << "High  slots remaining: " << pc.classKit2 << '\n';
				if (pos < killGoal - 1 && flor >= 0 && flor <= pc.level) {
					for (int i = flor - pc.exheight;i <= flor + pc.exheight;i++) {
						for (int j = pos + 1;j < pos + pc.expwidth;j++) {
							if (i <= pc.level && i >= 0 && j < killGoal && j >= 0) { 
								if (dead[i][j] != 100 && dead[i][j] != -50) {
									dead[i][j] += 10;
									killCount++;
								}
							}
						}
					}
				}
			}
			else if (gameState == 'b' && pc.character == "bard") {
				if (pc.classKit1 > 0) {
					pc.classKit1 -= 1;
					cout << "Which attack type do you wish to enhance? (s/b/m)\n";
					do {
						cin >> pc.strongAttack;
					} while (pc.strongAttack != 's' && pc.strongAttack != 'b' && pc.strongAttack != 'm');
				}
				else {
					cout << "You can't do that...\n";
					continue;
				}
			}
			else if ((gameState == 'c' && potion == true) || (gameState == 'h' && ((pc.character == "witch" && pc.classKit1 > 0)) && pc.HP < pc.maxHP) ||
					    (gameState == 'w' && pc.character == "knight" && pc.classKit2 > 0)) {
				if (gameState == 'c' && potion == true) {
					cout << "You set up camp and consume your monster essenses, regaining your strength\n";
					potion = false;
					pc.HP += (4 * killCount * pc.level);
					if (pc.HP > (2 * pc.maxHP)) {
						pc.HP = (2 * pc.maxHP);
					}
					cout << "HP is " << pc.HP << '\n';
					printHP(filler, pc);
					killCount = 0;
				}
				else {
					heal(killCount, pc, filler);
				}
			}
			else if (gameState == 'e' && pc.classKit2 < 1 && pc.character == "wizard") {
				cout << "You don't have any more high spell slots!\n";
		        continue;			
			}
			else if ((gameState == 'h' && pc.character != "witch") || (gameState == 'w' && pc.character == "knight" && pc.increase != "w")) {
				cout << "You can't do that...\n";
				continue;
			}
			else if (gameState == 'f') {
				rest(killCount, killGoal, filler, dungeon, pc, m);
				printHP(filler, pc);
				cout << "You can make camp once again\n";
				if (pc.character == "bard") {
					pc.classKit1 = 1;
					if (pc.race == "elf") {
						pc.classKit1++;
					}
				}
				potion = true;
				rooms.clear();
				dead.clear();
				for (flor = 0;flor <= pc.level;flor++) {
				for (pos = 0;pos < killGoal;pos++) {
					rooms.push_back(0);
				}
				dead.push_back(rooms);
					rooms.clear();
				}
				dead[0][0] = 1;
				dead[num][killGoal - 1] = -50;
				for (flor = 0;flor <= pc.level;flor++) {
					for (pos = 0;pos < killGoal;pos++) {
						if (obst[flor][pos] == true) {
							dead[flor][pos] = 100;
						}
					}
				}
				flor = 0;
				pos = 0;
			}
			else {
				cout << "You can't do that!\n";
			}
			if (dead[flor][pos] < 0) {
				pc.level++;
				killGoal += 2;
				killCount = 0;
				pc.maxHP += 25;
				disc = false;
				if (pc.level >= endgame) {
						system("color 0A");
						cout << "  _________________________________________________________________\n";
						cout << " /                                                                 \\\n"; 
						cout << "|                                                                   |\n";
						cout << "|                             You  win!                             |\n";
						cout << "|                                                                   |\n";
						cout << "|___________________________________________________________________|\n";
					break;
				}
				rooms.clear();
				dead.clear();
				for (flor = 0;flor <= pc.level;flor++) {
					for (pos = 0;pos < killGoal;pos++) {
						rooms.push_back(0);
					}
					dead.push_back(rooms);
					rooms.clear();
				}
				dead[0][0] = 1;
				levelUp(dungeon, killGoal, filler, pc, m, flor, pos);
				if (potion == false) {	
					potion = true;
					cout << "You can make camp once again\n";
				}
				num = rand() % pc.level + 1;
				dungeon[num][killGoal - 1] = 10;
				dead[num][killGoal - 1] = -50;
				for (int i = 0;i < pc.level;i++) {
					for (int ni = 0;ni < (killGoal/5);ni++) {
						dead[i][(rand() % (killGoal-2)) + 1] = 100;
					}
				}
				obst.clear();
				for (flor = 0;flor <= pc.level;flor++) {
					for (pos = 0;pos < killGoal + 1;pos++) {
						if (dead[flor][pos] == 100) {
							R.push_back(true);
						}
						else {
							R.push_back(false);
						}
					}
					obst.push_back(R);
					R.clear();
				}
				flor = 0;
				pos = 0;
				newNum = rand() % 3;
				m.damage = 10;
				monsterLibrary(pc, m, newNum);
				bossType = m.type;
				cout << "\n\nTo get even stronger, traverse the next floor and defeat" << bossType << '\n';
			}
	}
	pc.finScore -= (endgame - pc.level)*1000;
	if (pc.finScore <= 0) {
		pc.finScore = 0;
	}
	if (pc.difficulty == "medium") {
		pc.finScore *= 2;
	}
	else if (pc.difficulty == "hard") {
		pc.finScore *= 3;
	}
	cout << "YOUR FINAL SCORE: " << pc.finScore << '\n';
	cout << "  _________________________________________________________________\n";
	cout << " /                                                                 \\\n"; 
	cout << "|                                                                   |\n";
	cout << "|                              The End                              |\n";
	cout << "|                                                                   |\n";
	cout << "|___________________________________________________________________|\n";
	return 0;
}
void printHP(char &filler, player &pc) {
	int score = pc.finScore - (10000 - 1000*(pc.level - 1));
	if (pc.difficulty == "medium") {
		score *= 2;
	}
	else if (pc.difficulty == "hard") {
		score *= 3;
	}
	cout << "Score: " << score << '\n';
	int correction = pc.level;
	if (pc.character == "wizard" && (pc.race == "dwarf" || pc.race == "elf")) {
		correction -= 2;
	}
	else if (pc.race == "dwarf" || pc.race == "elf") {
		correction--;
	}
	else if (pc.character == "knight" && pc.race == "orc") {
		correction += 2;
	}
	else if (pc.race == "orc") {
		correction++;
	}
	if (correction < 1) correction = 1;
	if (pc.maxHP > pc.HP && pc.HP > 0) {
		cout << pc.cname << " [" << pc.level << "] : " << left << setw(pc.HP * 2 / correction) << setfill(filler) << "[" << filler; 
		cout << right << setw((pc.maxHP - pc.HP) * 2 / correction) << setfill('-') << "-" << "] " << pc.HP << '/' << pc.maxHP;
	}	
	else if (pc.HP <= 0) {
  		cout << pc.cname << " [" << pc.level << "] : " << left << setw(pc.maxHP * 2 / correction) << setfill('-') << "[" << '-' << "] " << pc.HP << '/' << pc.maxHP;
	}
	else {
		cout << pc.cname << " [" << pc.level << "] : " << left << setw(pc.HP * 2 / correction) << setfill(filler) << "[" << filler << "] " << pc.HP << '/' << pc.maxHP;
	}
 cout << '\n';
}
void discovery(bool &sod, bool &boh, bool &soa, bool &sodestiny, bool &boheroes, bool &soargon) {
	if (sod == true) {
	  sod = false;
	  sodestiny = true;
  	cout << "You discovered the Sword of Destiny!!!" << '\n';
	}
	else if (boh == true) {
	  boh = false;
		boheroes = true;
		cout << "You discovered the Bow of Heroes!!!" << '\n';
	}
	else if (soa == true) {
		soa = false;
		soargon = true;
		cout << "You discovered the Staff of Argon!!!" << '\n';
	}
}
void rest(int &killCount, int &killGoal, char &filler, vector<vector<int> > &dungeon, player &pc, monster &m) {
	if (pc.HP > 0) {
		if (pc.level < 4) {
			cout << "You flee to the entrance of this floor ";
		}
		else {
			if (killCount % pc.level == 0 && killCount > 0) {
				cout << "You can't find a path to escape, it's too dangerous...\n";
				return;
			}
			else {
				cout << "You flee to the entrance of this floor ";
			}
		}
	}
	pc.HP += killCount * 6 * pc.level;
	killCount = 0;
	if (pc.HP < pc.maxHP) {
		pc.HP = pc.maxHP;
		printHP(filler, pc);
	}
	cout << "and use your monster essenses to temporarily grow stronger\n\n";
	cout << "Your HP is now " << pc.HP << '\n';
	if (pc.character == "thief") {
		pc.classKit1 = pc.level;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
		}
		cout << "You can sneak attack " << pc.classKit1 << " more enemies.\n";
	}
	else if (pc.character == "knight" && pc.increase == "p") {
		pc.classKit1 = 1;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
			cout << "You can power attack 2 more times\n";
		}
		else {
			cout << "You can power attack once again\n";
		}
	}
	else if (pc.character == "knight" && pc.increase == "w") {
		pc.classKit2 = 1;
		if (pc.race == "elf") {
			pc.classKit2 += 1;
			cout << "You can war cry to recover your strength 2 more times\n";
		}
		else {
			cout << "You can war cry once again\n";
		}
	}
	else if (pc.character == "bard") {
		pc.classKit1 = 1;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
			cout << "You can now enhance one of your weapons 2 more times\n";
		}
		else {
			cout << "You can now enhance one of your weapons once again\n";
		}
	}
	else if (pc.character == "witch") {
		pc.classKit1 = pc.maxh;
		pc.classKit2 = pc.maxk;
		cout << "You now have " << pc.classKit1 << " potions and " << pc.classKit2 << " poisons.\n\n";
	}
	else if (pc.character == "duelist") {
		pc.classKit1 = 2 * pc.level;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
		}
		cout << "You can now counter " << pc.classKit1 << " monsters.\n\n";
	}
	else if (pc.character == "shinobi") {
		pc.classKit1 = 1;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
			cout << "You can stealth attack " <<  pc.classKit1 << " more times\n";
		}
		else {
			cout << "You can stealth attack once again\n";
		}
	}
}
void heal(int &killCount, player &pc, char &filler) {
	pc.HP += killCount * 4 * pc.level;
	if (pc.HP > pc.maxHP) {
		pc.HP = pc.maxHP;
	}
	if (pc.character == "witch") {
		cout << "You drink a healing Potion!\n";
		pc.classKit1 -= 1;
		cout << "Potions remaining: " << pc.classKit1 << '\n';
	}
	else if (pc.character == "knight") {
		pc.classKit2 -= 1;
		cout << "You let out a bellowing warcry that restores your strength!\n";
		cout << "\nYou can war cry " << pc.classKit2 << " more times\n";
	}
	cout << "HP is " << pc.HP << '\n';
	printHP(filler, pc);
}
void levelUp(vector<vector<int> > &dungeon, int &killGoal, char &filler, player &pc, monster &m, int &flor, int &pos) {
    flor = 0;
	pos = 0;
	pc.HP = pc.maxHP - 23;
	if (pc.character == "knight") {
  		pc.maxHP += (2 * pc.level);
    }
	else if (pc.character == "wizard") {
		pc.maxHP -= (2 * pc.level);
		
	}
	if (pc.race == "orc") {
		pc.maxHP += (2 * pc.level);
	}
	else if (pc.race == "elf" || pc.race == "dwarf") {
		pc.maxHP -= (2 * pc.level);
	}
	if (pc.HP > pc.maxHP) {
		pc.maxHP = pc.HP;
	}
	else {
		pc.HP = pc.maxHP;
	}
	buildDungeon(dungeon, killGoal, m, pc);
	string twine = m.type;
	twine.pop_back();
	cout << "You use the essense of" << twine << " to grow stronger.\n";
	cout << "  _________________________________________________________________\n";
	cout << " /                                                                 \\\n"; 
	cout << "|                                                                   |\n";
	cout << "|                             Level Up!                             |\n";
	cout << "|                                                                   |\n";
	cout << "|___________________________________________________________________|\n";
	cout << "You are now Level " << pc.level << '\n';
	printHP(filler, pc);
	if (pc.character == "wizard") {
		pc.classKit1 = 2 + pc.level;
		if (pc.level == 5) {
			pc.expwidth += 2;
			pc.exheight++;
		}
		else if (pc.level == 8) {
			pc.expwidth += 2;
			pc.exheight++;
		}
		if (pc.level > 6) {
			pc.classKit2 = 2;
		}
		else {
			pc.classKit2 = 1;
		}
		if (pc.race == "elf") {
			pc.classKit1 += 1;
		}
	  cout << "Spell slots remaining: " << pc.classKit1 << '\n';
	  cout << "High  slots remaining: " << pc.classKit2 << '\n';
	}
	else if (pc.character == "thief") {
		pc.classKit1 =  pc.level;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
		}
		cout << "Now you can sneak attack " << pc.classKit1 << " enemies.\n";
	}
	else if (pc.character == "knight") {
		if (pc.increase == "p") {
			cout << "Would you like to keep power attack, or switch to war cry? (p/w)\n";
		}
		else {
			cout << "Would you like to keep war cry, or switch to power attack? (p/w)\n";
		}
		do {
			cin >> pc.increase;
		}while (pc.increase != "p" && pc.increase != "w");
		if (pc.increase == "p") {
			pc.classKit1 = 1;
			pc.classKit2 = 0;
			if (pc.race == "elf") {
				pc.classKit1 += 1;
				cout << "You can power attack " << pc.classKit1 << " more times\n";
			}
			else {
				cout << "You can power attack once again\n";
			}
		}
		else {
			pc.classKit1 = 0;
			pc.classKit2 = 1;
			if (pc.race == "elf") {
				pc.classKit2 += 1;
				cout << "You can war cry to recover your strength " << pc.classKit2 << " more times\n";
			}
			else {
				cout << "You can war cry once again\n";
			}
		}
	}
	else if (pc.character == "bard") {
		pc.classKit1 = 1;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
			cout << "You can enhance one of your weapons outside of combat twice more\n";
		}
		else {
			cout << "You can enhance one of your weapons outside of combat once again\n";
		}
	}
	else if (pc.character == "duelist") {
		pc.classKit1 = 2 * pc.level;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
		}
		cout << "You can now counter " << pc.classKit1 << " monsters.\n";
	}
	else if (pc.character == "shinobi") {
		pc.classKit1 = 1;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
			cout << "You can stealth attack " << pc.classKit1 << " more times\n";
		}
		else {
			cout << "You can stealth attack once again\n";
		}
	}
	else if (pc.character == "witch") {
		pc.increase;
		do {
			cout << "Would you like to increase your Potions(h) or Poisons(k)?\n";
			cin >> pc.increase;
		}while (pc.increase != "h" && pc.increase != "k");
		if (pc.increase == "h") {
			pc.maxh += 1;
		}
		else {
			pc.maxk += 1;
		}
		pc.classKit1 = pc.maxh;
		pc.classKit2 = pc.maxk;
		cout << "You now have " << pc.classKit1 << " potions, and " << pc.classKit2 << " poisons.\n";
	}
}

void inventory(bool &potion, int &killCount, bool &sodestiny, bool &boheroes, bool &soargon, player &pc) {
	cout << "You have...\n";
				if (potion == true) {
					cout << "  camping supplies\n";
				}
				else {
					cout << "  no camping supplies\n";
				}
				cout << "  " << killCount << " monster essenses\n";
				if (sodestiny == true) {
					cout << "  the Sword of Destiny ";
					if (pc.character == "bard" && pc.strongAttack == 's') {
						cout << "(enhanced)";
					}
					cout << '\n';
				}
				else if (pc.character == "bard" && pc.strongAttack == 's') {
					cout << "  an enhanced sword\n";
				}
				else if (pc.strongAttack == 's' || pc.strongAttack2 == 's') {
					cout << "  a good sword\n";
				}
				else { 
					cout << "  a sword\n";
				}
				if (boheroes == true) {
					cout << "  the Bow of Heroes ";
					if (pc.character == "bard" && pc.strongAttack == 'b') {
						cout << "(enhanced)";
					}
					cout << '\n';
				}
				else if (pc.strongAttack == 'b' && pc.character == "bard") {
					cout << "  an enhanced bow\n";
				}
				else if (pc.strongAttack == 'b' || pc.strongAttack2 == 'b') {
					cout << "  a longbow\n";
				}
				else {
					cout << "  a bow\n";
				}
				if (soargon == true) {
					cout << "  the Staff of Argon ";
					if (pc.character == "bard" && pc.strongAttack == 'm') {
						cout << "(enhanced)";
					}
					cout << '\n';
				}
				else if (pc.strongAttack == 'm' && pc.character == "bard") {
					cout << "  an enhanced magic wand\n";
				}
				else if (pc.strongAttack == 'm' || pc.strongAttack2 == 'm') {
					cout << "  a powerful magic staff\n";
				}
				else {
					cout << "  a magic wand\n";
				}
				if (pc.character == "knight") {
					if (pc.increase == "w") {
						cout << "  " << pc.classKit2 << " war cries\n";
					}
					else {
						cout << "  " << pc.classKit1 << " power attacks\n";
					}
				}
				else if (pc.character == "thief") {
					cout << "  " << pc.classKit1 << " poison darts for sneak attacks\n";
				}
				else if (pc.character == "wizard") {
					cout << "  " << pc.classKit1 << " spell slots\n";
					cout << "  " << pc.classKit2 << " high  slots\n";
				}
				else if (pc.character == "witch") {
					cout << "  " << pc.classKit1 << " healing potions\n";
					cout << "  " << pc.classKit2 << " poisons\n";
				}
				else if (pc.character == "shinobi") {
					cout << "  " << pc.classKit1 << " kunai for assassinations\n";
				}
				else if (pc.character == "duelist") {
					cout << "  " << pc.classKit1 << " counter attacks\n";
				}
				else if (pc.character == "bard") {
					cout << "  " << pc.classKit1 << " enhancing performances\n";
				}
}
void intro(player &pc) {
	do {
		cout << "Choose a difficulty: (easy, medium, hard)\n";
		cin >> pc.difficulty;
	} while (pc.difficulty != "easy" && pc.difficulty != "medium" && pc.difficulty != "hard");
	cout << "Greetings traveler...\n";
	cout << "What is your name?\n";
	char name[256];
	cin.ignore();
	cin.getline(name, 256, '\n');
	pc.cname = name;
	cout << '\n';
	do {
		cout << "What are you? (dwarf, elf, orc, man)\n";
		cin >> pc.race;
	} while (pc.race != "dwarf" && pc.race != "elf" && pc.race != "orc" && pc.race != "man");
	if (pc.race == "orc") {
		pc.maxHP += 4;
		pc.HP = pc.maxHP;
	}
	do {
		cout << "What is your class? (easy: fighter, spell-slinger, dark-knight)\n";
		cout << "                    (moderate: knight, thief, bard, duelist)\n";
		cout << "                    (advanced: wizard, witch, shinobi)\n";
		cin >> pc.character;
		cout << '\n';
	} while (pc.character != "wizard" && pc.character != "knight" && pc.character != "thief" && pc.character != "spell-slinger" && pc.character != "fighter" && pc.character != "dark-knight" && pc.character != "witch" && pc.character != "duelist" && pc.character != "shinobi" && pc.character != "bard");
	if (pc.character == "witch") {
		pc.strongAttack = 'm';
		pc.classKit1 = 1;
		pc.classKit2 = 1;
		pc.maxh = 1;
		pc.maxk = 1;
		cout << "As a witch, you have ";
		if (pc.race == "elf") {
			cout << "two healing potions";
		}
		else {
			cout << "one healing potion";
		}
		cout << " (Enter h outside of combat), and one lethal poison (enter k during a fight).\n\n";
		cout << "These potions refill when you rest.\n\n";
	}
	else if (pc.character == "bard") {
		pc.classKit1 = 1;
		if (pc.race == "elf") {
			pc.classKit1 += 1;
		}
		cout << "As a bard, you get to choose what weapon type you enhance each level.\n";
		cout << "Choose one now...(s/b/m)\n";
		do {
			cin >> pc.strongAttack;
		}while (pc.strongAttack != 's' && pc.strongAttack != 'b' && pc.strongAttack != 'm');
		if (pc.race != "elf") {
			cout << "Once per level, outside of combat, you may choose to change your enhanced weapon type by entering 'b'\n\n";
		}
		else {
			cout << "Twice per level, outside of combat, you may choose to change your enhanced weapon type by entering 'b'\n\n";
		}
	}
	else if (pc.character == "duelist") {
		pc.strongAttack = 's';
		pc.classKit1 = 2;
		cout << "As a duelist, you are skilled with a sword, and can counter enemies for a chance to take no damage.\n";
		cout << "To counter attack, enter c during a fight.\n\n";
	}
	else if (pc.character == "shinobi") {
		pc.strongAttack = 'b';
		pc.classKit1 = 1;
		cout << "As a shinobi, you are skilled with a bow, and can always escape a fight back to the entrance of the dungeon (enter e during a fight).\n";
		cout << "To use your shinobi escape, you are required to rest.\n";
		cout << "Once per rest, you can stealth attack an enemy (enter k during a fight) to mitigate damage.\n\n";
	}
	else if (pc.character == "wizard") {
		pc.strongAttack = 'm';
		pc.classKit1 = 2;
		pc.classKit2 = 1;
		if (pc.race == "elf") {
			pc.classKit1++;
		}
		cout << "As a wizard, you have a few spells you can use, and two types of spells slots, high slots and low slots\n";
		cout << "You can cast Fire Ball (enter f during a fight) expending one of " << pc.classKit1 << " low spell slots that don't regenerate until you level up.\n\n";
		cout << "You can also use Invisibility (enter i during a fight), or Explosion (enter e outside of combat), expending one of " << pc.classKit2 << " high spell slots\n\n";
	}
	else if (pc.character == "knight") {
		pc.increase = "p";
		pc.strongAttack = 's';
		pc.classKit1 = 1;
		pc.classKit2 = 0;
		pc.maxHP += 4;
		pc.HP = pc.maxHP;
		cout << "As a knight, you are very hardy, you have a little more HP than other classes, and you are much stronger with a sword\n\n";
		cout << "Once per rest, you can power attack your enemy (enter p during a fight), ";
		cout << "taking more damage, but you will progress more than one space in the direction you were moving.\n\n";
	}
	else if (pc.character == "thief") {
		pc.strongAttack = 'b';
		pc.classKit1 = 1;
		cout << "As a thief, you are skilled with a bow and hard to detect, once per rest, you can sneak attack an enemy, taking zero damage in the fight\n\n";
		cout << "To sneak attack, enter h during a fight.\n\n";
	}
	else if (pc.character == "spell-slinger") {
		pc.strongAttack = 'b';
		pc.strongAttack2 = 'm';
		cout << "As a spell-slinger, you are quite skilled with magic attacks and a bow.\n\n";
	}
	else if (pc.character == "fighter") {
		pc.strongAttack = 's';
		pc.strongAttack2 = 'b';
		cout << "As a fighter, you are quite skilled with sword and bow.\n\n";
	}
	else if (pc.character == "dark-knight") {
		pc.strongAttack = 's';
		pc.strongAttack2 = 'm';
		cout << "As a dark-knight, you are quite skilled with the sword and magic attacks.\n\n";
	}
	if (pc.race == "elf" && pc.character != "wizard") {
		pc.classKit1 += 1;
		pc.maxh += 1;
	}
}
void buildDungeon(vector<vector<int> > &dungeon, int &killGoal, monster &m, player &pc) {
	dungeon.clear();
	vector<int> b;
	for (int j = 0;j <= pc.level;j++) {
		b.clear();
		for (int i = 0;i < killGoal;i++) {
			m.damage = rand() % 11;
			b.push_back(m.damage);
		}
		dungeon.push_back(b);
	}
}
void ins(vector<int> &dungeon, int killGoal) {
	int start;
	for (start = 0;start < killGoal;start++) {
		int j;
		int smallest_index = start;
		for(j = start + 1;j < killGoal;j++) {
			if (dungeon.at(j) < dungeon.at(smallest_index)) {
				smallest_index = j;
			}
		}
		int temp = dungeon.at(start);
		dungeon.at(start) = dungeon.at(smallest_index);
		dungeon.at(smallest_index) = temp;
	}

}
void preAttack(monster &m, bool &disc, bool &sodestiny, bool &sod, bool &boheroes, bool &boh, bool &soargon, bool &soa, player &pc) {
	if (m.damage == 15 && disc != true) {
		if (m.bestAttack == 's' && sodestiny != true) {
			sod = true;
			disc = true;
		}
		else if (m.bestAttack == 'b' && boheroes != true) {
			boh = true;
			disc = true;
		}
		else if (m.bestAttack == 'm' && soargon != true) {
			soa = true;
			disc = true;
		}
	}
	m.damage = m.damage * 2 * pc.level;
	cout << "It's" << m.type << '\n' << "How do you attack? (s/b/m";
	if (pc.character == "wizard" && pc.classKit1 > 0) {
		cout << "/f";
	}
	if (pc.character == "wizard" && pc.classKit2 > 0) {
		cout << "/i";
	}
	else if (pc.character == "thief" && pc.classKit1 > 0) {
		cout << "/h";
	}
	else if (pc.character == "knight" && pc.classKit1 > 0) {
		cout << "/p";
	}
	else if ((pc.character == "witch" && pc.classKit2 > 0) || (pc.character == "shinobi" && pc.classKit1 > 0)) {
		cout << "/k";
	}
	else if (pc.character == "duelist" && pc.classKit1 > 0) {
		cout << "/c";
	}
	if (pc.character == "shinobi") {
		cout << "/e";
	}
	cout << ")\n";
}
void damageCalc(char &attackType, bool &disc, bool &sod, bool &soa, bool &boh, bool &sodestiny, bool &boheroes, bool &soargon, int &killCount, int &killGoal, monster &m, player &pc) {
    if (attackType == 'e' && disc == true) {
		disc = false;
		sod = false;
		soa = false;
		boh = false;
	}
	if (pc.difficulty == "hard") {
		m.damage += 2;
	}
	else if (pc.difficulty == "easy") {
		m.damage -= 2;
	}
	if (attackType == m.bestAttack) {
		if (pc.race == "dwarf") {
			m.damage /= 3;
		}
	else {
			m.damage /= 2;
		}
		cout << '\n' << "It's super effective!\n" << '\n';
	}
	else if (attackType != 'f' && attackType != 'p' && attackType != 'h' && attackType != 'k' && attackType != 'c' && attackType != 'e' && attackType != 'i') {
		cout << '\n' << "Not very effective...\n" << '\n';
		pc.finScore -= 50;
	}
	if ((pc.strongAttack == m.bestAttack && attackType == m.bestAttack) || (pc.strongAttack2 == m.bestAttack && attackType == m.bestAttack)) {
		m.damage /= 2;
	}
	if (attackType == 's' && sodestiny == true) {
		m.damage /= 2;
	}
	if (attackType == 'b' && boheroes == true) {
		m.damage /= 2;
	}
	if (attackType == 'm' && soargon == true) {
		m.damage /= 2;
	}
	if (attackType == 'f' && pc.classKit1 > 0) {
		m.damage /= 8;
		if (sodestiny && boheroes && soargon) m.damage /= 4;
		cout << '\n' << "You cast Fire Ball!\n\n";
		pc.classKit1 -= 1;
		cout << "Spell slots remaining: " << pc.classKit1 << '\n';
	}
	else if (attackType == 'f' && pc.classKit1 < 1 && pc.character == "wizard") {
		cout << '\n' << "You don't have any more spell slots!\n";
	}
	if (attackType == 'i' && pc.classKit2 > 0) {
		m.damage = 0;
		cout << '\n' << "You cast Invisibility!\n\n";
		pc.classKit2 -= 1;
		cout << "High  slots remaining: " << pc.classKit2 << '\n';
	}
	else if (attackType == 'i' && pc.classKit2 < 1 && pc.character == "wizard") {
		cout << '\n' << "You don't have any more high spell slots!\n";
	}
	if ((attackType == 'h' && pc.character == "thief" && pc.classKit1 > 0) || pc.strongAttack == 'n') {
		pc.classKit1 -= 1;
		m.damage = 0;
		cout << '\n' << "You sneak attack the monster!\n";
		cout << "You can sneak attack " << pc.classKit1 << " more monsters.\n";
	}
	if (attackType == 'p' && pc.character == "knight" && pc.classKit1 > 0 && m.damage > 1) {
		cout << '\n' << "You rush the monster!\n";
		pc.classKit1 -= 1;
		killCount += pc.level;
		m.damage *= 2;
		if (pc.race == "elf") {
			cout << "You can power attack " << pc.classKit1 << " more times\n";
		}
		else {
				cout << "Rest to regain your strength\n\n";
		}
	}
	if (attackType == 'k' && ((pc.character == "witch" && pc.classKit2 > 0) || (pc.character == "shinobi" && pc.classKit1 > 0))) {
		m.damage /= 8;
		if (sodestiny && boheroes && soargon) m.damage /= 4;
		if (pc.character == "witch") {
			pc.classKit2 -= 1;
			cout << '\n' << "You poison the monster!\n";
			cout << "Poison remaining: " << pc.classKit2 << '\n';
		}
		else {
			pc.classKit1 -= 1;
			cout << '\n' << "You assassinate the monster!\n";
			if (pc.race == "elf") {
				cout << "You can stealth attack " << pc.classKit1 << " more times\n";
			}
			else {
				cout << '\n' << "Rest to regain your strength\n";
			}
		}
	}
	if (attackType == 'c' && pc.character == "duelist" && pc.classKit1 > 0) {
		int checker = rand() % pc.level;
		if (checker != 2) {
			m.damage = 0;
			cout << "You counter attack the monster!\n";
				pc.classKit1 -= 1;
			cout << "You can counter " << pc.classKit1 << " more monsters.\n";
		}
		else {
			cout << "You failed to counter the monster!\n";
			m.damage /= 2;
			if (sodestiny && boheroes && soargon) m.damage /= 4;
		}
	}
	if (attackType == 'e' && pc.character == "shinobi") {
		m.damage = 0;
		pc.finScore -= 300;
		pc.classKit1 = 1;
		cout << "You escape back to your hideout";
		pc.HP += killCount * 6 * pc.level;
		killCount = 0;
		if (pc.HP < pc.maxHP) {
			pc.HP = pc.maxHP;
		}
		cout << " and use your monster essenses to temporarily grow stronger\n\n";
	}
}
void monsterLibrary(player &pc, monster &m, int newNum) {
	if (newNum == 3) {
		newNum = rand() % 3;
	}
	if (pc.level == 1) {
		switch (m.damage) {	
			case 0:
			case 1:
				m.type = " a ghost";
				m.bestAttack = 'm';
				break;
			case 2:
			case 3:
				m.type = " a death vulture";
				m.bestAttack = 'b';
				break;
			case 4:
			case 5:
				m.type = " a goblin";
				m.bestAttack = 's';
				break;
			case 6:
			case 7:
				m.type = " a zombie";
				m.bestAttack = 'b';
				break;
			case 8:
			case 9:
				m.type = " an ogre";
				m.bestAttack = 's';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " a Troll!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " a Saber Leopard!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " a Wraith!";
					m.bestAttack = 'm';
				}
				break;
		}
	}
	else if (pc.level == 2) {
		switch (m.damage) {
			case 0:
			case 1:
				m.type = " a ghoul";
				m.bestAttack = 'b';
				break;
			case 2:
			case 3:
				m.type = " an oozing mass";
				m.bestAttack = 'm';
				break;
			case 4:
			case 5:
				m.type = " an orc fighter";
				m.bestAttack = 's';
				break;
			case 6:
			case 7:
				m.type = " a banshee";
				m.bestAttack = 'm';
				break;
			case 8:
			case 9:
				m.type = " a giant";
				m.bestAttack = 'b';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " an Orc Commander!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " a Cyclops!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " a Witch!";
					m.bestAttack = 'm';
				}
				break;
		}
	}
	else if (pc.level == 3) {
		switch (m.damage) {
			case 0:
			case 1:
				m.type = " a troll";
				m.bestAttack = 's';
				break;
			case 2:
			case 3:
				m.type = " a stone gollum";
				m.bestAttack = 'm';
				break;
			case 4:
			case 5:
				m.type = " an orc archer";
				m.bestAttack = 'b';
				break;
			case 6:
			case 7:
				m.type = " a hag";
				m.bestAttack = 'm';
				  
				break;
			case 8:
			case 9:
				m.type = " a saber leopard";
				m.bestAttack = 'b';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " a Giant Snake!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " an Ettin!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " a Necromancer!";
					m.bestAttack = 'm';
				}
				break;
		}			
	}
	else if (pc.level == 4) {
		switch (m.damage) {
			case 0:
			case 1:
				m.type = " a werewolf";
				m.bestAttack = 's';
				break;
			case 2:
			case 3:
				m.type = " a young dragon";
				m.bestAttack = 'b';
				break;
			case 4:
			case 5:
				m.type = " an orc shaman";
				m.bestAttack = 'm';
				break;
			case 6:
			case 7:
				m.type = " an orc duelist";
				m.bestAttack = 's';
				break;
			case 8:
			case 9:
				m.type = " a shadow tiger";
				m.bestAttack = 'b';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " a Frost Giant!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " a Griffin!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " a Rock Giant!";
					m.bestAttack = 'm';
				}
				break;
		}
	}
	else if (pc.level == 5) {
		switch (m.damage) {
			case 0:
			case 1:
				m.type = " a flame elemental";
				m.bestAttack = 'm';
				break;
			case 2:
			case 3:
				m.type = " an ettin";
				m.bestAttack = 'b';
				break;
			case 4:
			case 5:
				m.type = " an ancient draugr";
				m.bestAttack = 's';
				break;
			case 6:
			case 7:
				m.type = " an undead horde";
				m.bestAttack = 'b';
				break;
			case 8:
			case 9:
				m.type = " a poltergeist";
				m.bestAttack = 'm';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " the Orc Squadron!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " the Dragon!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " the Army of Sorcerers!";
					m.bestAttack = 'm';
				}
				break;
		}
	}	
  	else if (pc.level == 6) {
		switch (m.damage) {
			case 0:
				m.damage = 1;
				m.type = " a spriggan warlord";
				m.bestAttack = 's';
				break;
			case 1:
				m.type = " a griffin";
				m.bestAttack = 'b';
				break;
			case 2:
				m.type = " a monstrous owlbear";
				m.bestAttack = 's';
				break;
			case 3:
				m.type = " a water elemental";
				m.bestAttack = 'm';
				break;
			case 4:
				m.type = " a phoenix";
				m.bestAttack = 'm';
				break;
			case 5:
				m.type = " a frost giant";
				m.bestAttack = 's';
				break;
			case 6:
				m.type = " a manticore";
				m.bestAttack = 'b';
				break;
			case 7:
				m.type = " a necromancer";
				m.bestAttack = 'm';
				break;
			case 8:
				m.type = " a storm wizard";
				m.bestAttack = 'm';
				break;
			case 9:
				m.type = " a giant snake";
				m.bestAttack = 's';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " the Feral Werewolf!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " the Royal Griffin!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " the Vampire!";
					m.bestAttack = 'm';
				}
				break;
		}
	}	
	else if (pc.level == 7) {
		switch (m.damage) {
			case 0:
				m.damage = 1;
				m.type = " a bog hatcher";
				m.bestAttack = 'b';
				break;
			case 1:
				m.type = " a squadron of orcs";
				m.bestAttack = 's';
				break;
			case 2:
				m.type = " a drider";
				m.bestAttack = 's';
				break;
			case 3:
				m.type = " a persistant phantom";
				m.bestAttack = 'm';
				break;
			case 4:
				m.type = " a gogiteth";
				m.bestAttack = 'm';
				break;
			case 5:
				m.type = " a dragon";
				m.bestAttack = 'b';
				break;
			case 6:
				m.type = " a nilith";
				m.bestAttack = 's';
				break;
			case 7:
				m.type = " an army of sorcerers";
				m.bestAttack = 'm';
				break;
			case 8:
				m.type = " a shoggti";
				m.bestAttack = 'b';
				break;
			case 9:
				m.type = " an old griffin";
				m.bestAttack = 'b';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " the Horde of Trolls!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " the Elder Dragon!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " the Mindflayer!";
					m.bestAttack = 'm';
				}
				break;
		}
	}	
	else if (pc.level == 8) {
		switch (m.damage) {
			case 0:
				m.damage = 1;
				m.type = " a hound of Topedus";
				m.bestAttack = 's';
				break;
			case 1:
				m.type = " a feral werewolf";
				m.bestAttack = 's';
				break;
			case 2:
				m.type = " a wight stalker";
				m.bestAttack = 'b';
				break;
			case 3:
				m.type = " a royal griffin";
				m.bestAttack = 'b';
				break;
			case 4:
				m.type = " a graveknight";
				m.bestAttack = 'm';
				break;
			case 5:
				m.type = " a stone dragon";
				m.bestAttack = 'm';
				break;
			case 6:
				m.type = " a grothlut";
				m.bestAttack = 'b';
				break;
			case 7:
				m.type = " a shadow serpent";
				m.bestAttack = 's';
				break;
			case 8:
				m.type = " an uthul";
				m.bestAttack = 'm';
				break;
			case 9:
				m.type = " an orc warg rider";
				m.bestAttack = 'b';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " the Werewolf Pack!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " the Ancient Wyrm!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " the Vampire Lord!";
					m.bestAttack = 'm';
				}
				break;
		}
	}	
	else if (pc.level == 9) {
		switch (m.damage) {
			case 0:
				m.damage = 1;
				m.type = " a moonflower";
				m.bestAttack = 's';
				break;
			case 1:
				m.type = " a mindflayer";
				m.bestAttack = 'm';
				break;
			case 2:
				m.type = " a mohrg spawn";
				m.bestAttack = 'b';
				break;
			case 3:
				m.type = " a orc warg captain";
				m.bestAttack = 'b';
				break;
			case 4:
				m.type = " a hellcat";
				m.bestAttack = 's';
				break;
			case 5:
				m.type = " a horde of trolls";
				m.bestAttack = 's';
				break;
			case 6:
				m.type = " an irlgaunt";
				m.bestAttack = 's';
				break;
			case 7:
				m.type = " a king shadow serpent";
				m.bestAttack = 's';
				break;
			case 8:
				m.type = " a jabberwock";
				m.bestAttack = 'b';
				break;
			case 9:
				m.type = " a lich";
				m.bestAttack = 'm';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " Topedus the Mouse God!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " the Sea Monster!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " the Arch Demon!";
					m.bestAttack = 'm';
				}
				break;
		}
	}	
	else {
		switch (m.damage) {
			case 0:
				m.damage = 1;
				m.type = " a pit fiend";
				m.bestAttack = 'm';
				break;
			case 1:
				m.type = " an undead army";
				m.bestAttack = 'b';
				break;
			case 2:
				m.type = " a harpy queen";
				m.bestAttack = 'b';
				break;
			case 3: 
				m.type = " a mind flayer overlord";
				m.bestAttack = 'm';
				break;
			case 4:
				m.type = " a void worm";
				m.bestAttack = 's';
				break;
			case 5:
				m.type = " a werewolf pack";
				m.bestAttack = 's';
				break;
			case 6:
				m.type = " an ifrit";
				m.bestAttack = 'm';
				break;
			case 7:
				m.type = " a vampire lord";
				m.bestAttack = 'm';
				break;
			case 8:
				m.type = " an erlking";
				m.bestAttack = 'm';
				break;
			case 9:
				m.type = " a sea monster";
				m.bestAttack = 'b';
				break;
			case 10:
				m.damage = 15;
				if (newNum == 0) {
					m.type = " the Orc World Eater!";
					m.bestAttack = 's';
				}
				else if (newNum == 1) {
					m.type = " the Calamity Dragon!";
					m.bestAttack = 'b';
				}
				else {
					m.type = " the Elder Goddess of Death!";
					m.bestAttack = 'm';
				}
				break;
		}
	}
}