import pygame
import layout as l
import surface as su
from dictionaries import setcard as sc

''''
start_x = 1
start_y = 1

bild_2 = pygame.image.load("Karten_png/card_-2.png")
bild_1 = pygame.image.load("Karten_png/card_-1.png")
bild0 = pygame.image.load("Karten_png/card_0.png")
bild1 = pygame.image.load("Karten_png/card_1.png")
bild2 = pygame.image.load("Karten_png/card_2.png")
bild3 = pygame.image.load("Karten_png/card_3.png")
bild4 = pygame.image.load("Karten_png/card_4.png")
bild5 = pygame.image.load("Karten_png/card_5.png")
bild6 = pygame.image.load("Karten_png/card_6.png")
bild7 = pygame.image.load("Karten_png/card_7.png")
bild8 = pygame.image.load("Karten_png/card_8.png")
bild9 = pygame.image.load("Karten_png/card_9.png")
bild10 = pygame.image.load("Karten_png/card_10.png")
bild11 = pygame.image.load("Karten_png/card_11.png")
bild12 = pygame.image.load("Karten_png/card_12.png")
bildb = pygame.image.load("Karten_png/card_back.png")

bild_2 = pygame.transform.scale(bild_2, ( sc.card_width, sc.card_height))
bild_1 = pygame.transform.scale(bild_1, ( sc.card_width, sc.card_height))
bild0 = pygame.transform.scale(bild0, ( sc.card_width, sc.card_height))
bild1 = pygame.transform.scale(bild1, ( sc.card_width, sc.card_height))
bild2 = pygame.transform.scale(bild2, ( sc.card_width, sc.card_height))
bild3 = pygame.transform.scale(bild3, ( sc.card_width, sc.card_height))
bild4 = pygame.transform.scale(bild4, ( sc.card_width, sc.card_height))
bild5 = pygame.transform.scale(bild5, ( sc.card_width, sc.card_height))
bild6 = pygame.transform.scale(bild6, ( sc.card_width, sc.card_height))
bild7 = pygame.transform.scale(bild7, ( sc.card_width, sc.card_height))
bild8 = pygame.transform.scale(bild8, ( sc.card_width, sc.card_height))
bild9 = pygame.transform.scale(bild9, ( sc.card_width, sc.card_height))
bild10 = pygame.transform.scale(bild10, ( sc.card_width, sc.card_height))
bild11 = pygame.transform.scale(bild11, ( sc.card_width, sc.card_height))
bild12 = pygame.transform.scale(bild12, ( sc.card_width, sc.card_height))
bildb = pygame.transform.scale(bildb, ( sc.card_width, sc.card_height))

'''
su.WINDOW.blit(bild_2, (start_x + sc.card_2["x"], start_y + sc.card2-["y"]))
su.WINDOW.blit(bild_1, (start_x + sc.card_1["x"], start_y + sc.card1-["y"]))
su.WINDOW.blit(bild0, (start_x + sc.card0["x"], start_y + sc.card0["y"]))
su.WINDOW.blit(bild1, (start_x + sc.card1["x"], start_y + sc.card1["y"]))
su.WINDOW.blit(bild2, (start_x + sc.card2["x"], start_y + sc.card2["y"]))
su.WINDOW.blit(bild3, (start_x + sc.card3["x"], start_y + sc.card3["y"]))
su.WINDOW.blit(bild4, (start_x + sc.card4["x"], start_y + sc.card4["y"]))
su.WINDOW.blit(bild5, (start_x + sc.card5["x"], start_y + sc.card5["y"]))
su.WINDOW.blit(bild6, (start_x + sc.card6["x"], start_y + sc.card6["y"]))
su.WINDOW.blit(bild7, (start_x + sc.card7["x"], start_y + sc.card7["y"]))
su.WINDOW.blit(bild8, (start_x + sc.card8["x"], start_y + sc.card8["y"]))
su.WINDOW.blit(bild9, (start_x + sc.card9["x"], start_y + sc.card9["y"]))
su.WINDOW.blit(bild10, (start_x + sc.card10["x"], start_y + sc.card10["y"]))
su.WINDOW.blit(bild11, (start_x + sc.card11["x"], start_y + sc.card11["y"]))
su.WINDOW.blit(bild12, (start_x + sc.card12["x"], start_y + sc.card12["y"]))
su.WINDOW.blit(bildb, (start_x + sc.cardb["x"], start_y + sc.cardb["y"]))