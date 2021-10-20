# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 20:24:53 2019

@author: lenovo
"""

import pygame
import time
import random
import sqlite3

blue = (0,0,255)
white = (255,255,255)
red = (225, 12, 27)

pygame.init()

Donnees = "Donnees.sq3"
conn = sqlite3.connect(Donnees)
cur = conn.cursor()


surfaceW = 800
surfaceH = 500
ballonW = 50
ballonH = 66
nuageW = 300
nuageH = 300




surface = pygame.display.set_mode((surfaceW,surfaceH))
pygame.display.set_caption("Ballon volant")
horloge = pygame.time.Clock()

img = pygame.image.load('Ballon01.png')
img_nuage1 = pygame.image.load('NuageHaut.png')
img_nuage2 = pygame.image.load('NuageBas.png')


def jauge(compte):
    police = pygame.font.Font('BradBunR.ttf',30)
    texte = police.render("| " * (compte),True,white)
    surface.blit(texte,[0,470])

def score(compte):
    police = pygame.font.Font('BradBunR.ttf',16)
    texte = police.render("score : " + str(compte),True,red)
    surface.blit(texte,[10,0])

def Hscore(compte):
    police = pygame.font.Font('BradBunR.ttf',16)
    texte = police.render("meilleur score : " + str(compte),True,red)
    surface.blit(texte,[700,0])
    
    
def nuages(x_nuage,y_nuage,espace):
    surface.blit(img_nuage1,(x_nuage,y_nuage))
    surface.blit(img_nuage2,(x_nuage,y_nuage+nuageW+espace))


def rejoueOUQuitter():
    for event in pygame.event.get ([pygame.KEYDOWN,pygame.KEYUP,pygame.QUIT]):
        if event.type==pygame.QUIT:
            quit()
        elif event.type == pygame.KEYUP :
            continue
        return event.key
    return None

def creaTexteObj(texte,Police):
    texteSurface = Police.render(texte,True,white)
    return texteSurface, texteSurface.get_rect()
    

def message(texte):
    GOTexte = pygame.font.Font('BradBunR.ttf',150)
    petitTexte = pygame.font.Font('BradBunR.ttf',20)
    
    GOTexteSurf, GOTexteRect = creaTexteObj(texte,GOTexte)
    GOTexteRect.center = surfaceW/2 , ((surfaceH/2)-50)
    surface.blit(GOTexteSurf,GOTexteRect)
    
    petitTexteSurf,petitTexteRect =creaTexteObj("appuyer sur une touche pour continuer",petitTexte)
    petitTexteRect.center = surfaceW/2 , ((surfaceH/2)+50)
    surface.blit(petitTexteSurf,petitTexteRect)
    
    
    pygame.display.update()
    time.sleep(2)
    
    while rejoueOUQuitter() == None:
        horloge.tick()
    
    principale()
    

def gameOver(score_actuel):
    a = list(str(score_actuel))
    
    Donnees = "Donnees.sq3"
    conn = sqlite3.connect(Donnees)
    cur = conn.cursor()
    cur.execute("select* from membres")
    liste = list(cur)
    hscore=[]
    for i in range(0,len(liste)):
        hscore +=liste[i] 
        
    if (int(hscore[-1]) < score_actuel):
        cur.execute("insert into membres(score) values(?)",a)
        conn.commit()
        cur.close()
        conn.close()
    message("Boom!")
    

def ballon(x,y,image):
    surface.blit(image,(x,y))

def principale():
    x = 150
    y = 200
    y_mouvement = 0
    
    x_nuage = surfaceW
    y_nuage = random.randint(-300,20)
    espace = ballonH*3
    nuage_vitesse = 3

    score_actuel = 0
    jeton = 0
    
   
    game_over = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_mouvement = -1
            if event.type == pygame.KEYUP:
                y_mouvement = 1
        y+= y_mouvement
                    
        surface.fill(blue)
        ballon(x,y,img)
        
        nuages(x_nuage,y_nuage,espace)
        
        score(score_actuel)
        jauge(jeton)
        
        cur.execute("select * from membres")
        liste = list(cur)
        
        
        hscore = []
        for  i in range (0,len(liste)):
            hscore +=liste[i]
        
        
        Hscore(hscore[-1])
        
        x_nuage -=nuage_vitesse
        
        if y>surfaceH -30 or y<-20:
            gameOver(score_actuel)
            
        if (x+ballonW) > x_nuage +40   and  x + 40 < (x_nuage + nuageW) :
            if y +20 < (y_nuage+ nuageH) or y+ballonH > (y_nuage + nuageH + espace + 30) :
                gameOver(score_actuel)
        
       
        
        if x_nuage<(-1*nuageW):
            x_nuage = surfaceW
            y_nuage = random.randint(-300,20)
            score_actuel +=1
            jeton+=1
        
        
        pygame.display.update()

principale()

pygame.quit()
quit()