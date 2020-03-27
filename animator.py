import time

class Animator:
    def __init__(self, gui_constants):
        self.constants = gui_constants

    def animate_move(self, piece, from_x, from_y, to_x, to_y):
        delta_x_coords = to_x - from_x
        delta_y_coords = -1 *(to_y - from_y)

        delta_x_pixels = delta_x_coords*(self.constants.TYLE_SIZE + self.constants.BEETWEEN_TYLE_SIZE)
        delta_y_pixels = -1*delta_y_coords * (self.constants.TYLE_SIZE + self.constants.BEETWEEN_TYLE_SIZE)

        print("Delta x coords:", delta_x_coords)
        print("Delta y coords:", delta_y_coords)
        print("Delta x pixels:", delta_x_pixels)
        print("Delta y pixels:", delta_y_pixels)
        # time.sleep(1.5)