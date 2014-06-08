import pygame, os, sys, random, time
from pygame.locals import *
from pygame import surface

pygame.init()
pygame.display.init()
pygame.font.init()

sh=50
score=0
scoref=pygame.font.SysFont(pygame.font.get_default_font(), 50)
scorei=scoref.render(str(score), 0, (255, 255, 255))
lscore=score

screen = pygame.display.set_mode((550, 550+sh))
screen.set_alpha(None)
pygame.display.set_caption("2048")
f=pygame.font.SysFont(pygame.font.get_default_font(), 70)
numimg=[]
lag=2.5
def DrawRoundRect(surface, color, rect, width, xr, yr):
    clip = surface.get_clip()
    surface.set_clip(clip.clip(rect.inflate(0, -yr*2)))
    pygame.draw.rect(surface, color, rect.inflate(1-width,0), width)
    surface.set_clip(clip.clip(rect.inflate(-xr*2, 0)))
    pygame.draw.rect(surface, color, rect.inflate(0,1-width), width)
    surface.set_clip(clip.clip(rect.left, rect.top, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.top, 2*xr, 2*yr), width)
    surface.set_clip(clip.clip(rect.right-xr, rect.top, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(rect.right-2*xr, rect.top, 2*xr, 2*yr), width)
    surface.set_clip(clip.clip(rect.left, rect.bottom-yr, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(rect.left, rect.bottom-2*yr, 2*xr, 2*yr), width)
    surface.set_clip(clip.clip(rect.right-xr, rect.bottom-yr, xr, yr))
    pygame.draw.ellipse(surface, color, pygame.Rect(rect.right-2*xr, rect.bottom-2*yr, 2*xr, 2*yr), width)
    surface.set_clip(clip)

colors=[(238, 228, 218), (236, 224, 202), (242, 177, 121), (245, 149, 101), (245, 124, 95), (255, 105, 52), (237, 206, 113), (237, 204, 97), (236, 200, 80), (242, 192, 57), (236, 196, 0), (58, 59, 51)]  
for i in range(1, 13):
    numimg.append(pygame.Surface([117, 117], pygame.SRCALPHA, 32))
    numimg[-1]=numimg[-1].convert_alpha()
    DrawRoundRect(numimg[-1], colors[i-1], pygame.Rect(0, 0, 117, 70), 0, 10, 10)
    numimg[-1].blit(pygame.transform.flip(numimg[-1], 0, 1), (0, 0))
    if i<3:
        s=f.render(str(2**i), 0, (120, 109, 103))
    else:
        s=f.render(str(2**i), 0, (255, 255, 255))    
    numimg[-1].blit(s, ((numimg[-1].get_width()/2)-(s.get_width()/2), (numimg[-1].get_height()/2)-(s.get_height()/2)))
try:
    pygame.display.set_icon(numimg[10])
except Exception as x:
    print(x)

bg=pygame.Surface((550, 550+sh))
bg.fill((187, 173, 160))
blank=pygame.Surface([117, 117], pygame.SRCALPHA, 32).convert_alpha()
DrawRoundRect(blank, (204, 192, 179), pygame.Rect(0, 0, 117, 70), 0, 10, 10)
blank.blit(pygame.transform.flip(blank, 0, 1), (0, 0))
for y in range(4):
    for x in range(4):
        bg.blit(blank, ((x*133)+16, (y*133)+16+sh))
overimg=pygame.Surface((screen.get_width(), screen.get_height()))
overimg.fill((255, 227, 136))
overimg.set_alpha(125)
nums=[2**i for i in range(1, 12)]
def spawn():
    global p
    if 0 in p:
        x=random.randint(0, 15)
        while p[x]!=0:
            x=random.randint(0, 15)
        p[x]=random.choice([2, 4])
    else:
        gameovr()
p=[0]*16   
coors=[]
n=[16, 149, 283, 416]
for y in range(4):
       for x in range(4):
           coors.append((n[x], n[y]+sh))
spawn()
spawn()

def gameovr():
    global p, overimg, score
    score=0
    n=screen
    n.blit(overimg, (0, 0))
    s=pygame.font.SysFont(pygame.font.get_default_font(), 100).render('Game Over', 0, (116, 109, 105))
    n.blit(s, ((n.get_width()/2)-(s.get_width()/2), (n.get_height()/2)-(s.get_height()/2)))

    r=pygame.Rect(213, 303, 120, 40)
    d=1
    while d:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                p=[0]*16   
                spawn()
                spawn()
                d=0
        screen.blit(n, (0, 0))
        pygame.display.update()

def youwin():
    global p, overimg
    n=screen
    n.blit(overimg, (0, 0))
    s=pygame.font.SysFont(pygame.font.get_default_font(), 100).render('You Win!', 0, (116, 109, 105))
    n.blit(s, ((n.get_width()/2)-(s.get_width()/2), (n.get_height()/2)-(s.get_height()/2)))

    r=pygame.Rect(213, 303, 120, 40)
    d=1
    while d:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                d=0
        screen.blit(n, (0, 0))
        pygame.display.update()
        
def ifend():
    global p
    xs=[p[0:4], p[4:8], p[8:12], p[12:16]]
    ys=[[p[0], p[4], p[8], p[12]], [p[1], p[5], p[9], p[13]], [p[2], p[6], p[10], p[14]], [p[3], p[7], p[11], p[15]]]
    c=1
    for i in xs:
        for m in range(3):
            if i[m]==i[m+1] and i[m]!=0:
                c=0
    for i in ys:
        for m in range(3):
            if i[m]==i[m+1] and i[m]!=0:
                c=0
    for i in xs:
        for m in range(1, 4):
            if i[m]==i[m-1] and i[m]!=0:
                c=0
    for i in ys:
        for m in range(1, 4):
            if i[m]==i[m-1] and i[m]!=0:
                c=0
    return c
def update():
    global lscore, score, scoref, scorei, blank, scoreb
    screen.fill((187, 173, 160))
    if lscore!=score or score==0:
        scorei=scoref.render(str(score), 0, (0, 0, 0))
        scoreb = pygame.transform.scale(blank, (scorei.get_width()+20, scorei.get_height()+10))
    lscore=score
    screen.blit(bg, (0, 0))
    screen.blit(scoreb, (screen.get_width()-20-scoreb.get_width(), 10))
    screen.blit(scorei, (((screen.get_width()-20)-(scoreb.get_width()/2))-(scorei.get_width()/2), (10+(scoreb.get_height()/2))-(scorei.get_height()/2)))
    for i in range(16):
        if p[i]!=0:
            screen.blit(numimg[nums.index(p[i])], coors[i])
    pygame.display.update()
lastp=p

def move(c, d, p):
    d[1]*=-1
    global numimg, nums, lag
    i=[]
    cs=[]
    s=pygame.Surface(screen.get_size())
    s.blit(bg, (0, 0))
    s.blit(scoreb, (screen.get_width()-20-scoreb.get_width(), 10))
    s.blit(scorei, (((screen.get_width()-20)-(scoreb.get_width()/2))-(scorei.get_width()/2), (10+(scoreb.get_height()/2))-(scorei.get_height()/2)))
    for m in range(16):
        if p[m]!=0 and (not (m in c)):
            s.blit(numimg[nums.index(p[m])], coors[m])
            
    for m in c:
        i.append(numimg[nums.index(p[m])])
        cs.append(list(coors[m]))
    for w in range(int(133/lag)):
        screen.blit(s, (0, 0))
        for x in range(len(i)):
            screen.blit(i[x], cs[x])
            cs[x][d[0]]+=(lag*d[1])
        pygame.display.update()
def moveb(xs, v, s, g):
    global p, score
    c=1   
    while c:
        c=0
        z=-1
        lp=p
        changes=[]
        for i in xs:
            z+=1
            for m in g:
                if i[m]==0 and i[m+v]!=0:
                    i[m]=i[m+v]
                    i[m+v]=0
                    c=1
                    if s=='xs':
                        p=xs[0]+xs[1]+xs[2]+xs[3]
                        if v==1:
                            changes.append((4*z)+(m+1))
                        else:
                            changes.append(((4*z)+(m+1))-2)
                    else:
                        p=[i[0] for i in ys]+[i[1] for i in ys]+[i[2] for i in ys]+[i[3] for i in ys]
                        if v==-1:
                            changes.append((4*(m-1))+(z))
                        else:
                            changes.append((4*(m+1))+(z))
        move(changes, [int(s=='ys'), v], lp)

def check(xs, v, s, g):
    global p, score
    try:
        moveb(xs, v, s, g)
    except Exception as a:
        print(a)

    for i in xs:
        for m in g:  
            if i[m]==i[m+v] and i[m]!=0:
                i[m]*=2
                i[m+v]=0
                score+=i[m]
    try:
        moveb(xs, v, s, g)
    except Exception as a:
        print(a)
    update()
    if s=='xs':
        p=xs[0]+xs[1]+xs[2]+xs[3]
    else:
        p=[i[0] for i in ys]+[i[1] for i in ys]+[i[2] for i in ys]+[i[3] for i in ys]
win=0
while 1:
    xs=[p[0:4], p[4:8], p[8:12], p[12:16]]
    ys=[[p[0], p[4], p[8], p[12]], [p[1], p[5], p[9], p[13]], [p[2], p[6], p[10], p[14]], [p[3], p[7], p[11], p[15]]]
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    check(xs, 1, 'xs', range(3))
                    if lastp!=p:
                        spawn()
                if event.key == K_RIGHT:
                    check(xs, -1, 'xs', range(3, 0, -1))
                    if lastp!=p:
                        spawn()
                if event.key == K_UP:
                    check(ys, 1, 'ys', range(3))
                    if lastp!=p:
                        spawn()
                if event.key == K_DOWN:
                    check(ys, -1, 'ys', range(3, 0, -1))
                    if lastp!=p:
                        spawn()
                if (2048 in p) and (not win):
                    win=1
                    youwin()
                if (not (0 in p)):
                    if ifend():
                        update()
                        gameovr()
    
    lastp=p
    update()

