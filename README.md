
**Overview**

Nim is a mathematical game in which two player take turns removing objects from distinct piles. The goal is to take the last object, although there are other variations too. The numbers are represented in base-2, where the nim-sum is computed using XOR operations. Nim is fundamental to the Sprague–Grundy theorem, which generalizes strategies for impartial games.


**Rules**

Players take turns removing at least one object from a single pile.
A player may remove any number of objects, but only from one pile per turn.
The game ends when all objects have been removed.

**Strategy & Winning Conditions**

The optimal strategy relies on computing the nim-sum (binary XOR of pile sizes).
If the nim-sum at the start of a turn is 0, the player to move is in a losing position if the opponent plays optimally.
If the nim-sum is nonzero, the player can force a win by making a move that results in a nim-sum of 0.

**Variations**

Misère Nim: The last move determines the loser rather than the winner as whoever has the last object loses.
Greedy Nim: Players can only take objects from the largest pile.




![Screenshot 2025-02-24 224604](https://github.com/user-attachments/assets/1adc6d5a-90eb-49c6-8010-bc5ebbb50622)


The game is implemented in python.

