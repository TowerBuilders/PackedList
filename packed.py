MAXIMUM_ARRAY_LENGTH = 2

def Main(operation, args):
    if operation == 'PackedTest':
        return PackedTest()
    return False


def PackedTest():
    packed = PackedList()                               # []
    PackedAppend(packed, 1)                             # [1]
    PackedAppend(packed, 2)                             # [1, 2]
    PackedAppend(packed, 3)                             # [[1, 2], 3]
    itemCount = packed["items"]
    assert(itemCount == 3)

    PackedRemove(packed, 5)                             # [[1, 2], 3]
    PackedRemove(packed, 6)                             # [[1, 2], 3]
    PackedRemove(packed, 2)                             # [1, 3]
    PackedRemove(packed, 2)                             # [1, 3]
    itemCount = packed["items"]
    assert(itemCount == 2)
    assert(packed["array"][0] == 1)
    assert(packed["array"][1] == 3)

    PackedAppend(packed, 2)                             # [[1, 3], 2]
    itemCount = packed["items"]
    assert(itemCount == 3)

    PackedAppend(packed, 4)                             # [[[1, 3], 2], 4]
    itemCount = packed["items"]
    assert(itemCount == 4)

    PackedAppend(packed, 5)                             # [[[[1, 3], 2], 4], 5]
    itemCount = packed["items"]
    assert(itemCount == 5)

    PackedAppend(packed, 6)                             # [[[[[1, 3], 2], 4], 5], 6]
    itemCount = packed["items"]
    assert(itemCount == 6)

    PackedAppend(packed, 7)                             # [[[[[[1, 3], 2], 4], 5], 6], 7]
    itemCount = packed["items"]
    assert(itemCount == 7)

    PackedAppend(packed, 8)                             # [[[[[[[1, 3], 2], 4], 5], 6], 7], 8]
    itemCount = packed["items"]
    assert(itemCount == 8)

    PackedAppend(packed, 9)                             # [[[[[[[[1, 3], 2], 4], 5], 6], 7], 8], 9]
    itemCount = packed["items"]
    assert(itemCount == 9)

    PackedRemove(packed, 2)                             # [[[[[[[1, 3], 9], 4], 5], 6], 7], 8]
    itemCount = packed["items"]
    assert(itemCount == 8)

    PackedRemove(packed, 4)                             # [[[[[[1, 3], 9], 8], 5], 6], 7]
    itemCount = packed["items"]
    assert(itemCount == 7)

    PackedRemove(packed, 5)                             # [[[[[1, 3], 9], 8], 7], 6]
    itemCount = packed["items"]
    assert(itemCount == 6)

    PackedRemove(packed, 6)                             # [[[[1, 3], 9], 8], 7]
    itemCount = packed["items"]
    assert(itemCount == 5)

    PackedRemove(packed, 7)                             # [[[1, 3], 9], 8]
    itemCount = packed["items"]
    assert(itemCount == 4)

    PackedRemove(packed, 8)                             # [[1, 3], 9]
    itemCount = packed["items"]
    assert(itemCount == 3)

    PackedRemove(packed, 9)                             # [1, 3]
    itemCount = packed["items"]
    assert(itemCount == 2)

    return True


def PackedList():
    '''
    Creates a new PackedList
    '''
    packed = {
        "array": [],
        "items": 0
    }
    return packed


def PackedAppend(packed, itm):
    '''
    Appends an item to the PackedList.array or wraps it in a new layer if full.
    Increments the PackedList.items count.

    :param packed: The PackedList
    :param itm: The item to add to the PackedList
    '''
    array = packed["array"]
    length = len(array)
    if length == MAXIMUM_ARRAY_LENGTH:
        tmp = [array]
        tmp.append(itm)
        array = tmp
    else:
        array.append(itm)
    packed["array"] = array
    packed["items"] += 1


def PackedRemove(packed, itm):
    '''
    Removes an item from the PackedList.array.

    :param packed: The PackedList
    :param itm: The item to remove from the PackedList
    '''
    if not do_swap(packed, itm): # Item not found
        return

    if len(packed["array"]) == 2: # Peel off layer
        peel(packed)
    else: # Remove last item
        remove_last(packed["array"])
    packed["items"] -= 1


def peel(packed):
    '''
    Peels a layer off of the PackedList

    :param packed: The PackedList
    '''
    packed["array"] = packed["array"][0]


def remove_last(lst):
    '''
    Removes the last item from a list.

    :param lst: The list to remove the item from
    '''
    length = len(lst)
    nLst = []
    for i in range(length - 1):
        nLst.append(lst[i])
    lst = nLst


def do_swap(packed, itm):
    '''
    Swaps the last item in the PackedList.array with the item.

    :param packed: The PackedList
    :param itm: The item to swap
    '''
    array = packed["array"]
    items = packed["items"]
    length = len(array)
    if length is 0:
        return False

    last = array[length - 1]
    if last is itm:
        return True

    layers = get_layers(items)
    if do_find(array, length, layers, itm, last):
        array[length - 1] = itm
        return True
    return False


def do_find(array, length, layers, itm, last):
    '''
    Finds the item in the array and swaps it with the last item

    :param array: The PackedList.array
    :param length: The length of the PackedList.array
    :param layers: The amount of layers in the PackedList.array
    :param itm: The item to swap
    :param last: The last item in the PackedList.array
    '''
    for i in range(length):
        item = array[i]
        if i == 0 and layers > 1:
            if do_find(item, len(item), layers - 1, itm, last):
                return True
        elif item is itm:
            array[i] = last
            return True
    return False


# Input             Layers      Items(n=2)      Items(n=3)          Items(n=4)

# 1   ... 1n-0      1           [1...2]         [1 ... 3]           [1 ... 4]
# 1n+1... 2n-1      2           [3]             [4 ... 5]           [5 ... 7]
# 2n-0... 3n-2      3           [4]             [6 ... 7]           [8 ... 10]
# 3n-1... 4n-3      4           [5]             [8 ... 9]           [11 ... 13]
# 4n-2... 5n-4      5           [6]             [10 ... 11]         [14 ... 16]

def get_layers(items):
    '''
    Calculated the amount of layers in the PackedList

    :param items: The amount of items in the PackedList
    '''
    x = items
    x -= MAXIMUM_ARRAY_LENGTH
    layers = 1
    while x > 0:
        x -= (MAXIMUM_ARRAY_LENGTH - 1)
        layers += 1
    return layers
