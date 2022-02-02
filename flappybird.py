import pygame
import random
import time
import math
import numpy as np

# your code.

pygame.init();
# rgb color selector
WHITE = (250,250,250)
RED=(255,0,0)
BLUE=(0,0,255)
Color_line=(255,0,0)
# dài rộng screen
WINDOWWIDTH = 500
WINDOWHEIGHT = 800
# Screen
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
# load background image
background = pygame.image.load('screen.jpg')
background =pygame.transform.scale(background,(WINDOWWIDTH,WINDOWHEIGHT))
# Đất
land = pygame.image.load('land.jpg')
land =pygame.transform.scale(land,(500,250))
# Y_tube
Y_tube1=random.randint(100,450)
Y_tube2=random.randint(100,450)
Y_tube3=random.randint(100,450)
Y_tubeop1=(Y_tube1+170)
Y_tubeop2=(Y_tube2+170)
Y_tubeop3=(Y_tube3+170)
X_tube1=500
X_tube2=800
X_tube3=1100
X_tubeop1=500
X_tubeop2=800
X_tubeop3=1100

gen_pop = 100
# pipe mario
tube1 = pygame.image.load('tube.png')
tube1 =pygame.transform.scale(tube1,(50,Y_tube1))
tube2 = pygame.image.load('tube.png')
tube2 =pygame.transform.scale(tube2,(50,Y_tube2))
tube3 = pygame.image.load('tube.png')
tube3 =pygame.transform.scale(tube3,(50,Y_tube3))
tubeop1 = pygame.image.load('tupeop.jpg')
tubeop1 =pygame.transform.scale(tubeop1,(50,630-Y_tubeop1))
tubeop2 = pygame.image.load('tupeop.jpg')
tubeop2 =pygame.transform.scale(tubeop2,(50,630-Y_tubeop2))
tubeop3 = pygame.image.load('tupeop.jpg')
tubeop3 =pygame.transform.scale(tubeop3,(50,630-Y_tubeop3))

# flappy bird
bird = pygame.image.load('bird.png')
bird=pygame.transform.scale(bird,(60,50))
# icon and caption
pygame.display.set_caption('Flappy bird')
icon=pygame.image.load('bird.png')
pygame.display.set_icon(icon)
# X-Y bird
X_bird=200
Y_bird=[]
for i in range(gen_pop):
    Y_bird.append(random.randint(0,600))

degree=-3

# X land
X_land1=0
X_land2=500
X_land3=1000
# Change
X_land_change=0
X_tube_change=0
Y_bird_change=0

degree_change=0
#font chữ
font=pygame.font.SysFont('san',40)
fontgameover=pygame.font.SysFont('san',100)
font_score=pygame.font.SysFont('san',100)
font_pause=pygame.font.SysFont('san',30)
max_best_rank_bird = []


clock = pygame.time.Clock()

population = gen_pop
score=[0 for i in range(gen_pop)]
rank_bird = [[0,0,i] for i in range(gen_pop)]
image = []
pausing = [False for i in range(gen_pop)]
count_gens = 1
max_score =0
best_gens_arr = []
# Neural Networks 
class NNN:
    def __init__(self):
        self.w1 = 0.1
        self.w2 = 0.1
        self.w3 = 0.1
        self.w4 = 0.1
        self.w5 = 0.1
        self.w6 = 0.1
        self.w7 = 0.1
        self.w8 = 0.1
        self.b1 = 0
        self.b2 = 0
        self.b3 = 0
        self.input1 = 0
        self.input2 = 0
        self.input3 = 0
    def tanh(self,x):
        return math.tanh(x)
    def input(self,top_tupe,bottom_tupe,Y_bird):
        self.input1 = top_tupe
        self.input2 = bottom_tupe
        self.input3 = Y_bird
    def output(self):
        x1 = self.input1*self.w1 + self.input2*self.w2 + self.input3*self.w3 + self.b1
        y1 = self.tanh(x1)
        x2 = self.input1*self.w4 + self.input2*self.w5 + self.input3*self.w6 +self.b2
        y2 = self.tanh(x2)
        y = (y1*self.w7 + y2*self.w8 + self.b3)
        return 1/(1+math.exp(-y))


class Container():
    def __init__(self,objects):
        self.w1 = [obj.w1 for obj in objects]
        self.w2 = [obj.w2 for obj in objects]
        self.w3 = [obj.w3 for obj in objects]
        self.w4 = [obj.w4 for obj in objects]
        self.w5 = [obj.w5 for obj in objects]
        self.w6 = [obj.w6 for obj in objects]
        self.w7 = [obj.w7 for obj in objects]
        self.w8 = [obj.w8 for obj in objects]
        self.b1 = [obj.b1 for obj in objects]
        self.b2 = [obj.b2 for obj in objects]
        self.b3 = [obj.b3 for obj in objects]
        self.input1 = [obj.input1 for obj in objects]
        self.input2 = [obj.input2 for obj in objects]
        self.input3 = [obj.input3 for obj in objects]

# brain bird
brain_bird = []
for i in range(gen_pop):
    obj_brain = NNN()
    brain_bird.append(obj_brain)


brain_bird[0].w1 = 100
c = Container(brain_bird)

# create 100 gens
gens = []
for i in range(gen_pop):
    brain_bird[i].w1 = random.uniform(-10,10)
    brain_bird[i].w2 = random.uniform(-10,10)
    brain_bird[i].w3 = random.uniform(-10,10)
    brain_bird[i].w4 = random.uniform(-10,10)
    brain_bird[i].w5 = random.uniform(-10,10)
    brain_bird[i].w6 = random.uniform(-10,10)
    brain_bird[i].w7 = random.uniform(-10,10)
    brain_bird[i].w8 = random.uniform(-10,10)
    brain_bird[i].b1 = random.uniform(-10,10)
    brain_bird[i].b2 = random.uniform(-10,10)
    brain_bird[i].b3 = random.uniform(-10,10)
    gens.append([brain_bird[i].w1,brain_bird[i].w2,brain_bird[i].w3,brain_bird[i].w4,brain_bird[i].w5,brain_bird[i].w6,brain_bird[i].w7,brain_bird[i].w8,brain_bird[i].b1,brain_bird[i].b2,brain_bird[i].b3])

while True:
    screen.fill(WHITE)    
    clock.tick(30)
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        #start game

            
                
                
    X_land_change=5
    X_tube_change=5        
    if population ==0:
        Y_tube1=random.randint(100,450)
        Y_tube2=random.randint(100,450)
        Y_tube3=random.randint(100,450)
        Y_tubeop1=(Y_tube1+170)
        Y_tubeop2=(Y_tube2+170)
        Y_tubeop3=(Y_tube3+170)
        X_land_change=0
        X_tube_change=0
        Y_bird_change=0
        X_tube1=500
        X_tube2=800
        X_tube3=1100
        X_tubeop1=500
        X_tubeop2=800
        X_tubeop3=1100 
        X_bird=200
        Y_bird=[]
        rank_bird.sort(key=lambda x:int(x[1])) #sort score
        rank_bird.reverse()
        count = 0
        score_max = max([brain[1] for brain in rank_bird])
        for brain in rank_bird:
            if brain[1] == score_max:
                count+=1

        
        best_brain = []
        best_brain = rank_bird[:count]
        
        best_brain.sort() # sort second
        best_brain.reverse()

        x = random.choice(best_brain[:10])
        best_gens_arr.append(x)
        
        try:
            best_gens_arr.sort(key=lambda x:int(x[1]))# sort score
            best_gens_arr.reverse()
            count = 0
            score_max = max([brain[1] for brain in best_gens_arr])
            for brain in best_gens_arr:
                if brain[1] == score_max:
                    count+=1
            best_brain_in_best_gens = []
            best_brain_in_best_gens = best_gens_arr[:count]
            best_brain_in_best_gens.sort()
            best_brain_in_best_gens.reverse()
        except:
            pass
        y = best_brain_in_best_gens[0]
        print 
        print(y)
        new_gens = []
        for i in range(gen_pop):
            brain_bird[i].w1 = gens[y[2]][0]+random.uniform(-1,1)
            brain_bird[i].w2 = gens[y[2]][1]+random.uniform(-1,1)
            brain_bird[i].w3 = gens[y[2]][2]+random.uniform(-1,1)
            brain_bird[i].w4 = gens[y[2]][3]+random.uniform(-1,1)
            brain_bird[i].w5 = gens[y[2]][4]+random.uniform(-1,1)
            brain_bird[i].w6 = gens[y[2]][5]+random.uniform(-1,1)
            brain_bird[i].w7 = gens[y[2]][6]+random.uniform(-1,1)
            brain_bird[i].w8 = gens[y[2]][7]+random.uniform(-1,1)
            brain_bird[i].b1 = gens[y[2]][8]+random.uniform(-1,1)
            brain_bird[i].b2 = gens[y[2]][9]+random.uniform(-1,1)
            brain_bird[i].b3 = gens[y[2]][10]+random.uniform(-1,1)
            new_gens.append([brain_bird[i].w1,brain_bird[i].w2,brain_bird[i].w3,brain_bird[i].w4,brain_bird[i].w5,brain_bird[i].w6,brain_bird[i].w7,brain_bird[i].w8,brain_bird[i].b1,brain_bird[i].b2,brain_bird[i].b3])
        gens = new_gens
        for i in range(gen_pop):
            Y_bird.append(random.randint(0,600))
            pausing[i]=False  
            score[i]= 0 
            rank_bird[i] = [0,0,i]  
        best_gen_index = []
        count_gens+=1          
    X_land1-=X_land_change
    X_land2-=X_land_change
    X_land3-=X_land_change

    X_tube1-=X_tube_change
    X_tube2-=X_tube_change
    X_tube3-=X_tube_change
    X_tubeop1-=X_tube_change
    X_tubeop2-=X_tube_change
    X_tubeop3-=X_tube_change

    land_draw1=screen.blit(land,(X_land1,630))
    land_draw2=screen.blit(land,(X_land2,630))
    land_draw3=screen.blit(land,(X_land3,630))

    tube1_draw=screen.blit(tube1,(X_tube1,0))
    tube2_draw=screen.blit(tube2,(X_tube2,0))
    tube3_draw=screen.blit(tube3,(X_tube3,0))
    tubeop1_draw=screen.blit(tubeop1,(X_tubeop1,Y_tubeop1))
    tubeop2_draw=screen.blit(tubeop2,(X_tubeop2,Y_tubeop2))
    tubeop3_draw=screen.blit(tubeop3,(X_tubeop3,Y_tubeop3))
    

    degree=0

    for i in range(gen_pop):
        ima=pygame.transform.rotate(bird, degree)
        image.append(ima)
    # for i in range(gen_pop):
    #     if pausing[i] == False:
    for i in range(gen_pop):
        if pausing[i] == False:
             
            rank_bird[i][0] +=1       
    for i in range(gen_pop):
        if pausing[i] == False:
            if 140<X_tube1<=500-5:
                Y_tube = Y_tube1
                X_tube = X_tube1
            elif 140<X_tube2<=500-5:
                Y_tube = Y_tube2
                X_tube = X_tube2
            elif 140<X_tube3 <= 500-5:
                Y_tube = Y_tube3
                X_tube = X_tube3
            pygame.draw.line(screen,Color_line,(230,Y_bird[i]),(X_tube,Y_tube),width=1)
            pygame.draw.line(screen,Color_line,(230,Y_bird[i]+50),(X_tube,Y_tube+170),width=1)
            
            brain_bird[i].input(Y_tube,Y_tube+170,Y_bird[i]+25)
            try:
                jump = brain_bird[i].output()
                if 0.5<=jump<1:
                    Y_bird_change = -50
            except:
                pass
            Y_bird[i] +=Y_bird_change
            Y_bird_change=2**3
            bird_draw=screen.blit(image[i],(X_bird,Y_bird[i]))
            pipes=[tube1_draw,tube2_draw,tube3_draw,tubeop1_draw,tubeop2_draw,tubeop3_draw]
            for pipe in pipes:
                if bird_draw.colliderect(pipe):                      
                    pausing[i]=True
    tube1 = pygame.image.load('tube.png')
    tube1 =pygame.transform.scale(tube1,(50,Y_tube1))
    tube2 = pygame.image.load('tube.png')
    tube2 =pygame.transform.scale(tube2,(50,Y_tube2))
    tube3 = pygame.image.load('tube.png')
    tube3 =pygame.transform.scale(tube3,(50,Y_tube3))
    tubeop1 = pygame.image.load('tupeop.jpg')
    tubeop1 =pygame.transform.scale(tubeop1,(50,630-Y_tubeop1))
    tubeop2 = pygame.image.load('tupeop.jpg')
    tubeop2 =pygame.transform.scale(tubeop2,(50,630-Y_tubeop2))
    tubeop3 = pygame.image.load('tupeop.jpg')
    tubeop3 =pygame.transform.scale(tubeop3,(50,630-Y_tubeop3))
    #cập nhật vị trí của land 
    if X_land1<=-500:
        X_land1=1000
    if X_land2<=-500:
        X_land2=1000
    if X_land3<=-500:
        X_land3=1000 
    #cập nhật vị trí của tube
    if X_tube1<=0:
        X_tube1=1000
        Y_tube1=random.randint(100,450)
        tube1 = pygame.image.load('tube.png')
        tube1 =pygame.transform.scale(tube1,(50,Y_tube1))
    if X_tube2<=0:
        X_tube2=1000
        Y_tube2=random.randint(100,450)
        tube2 = pygame.image.load('tube.png')
        tube2 =pygame.transform.scale(tube2,(50,Y_tube2))
    if X_tube3<=0:
        X_tube3=1000
        Y_tube3=random.randint(100,450)
        tube3 = pygame.image.load('tube.png')
        tube3 =pygame.transform.scale(tube3,(50,Y_tube3))
    if X_tubeop1<=0:
        X_tubeop1=1000
        Y_tubeop1=(Y_tube1+170)
        tubeop1 = pygame.image.load('tupeop.jpg')
        tubeop1 =pygame.transform.scale(tubeop1,(50,630-Y_tubeop1))
    

    if X_tubeop2<=0:
        X_tubeop2=1000
        Y_tubeop2=(Y_tube2+170)
        tubeop2 = pygame.image.load('tupeop.jpg')
        tubeop2 =pygame.transform.scale(tubeop2,(50,630-Y_tubeop2))
    

    if X_tubeop3<=0:
        X_tubeop3=1000
        Y_tubeop3=(Y_tube3+170)
        tubeop3 = pygame.image.load('tupeop.jpg')
        tubeop3 =pygame.transform.scale(tubeop3,(50,630-Y_tubeop3))
    if X_tube1==200 or X_tube2==200 or X_tube3==200:
        for i in range(gen_pop):
            if pausing[i] == False:
                score[i]+=1
                rank_bird[i][1]+=1
    
    for i in range(gen_pop):
        if Y_bird[i] > 600 or Y_bird[i]<0:
            pausing[i] = True
    population = gen_pop
    for i in range(gen_pop):
        if pausing[i]:
            population -= 1

    # game over
    if population <= 0:
        X_land_change=0
        X_tube_change=0
        Y_bird_change=3**2
        best_score = max(score)
        max_score = max(max_score,best_score)
        gameover_txt=fontgameover.render("Game over",True,WHITE)
        screen.blit(gameover_txt,(100,60))
        score_txt=font_score.render(str(best_score),True,WHITE)
        screen.blit(score_txt,(250,160)) 
 
    
    
    score_txt=font.render("Score:"+str(max(score)),True,WHITE)
    screen.blit(score_txt,(350,5))
    score_txt=font.render("Score Max:"+str(max_score),True,WHITE)
    screen.blit(score_txt,(320,30))
    alive_txt=font.render("Alive:"+str(population),True,WHITE)
    screen.blit(alive_txt,(5,30))
    gen_txt=font.render("Gens:"+str(count_gens),True,WHITE)
    screen.blit(gen_txt,(5,5))
    pygame.display.flip()   
    pygame.display.update() 