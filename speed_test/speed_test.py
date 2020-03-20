import timeit

import_old = "import speed_test_utils_old as nutils"
import_new = "import speed_test_utils_new as nutils"

old_victory = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.victory(nutils.Player.Black, state)
'''

new_victory = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.victory(nutils.Player.Black, state, 5)
'''

old___neutron_to = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.__neutron_to(nutils.Player.Black, state, (3, 4))
'''

new___neutron_to = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.__neutron_to(nutils.Player.Black, state, 5)
'''

old___num_empty_tiles = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.__num_empty_tiles(nutils.Player.Black, state)
'''

new___num_empty_tiles = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.__num_empty_tiles(nutils.Player.Black, state, 5)
'''

old_victory_opponent = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.victory_opponent(nutils.Player.Black, state)
'''

new_victory_opponent = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.victory_opponent(nutils.Player.Black, state, 5)
'''

old_victory_player = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.victory_player(nutils.Player.Black, state)
'''

new_victory_player = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.victory_player(nutils.Player.Black, state, 5)
'''

old_odd = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.odd(state, (3, 4))
'''

new_odd = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.odd(state)
'''

old_num_empty_fields_around_neutron = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.num_empty_fields_around_neutron(state, (3, 4))
'''

new_num_empty_fields_around_neutron = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.num_empty_fields_around_neutron(state)
'''

old_neutron_to_opponent = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.neutron_to_opponent(nutils.Player.Black, state, (3, 4))
'''

new_neutron_to_opponent = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.neutron_to_opponent(nutils.Player.Black, state, 5)
'''

old_neutron_to_player = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.neutron_to_player(nutils.Player.Black, state, (3, 4))
'''

new_neutron_to_player = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.neutron_to_player(nutils.Player.Black, state, 5)
'''

old_num_empty_tiles_opponent = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.num_empty_tiles_opponent(nutils.Player.Black, state)
'''

new_num_empty_tiles_opponent = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.num_empty_tiles_opponent(nutils.Player.Black, state, 5)
'''

old_num_empty_tiles_player = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.num_empty_tiles_player(nutils.Player.Black, state)
'''

new_num_empty_tiles_player = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.num_empty_tiles_player(nutils.Player.Black, state, 5)
'''

old_get_score = '''
state = [["0", "B", "0", "0", "B"], ["0", "0", "0", "0", "0"], ["0", "0", "B", "B", "W"], ["0", "0", "B", "0", "N"], ["0", "W", "W", "W", "W"]]
aux = nutils.get_score(nutils.Player.Black, state, (3, 4))
'''

new_get_score = '''
state = [2, 2, 0, 1, 3, 2, 2, 3, 0, 4, 2, 4, 4, 1, 4, 2, 4, 3, 4, 4, 3, 4]
aux = nutils.get_score(nutils.Player.Black, state, 5)
'''

time = timeit.repeat(stmt=old_victory, setup=import_old)
print("Old victory: " + str(time))
time = timeit.repeat(stmt=new_victory, setup=import_new)
print("New victory: " + str(time))
print("")

time = timeit.repeat(stmt=old___neutron_to, setup=import_old)
print("Old __neutron_to: " + str(time))
time = timeit.repeat(stmt=new___neutron_to, setup=import_new)
print("New __neutron_to: " + str(time))
print("")

time = timeit.repeat(stmt=old___num_empty_tiles, setup=import_old)
print("Old __num_empty_tiles: " + str(time))
time = timeit.repeat(stmt=new___num_empty_tiles, setup=import_new)
print("New __num_empty_tiles: " + str(time))
print("")

time = timeit.repeat(stmt=old_victory_opponent, setup=import_old)
print("Old victory_opponent: " + str(time))
time = timeit.repeat(stmt=new_victory_opponent, setup=import_new)
print("New victory_opponent: " + str(time))
print("")

time = timeit.repeat(stmt=old_victory_player, setup=import_old)
print("Old victory_player: " + str(time))
time = timeit.repeat(stmt=new_victory_player, setup=import_new)
print("New victory_player: " + str(time))
print("")

time = timeit.repeat(stmt=old_odd, setup=import_old)
print("Old odd: " + str(time))
time = timeit.repeat(stmt=new_odd, setup=import_new)
print("New odd: " + str(time))
print("")

time = timeit.repeat(stmt=old_num_empty_fields_around_neutron, setup=import_old)
print("Old num_empty_fields_around_neutron: " + str(time))
time = timeit.repeat(stmt=new_num_empty_fields_around_neutron, setup=import_new)
print("New num_empty_fields_around_neutron: " + str(time))
print("")

time = timeit.repeat(stmt=old_neutron_to_opponent, setup=import_old)
print("Old neutron_to_opponent: " + str(time))
time = timeit.repeat(stmt=new_neutron_to_opponent, setup=import_new)
print("New neutron_to_opponent: " + str(time))
print("")

time = timeit.repeat(stmt=old_neutron_to_player, setup=import_old)
print("Old neutron_to_player: " + str(time))
time = timeit.repeat(stmt=new_neutron_to_player, setup=import_new)
print("New neutron_to_player: " + str(time))
print("")

time = timeit.repeat(stmt=old_num_empty_tiles_opponent, setup=import_old)
print("Old num_empty_tiles_opponent: " + str(time))
time = timeit.repeat(stmt=new_num_empty_tiles_opponent, setup=import_new)
print("New num_empty_tiles_opponent: " + str(time))
print("")

time = timeit.repeat(stmt=old_num_empty_tiles_player, setup=import_old)
print("Old num_empty_tiles_player: " + str(time))
time = timeit.repeat(stmt=new_num_empty_tiles_player, setup=import_new)
print("New num_empty_tiles_player: " + str(time))
print("")

time = timeit.repeat(stmt=old_get_score, setup=import_old)
print("Old get_score: " + str(time))
time = timeit.repeat(stmt=new_get_score, setup=import_new)
print("New get_score: " + str(time))
print("")