# py-poker-test

<p align="right">
  <a href="./README.md">English</a>
  |
  <a href="./README-RU.md">Русский</a>
</p>

**This is a classic poker game with 2 bots. The game is made entirely in Python in 1 file using the random and time libraries. Also the game is completely made in console without interface(further updates are still possible). But despite this, it is a very exciting game. Rules:**

*You are dealt cards and your combination is told in the format:*
```
♣3 ♥5 ♣K ♥K ♣T
2 - Pair
```
*Then all players make their bets (you initially have 100 points on your balance). After betting, you change the cards by indicating their ID separated by a space (the ID is indicated above them):*
```
 1  2  3  4  5
♣3 ♥5 ♣K ♥K ♣T
```

*After this, you will be asked to surrender. If you remain in the game, then all players make additional bets and a verdict is made on the winner, and the entire bank is credited to him.*
