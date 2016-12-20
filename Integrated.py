c=1
b_object = []
temp_object = []

output_1 = []                  # first required output


def first_out(board):          # extract all the obstacles' and objects' positions
    c = 1
    for block in board:
        if block != ('NoShape',):
            x = c % 10
            y = c / 10
            output_1.append((x, y))

            temp_object.append(block)
            block += (c,)
            b_object.append(block)
        c += 1


def do_obstacle(board, tmap):
    c = 1
    for block in board:
        if block == ('black', '4-sided'):
            x = c % 10
            y = c / 10
            tmap[y][x] = 1
        c += 1

    return tmap

def do_path(board, tmap):
    if __name__ == '__main__':
        for block in board :
            if block[0:2] != ('black', '4-sided'):
                # ok fuck... we dont have the xB and yB coordinates here, we need to find which is the shortest destination.
                # ok... we can get that after mapping to all the destination and comapring to find the shortest one
                # so in that find_path function in AstarAlgo, do something!!!... m sleeping.z.z.z.zzzz
                pass