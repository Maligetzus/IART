import pygame
from NeutronGame.neutron_util import get_time_miliseconds
from NeutronGame.gui_utils import get_piece_coords_from_board_coords


class Animator:
    def __init__(self, gui):
        self.constants = gui.constants
        self.gui = gui

    def animate_move(self, piece, from_x, from_y, to_x, to_y, time_animation):
        # Calculates the number of board tiles between (from_x, from_y) and (to_x, to_y)
        # Y is inverted due to orientation purposes
        delta_x_coords = to_x - from_x
        delta_y_coords = -1 *(to_y - from_y)

        # Converts number of board tiles to screen coordinates
        delta_x_pixels = delta_x_coords*(self.constants.TYLE_SIZE + self.constants.BEETWEEN_TYLE_SIZE)
        delta_y_pixels = -1*delta_y_coords * (self.constants.TYLE_SIZE + self.constants.BEETWEEN_TYLE_SIZE)

        # Gets the coordinates of the top-left corner of the piece at (from_x, from_y)
        resource_x, resource_y = get_piece_coords_from_board_coords(self.constants, (from_x, from_y))
        # Gets the piece resource, to be displayed later
        piece_resource = self.gui.get_resource(piece)

        # Registers the current instant (ms) - Animation start time
        start_time = get_time_miliseconds()
        # Calculates the animation end instant (ms), based on the start_time
        end_time = int(start_time + time_animation*1000)
        # Used to limit number of executions per second
        clock = pygame.time.Clock()

        # Updates current time
        current_time = get_time_miliseconds()
        while current_time <= end_time:
            # Limits executions to 60 per seconds => aprox. 60 times per second
            clock.tick(60)

            # How much of the animation should be done by now
            progress = (current_time - start_time)/(end_time - start_time)

            # Loads animation_piece and animation_piece_coords of gui, to be displayed when gui.display() is called
            self.gui.animation_piece = piece_resource
            self.gui.animation_piece_coords = (resource_x + delta_x_pixels*progress, resource_y + delta_y_pixels*progress)
            # Calls the display function
            self.gui.display()

            # Updates current time
            current_time = get_time_miliseconds()
