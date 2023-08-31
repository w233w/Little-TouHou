# Little-TouHou

A mini-game developed by using Pygame.

## Introduction

The game is a small STG game that idea came from the Touhou Project.

## Start game

```shell
python danmuku.py
```

## Game Play

- Hold Z to shot
- Hold Shift to speed up
- Press X to use the bomb (Noticing there is 1 second between two bomb uses)
- Hold the arrow key to move

You can find your HP on the upper left and bombs on the upper right.

Every single enemy's bullet will cause 1 HP lost. There is no interval between two incoming damages, so if you are hit by X enemy bullets together, you lose X HP instantly.

## On Going

- Refactoring code

## TODO

- Currently, only 10 enemies will come in 2 waves; You win if you kill them all. Need to add more content.
- Currently, the game has no start button or screen; The game starts running after the game window shows up. Need to add an init screen with the start game button.
- Currently, the game is stuck after you die. Need to add a replay button.
