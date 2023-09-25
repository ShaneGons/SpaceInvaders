from tkinter import *
from random import randint
from PIL import Image, ImageTk

#Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 450
BLOCK_SIZE = 50
FRAME_HEIGHT = WINDOW_HEIGHT-BLOCK_SIZE
paused = False
player_img = "playerShip2_green.png"

def run_game():
    
    spawn_enemy()
    add_ammo()
    check_if_enemy_killed()
    check_if_enemy_deals_damage()
    is_game_over()
    top_frame.pack(side=TOP)
    game_frame.pack(side=BOTTOM)
    top_canvas.pack()
    canvas.pack()

def main_menu():
    leaderboard_button.pack()
    play_button.pack()
    change_skins_button.pack()
    main_menu_canvas.pack()

def play_game():
    main_menu_canvas.pack_forget()
    ship = Ship(5)
    run_game()

def leaderboard():
    f = open("scores.txt", "r")

def change_icons():
    global player_img
    if player_img == "ufoRed.png":
        player_img = "playerShip2_green.png"
    else:
        player_img = "ufoRed.png"

class Ship:
    def __init__(self, ammo_count):
        self.coordinates = [(WINDOW_WIDTH-BLOCK_SIZE)//(2*BLOCK_SIZE),(FRAME_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE]
        self.ship_image = ImageTk.PhotoImage((Image.open(player_img)).resize((BLOCK_SIZE,BLOCK_SIZE)))
        self.ship = canvas.create_image(BLOCK_SIZE*self.coordinates[0],BLOCK_SIZE*self.coordinates[1]+15,image=self.ship_image)
        self.ammo_count = ammo_count

        # self.shot1 = Bullet(0, -5, False)
        # self.shot2 = Bullet(0, -5, False)
        # self.shot3 = Bullet(0, -5, False)
        # self.shot4 = Bullet(0, -5, False)
        # self.shot5 = Bullet(0, -5, False)
        # self.bullets = [self.shot1,self.shot2,self.shot3,self.shot4,self.shot5]
    
    #Moves ship by 1 block to the right/left depending on the input
    def move_ship(self, event):
        if event == "right":
            if self.coordinates[0] < 15:
                canvas.move(self.ship,BLOCK_SIZE,0)
                self.coordinates[0] += 1
        elif event == "left":
            if self.coordinates[0] > 1:
                canvas.move(self.ship,-BLOCK_SIZE,0)
                self.coordinates[0] -= 1

    #creates bullet at location of ship
    def shoot(self):
        bullet_list.append(Bullet(0,-5,self.coordinates))
    #     if self.shot1.is_fired == True:
    #         self.shot1.fire()
    #     if self.shot2.is_fired == True:
    #         self.shot2.fire()
    #     if self.shot3.is_fired == True:
    #         self.shot3.fire()
    #     if self.shot4.is_fired == True:
    #         self.shot4.fire()
    #     if self.shot5.is_fired == True:
    #         self.shot5.fire()

class Enemy:
    def __init__(self):
        x = randint(2,14)
        self.coordinates = [x,0]
        self.enemy_image = ImageTk.PhotoImage((Image.open("enemyBlack1.png")).resize((BLOCK_SIZE,BLOCK_SIZE)))
        self.enemy = canvas.create_image(BLOCK_SIZE*self.coordinates[0],BLOCK_SIZE*self.coordinates[1],image=self.enemy_image)
        self.move()

    def move(self):
        canvas.move(self.enemy, 0, 1) #Moves enemy down by 1 pixel
        if not paused:
            canvas.after(20, self.move) #Calls enemy.move() every 20ms
    
    def get_coordinates(self):
        return canvas.coords(self.enemy)
    
    #bullet dissappears from canvas
    def delete_enemy(self):
        canvas.delete(self.enemy)

class Ufo:
    pass

class Bullet:
    def __init__(self, velocity_x, velocity_y, ship_coordinates):
        self.bullet = canvas.create_oval(10,10,20,20,) #creates invisible bullet
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        #self.is_fired = is_fired
        self.coordinates = ship_coordinates
        self.set_coordinates(self.coordinates) #moves bullet to ship's coordinates
        self.count = 0
        self.fire()

    def fire(self):
        canvas.itemconfig(self.bullet,fill="white") #makes bullet visible
        canvas.move(self.bullet, self.velocity_x, self.velocity_y) #moves bullet by set velocity
        # self.count += 1
        # if self.count%20 == 0:
        #     self.coordinates[1] += 1
        if not paused:
            canvas.after(10,self.fire) #calls bullet.fire() ever 10ms
    
    def set_coordinates(self, coordinates):
        canvas.coords(self.bullet,coordinates[0]*BLOCK_SIZE-3,coordinates[1]*BLOCK_SIZE,coordinates[0]*BLOCK_SIZE+3,coordinates[1]*BLOCK_SIZE+15)
    
    def get_coordinates(self):
        return canvas.coords(self.bullet)

    #bullet dissapears from canvas
    def delete_bullet(self):
        canvas.delete(self.bullet)

#Repeatedly refils ammo every 3 seconds by one bullet
def add_ammo():
    if ship.ammo_count < 5:
        ship.ammo_count += 1
    if not paused:
        canvas.after(1500, add_ammo)

#Waits a random amount of time before spawning more enemies
def spawn_enemy():
    global count
    count += 1
    ub = 400
    lb = 3000
    if count > 10:
        ub = 300
        lb = 2000
        if count > 20:
            ub = 200
            lb = 1000
    time = randint(ub, lb)
    enemy_list.append(Enemy())
    if not paused:
        canvas.after(time, spawn_enemy)

def check_if_enemy_deals_damage():
    global lives
    for enemy in enemy_list:
        enemy_coord = enemy.get_coordinates()
        if enemy_coord[1] >= (WINDOW_HEIGHT-(1.5*BLOCK_SIZE)):
            lives -= 1
            lives_label.config(text="Lives = "+str(lives))
            enemy_list.remove(enemy)
            enemy.delete_enemy()
    if not paused:
        canvas.after(100,check_if_enemy_deals_damage)

#checks if any bullet overlaps with any enemy in order to destroy enemy
def check_if_enemy_killed():
    global score
    #loops through every current bullet on screen
    for bullet in bullet_list:
        #creates square of coordinates around bullet
        bullet_coords = bullet.get_coordinates()
        #loops through every current enemy on screen
        for enemy in enemy_list:
            #creates square of coordinates around enemy
            enemy_coord = enemy.get_coordinates()
            enemy_coords = [enemy_coord[0]-(BLOCK_SIZE//2),enemy_coord[1]-(BLOCK_SIZE//2),enemy_coord[0]+(BLOCK_SIZE//2),enemy_coord[1]+(BLOCK_SIZE//2)]
            if (((bullet_coords[2]>enemy_coords[0] and bullet_coords[2]<enemy_coords[2]) and
                ((bullet_coords[3]>enemy_coords[1] and bullet_coords[3]<enemy_coords[3]) or 
                (bullet_coords[1]>enemy_coords[3] and bullet_coords[1]<enemy_coords[1]))) or 
                ((bullet_coords[0]>enemy_coords[0] and bullet_coords[0]<enemy_coords[2]) and
                ((bullet_coords[3]>enemy_coords[1] and bullet_coords[3]<enemy_coords[3]) or 
                (bullet_coords[1]>enemy_coords[3] and bullet_coords[1]<enemy_coords[1])))):
                enemy_list.remove(enemy) #removes it from list of on screen enemies
                bullet_list.remove(bullet) #removes it from list of on screen bullets
                enemy.delete_enemy()
                bullet.delete_bullet()
                score += 1
                score_label.config(text="Score = "+str(score))
    #checks for collisions every 150ms
    if not paused:
        canvas.after(50,check_if_enemy_killed) #Every 100ms as 150ms is minimum for accuracte hit reg, ~100ms buffer

def is_game_over():
    global paused
    if lives <= 0:
        paused = True
        top_frame.pack_forget()
        game_frame.pack_forget()
        name_label = Label(score_canvas,font=("Ariel",10),text="Name: ")
        name_label.grid(row=0,column=0)
        enter_name = Entry(score_canvas, width=10)
        enter_name.grid(row=0,column=4)
        submit_button = Button(score_canvas,font=("Ariel",10),text="Submit",command=lambda: save_score(enter_name.get()))
        submit_button.grid(row=1,column=1)
        score_canvas.pack()
    if not paused:
        canvas.after(100,is_game_over)

def save_score(name):
    f = open("scores.txt", "a")
    f.write(str(name)+" "+str(score))
    f.close()
    score_canvas.pack_forget()
    main_menu()

#binds arrow keys to movement 
def leftKey(event):
    if not paused:
        ship.move_ship("left")
def rightKey(event):
    if not paused:
        ship.move_ship("right")
def spaceKey(event):
    if not paused:
        if ship.ammo_count > 0:
            ship.ammo_count -= 1
            ship.shoot()
def wKey(event):
    for enemy in enemy_list:
        enemy_list.remove(enemy)
        enemy.delete_enemy()
def bossKey(event):
    work_window = Tk()
    screen_width = work_window.winfo_screenwidth()
    screen_height = work_window.winfo_screenheight()
    work_window.geometry(str(WINDOW_WIDTH)+"x"+str(WINDOW_HEIGHT )+"+"+str(screen_width//3)+"+"+str(screen_height//8))
    work_label = Label(work_window,font=("Ariel",50),text="WORK")
    work_label.pack()

def pause_game():
    global paused
    global pause_text
    if lives > 0:
        if paused:
            pause_text.set("Pause")
            paused = False
            for enemy in enemy_list:
                enemy.move()
            for bullet in bullet_list:
                bullet.fire()
            add_ammo()
            spawn_enemy()
            check_if_enemy_deals_damage()
            check_if_enemy_killed()
            is_game_over()
        else:
            pause_text.set("Play")
            paused = True
        
def set_window_dimensions(w,h):
    root.title("Space Invaders")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(str(w)+"x"+str(h)+"+"+str(screen_width//3)+"+"+str(screen_height//8))
    return root

root = Tk()
window = set_window_dimensions(WINDOW_WIDTH, WINDOW_HEIGHT)
game_frame = Frame(window,bd=2,width=WINDOW_WIDTH,height=WINDOW_HEIGHT-BLOCK_SIZE,bg="black")

top_frame = Frame(window,bd=2,width=WINDOW_WIDTH,height=BLOCK_SIZE,bg="green")

canvas = Canvas(game_frame, bg="black", width = WINDOW_WIDTH, height = WINDOW_HEIGHT-BLOCK_SIZE)
top_canvas = Canvas(top_frame,bg="pink",width=WINDOW_WIDTH,height=BLOCK_SIZE)
#binds key presses to in-game actions
canvas.bind("<Left>",leftKey)
canvas.bind("<Right>",rightKey)
canvas.bind("<space>",spaceKey)
canvas.bind("w",wKey)
canvas.bind("b",bossKey)
canvas.focus_set()

lives = 3
lives_label = Label(top_frame,font=("Ariel",10),text="Lives = "+str(lives))
lives_label.pack(side=LEFT)
score = 0
score_label = Label(top_frame,font=("Ariel",10),text="Score = "+str(score))
score_label.pack(side=LEFT)
pause_text = StringVar()
pause_button = Button(top_frame,font=("Ariel", 10),textvariable=pause_text,command=pause_game).pack(side=RIGHT)
pause_text.set("Pause")
enemy_list = []
bullet_list = []
ship = Ship(5)
main_menu_canvas = Canvas(window,width=WINDOW_WIDTH,height=WINDOW_HEIGHT,bg="white")
score_canvas = Canvas(window,width=WINDOW_WIDTH,height=WINDOW_HEIGHT,bg="white")
play_button = Button(main_menu_canvas,text="Play Game",bg="grey",width=15,height=2,command=play_game)
leaderboard_button = Button(main_menu_canvas,text="Leaderboard",bg="grey",width=15,height=2,command=leaderboard)
change_skins_button = Button(main_menu_canvas,text="Customise Icons",bg="grey",width=15,height=2,command=change_icons)
count = 0



main_menu()

mainloop()

