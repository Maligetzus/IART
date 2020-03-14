from minimax import minimax
from neutron import Neutron


def main():
    game = Neutron.get()
    minimax(game)


if __name__ == '__main__':
    main()
