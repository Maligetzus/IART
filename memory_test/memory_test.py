import sys
import memory_test_utils_new
import memory_test_utils_old

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

print("Size of NEW state representation (not the board, only the coordinates): ", end="")
print(get_size(memory_test_utils_new.get_state()))

print("Size of state with string in list of lists: ", end="")
print(get_size(memory_test_utils_old.get_list_of_lists_string_state()))

print("Size of state with int in list of lists: ", end="")
print(get_size(memory_test_utils_old.get_list_of_lists_int_state()))

print("Size of state with string in single list: ", end="")
print(get_size(memory_test_utils_old.get_list_string_state()))

print("Size of state with int in single list: ", end="")
print(get_size(memory_test_utils_old.get_list_int_state()))