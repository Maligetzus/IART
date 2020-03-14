def get_score(game):
    return 1000 + 10 * num_empty_tiles_player(game) - 10 * num_empty_tiles_opponent(game) +\
           200 * neutron_to_player(game) - 200 * neutron_to_opponent(game) + 10 * odd(game) *\
           (8 - num_empty_fields_around_neutron(game)) + 500 * victory_player(game) - 500 * victory_opponent(game)


def num_empty_tiles_player(game):
    return __num_empty_tiles(game.curr_player, game)


def num_empty_tiles_opponent(game):
    if game.curr_player == "Black":
        return __num_empty_tiles("White", game)
    elif game.curr_player == "White":
        return __num_empty_tiles("Black", game)


def neutron_to_player(game):
    return __neutron_to(game.curr_player, game)


def neutron_to_opponent(game):
    if game.curr_player == "Black":
        return __neutron_to("White", game)
    elif game.curr_player == "White":
        return __neutron_to("Black", game)


def num_empty_fields_around_neutron(game):
    counter = 0
    middle = game.size / 2
    if game.state[middle + 1][middle + 1] == '0':
        counter += 1
    if game.state[middle + 1][middle] == '0':
        counter += 1
    if game.state[middle + 1][middle - 1] == '0':
        counter += 1
    if game.state[middle][middle + 1] == '0':
        counter += 1
    if game.state[middle][middle - 1] == '0':
        counter += 1
    if game.state[middle - 1][middle + 1] == '0':
        counter += 1
    if game.state[middle - 1][middle] == '0':
        counter += 1
    if game.state[middle - 1][middle - 1] == '0':
        counter += 1
    return counter


def odd(game):
    return num_empty_fields_around_neutron(game) % 2


def victory_player(game):
    return __victory(game.curr_player, game)


def victory_opponent(game):
    if game.curr_player == "Black":
        return __neutron_to("White", game)
    elif game.curr_player == "White":
        return __neutron_to("Black", game)


def __num_empty_tiles(player, game):
    counter = 0
    if player == "Black":
        for tile in game.state[0]:
            if tile == '0':
                counter += 1
    elif player == "White":
        for tile in game.state[game.size - 1]:
            if tile == '0':
                counter += 1

    return counter


def __neutron_to(player, game):
    if player == "Black":
        for tile in game.state[1]:
            if tile == 'N':
                return 1
    elif player == "White":
        for tile in game.state[game.size - 2]:
            if tile == 'N':
                return 1
    return 0


def __victory(player, game):
    if player == "Black":
        for tile in game.state[0]:
            if tile == 'N':
                return 1
    elif player == "White":
        for tile in game.state[game.size - 1]:
            if tile == 'N':
                return 1
    return 0
