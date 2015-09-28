import random
from dungeonVars import *

# global variables:
health = 100
tracker = 0
monsters = {2:goblin,3:troll,6:troll}
items = {1:sword, 4:lthrArmor, 6:axe, 5:chainMail}
curWpn = knife
curArmor = plainClothes
life = True
textBreak = '= ' * 20 + '\n'
status = '\nHP: %s\nposition: %s\nweapon: %s\narmor: %s\nATK: %s\nDEF: %s\nLUK: %s\n'

# COMBAT CALCULATOR
def combatEvent(health,weapon,armor,enemy):
	print '\nYou encounter a %s!\n'%(enemy[0])
#	print '\nYou encounter a %s!\n\nYou are equipped with a %s and %s.\nYour attack is %s.\
# Your defense is %s. Your health is %s/100. Your luck is %s.\n'%(enemy[0],weapon[0],armor\
# [0],weapon[1],armor[1],health,weapon[2])
 
	enemyHealth = enemy[2]
	while enemyHealth > 0:
		netDmg = (enemy[1] - armor[1])
		health -= netDmg
		print 'The %s hits you for %s damage! You have %s health remaining.'%(enemy[0],netDmg,health)
		
		if health > 0:
			diceRoll = random.random()
			if diceRoll > 1.0/weapon[2]:
				enemyHealth -= weapon[1]
				print 'You hit the %s for %s damage! It has %s health remaining.'%(enemy[0]\
,weapon[1],enemyHealth)

		else:
			print 'The %s has killed you.'%(enemy[0])
			return health
		nothing = raw_input()
	
	if enemyHealth <= 0:
		print 'You have killed the %s!'%(enemy[0])
		return health

# FIND / PICKUP ITEM
def findWeapon(curWpn,newWpn):
	choice = ''
	while choice != 'Y' and choice != 'N':
		choice = raw_input('You find a %s on the ground. Take it? (Y/N) '%(newWpn[0]))
 		if choice == 'Y':
 			print 'You pick up the %s and leave the %s in its place.\n'%(newWpn[0],curWpn[0])
 			return newWpn,curWpn
 		elif choice == 'N':
 			print 'You keep the %s and leave the %s.\n'%(curWpn[0],newWpn[0])
 			return curWpn,newWpn
		else:
			print 'Please enter "Y" or "N".'

# Goblin boss fight. Chance of 1hit kill
def gBoss(health):
	print 'You encounter the goblin boss at the end of the tunnel!'
	health -= int(round(random.randint(2,5)*20))
	print health
	return health

def forwOrBack():
	option = ''
	while option != 'L' and option != 'R':
		option = raw_input('Go Forward or Back? (F/B): ')
		if option == 'F':
			return True
		elif option == 'B':
			return False

# CHOICE MAKER
def choiceMaker():
	global tracker, health, monsters,items,curWpn,curArmor
	print textBreak + status%(str(health).rjust(10),str(tracker).rjust(10),\
	curWpn[0].rjust(10),curArmor[0].rjust(10),str(curWpn[1]).rjust(10),\
	str(curArmor[1]).rjust(10),str(curWpn[2]).rjust(10))
# First move...	
	if tracker == 0:
		opt0 = ''
		while opt0 != 'L' and opt0 != 'R':
			opt0 = raw_input('Go Left of Right? (L/R): ')
			if opt0 == 'L':
				tracker = 1
				return True
			elif opt0 == 'R':
				tracker = 4	
				return True
# - every other move...
	elif tracker > 0 and tracker <= 6:
# Check if you run into a monster
		if tracker in monsters:
			health = combatEvent(health,curWpn,curArmor,monsters[tracker])
			if health <= 0:
				return False
			else:
				print textBreak + status%(health,tracker,curWpn[0],curArmor[0],curWpn[1],curArmor[1],curWpn[2])
				monsters.pop(tracker) # Removes monster if player wins
# Check if there's an item at your position that can be picked up
		if tracker in items:
			if len(items[tracker]) == 3:
				curWpn,items[tracker] = findWeapon(curWpn,items[tracker])
			else:
				curArmor,items[tracker] = findWeapon(curArmor,items[tracker])
			print textBreak + status%(health,tracker,curWpn[0],curArmor[0],curWpn[1],curArmor[1],curWpn[2])
# Allows decision if player lives
		optX = forwOrBack()
		if optX:
			if tracker == 3:
				tracker += 4
			else:
				tracker += 1
			return True
		elif not optX and tracker == 4:
			tracker = 0
			return True
		elif not optX:
			tracker -= 1
			return True
# Final move
	elif tracker == 7:
		health = combatEvent(health,curWpn,curArmor,chiefGoblin)
		if health <= 0:
			return False
		else:
			tracker += 1
			return True
	
def main():
	global tracker, life
	start = raw_input('\nPlay Goblin Hole? (Y/N): ')
	print '\n'
	if start == 'Y':
		while tracker <= 7:
			life = choiceMaker()
			if not life:
				print '\n*** You have died ***\n'
				return
		print '\n*** YOU WIN ***\n'
	else:
		return

main()
