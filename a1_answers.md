Q1 

(a) Which heuristic performs better, misplaced tiles or Manhattan distance.

How do you measure the effectiveness of the heuristic?
Solution cost? Solution cost is the same for both heuristics.
Nodes expanded? h_misplacedTiles expands more nodes than h_MHDist. the differences increases as the difficulty of the problem increases.
States generated? h_misplacedTiled generates more tiles than h_MHDist. significantly more.
States cycle check pruned? cycle check prunes more states more h_misplacedTiles than it does for h_MHDist

===========Test 1, EASY, ASTAR, h_MHDist==============
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 5, Goal state:
     Action= "Blank-Down", S13, g-value = 5, (From S12)
----------------------------
Search time = 0.0, nodes expanded = 12, states generated = 16, states cycle check pruned = 4
======================================================

===========Test 1, EASY, ASTAR, h_misplacedTiles======
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 5, Goal state:
     Action= "Blank-Down", S16, g-value = 5, (From S15)
----------------------------
Search time = 0.0, nodes expanded = 14, states generated = 19, states cycle check pruned = 5
======================================================

===========Test 1, MEDIUM 1, ASTAR, h_MHDist==============
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 9, Goal state:
     Action= "Blank-Down", S25, g-value = 9, (From S24)
----------------------------
Search time = 0.0, nodes expanded = 19, states generated = 28, states cycle check pruned = 9
======================================================

===========Test 1, MEDIUM 1, ASTAR, h_misplacedTiles======
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 9, Goal state:
     Action= "Blank-Down", S58, g-value = 9, (From S57)
----------------------------
Search time = 0.0, nodes expanded = 41, states generated = 61, states cycle check pruned = 20
======================================================

===========Test 1, MEDIUM 2, ASTAR, h_MHDist==============
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 12, Goal state:
     Action= "Blank-Down", S60, g-value = 12, (From S59)
----------------------------
Search time = 0.01, nodes expanded = 42, states generated = 63, states cycle check pruned = 21
======================================================

===========Test 1, MEDIUM 2, ASTAR, h_misplacedTiles======
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 12, Goal state:
     Action= "Blank-Down", S166, g-value = 12, (From S165)
----------------------------
Search time = 0.0, nodes expanded = 110, states generated = 169, states cycle check pruned = 59
======================================================

===========Test 1, HARD, ASTAR, h_MHDist==============
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 30, Goal state:
     Action= "Blank-Up", S6773, g-value = 30, (From S6772)
----------------------------
Search time = 0.1, nodes expanded = 4037, states generated = 6776, states cycle check pruned = 2739
======================================================

======================================================
===========Test 1, HARD, ASTAR, h_misplacedTiles======
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 30, Goal state:
     Action= "Blank-Up", S664676, g-value = 30, (From S664675)
----------------------------
Search time = 10.89, nodes expanded = 319374, states generated = 664679, states cycle check pruned = 345305
======================================================

======================================================
===========Test 2, HARD, ASTAR, h_MHDist======
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 20, Goal state:
     Action= "Blank-Right", S123, g-value = 20, (From S121)
----------------------------
Search time = 0.02, nodes expanded = 79, states generated = 125, states cycle check pruned = 46
======================================================

======================================================
===========Test 2, HARD, ASTAR, h_misplacedTiles======
============================
Search Successful! (strategy 'astar with full cycle checking') Solution cost = 20, Goal state:
     Action= "Blank-Right", S5657, g-value = 20, (From S5655)
----------------------------
Search time = 0.06, nodes expanded = 3386, states generated = 5659, states cycle check pruned = 2273
======================================================

(b) Create a graph (up to 1/2 page) of the number of nodes explored by the Manhattan distance
heuristic on the x-axis, and the number of nodes explored by the misplaced tiles heuristic on the
y-axis. Put a point on this graph for each eightpuzzle problem solved from file eightpuzzle tests.py.
Can you say anything about the trend, i.e., as Manhattan distance has to explore more nodes how
is the number of nodes explored by misplaced tiles growing? (1-2 sentences).

What is the number of nodes explored? Is it the 'nodes expanded' value in the sample output file?

