# Hanabi
A thing for playing hanabi.

Written as an exercise in object-oriented. I'm not sure I've followed every OO best practice, but it was a fun exercise to 
learn with.

The ultimate aim is to write an AI using a learning algorithm. The problem... is that dealing with hidden information is very difficult.
Maybe a neural network could just style it's way around the issue, in the way that neural networks seem to be able to do?

In its current form, playing should be pretty self-explanatory. The program will ask each player what they want to do and will
present them with the cards that they can see. 

Philosophical notes on object-oriented______________________
What does a player object know? Is this just a matter of convenience, or is it a good way of thinking about object oriented programming?
It makes sense that the ability to make manual movements belongs to the players. It makes sense that hands also belong to the players.
Could be argued that friends, decks and boards shouldn't be part of the player, but deck is referenced several times so it must be easier, ditto boards.
I guess the more general player object could be used in other games!!! That's actually quite cool.
Knowledge is a thorny one: is knowledge part of the player? Given that I'm treating the player as a mindless automaton who takes instructions from a strategy object, perhaps 
the strategy object should hold the knowledge. Actually, that would make the strategy code much less clean and wouldn't allow you to apply strategies to any situation - that is,
a strategy should be independent of the game state and should read the game state almost certainly, that makes the most sense.
Giving clues? I'm putting that as part of the player because other actions are with the player. Also because there's physical pointing going on irl. But there's no coding need for
it to belong to the player - is that me overthinking the philosophy here then? Brutal code or ontological sensibility?

To do list_____
Work out reordering the hand in game context?
We should probably draw a card into a specified spot. 
start looking at how to make an AI? Do I need to write the evaluation function myself?
Or could I just say "it's the score" for finished games, and score positions over their possible subsequent positions?
The problem there is that I'm trying to communicate information! So a position's goodness is a function of how smart my friend is, or at least how likely he is to pick up on my cues!
So do I need to train each AI against itself, to discover how itself reacts to different situations?
Is that similar to how a poker AI learns against a player?
NB: do poker AIs learn from their individual opponents, or just play against a generalised assumption of an opponent?
NB: is it a bit of both? In that case, is that process manually calibrated or can it be auto-optimised?
Damn, this is actually rather hard!
