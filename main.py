from tkinter import *
import random

DIFFICULTY_SETTINGS = {
    'easy': {'speed_range': (10, 15), 'max_asteroids': 3, 'spawn_interval': 3000},
    'medium': {'speed_range': (15, 25), 'max_asteroids': 5, 'spawn_interval': 2000},
    'hard': {'speed_range': (25, 35), 'max_asteroids': 7, 'spawn_interval': 1000}
}

def start_game():
    global tk, c, asteroid_list, player, current_difficulty
    
    menu_window.destroy()
    
    tk = Tk()
    tk.title('Астероиды !')
    c = Canvas(tk, width=1040, height=640, bg='white')
    c.pack()

    asteroid_list = []
    
    asteroid_image = PhotoImage(file='Asteroid.gif')
    player_image = PhotoImage(file='Armored_shuttle_2.gif')
    cosmos_image = PhotoImage(file='Cosmos.gif')
    c.create_image(0, 0, image=cosmos_image, anchor=NW)

    player = c.create_image(500, 300, image=player_image, anchor=NW)
    player_hitbox = c.create_rectangle(500, 300, 540, 340)

    settings = DIFFICULTY_SETTINGS[current_difficulty]
    speed_min, speed_max = settings['speed_range']
    max_asteroids = settings['max_asteroids']
    spawn_interval = settings['spawn_interval']

    def create_asteroid():
        if len(asteroid_list) < max_asteroids:
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x, y = random.randint(0, 900), 15
            if side == 'bottom':
                x, y = random.randint(0, 900), 600
            if side == 'left':
                x, y = 15, random.randint(0, 600)
            else:
                x, y = 970, random.randint(0, 600)

            asteroid_data = c.create_image(x, y, image=asteroid_image, anchor=NW)
            asteroid_hitbox = c.create_rectangle(x, y, x + 40, y + 40)

            vx = random.randint(speed_min, speed_max) * random.choice([-1, 1])
            vy = random.randint(speed_min, speed_max) * random.choice([-1, 1])

            asteroid_list.append({
                'asteroid_image': asteroid_data,
                'asteroid_hitbox': asteroid_hitbox,
                'vx': vx,
                'vy': vy
            })

        c.after(spawn_interval, create_asteroid)

    def move_all_asteroids():
        for asteroid in asteroid_list:
            asteroid_hitbox = asteroid['asteroid_hitbox']
            vx = asteroid['vx']
            vy = asteroid['vy']

            x1, y1, x2, y2 = c.coords(asteroid_hitbox)

            if x1 <= 10 or x2 >= 1030:
                vx *= -1
                asteroid['vx'] = vx

            if y1 <= 10 or y2 >= 630:
                vy *= -1
                asteroid['vy'] = vy

            c.move(asteroid['asteroid_image'], vx, vy)
            c.move(asteroid_hitbox, vx, vy)

            if player_hitbox:
                player_coords = c.coords(player_hitbox)
                if (x1 < player_coords[2] and x2 > player_coords[0] and
                        y1 < player_coords[3] and y2 > player_coords[1]):
                    game_over()

        c.after(50, move_all_asteroids)

    def game_over():
        c.create_text(520, 320, text='ИГРА ОКОНЧЕНА !', font=('Arial', 40), fill='red')
        tk.unbind('<KeyPress>')

    def move_player(key):
        x, y = c.coords(player)

        if key.char == 'a':
            c.move(player, -40, 0)
            c.move(player_hitbox, -40, 0)
        elif key.char == 'd':
            c.move(player, 40, 0)
            c.move(player_hitbox, 40, 0)
        elif key.char == 'w':
            c.move(player, 0, -40)
            c.move(player_hitbox, 0, -40)
        elif key.char == 's':
            c.move(player, 0, 40)
            c.move(player_hitbox, 0, 40)

        x, y = c.coords(player)
        if x < 0:
            c.move(player, -x, 0)
            c.move(player_hitbox, -x, 0)
        if x > 1000:
            c.move(player, 1000 - x, 0)
            c.move(player_hitbox, 1000 - x, 0)
        if y < 0:
            c.move(player, 0, -y)
            c.move(player_hitbox, 0, -y)
        if y > 600:
            c.move(player, 0, 600 - y)
            c.move(player_hitbox, 0, 600 - y)

    tk.bind('<KeyPress>', move_player)

    create_asteroid()
    move_all_asteroids()

    c.create_text(60, 20, text=f'Сложность: {current_difficulty.upper()}', fill='white')

    mainloop()

def set_easy():
    global current_difficulty
    current_difficulty = 'easy'
    start_game()

def set_medium():
    global current_difficulty
    current_difficulty = 'medium'
    start_game()

def set_hard():
    global current_difficulty
    current_difficulty = 'hard'
    start_game()


menu_window = Tk()
title_label = Label(menu_window, text='АСТЕРОИДЫ !', font=('Arial', 40), bg='#2c3e50', fg='white')
title_label.pack(pady=20)
menu_window.title('Выбор сложности')
menu_window.geometry('400x300')
menu_window.configure(bg='#2c3e50')

subtitle_label = Label(menu_window, text='Выберите уровень сложности:', bg='#2c3e50', fg='#ecf0f1')
subtitle_label.pack(pady=10)

button_frame = Frame(menu_window, bg='#2c3e50')
button_frame.pack(pady=20)

easy_btn = Button(button_frame, text='ЛЁГКИЙ', bg='#27ae60', fg='white', command=set_easy)
easy_btn.pack(pady=5)

medium_btn = Button(button_frame, text='СРЕДНИЙ', bg='#f39c12', fg='white', command=set_medium)
medium_btn.pack(pady=5)

hard_btn = Button(button_frame, text='СЛОЖНЫЙ', bg='#e74c3c', fg='white', command=set_hard)
hard_btn.pack(pady=5)

menu_window.mainloop()