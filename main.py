# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 20:40:04 2020

@author: soumitra
"""


import pygame
import numpy as np


WIDTH = 1500
HEIGHT = 600

lin_start = [24, 3 * HEIGHT//4]
lin_end = [WIDTH - 1, 3 * HEIGHT//4]

SCREEN = (WIDTH, HEIGHT)
timesteps = 10
digits = 5



class Block:
    def __init__(self, x, size, m, v, colour, constraint):
        self.x = x
        self.w = size
        self.m = m
        self.v = v
        self.collide = False
        self.colour = colour
        self.count = 0
        self.constraint = constraint
        
    def updateVelocity(self):
        self.x += self.v
        
        
    def draw(self, screen):
        if self.x < self.constraint:
            pygame.draw.rect(screen, self.colour, [self.constraint, 450 - self.w, self.w, self.w])
        else:
            pygame.draw.rect(screen, self.colour, [self.x, 450 - self.w, self.w, self.w])
        
    def checkCollision(self, other):
        if not ((other.x + other.w < self.x) or (self.x + self.w < other.x)):
            return True
        else:
            return False
            
        
    def changeVelocityonCollision(self, other):
        newv = (self.v * (self.m - other.m) + 2 * other.v * other.m)/(self.m + other.m)
        #other.v = (other.v * (other.m - self.m) + 2 * self.m * oldSelfv)/(self.m + other.m)
        return newv
    
    def checkWallCollision(self):
        if self.x < 24 or self.x + self.w >= 1498:
            return True
        else:
            return False
         



screen = pygame.display.set_mode(SCREEN)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

listy = [y for y in range(0, HEIGHT - 1, 5)]
listx = [20, 0] * len(listy)
lines = [(x, y) for x, y in zip(listx, listy)]

M = 200

block1 = Block(250, 100, M, -1/timesteps, RED, 50 + 24)
block2 = Block(100, 50, M - 1, 0, BLUE, 24)

count = 0

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, (255, 255, 255), lin_start, lin_end, 3)
    pygame.draw.line(screen, (255, 255, 255), (20, 0), (20, HEIGHT - 1), 3)
    
    for i, (x, y) in enumerate(lines):
        if x == 20:
            pygame.draw.line(screen, (255, 255, 255), (x, y), (0, y + 10), 3)
    
    
    for i in range(timesteps):
        if block1.checkCollision(block2):
            v1 = block1.changeVelocityonCollision(block2)
            count += 1
            v2 = block2.changeVelocityonCollision(block1)
            
            block1.v = v1
            block2.v = v2
    
            
        if block1.checkWallCollision():
            block1.v *= -1 
            count = count + 1
        
        if block2.checkWallCollision():
            block2.v *= -1
            count = count + 1
    
           
        block1.updateVelocity()
        block2.updateVelocity()
        # if block1.x < block2.x + block2.w:
        #     block1.x = block2.x + block2.w
        # if block2.x < 24:
        #     block2.x = 24
        #print(block1.v, ' ', block2.v)

    block1.draw(screen) 
    block2.draw(screen)
    


    pygame.font.init()
    font = pygame.font.Font('freesansbold.ttf', 30) 
    text = font.render(f'{count}', True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()  
    textRect.center = (800, 520)
    
    font2 = pygame.font.Font('freesansbold.ttf', 30) 
    text2 = font2.render(f'M = {M}, m = {1}', True, (255, 255, 255), (0, 0, 0))
    textRect2 = text2.get_rect()  
    textRect2.center = (200, 100) 
    
    
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)
        
    pygame.display.update()


#print('collision = ', count)