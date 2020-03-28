from neutron_util import get_time_miliseconds
import pygame
from gui_utils import get_resource_coords_from_board_coords


class Animator:
    def __init__(self, gui):
        self.constants = gui.constants
        self.gui = gui

    def animate_move(self, piece, from_x, from_y, to_x, to_y, time_animation):
        delta_x_coords = to_x - from_x
        delta_y_coords = -1 *(to_y - from_y)

        delta_x_pixels = delta_x_coords*(self.constants.TYLE_SIZE + self.constants.BEETWEEN_TYLE_SIZE)
        delta_y_pixels = -1*delta_y_coords * (self.constants.TYLE_SIZE + self.constants.BEETWEEN_TYLE_SIZE)

        resource_x, resource_y = get_resource_coords_from_board_coords(self.constants, (from_x, from_y))
        piece_resource = self.gui.get_resource(piece)

        start_time = get_time_miliseconds()
        end_time = int(start_time + time_animation*1000)
        clock = pygame.time.Clock()

        current_time = get_time_miliseconds()
        while current_time <= end_time:
            # Max 60 frames per second
            clock.tick(60)

            # How much of the animation should be done by now
            progress = (current_time - start_time)/(end_time - start_time)

            # Loads animation_piece and animation_piece_coords of gui, to be displayed when gui.display() is called
            self.gui.animation_piece = piece_resource
            self.gui.animation_piece_coords = (resource_x + delta_x_pixels*progress, resource_y + delta_y_pixels*progress)
            self.gui.display()

            # Updates current time
            current_time = get_time_miliseconds()
