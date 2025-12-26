from tkinter import *
import random

tk = Tk()
c = Canvas(tk, width=1040, height=640, bg='white')
c.pack()

asteroid_list = []

def create_asteroid():
    colors = ['blue', 'green', 'purple']
    color = random.choice(colors)

    asteroid_data = c.create_oval(15, 15, 55, 55, fill=color)
    
    vx = random.randint(15, 25)
    vy = random.randint(15, 25)
    
    asteroid_list.append({
        'asteroid_data': asteroid_data,
        'vx': vx,
        'vy': vy
    })

    if len(asteroid_list) < 5:
        c.after(2000, create_asteroid)

def move_all_asteroids():
    for asteroid in asteroid_list:
        asteroid_data = asteroid['asteroid_data']
        vx = asteroid['vx']
        vy = asteroid['vy']

        x1, y1, x2, y2 = c.coords(asteroid_data)

        if x1 <= 10 or x2 >= 1035:
            vx *= -1
            asteroid['vx'] = vx

        if y1 <= 10 or y2 >= 635:
            vy *= -1
            asteroid['vy'] = vy

        c.move(asteroid_data, vx, vy)

    c.after(50, move_all_asteroids)

create_asteroid()

move_all_asteroids()

mainloop()