# Little-TouHou

A mini-game developed by using Pygame.

## Introduction

The game is a small STG game that idea came from Touhou Project.

## Start game

```shell
python danmuku.py
```

## Game Play

* Hold Z to shot
* Hold Shift to speed up
* Press X to use the bomb (Notice there is 1 second between two bomb use)
* Hold arrow key to move

You start with 4 HP and 3 bomb. Every single enemy's bullet will cause 1 hp lost. There is no interval between two incoming damage, so if you hit by 4 enemy's bullets at the same time, you die instantly.

## On Going

* Refactoring code

## TODO

* Currently only 10 enemy comes up in total 2 waves, you win if you kill them all. Need to add more content.
* Currently game has not start buttom or screen, game start running after game window shows up. Need to add a init screen with start game buttom.
* Currently game stuck after you die. Need to add a replay buttom.
