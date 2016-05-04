import random
import os

#Initiate the Card class, with value and colour (as integers)

class card:
	def __init__(self, value, colour):
		self.value = value
		self.colour = colour
		
	def __repr__(self):
		return "[" + str(self.value) + "/" + str(self.colour) + "]"
		
#Make a deck		

class deck:
	def __init__(self):
		self.stack = []
		for v in [1,1,1,2,2,3,3,4,4,5]:
			for c in range(0,5):
				self.stack.append(card(v,c))
				
	def __str__(self):
		s = "Deck of " + str(len(self.stack)) + " cards: "
		for i in range(0,len(self.stack)):
			s = s + str(self.stack[i])
		return s
		
	def shuffle(self):
		random.seed()
		random.shuffle(self.stack)
		print self.stack
		print self
		
class discardpile:
	def __init__(self):
		self.stack = []
	
	def __str__(self):
		s = "Discard pile has " + str(len(self.stack)) + " cards: "
		for i in range(0,len(self.stack)):
			s = s + str(self.stack[i])
		return s
		
	def query(self, colour, value):
	#Counts the number of the specified card in the discard.
		count = 0
		for c in self.stack:
			if c.colour == colour and c.value == value:
				count = count + 1
		return count
		
	def add(self, discardedcard):
		self.stack.append(discardedcard)
		
#Initiate the Player class, with five cards in hand
#and blank knowledge of these cards (-1 represents no knowledge)

class player:
	def __init__(self, deck, board, discardpile, strat):
		self.deck = deck
		self.bin = discardpile
		self.hand = [deck.stack.pop(), deck.stack.pop(), deck.stack.pop(), deck.stack.pop(), deck.stack.pop()]	
		self.knowledge = [ card(-1,-1), card(-1,-1), card(-1,-1), card(-1,-1), card(-1,-1) ]
		self.board = board
		self.strategy = strat
		
	def __str__(self):
		return "My hand is "+ str(self.hand) + ". I know " + str(self.knowledge) + "."
		
	#def allocatefriend(self,friend):
	#	self.friend = friend
	#Got rid of in favour of passing the friend to the player when giving a clue. (That's a neater solution which extends to n player games :o )
	
	def setfriend(self, friend)
		self.friend = friend
	
	def draw(self,position):
	#Tries to draw card. Return 0 if game continues, 1 if empty deck.
		if len(self.deck.stack) > 0:
			self.hand[position] = self.deck.stack.pop()
			self.knowledge[position] = card(-1,-1)
		else: 
			self.hand[position] = card(-1,-1)
			self.knowledge[position] = card(-1,-1)
		
		if len(self.deck.stack) == 0:
			return 1
		else:
			return 0
		
	def movecard(self,original,target):
	#Takes integers original & target. 
	#Moves card from original to target, shifting other cards in the direction of Original.
	#Do nothing if original = target. 															NB: add error catching here! Original, target not in 0-4, also original = target?
		tempcard = self.hand[original]
		tempknowledge = self.knowledge[original]
		if original < target:
			for i in range(original, target):
				self.hand[i] = self.hand[i+1]
				self.knowledge[i] = self.knowledge[i+1]
			self.hand[target] = tempcard
			self.knowledge[target] = tempknowledge
		
		if original > target:
			for i in range(original, target, -1):
				self.hand[i] = self.hand[i-1]
				self.knowledge[i] = self.knowledge[i-1]
			self.hand[target] = tempcard
			self.knowledge[target] = tempknowledge
			
	def playcard(self,handposition):
	#Tries to play card onto the board
	#Returns 0 if success, 1 if failure														
		chosencard = self.hand[handposition]
		if self.board[chosencard.colour].value == chosencard.value - 1:
			self.board[chosencard.colour] = chosencard
			self.draw(handposition)
			return 0
		else:
			self.bin.add(chosencard)
			self.draw(handposition)	
																								#NB: there's no memory of the discard pile at the moment.
			return 1
	
	def giveclue(self,friend,attribute,number):
	#Gives a clue to the targeted friend.
		if attribute == "colour":
			for i in range(0,5):
				if friend.hand[i].colour == number:
					friend.knowledge[i].colour = friend.hand[i].colour
		
		if attribute == "value":
			for i in range(0,5):
				if friend.hand[i].value == number:
					friend.knowledge[i].value = friend.hand[i].value
																									#I'm going to need to store the last play as a minimum, in order to have a hope of useful strategies
	def discard(self,handposition):
		self.bin.add(self.hand[handposition])
		return self.draw(handposition)
																									#That will need... a history array? And for this function to return which cards were targeted?
																									#Also - add error catching!
			
def playhanabi():
	print " Let's play Hanabi with player's own strategies! Initialising:"		
	gamedeck = deck()
	board = [card(0,0),card(0,1),card(0,2),card(0,3),card(0,4)]
	gamedeck.shuffle()
	trash = discardpile()
	activeplayer = player(gamedeck, board, trash, strategy_askplayer)
	inactiveplayer = player(gamedeck, board, trash, strategy_askplayer)
	global clues 
	clues = 8
	global lives 
	lives = 3
	
	print "Deck   : ", gamedeck
	print "P1     : ", player1
	print "P2     : ", player2
	print "Board  : ", board
	print "Discard: ", trash
		
	activeplayer.setfriend(inactiveplayer)
	inactiveplayer.setfriend(activeplayer)
	
	#Play continues until the deck is empty or we're out of lives.
	while len(gamedeck.stack) > 0	and lives > 0:
		taketurn(activeplayer,inactiveplayer)
		activeplayer, inactiveplayer = inactiveplayer, activeplayer

	#At the end of the loop, if we're not out of lives then players get one more turn each.
	if lives > 0:
		taketurn(activeplayer, inactiveplayer)
		
		if lives > 0:
			taketurn(inactiveplayer, activeplayer)
	
	if lives == 0:
		print "BOOM! Out of lives."
		
	score = 0
	for suit in board:
		score = score + suit.value	
	
	print "Wasn't that fun? Your final score is ", str(score), ". Well done!"
	
	
def taketurn(activeplayer,inactiveplayer):
	#On your turn, ask the player's strategy what to do:
	#Give a clue
	#Play a card
	#discard a card
	#																								#NB: how to reflect the fact that at any time the player can rearrange their hand?
	global clues	
	global lives
	#																								Maybe after each action, ask each strategy if they want to?
	
	print " "
	print "Deck    : ", activeplayer.deck
	print "Active  :", activeplayer
	print "Inactive:", inactiveplayer
	print "Board   :", activeplayer.board
	print "Clues   :", str(clues)
	print "Lives   :", str(lives)
	
	while True:
	
		idea = activeplayer.strategy(activeplayer.deck, activeplayer.board, clues, lives)		
		#idea is a list, with first element as the action to take and the remaining variables as parameters. 
	
		if idea[0] == "clue":
			if clues > 0:
				clues = clues - 1
				activeplayer.giveclue(inactiveplayer,idea[1],idea[2])
				break
			else:
				print "shit, no more clues"
		
		elif idea[0] == "play":
			result = activeplayer.playcard(idea[2])	
			if result == 1: 
				lives = lives-1
				print "Argh! ", str(lives), " lives remaining."									#What if deck is empty?
			break	
			
		elif idea[0] == "discard":
			result = activeplayer.discard(idea[2])
			if clues < 8:
				clues = clues + 1
			break
			
		else:
			print "error, unrecognised idea"
	
	return 0
			
	
	
	
def strategy_askplayer():
	#Player-defined strategy: ask the player what to do!
	param1 = ""
	param2 = 0
	idea = raw_input("What's the play?")
	if idea == "clue":
		param1 = raw_input("'colour' or 'value'?   ")
		param2 = raw_input("which one? (0-5)   ")
	elif idea == "play" or idea == "discard":
		param2 = raw_input("Which card? (0-4)   ")
	
	return [idea,param1,int(param2)]

			
playhanabi()




#________________How to do knowledge?____________________
#Knowledge for a player is a 2d array: one for colour, one for number.
#That means a strategy is a function of my friend's hand, the board and my knowledge.
#Make sure when we draw, play and move cards, knowledge behaves sensibly.

#Alternative: knowledge could be a property of the cards?
#That would require the cards to reference up to their owners though, which is less neat.
#And knowledge feels like a function of the players, rather than of the cards. I think.
#But then again, the first method is dropping some of the object orientation and working with janky arrays..?

#________________How to do turns and rules?______________
#Just a function I guess.
#Variable numclues for number of clues remaining
#Each turn, call getstrat to get the play - at the moment, just taking manual input.

#_______________Plan for discard pile?___________________
#Discardpile object? Takes cards and appends them onto a discard pile list.
#Could have a function for returning how many copies of a (number,colour) pair have been discarded.
#But is that function amenable to being read by a strategy?

#_______________Philosophical notes______________________
#What does a player object know? Is this just a matter of convenience, or is it a good way of thinking about object oriented programming?
#It makes sense that the ability to make manual movements belongs to the players. It makes sense that hands also belong to the players.
#Could be argued that friends, decks and boards shouldn't be part of the player, but deck is referenced several times so it must be easier, ditto boards.
#I guess the more general player object could be used in other games!!! That's actually quite cool.
#Knowledge is a thorny one: is knowledge part of the player? Given that I'm treating the player as a mindless automaton who takes instructions from a strategy object, perhaps 
#the strategy object should hold the knowledge. Actually, that would make the strategy code much less clean and wouldn't allow you to apply strategies to any situation - that is,
#a strategy should be independent of the game state and should read the game state almost certainly, that makes the most sense.
#Giving clues? I'm putting that as part of the player because other actions are with the player. Also because there's physical pointing going on irl. But there's no coding need for
#it to belong to the player - is that me overthinking the philosophy here then? Brutal code or ontological sensibility?
#
#_____Next_____
#Work out reordering the hand in game context?
#We should probably draw a card into a specified spot. 
#start looking at how to make an AI? Do I need to write the evaluation function myself?
#Or could I just say "it's the score" for finished games, and score positions over their possible subsequent positions?
#The problem there is that I'm trying to communicate information! So a position's goodness is a function of how smart my friend is, or at least how likely he is to pick up on my cues!
#So do I need to train each AI against itself, to discover how itself reacts to different situations?
#Is that similar to how a poker AI learns against a player?
#NB: do poker AIs learn from their individual opponents, or just play against a generalised assumption of an opponent?
#NB: is it a bit of both? In that case, is that process manually calibrated or can it be auto-optimised?
#Damn, this is actually rather hard!

#clear screen:
#
#


