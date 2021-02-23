import pygame
import random
import engine as e

from math import cos, sin

pygame.init()

FPS = 60
RES = [1280, 720]
screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()
engine = e.Engine(RES)

btn_rects = []
box_active = []
timer_range = [120, 210]
timer = random.randint(timer_range[0], timer_range[1])

for y_mod in [-1, 0, 1]:
    for x_mod in [-1, 0, 1]:
        btn_rects.append(pygame.Rect(
            RES[0]//2 + x_mod*160 - 60, 
            RES[1]//2 + y_mod*160 - 60, 
            120, 120
        ))

for rect in btn_rects:
    engine.add_box(
        e.Box(rect, 10, [209, 209, 209], [199, 199, 199])
    )

for rect in [pygame.Rect(0, 0, RES[0]/4, RES[1]), pygame.Rect(3*RES[0]/4, 0, RES[0]/4, RES[1])]:
    engine.add_box(
        e.Box(rect, 30, [199, 199, 199], [189, 189, 189])
    )

def render_all(display):
    display.fill((255, 173, 27))
    pygame.draw.rect(display, [229, 229, 229], [0, 40, RES[0], RES[1]-80])
    engine.run_cycle(display, [0,0])
    pygame.display.update()


''' main loop '''
run = True
while run:
    ''' timer action '''
    timer -= clock.get_time()
    if timer <= 0:
        timer = random.randint(timer_range[0], timer_range[1])
        box_active.append(random.choice(range(len(btn_rects))))
        box_active = list(set(box_active))

    ''' box stuff '''
    # list comprehension [2:] because the first two boxes
    # are the left and right box
    for i, box in enumerate(engine.box_list[2:]):
        if i in box_active:
            box.front_color = [252, 163, 17]
            box.side_color = [242, 153, 12]
            if box.width < 70:
                box.width += -0.0027*(box.width-10)**2 + 10
        else:
            box.front_color = [209, 209, 209]
            box.side_color = [199, 199, 199]
            if box.width > 10:
                box.width -= -0.0027*(box.width-10)**2 + 10
    
    engine.box_list[0].width = 30 + 10*sin(pygame.time.get_ticks()/1000-1)
    engine.box_list[1].width = 30 + 10*sin(pygame.time.get_ticks()/1000)

    ''' events '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, box in enumerate(engine.box_list[2:]):
                print(box_active)
                front_rect = pygame.Rect(
                    box.front_points[0][0], box.front_points[0][1], 
                    box.back_rect[2], box.back_rect[3]
                )
                if i in box_active and front_rect.collidepoint(mouse_pos):
                    timer += timer_range[0]
                    box_active.remove(i)

    ''' other stuff '''
    clock.tick(FPS)
    render_all(screen)
