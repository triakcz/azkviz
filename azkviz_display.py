#!/usr/bin/python
# -*- encoding: utf-8 -*-

import pygame
import sys

pygame.init()
window = pygame.display.set_mode((640, 480))
pygame.display.set_caption('AZ-Kviz user display') 
screen = pygame.display.get_surface()

MAXTIMER=15

buf=0
charbuf=""

def writebuf():
    pygame.draw.rect(screen,pygame.Color('black'),(500,140,140,30),0)
    write_text(500,140,str(buf),flip=True)

def writecharbuf():
    pygame.draw.rect(screen,pygame.Color('black'),(50,25,180,80),0)
    if (len(charbuf)>0):
        write_text(50,25,'ENTER - smazat',size=17)
        write_text(50,40,str(charbuf),flip=True,size=50)

def write_text(x,y,txt,size=30,flip=False):
    font = pygame.font.Font(None, size)
    t = font.render(str(txt), 1, pygame.Color('white'))
    screen.blit(t, (x,y))
    if flip:
        pygame.display.flip()

def draw_timer():
    print timer
    pygame.draw.rect(screen, pygame.Color('black'),(260,400,60,60),0)
    pygame.draw.arc(screen, pygame.Color('red'),(260,400,60,60) , 3.14/2, (2*3.14*timer/MAXTIMER)+(3.14/2),5)
    pygame.display.flip()


def input(events): 
    global buf,timer,charbuf
    for event in events: 
        print event
        if (event.type == pygame.QUIT): 
            sys.exit(0)

        elif event.type == pygame.KEYDOWN:

            if event.key == 27:
                sys.exit(0)
            elif event.unicode>='0' and event.unicode<='9':
                buf*=10
                buf+=int(event.unicode)
                if buf>28:
                    buf=28
                print buf
                writebuf()
            elif event.key == 8:
                buf/=10
                writebuf()
            elif event.key == 32:
                timer=MAXTIMER
                draw_timer()

            elif event.key == pygame.K_F6 or event.key == pygame.K_F10:
                charbuf=""
                writecharbuf()
                timer=0
                if buf<0 or buf>28:
                    continue
                p=buf-1
                if (pole[p]) == 0:
                    if event.key == pygame.K_F6:
                        pole[p] = 1
                    else:
                        pole[p] = 2
                    draw_field()
                  
                buf=0
                writebuf()
                draw_timer()
            elif event.key == pygame.K_F8:
                if buf<0 or buf>28:
                    continue
                p=buf-1
                pole[p] = 0
                draw_field()
            elif (event.unicode>='a' and event.unicode<='z') or (event.unicode>='A' and event.unicode<='Z'):
                if len(charbuf) >= 6:
                    charbuf=""
                charbuf+=event.unicode
                writecharbuf()
            elif (event.key == pygame.K_RETURN):
                charbuf="";
                writecharbuf()


        elif event.type == pygame.USEREVENT+1:
            if timer>0:
                timer-=1
                if timer>2:
                    tuksnd.play()
                elif timer==0:
                    tddmtmsnd.play()
                else:
                    tukcinksnd.play()
            print timer
            draw_timer()

def draw_hexagon(x,y,c=pygame.Color('red'),size=10,text=None):
    m=size*2
    v=size*4
    pygame.draw.polygon(screen, c, [(x,y-v),(x+v,y-m),(x+v,y+m),(x,y+v),(x-v,y+m),(x-v,y-m)],0)
    if text is not None:
        font = pygame.font.Font(None, 36)
        t = font.render(text, 1, pygame.Color('black'))
        textpos = t.get_rect(centerx=x,centery=y)
        screen.blit(t, textpos)

def draw_field():
    xs=320
    ys=0
    offset=52
    yoffset=12
    for i in range(8):
        for j in range(i):
            fid=(i*(i-1)/2+j)
            y=i*offset+ys
            x=j*(offset+yoffset)-(i/2.)*(offset+yoffset)+xs
            if pole[fid]==0:
                c=pygame.Color('gray');
            elif pole[fid]==1:
                c=pygame.Color('orange');
            else:
                c=pygame.Color('blue');
            draw_hexagon(x,y,size=7,text=str(fid+1),c=c)
            
    pygame.display.flip()

pole=[0]*28
draw_field()
draw_hexagon(50,430,pygame.Color('orange'),size=5)
write_text(50,430,sys.argv[1])
write_text(50,470,'F6 - Oznacit',size=17)
draw_hexagon(500,430,pygame.Color('blue'),size=5)
write_text(500,430,sys.argv[2])
write_text(500,470,'F10 - Oznacit',size=17)
write_text(200,470,'F8 - Opravit',size=17,flip=True)

timer=0

pygame.mixer.init()
snd=pygame.mixer.Sound('sounds/znelka.wav')
snd.play()

tuksnd=pygame.mixer.Sound('sounds/tuk.wav')
tukcinksnd=pygame.mixer.Sound('sounds/cink.wav')
tddmtmsnd=pygame.mixer.Sound('sounds/ttdmtm.wav')

pygame.time.set_timer(pygame.USEREVENT+1, 1000)

while True: 
   input(pygame.event.get())
