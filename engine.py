import pygame

class Engine:
    def __init__(self, resolution: list):
        self.res = resolution
        self.box_list = []

    def add_box(self, box: object):
        '''
        add a `box` class to `self.box_list`
        '''
        self.box_list.append(box)

    def run_cycle(self, display: object, scroll: list):
        '''
        update and draw 3D objects
        '''
        self.box_list.sort(key=lambda x: abs(x.dim_factors[0]) + abs(x.dim_factors[1]), reverse=True)
        for box in self.box_list:
            box.set_dim_factors(
                scroll, self.res
            )
            box.render(display, scroll)


class Box:
    def __init__(self, back_rect: object, width: int, front_color: tuple, side_color: tuple = None):
        self.width = width
        self.back_rect = back_rect
        self.front_color = front_color
        self.side_color = side_color

        self.front_points = []
        self.dim_factors = [0.0, 0.0]
        self.center = [back_rect[0] + back_rect[2]//2, back_rect[1] + back_rect[3]//2]

    def set_dim_factors(self, scroll: list, res: list):
        '''
        set new 3D perspective factors
        '''
        self.dim_factors = [
            2*(self.center[0] - scroll[0]) / res[0] - 1,
            2*(self.center[1] - scroll[1]) / res[1] - 1
        ]

    def render(self, display: object, scroll: list):
        '''
        Render box to `display`.
        '''
        # determine sides to render
        top = True
        left = True
        if self.dim_factors[1] < 0:
            top = False
        if self.dim_factors[0] > 0:
            left = False
        # calculate back rect coords
        back_points = [
            [self.back_rect[0] - scroll[0], self.back_rect[1] - scroll[1]], # top left
            [self.back_rect[0] + self.back_rect[2] - scroll[0], self.back_rect[1] - scroll[1]], # top right
            [self.back_rect[0] + self.back_rect[2] - scroll[0], self.back_rect[1] + self.back_rect[3] - scroll[1]], # bottom right
            [self.back_rect[0] - scroll[0], self.back_rect[1] + self.back_rect[3] - scroll[1]], # bottom left
        ]
        # calculate translation
        transl = [self.width * self.dim_factors[0], self.width * self.dim_factors[1]]
        self.front_points = []
        for i in range(4):
            self.front_points.append([back_points[i][0] + transl[0], back_points[i][1] + transl[1]])

        # draw side rects (polygons)
        if top:
            pygame.draw.polygon(display, self.side_color, (
                back_points[0], self.front_points[0], 
                self.front_points[1], back_points[1]
            ))
        else:
            pygame.draw.polygon(display, [abs(n-11) for n in self.side_color], (
                back_points[2], self.front_points[2], 
                self.front_points[3], back_points[3]
            ))
        if left:
            pygame.draw.polygon(display, [abs(n-6) for n in self.side_color], (
                back_points[1], self.front_points[1], 
                self.front_points[2], back_points[2]
            ))
        else:
            pygame.draw.polygon(display, [abs(n-6) for n in self.side_color], (
                back_points[3], self.front_points[3], 
                self.front_points[0], back_points[0]
            ))
        # draw front rect
        pygame.draw.rect(
            display, self.front_color, 
            [self.front_points[0][0], self.front_points[0][1], 
            self.back_rect[2], self.back_rect[3]]
        )
