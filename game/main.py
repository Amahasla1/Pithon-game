from enemy import Enemy
from turret import Turret
from locks import Lock
from medic_bag import Medic_bag
from doors import Door
from wall import Wall
from player import Player
from bullet import Bullet
from shooting_enemy import Shooting_Enemy
from golden_key import Golden_key
import random
import tkinter as tk
import threading

class Game:
    def __init__(self, root):
        self.root = root
        self.golden_key_j=-1
        self.golden_key_i=-1
        self.boss_i=0
        self.boss_j=-1
        self.room_x=2
        self.room_y=2
        self.canvas_int = tk.Canvas(root, width = 600, height = 150, bg = "grey")
        self.canvas_int.pack()
        self.canvas =tk.Canvas(root, width = 600, height = 600, bg = "black")
        self.canvas.pack()
        self.player = Player(self.canvas, 300, 300)
        self.health_bar = self.canvas_int.create_text(300, 25, text = f"Здоровье: {self.player.health}", font =("Arial", 14), fill = "black")

        self.map = [[],[],[],[],[]]
        self.range_map = [[],[],[],[],[]]
        self.enemy_map = [[],[],[],[],[]]
        self.enemies = []
        self.turrets=[]
        self.snake_boss = []
        self.snake_boss_room=[[300,300]]
        self.enemy_room=[
            [15,15],
            [580,580],
            [15,580],
            [580,15]
        ]
        self.doors=[
            Door(self.canvas,0,275,5,325),
            Door(self.canvas,598,275,600,325),
            Door(self.canvas,275,0,325,5),
            Door(self.canvas,275,598,325,600),

        ]
        self.locks=[]

        self.walls = [
            #края
            Wall(self.canvas, 0, 0, 275,8),
            Wall(self.canvas,  325, 0, 600,8),
            Wall(self.canvas, 0, 0, 8,275),
            Wall(self.canvas, 0, 325, 8,600),
            Wall(self.canvas, 0, 592, 275,600),
            Wall(self.canvas, 325, 592, 600,600),
            Wall(self.canvas, 592, 0, 600,275),
            Wall(self.canvas, 592, 325, 600,600),
            #2вертик
            Wall(self.canvas, 288, 50, 312,250),
            Wall(self.canvas, 288, 350, 312, 550),
            #2горизонт
            Wall(self.canvas,  50,288,250,312),
            Wall(self.canvas,  350, 288, 550,312),

        ]
        self.block_r_door=[592,0,600,600]
        self.block_l_door=[0,0,9,600]
        self.block_u_door=[0,0,600,9]
        self.block_d_door=[0,592,600,600]
        self.room1=[
            [0, 0, 275,8],
            [ 325, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 275,600],
            [325, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [288, 50, 312,250],
            [288, 350, 312, 550],
            [50,288,250,312],
            [350, 288, 550,312],
        ]
        self.room2=[
            [0, 0, 275,8],
            [ 325, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 275,600],
            [325, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [288, 50, 312,250],
            [288, 350, 312, 550],
        ]
        self.room3=[
            [0, 0, 275,8],
            [ 325, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 275,600],
            [325, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [50,288,250,312],
            [350, 288, 550,312],
        ]
        self.room4=[
            [0, 0, 275,8],
            [ 325, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 275,600],
            [325, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [288, 350, 312, 550],
            [350, 288, 550,312],
        ]
        self.room5=[
            [0, 0, 275,8],
            [ 325, 0, 600,8],
            [0, 0, 8,275],
            [0, 325, 8,600],
            [0, 592, 275,600],
            [325, 592, 600,600],
            [592, 0, 600,275],
            [592, 325, 600,600],
            [288, 50, 312,250],
            [50,288,250,312],
        ]

        self.medic_bags=[]
        self.golden_keys=[]
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.update_movement()
        self.create_map()



    def create_map(self):
        room_counter=0
        self.map
        for i in range(0,5):
            for j in range(0,5):
                self.map[i].append(0)
        self.map[2][2]=1
        while room_counter <=8 :
            for i in range(0,5):
                for j in range(0,5):
                    if self.map[i][j]!=0:
                        if j!=4 and self.map[i][j+1]==0 and (i==4 or (self.map[i+1][j+1]==0)) and (i==0 or (self.map[i-1][j+1]==0)):
                            chance=random.randint(0,5)
                            if chance==3:
                                self.map[i][j+1]=random.randint(2,5)
                                room_counter+=1
                                pass
                            else:
                                chance=0
                        if i!=4 and self.map[i+1][j]==0 and (j==4 or (self.map[i+1][j+1]==0)) and (j==0 or (self.map[i+1][j-1]==0)) and chance==0:
                            chance=random.randint(0,5)
                            if chance==3:
                                self.map[i+1][j]=random.randint(2,5)
                                room_counter+=1
                                pass
                            else:
                                chance=0
                        if  j!=0 and self.map[i][j-1]==0 and (i==4 or (self.map[i+1][j-1]==0)) and (i==0 or (self.map[i-1][j-1]==0)) and chance==0:
                            chance=random.randint(0,5)
                            if chance==3:
                                self.map[i][j-1]=random.randint(2,5)
                                room_counter+=1
                                pass
                            else:
                                chance=0
                        if i!=0 and self.map[i-1][j]==0 and (j==4 or (self.map[i-1][j+1]==0)) and (j==0 or (self.map[i-1][j-1]==0)) and chance==0:
                            chance=random.randint(0,5)
                            if chance==3:
                                self.map[i-1][j]=random.randint(2,5)
                                room_counter+=1
                                pass
                            else:
                                chance=0
                        chance=0
        chance=1

        for i in range(0,5):
            for j in range(0,5):
                self.range_map[j].append(0)
        for i in range(0,5):
            for j in range(0,5):
                if self.map[i][j]!=0:
                    self.range_map[i][j]=1
        self.range_map[2][2]=2
        k=2
        e=1
        while e!=0:
            e=0
            for i in range(0,5):
                for j in range(0,5):
                    if self.range_map[i][j]==k:
                        if j!=4 and self.range_map[i][j+1]==1:
                            self.range_map[i][j+1]=(k+1)
                            e=1
                        if j!=0 and self.range_map[i][j-1]==1:
                            self.range_map[i][j-1]=(k+1)
                            e=1
                        if i!=4 and self.range_map[i+1][j]==1:
                            self.range_map[i+1][j]=(k+1)
                            e=1
                        if i!=0 and self.range_map[i-1][j]==1:
                            self.range_map[i-1][j]=(k+1)
                            e=1
            print(k)
            k=k+1

        print(self.range_map[0])
        print(self.range_map[1])
        print(self.range_map[2])
        print(self.range_map[3])
        print(self.range_map[4])
        print()

        while self.boss_j==-1:
            for i in range(0,5):
                    for j in range(0,5):
                        if self.map[i][j]==0:
                            self.enemy_map[i].append(0)
                        else:
                            self.enemy_map[i].append(1)
                            if self.range_map[i][j]==k and ((i!=0 and self.map[i-1][j]!=0 and ((i==4 or self.map[i+1][j]==0) and (j==0 or self.map[i][j-1]==0) and (j==4 or self.map[i][j+1]==0)))or(i!=4 and self.map[i+1][j]!=0 and ((i==0 or self.map[i-1][j]==0) and (j==0 or self.map[i][j-1]==0) and (j==4 or self.map[i][j+1]==0)))or(j!=0 and self.map[i][j-1]!=0 and ((i==0 or self.map[i-1][j]==0) and (i==4 or self.map[i+1][j]==0) and (j==4 or self.map[i][j+1]==0)))or(j!=4 and self.map[i][j+1]!=0 and ((i==0 or self.map[i-1][j]==0) and (i==4 or self.map[i+1][j]==0) and (j==0 or self.map[i][j-1]==0)))):
                                if chance==1:
                                    self.boss_j=j
                                    self.boss_i=i
                                chance=random.randint(0,1)
            k=k-1
        self.map[self.boss_i][self.boss_j]=6
        chance=1
        for i in range(0,5):
                    for j in range(0,5):
                        if self.map[i][j]!=0 and self.map[i][j]!=6 and (i!=2 and i!=2):
                            if chance==1:
                                    self.golden_key_j=j
                                    self.golden_key_i=i
                            chance=random.randint(0,1)
        print(self.golden_key_j)
        print(self.golden_key_i)
        print()
        print(self.boss_j)
        print(self.boss_i)

        self.enemy_map[self.boss_i][self.boss_j]=2
            
        print(self.map[0])
        print(self.map[1])
        print(self.map[2])
        print(self.map[3])
        print(self.map[4])

        self.current_room=self.map[self.room_y][self.room_x]
        self.block_door()
        self.create_mini_map()
        self.block_room()



    def create_mini_map(self):
        self.canvas_int.create_rectangle(0, 0, 150, 150, fill = "black", outline= 'black', width=1)
        for i in range(0,5):
                for j in range(0,5):
                    if self.map[i][j]!=0:
                        self.canvas_int.create_rectangle(30*j, 30*i, 30*(j+1), 30*(i+1), fill = "grey", outline= 'black', width=1)
        self.canvas_int.create_rectangle(30*self.boss_j, 30*self.boss_i, 30*(self.boss_j+1), 30*(self.boss_i+1), fill = "grey", outline= 'red', width=1)
        self.mini_map=self.canvas_int.create_rectangle(30*self.room_x, 30*self.room_y, 30*(self.room_x+1), 30*(self.room_y+1), fill = "grey", outline= 'green', width=1)
        




    def key_press(self, event):
        key = event.keysym.lower()
        if key in ("w", "a", "s", "d","left","up","down","right"):
            self.player.keys_pressed.add(key)

    def key_release(self, event):
        key = event.keysym.lower()
        self.player.keys_pressed.discard(key)

    def update_movement(self):
        player_coords = self.canvas.coords(self.player.rect)
        for key in self.player.keys_pressed:
            if key == "w" :
                self.move_player(0, -4)
            elif key == "s":
                self.move_player(0, 4)
            elif key == "a":
                self.move_player(-4, 0)
            elif key == "d":
                self.move_player(4, 0)
            elif key == "up":
                self.use_sword(player_coords[0],player_coords[1]-20,player_coords[2],player_coords[3]-20)
            elif key == "down":
                self.use_sword(player_coords[0],player_coords[1]+20,player_coords[2],player_coords[3]+20)
            elif key == "left":
                self.use_sword(player_coords[0]-20,player_coords[1],player_coords[2]-20,player_coords[3])
            elif key == "right":
                self.use_sword(player_coords[0]+20,player_coords[1],player_coords[2]+20,player_coords[3])
            if len(self.enemies)==0 and len(self.snake_boss)==0:
                self.enemy_map[self.room_y][self.room_x]=0
                for wall in self.walls:
                    self.canvas.delete(wall.rect)
                self.walls.clear()
                self.block_door()
                if self.current_room==1 or self.current_room==6:
                    for wall in self.room1:
                        x1=wall[0]
                        y1=wall[1]
                        x2=wall[2]
                        y2=wall[3]
                        self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                elif self.current_room==2:
                    for wall in self.room2:
                        x1=wall[0]
                        y1=wall[1]
                        x2=wall[2]
                        y2=wall[3]
                        self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                elif self.current_room==3:
                    for wall in self.room3:
                        x1=wall[0]
                        y1=wall[1]
                        x2=wall[2]
                        y2=wall[3]
                        self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                elif self.current_room==4:
                    for wall in self.room4:
                        x1=wall[0]
                        y1=wall[1]
                        x2=wall[2]
                        y2=wall[3]
                        self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                elif self.current_room==5:
                    for wall in self.room5:
                        x1=wall[0]
                        y1=wall[1]
                        x2=wall[2]
                        y2=wall[3]
                        self.walls.append(Wall(self.canvas,x1,y1,x2,y2))

        self.enemy_chase()
        self.snake_boss_chase()
        self.root.after(16, self.update_movement)
        self.check_enemy_collision()
        self.check_snake_collision()
        self.check_bullet_collision() 

    def enemy_chase(self):
        player_coords = self.canvas.coords(self.player.rect)
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy.rect)
            if player_coords[0]==enemy_coords[0]:
                enemy.dx=0
                enemy.ddx=0
            elif player_coords[0]<enemy_coords[0]:
                enemy.dx=-3
                enemy.ddx=player_coords[0]-enemy_coords[0]
            elif player_coords[0]>enemy_coords[0]:
                enemy.dx=3
                enemy.ddx=player_coords[0]-enemy_coords[0]
            if player_coords[1]==enemy_coords[1]:
                enemy.dy=0
                enemy.ddy=0
            elif player_coords[1]<enemy_coords[1]:
                enemy.dy=-3
                enemy.ddy=player_coords[1]-enemy_coords[1]
            elif player_coords[1]>enemy_coords[1]:
                enemy.dy=3
                enemy.ddy=player_coords[1]-enemy_coords[1]
        for enemy in self.turrets:
            enemy_coords = self.canvas.coords(enemy.rect)
            if player_coords[0]==enemy_coords[0]:
                enemy.dx=0
                enemy.ddx=0
            elif player_coords[0]<enemy_coords[0]:
                enemy.dx=-3
                enemy.ddx=player_coords[0]-enemy_coords[0]
            elif player_coords[0]>enemy_coords[0]:
                enemy.dx=3
                enemy.ddx=player_coords[0]-enemy_coords[0]
            if player_coords[1]==enemy_coords[1]:
                enemy.dy=0
                enemy.ddy=0
            elif player_coords[1]<enemy_coords[1]:
                enemy.dy=-3
                enemy.ddy=player_coords[1]-enemy_coords[1]
            elif player_coords[1]>enemy_coords[1]:
                enemy.dy=3
                enemy.ddy=player_coords[1]-enemy_coords[1]
    
    def snake_boss_chase(self):
        if len(self.snake_boss)!=0:
            player_coords = self.canvas.coords(self.player.rect)
            snake_head1_coords = self.canvas.coords(self.snake_boss[0].rect)
            if player_coords[0]==snake_head1_coords[0]:
                self.snake_boss[0].dx=0
                self.snake_boss[0].ddx=0
            elif player_coords[0]<snake_head1_coords[0]:
                self.snake_boss[0].dx=-3
                self.snake_boss[0].ddx=player_coords[0]-snake_head1_coords[0]
            elif player_coords[0]>snake_head1_coords[0]:
                self.snake_boss[0].dx=3
                self.snake_boss[0].ddx=player_coords[0]-snake_head1_coords[0]
            if player_coords[1]==snake_head1_coords[1]:
                self.snake_boss[0].dy=0
                self.snake_boss[0].ddy=0
            elif player_coords[1]<snake_head1_coords[1]:
                self.snake_boss[0].dy=-3
                self.snake_boss[0].ddy=player_coords[1]-snake_head1_coords[1]
            elif player_coords[1]>snake_head1_coords[1]:
                self.snake_boss[0].dy=3
                self.snake_boss[0].ddy=player_coords[1]-snake_head1_coords[1]

            for i in range(1,(len(self.snake_boss))) :
                snake_head_coords=self.canvas.coords(self.snake_boss[i-1].rect)
                snake_body_coords=self.canvas.coords(self.snake_boss[i].rect)
                if snake_head_coords[0]==snake_body_coords[0]:
                    self.snake_boss[i].dx=0
                    self.snake_boss[i].ddx=0
                elif snake_head_coords[0]<snake_body_coords[0]:
                    self.snake_boss[i].dx=-3
                    self.snake_boss[i].ddx=snake_head_coords[0]-snake_body_coords[0]
                elif snake_head_coords[0]>snake_body_coords[0]:
                    self.snake_boss[i].dx=3
                    self.snake_boss[i].ddx=snake_head_coords[0]-snake_body_coords[0]
                if snake_head_coords[1]==snake_body_coords[1]:
                    self.snake_boss[i].dy=0
                    self.snake_boss[i].ddy=0
                elif snake_head_coords[1]<snake_body_coords[1]:
                    self.snake_boss[i].dy=-3
                    self.snake_boss[i].ddy=snake_head_coords[1]-snake_body_coords[1]
                elif snake_head_coords[1]>snake_body_coords[1]:
                    self.snake_boss[i].dy=3
                    self.snake_boss[i].ddy=snake_head_coords[1]-snake_body_coords[1]
                
                """if abs(snake_head_coords[0]-snake_body_coords[0])>5:
                    if player_coords[0]==snake_body_coords[0]:
                        self.snake_boss[0].dx=0
                        self.snake_boss[0].ddx=0
                    elif player_coords[0]<snake_body_coords[0]:
                        self.snake_boss[0].dx=-3
                        self.snake_boss[0].ddx=player_coords[0]-snake_body_coords[0]
                    elif player_coords[0]>snake_body_coords[0]:
                        self.snake_boss[0].dx=3
                        self.snake_boss[0].ddx=player_coords[0]-snake_body_coords[0]
                    if player_coords[1]==snake_body_coords[1]:
                        self.snake_boss[0].dy=0
                        self.snake_boss[0].ddy=0
                    elif player_coords[1]<snake_body_coords[1]:
                        self.snake_boss[0].dy=-3
                        self.snake_boss[0].ddy=player_coords[1]-snake_body_coords[1]
                    elif player_coords[1]>snake_body_coords[1]:
                        self.snake_boss[0].dy=3
                        self.snake_boss[0].ddy=player_coords[1]-snake_body_coords[1]"""


    def check_enemy_collision(self):
        player_coords = self.canvas.coords(self.player.rect)
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy.rect)
            for wall in self.walls:
                wall_coords = self.canvas.coords(wall.rect)
                if (enemy_coords[2] > wall_coords[0] and enemy_coords[0] < wall_coords[2] and
                    enemy_coords[3] > wall_coords[1] and enemy_coords[1] < wall_coords[3]):
                    if enemy_coords[0] < wall_coords[0]:
                        enemy.dx-=7
                    if enemy_coords[1] > wall_coords[1]:
                        enemy.dy+=7
                    if enemy_coords[2] > wall_coords[2]:
                        enemy.dx+=7
                    if enemy_coords[3] < wall_coords[3]:
                        enemy.dy-=7
                if (player_coords[2] > enemy_coords[0] and player_coords[0] < enemy_coords[2] and player_coords[3] > enemy_coords[1] and player_coords[1] < enemy_coords[3]):
                    self.player.health -= 0.1
                    self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: {int(self.player.health)}")
                    if self.player.health <= 0:
                        self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: 0")
                        self.game_over()
    
    def check_snake_collision(self):
        player_coords = self.canvas.coords(self.player.rect)
        for wall in self.walls:
                wall_coords = self.canvas.coords(wall.rect)
                for snake_boss in self.snake_boss:
                    snake_boss_coords = self.canvas.coords(snake_boss.rect)     
                    if (snake_boss_coords[2] > wall_coords[0] and snake_boss_coords[0] < wall_coords[2] and
                            snake_boss_coords[3] > wall_coords[1] and snake_boss_coords[1] < wall_coords[3]):
                            if snake_boss_coords[0] < wall_coords[0]:
                                snake_boss.dx-=7
                            if snake_boss_coords[1] > wall_coords[1]:
                                snake_boss.dy+=7
                            if snake_boss_coords[2] > wall_coords[2]:
                                snake_boss.dx+=7
                            if snake_boss_coords[3] < wall_coords[3]:
                               snake_boss.dy-=7
                
                    if (player_coords[2] > snake_boss_coords[0] and player_coords[0] < snake_boss_coords[2] and player_coords[3] > snake_boss_coords[1] and player_coords[1] < snake_boss_coords[3]):
                        self.player.health -= 0.1
                        self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: {int(self.player.health)}")
                        if self.player.health <= 0:
                            self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: 0")
                            self.game_over()

    def use_sword(self, x1, y1,x2,y2):
        chance=random.randint(0,6)
        if chance==1:
            sword=self.canvas.create_rectangle(x1, y1, x2, y2, fill = "pink", outline= 'grey', width=0)
            atk=2
        else:
            sword=self.canvas.create_rectangle(x1, y1, x2, y2, fill = "blue", outline= 'grey', width=0)
            atk=1
        for enemy in self.enemies:
            enemy_coords = self.canvas.coords(enemy.rect)
            if enemy.health==0 or enemy.health==-1:
                self.medic_bags.append(Medic_bag(self.canvas,enemy_coords[0]+5,enemy_coords[1]+5))
                self.enemies.remove(enemy)
                self.canvas.delete(enemy.rect)
            if (enemy_coords[2] > x1 and enemy_coords[0] < x2 and
                enemy_coords[3] > y1 and enemy_coords[1] < y2):
                
                if enemy_coords[0] < x1:
                    enemy.health-=atk
                    
                elif enemy_coords[1] > y1:
                    enemy.health-=atk
                    
                elif enemy_coords[2] > x2:
                    enemy.health-=atk
                    
                elif enemy_coords[3] < y2:
                    enemy.health-=atk

        for enemy in self.snake_boss:
            enemy_coords = self.canvas.coords(enemy.rect)
            if enemy.health==0 or enemy.health==-1 :
                self.medic_bags.append(Medic_bag(self.canvas,enemy_coords[0]+5,enemy_coords[1]+5))
                self.snake_boss.remove(enemy)
                self.canvas.delete(enemy.rect)
            if (enemy_coords[2] > x1 and enemy_coords[0] < x2 and
                enemy_coords[3] > y1 and enemy_coords[1] < y2):
                if enemy_coords[0] < x1:
                    enemy.health-=atk
                    
                elif enemy_coords[1] > y1:
                    enemy.health-=atk
                    
                elif enemy_coords[2] > x2:
                    enemy.health-=atk
                    
                elif enemy_coords[3] < y2:
                    enemy.health-=atk

        def del_sword():
                self.canvas.delete(sword)
        timer = threading.Timer(0.01, del_sword)
        timer.start()

    def block_room(self):
        if self.enemy_map[self.room_y][self.room_x]==1 or self.enemy_map[self.room_y][self.room_x]==2:
            x1=self.block_r_door[0]
            y1=self.block_r_door[1]
            x2=self.block_r_door[2]
            y2=self.block_r_door[3]
            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
            x1=self.block_l_door[0]
            y1=self.block_l_door[1]
            x2=self.block_l_door[2]
            y2=self.block_l_door[3]
            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
            x1=self.block_u_door[0]
            y1=self.block_u_door[1]
            x2=self.block_u_door[2]
            y2=self.block_u_door[3]
            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
            x1=self.block_d_door[0]
            y1=self.block_d_door[1]
            x2=self.block_d_door[2]
            y2=self.block_d_door[3]
            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))

    def block_door(self):
        if self.room_x==4 or self.map[self.room_y][self.room_x+1]==0:
                            x1=self.block_r_door[0]
                            y1=self.block_r_door[1]
                            x2=self.block_r_door[2]
                            y2=self.block_r_door[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
        if self.room_x==0 or self.map[self.room_y][self.room_x-1]==0: 
                            x1=self.block_l_door[0]
                            y1=self.block_l_door[1]
                            x2=self.block_l_door[2]
                            y2=self.block_l_door[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
        if self.room_y==4 or self.map[self.room_y+1][self.room_x]==0:
                            x1=self.block_d_door[0]
                            y1=self.block_d_door[1]
                            x2=self.block_d_door[2]
                            y2=self.block_d_door[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
        if self.room_y==0 or self.map[self.room_y-1][self.room_x]==0:
                            x1=self.block_u_door[0]
                            y1=self.block_u_door[1]
                            x2=self.block_u_door[2]
                            y2=self.block_u_door[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
        if self.room_x!=4 and self.map[self.room_y][self.room_x+1]==6:
            x1=593
            y1=275
            x2=600
            y2=325
            self.locks.append(Lock(self.canvas,x1,y1,x2,y2))
        if self.room_x!=0 and self.map[self.room_y][self.room_x-1]==6:
            x1=0
            y1=275
            x2=9
            y2=325
            self.locks.append(Lock(self.canvas,x1,y1,x2,y2))
        if self.room_y!=4 and self.map[self.room_y+1][self.room_x]==6:
            x1=275
            y1=593
            x2=325
            y2=600
            self.locks.append(Lock(self.canvas,x1,y1,x2,y2))
        if self.room_y!=0 and self.map[self.room_y-1][self.room_x]==6:
            x1=275
            y1=0
            x2=325
            y2=8
            self.locks.append(Lock(self.canvas,x1,y1,x2,y2))

    def move_player(self, dx, dy):
        self.canvas.move(self.player.rect, dx, dy)
        if self.check_collision():
            self.canvas.move(self.player.rect, -dx, -dy)

    def update_room(self):
        player_coords=self.canvas.coords(self.player.rect)
        
        for door in self.doors:
            door_coords = self.canvas.coords(door.rect)
            if (player_coords[2] > door_coords[0] and player_coords[0] < door_coords[2] and
                player_coords[3] > door_coords[1] and player_coords[1] < door_coords[3]):
                    #левая
                if player_coords[0] < 100:
                    self.move_player(560,0)
                    self.room_x=self.room_x-1
                    self.current_room=self.map[self.room_y][self.room_x]
                    for turret in self.turrets:
                        self.canvas.delete(turret.rect)
                    for lock in self.locks:
                        self.canvas.delete(lock.rect)
                    for wall in self.walls:
                        self.canvas.delete(wall.rect)
                    for medic_bag in self.medic_bags:
                        self.canvas.delete(medic_bag.rect)
                    for bullet in Bullet.bullets:
                        self.canvas.delete(bullet.oval)
                    for enemy in self.enemies:
                        self.canvas.delete(enemy.rect)
                    self.turrets.clear()
                    self.locks.clear()
                    self.walls.clear()
                    self.enemies.clear()
                    self.medic_bags.clear()
                    Bullet.bullets.clear()
                    self.block_door()
                    self.block_room()
                    if self.room_y==self.golden_key_i and self.room_x==self.golden_key_j and self.player.golden_key==0:
                        self.golden_keys.append(Golden_key(self.canvas,300,300))
                    else:
                        for golden_key in self.golden_keys:
                            self.canvas.delete(golden_key.rect)
                        self.golden_keys.clear()
                    if self.current_room==1:
                        for wall in self.room1:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==2:
                        for wall in self.room2:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==3:
                        for wall in self.room3:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==4:
                        for wall in self.room4:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==5:
                        for wall in self.room5:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==6:
                        for wall in self.room1:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    if self.enemy_map[self.room_y][self.room_x]==1:
                        for enemy in self.enemy_room:
                            x=enemy[0]
                            y=enemy[1]
                            i=random.randint(0,1)
                            if i==0:
                                self.enemies.append(Enemy(self.canvas,x,y))
                            else:
                                self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                        xi=50
                        xj=50
                        self.turrets.append(Turret(self.canvas,xi,xj))
                    if self.enemy_map[self.room_y][self.room_x]==2:
                        self.block_room()
                        for snake_boss in self.snake_boss_room:
                            x=snake_boss[0]
                            y=snake_boss[1]
                            for i in range(150):
                                self.snake_boss.append(Enemy(self.canvas,x,y))
                    self.canvas_int.delete(self.mini_map)
                    self.mini_map=self.canvas_int.create_rectangle(30*self.room_x, 30*self.room_y, 30*(self.room_x+1), 30*(self.room_y+1), fill = "grey", outline= 'green', width=1)   
                    #правая
                    
                if player_coords[2] > 500:
                    self.move_player( -560,0)
                    self.room_x=self.room_x+1
                    self.current_room=self.map[self.room_y][self.room_x]
                    for turret in self.turrets:
                        self.canvas.delete(turret.rect)
                    for lock in self.locks:
                        self.canvas.delete(lock.rect)
                    for wall in self.walls:
                        self.canvas.delete(wall.rect)
                    for medic_bag in self.medic_bags:
                        self.canvas.delete(medic_bag.rect)
                    for bullet in Bullet.bullets:
                        self.canvas.delete(bullet.oval)
                    for enemy in self.enemies:
                        self.canvas.delete(enemy.rect)
                    self.turrets.clear()
                    self.walls.clear()
                    self.enemies.clear()
                    self.medic_bags.clear()
                    self.locks.clear()
                    Bullet.bullets.clear()
                    self.block_door()
                    self.block_room()
                    if self.room_y==self.golden_key_i and self.room_x==self.golden_key_j and self.player.golden_key==0:
                        self.golden_keys.append(Golden_key(self.canvas,300,300))
                    else:
                        for golden_key in self.golden_keys:
                            self.canvas.delete(golden_key.rect)
                        self.golden_keys.clear()
                    if self.current_room==1 or self.current_room==6:
                        for wall in self.room1:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==2:
                        for wall in self.room2:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==3:
                        for wall in self.room3:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==4:
                        for wall in self.room4:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==5:
                        for wall in self.room5:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==6:
                        for wall in self.room1:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    if self.enemy_map[self.room_y][self.room_x]==1:
                        for enemy in self.enemy_room:
                            x=enemy[0]
                            y=enemy[1]
                            i=random.randint(0,1)
                            if i==0:
                                self.enemies.append(Enemy(self.canvas,x,y))
                            else:
                                self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                        xi=50
                        xj=50
                        self.turrets.append(Turret(self.canvas,xi,xj))
                    if self.enemy_map[self.room_y][self.room_x]==2:
                        self.block_room()
                        for snake_boss in self.snake_boss_room:
                            x=snake_boss[0]
                            y=snake_boss[1]
                            for i in range(150):
                                self.snake_boss.append(Enemy(self.canvas,x,y))
                    self.canvas_int.delete(self.mini_map)
                    self.mini_map=self.canvas_int.create_rectangle(30*self.room_x, 30*self.room_y, 30*(self.room_x+1), 30*(self.room_y+1), fill = "grey", outline= 'green', width=1)

                #верхняя

                if player_coords[1] < 100:
                    self.move_player( 0,560)
                    self.room_y=self.room_y-1
                    self.current_room=self.map[self.room_y][self.room_x]
                    for turret in self.turrets:
                        self.canvas.delete(turret.rect)
                    for lock in self.locks:
                        self.canvas.delete(lock.rect)
                    for wall in self.walls:
                        self.canvas.delete(wall.rect)
                    for medic_bag in self.medic_bags:
                        self.canvas.delete(medic_bag.rect)
                    for bullet in Bullet.bullets:
                        self.canvas.delete(bullet.oval)
                    for enemy in self.enemies:
                        self.canvas.delete(enemy.rect)
                    self.turrets.clear()
                    self.walls.clear()
                    self.enemies.clear()
                    self.locks.clear()
                    self.medic_bags.clear()
                    Bullet.bullets.clear()
                    self.block_door()
                    self.block_room()
                    if self.room_y==self.golden_key_i and self.room_x==self.golden_key_j and self.player.golden_key==0:
                        self.golden_keys.append(Golden_key(self.canvas,300,300))
                    else:
                        for golden_key in self.golden_keys:
                            self.canvas.delete(golden_key.rect)
                        self.golden_keys.clear()
                    if self.current_room==1 or self.current_room==6:
                        for wall in self.room1:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==2:
                        for wall in self.room2:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==3:
                        for wall in self.room3:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==4:
                        for wall in self.room4:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==5:
                        for wall in self.room5:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==6:
                        for wall in self.room1:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    if self.enemy_map[self.room_y][self.room_x]==1:
                        for enemy in self.enemy_room:
                            x=enemy[0]
                            y=enemy[1]
                            i=random.randint(0,1)
                            if i==0:
                                self.enemies.append(Enemy(self.canvas,x,y))
                            else:
                                self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                        xi=50
                        xj=50
                        self.turrets.append(Turret(self.canvas,xi,xj))
                    if self.enemy_map[self.room_y][self.room_x]==2:
                        self.block_room()
                        for snake_boss in self.snake_boss_room:
                            x=snake_boss[0]
                            y=snake_boss[1]
                            for i in range(150):
                                self.snake_boss.append(Enemy(self.canvas,x,y))
                    self.canvas_int.delete(self.mini_map)
                    self.mini_map=self.canvas_int.create_rectangle(30*self.room_x, 30*self.room_y, 30*(self.room_x+1), 30*(self.room_y+1), fill = "grey", outline= 'green', width=1)


                #нижняя

                if player_coords[3] > 500:
                    self.move_player( 0,-560)
                    self.room_y=self.room_y+1
                    self.current_room=self.map[self.room_y][self.room_x]
                    for turret in self.turrets:
                        self.canvas.delete(turret.rect)
                    for lock in self.locks:
                        self.canvas.delete(lock.rect)
                    for wall in self.walls:
                        self.canvas.delete(wall.rect)
                    for medic_bag in self.medic_bags:
                        self.canvas.delete(medic_bag.rect)
                    for bullet in Bullet.bullets:
                        self.canvas.delete(bullet.oval)
                    for enemy in self.enemies:
                        self.canvas.delete(enemy.rect)
                    self.turrets.clear()
                    self.walls.clear()
                    self.enemies.clear()
                    self.locks.clear() 
                    self.medic_bags.clear()
                    Bullet.bullets.clear()
                    self.block_door()
                    self.block_room()
                    if self.room_y==self.golden_key_i and self.room_x==self.golden_key_j and self.player.golden_key==0:
                        self.golden_keys.append(Golden_key(self.canvas,300,300))
                    else:
                        for golden_key in self.golden_keys:
                            self.canvas.delete(golden_key.rect)
                        self.golden_keys.clear()
                    if self.current_room==1 or self.current_room==6:
                        for wall in self.room1:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==2:
                        for wall in self.room2:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==3:
                        for wall in self.room3:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==4:
                        for wall in self.room4:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==5:
                        for wall in self.room5:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2))
                    elif self.current_room==6:
                        for wall in self.room1:
                            x1=wall[0]
                            y1=wall[1]
                            x2=wall[2]
                            y2=wall[3]
                            self.walls.append(Wall(self.canvas,x1,y1,x2,y2)) 
                    if self.enemy_map[self.room_y][self.room_x]==1:
                        for enemy in self.enemy_room:
                            x=enemy[0]
                            y=enemy[1]
                            i=random.randint(0,1)
                            if i==0:
                                self.enemies.append(Enemy(self.canvas,x,y))
                            else:
                                self.enemies.append(Shooting_Enemy(self.canvas,x,y))
                        xi=50
                        xj=50
                        self.turrets.append(Turret(self.canvas,xi,xj))
                    if self.enemy_map[self.room_y][self.room_x]==2:
                        self.block_room()
                        for snake_boss in self.snake_boss_room:
                            x=snake_boss[0]
                            y=snake_boss[1]
                            for i in range(150):
                                self.snake_boss.append(Enemy(self.canvas,x,y))
                    self.canvas_int.delete(self.mini_map)
                    self.mini_map=self.canvas_int.create_rectangle(30*self.room_x, 30*self.room_y, 30*(self.room_x+1), 30*(self.room_y+1), fill = "grey", outline= 'green', width=1)

    def check_collision(self):
        self.update_room()
        player_coords = self.canvas.coords(self.player.rect)
        
        for golden_key in self.golden_keys:
            golden_key_coords=self.canvas.coords(golden_key.rect)    
            if (player_coords[2] > golden_key_coords[0] and player_coords[0] < golden_key_coords[2] and
                player_coords[3] > golden_key_coords[1] and player_coords[1] < golden_key_coords[3]):
                self.player.golden_key=1
                self.golden_keys.remove(golden_key)
                self.canvas.delete(golden_key.rect)  
        
        for medic_bag in self.medic_bags:
            medic_bag_coords = self.canvas.coords(medic_bag.rect)
            if (player_coords[2] > medic_bag_coords[0] and player_coords[0] < medic_bag_coords[2] and
                player_coords[3] > medic_bag_coords[1] and player_coords[1] < medic_bag_coords[3]):
                self.player.health += 20
                self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: {int(self.player.health)}")
                self.medic_bags.remove(medic_bag)
                self.canvas.delete(medic_bag.rect)

        for lock in self.locks:
            lock_coords = self.canvas.coords(lock.rect)
            if (player_coords[2] > lock_coords[0] and player_coords[0] < lock_coords[2] and
                player_coords[3] > lock_coords[1] and player_coords[1] < lock_coords[3]) and self.player.golden_key==0:
                return True
            elif (player_coords[2] > lock_coords[0] and player_coords[0] < lock_coords[2] and
                player_coords[3] > lock_coords[1] and player_coords[1] < lock_coords[3]) and self.player.golden_key==1 and len(self.enemies)==0:
                return False
               
        for wall in self.walls:
            wall_coords = self.canvas.coords(wall.rect)
            if (player_coords[2] > wall_coords[0] and player_coords[0] < wall_coords[2] and
                player_coords[3] > wall_coords[1] and player_coords[1] < wall_coords[3]):
                return True
        return False
    
    def check_bullet_collision(self):
        player_coords = self.canvas.coords(self.player.rect)
        
        for bullet in Bullet.bullets[:]:
            bullet_coords = self.canvas.coords(bullet.oval)
            if (player_coords[2] > bullet_coords[0] and player_coords[0] < bullet_coords[2] and player_coords[3] > bullet_coords[1] and player_coords[1] < bullet_coords[3]):
                self.player.health -= 10
                self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: {int(self.player.health)}")
                if self.player.health <= 0:
                    self.canvas_int.itemconfig(self.health_bar, text = f"Здоровье: 0")
                    self.game_over()
                Bullet.bullets.remove(bullet)
                self.canvas.delete(bullet.oval)
            for wall in self.walls:
                wall_coords = self.canvas.coords(wall.rect)
                if (bullet_coords[2] > wall_coords[0] and bullet_coords[0] < wall_coords[2] and
                    bullet_coords[3] > wall_coords[1] and bullet_coords[1] < wall_coords[3]):
                    if len(Bullet.bullets)!=0:
                        Bullet.bullets.remove(bullet)
                    self.canvas.delete(bullet.oval)

    def game_over(self):
        self.canvas_int.create_text(300, 50, text = "ПОТРАЧЕНО", font =("Arial", 30), fill ="red")
        for medic_bag in self.medic_bags:
            self.canvas.delete(medic_bag.rect)
        for bullet in Bullet.bullets:
            self.canvas.delete(bullet.oval)
        for enemy in self.enemies:
            self.canvas.delete(enemy.rect)
        self.enemies.clear()
        self.medic_bags.clear()
        Bullet.bullets.clear()
        self.canvas.delete(self.player.rect)
        
        

root = tk.Tk()
game = Game(root)
root.mainloop()