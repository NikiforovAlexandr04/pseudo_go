white_stones = []
black_stones = []
field = []


class Stone:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.visited = False
        self.second_visited = False


def fill_field():
    data = []
    with open("input.txt") as file:
        for line in file:
            data.append(line)
    positions = []
    for line in data:
        for pos in line:
            if pos != " " and pos != "\n":
                positions.append(int(pos))
    number_of_zero = positions.index(0)
    for i in range(number_of_zero):
        if i % 2 == 0:
            continue
        stone = Stone(positions[i-1] - 1, positions[i] - 1, "w")
        white_stones.append(stone)
        field[stone.y][stone.x] = stone
    positions_black = positions[number_of_zero + 2:len(positions) - 2]
    for i in range(len(positions_black)):
        if i % 2 == 0:
            continue
        stone = Stone(positions_black[i-1] - 1, positions_black[i] - 1, "b")
        black_stones.append(stone)
        field[stone.y][stone.x] = stone


def initialize_field():
    for i in range(8):
        line = []
        for j in range(8):
            line.append(Stone(j, i, "n"))
        field.append(line)


def check_bests():
    for white_stone in white_stones:
        if not white_stone.visited:
            check_pre_capture(white_stone)
    for black_stone in black_stones:
        if not black_stone.visited:
            check_pre_capture(black_stone)


white_pre_captures = []
black_pre_captures = []


def check_pre_capture(stone):
    stone.visited = True
    is_pre_capture = True
    free_spaces = check_free_spaces(stone)
    if free_spaces == 1:
        possible_capture = 1
        possible_capture_position = []
        borders = append_boarders(stone)
        queue = []
        for border in borders:
            if border.color == "n":
                possible_capture_position.append(border.x)
                possible_capture_position.append(border.y)
            if border.color == stone.color:
                queue.append(border)
                possible_capture += 1
        while len(queue) != 0:
            current_stone = queue[0]
            current_stone.visited = True
            queue = queue[1:]
            current_free_spaces = check_free_spaces(current_stone)
            if current_free_spaces == 0:
                bords = append_boarders(current_stone)
                for bord in bords:
                    if bord.color == stone.color and not bord.visited:
                        queue.append(bord)
            else:
                is_pre_capture = False
        if is_pre_capture:
            possible_capture_position.append(possible_capture)
            #if check_group_around(possible_capture_position, stone.color):
            if stone.color == "w":
                black_pre_captures.append(possible_capture_position)
            else:
                white_pre_captures.append(possible_capture_position)


def check_group_around(possible_capture_position, color):
    check = False
    x = possible_capture_position[0]
    y = possible_capture_position[1]
    stone = field[x][y]
    queue = [stone]
    while len(queue) != 0:
        cur_stone = queue[0]
        queue = queue[1:]
        borders = append_boarders(cur_stone)
        cur_stone.second_visited = True
        for border in borders:
            if border.color == "n" and not border.second_visited:
                queue.append(border)
            else:
                if color != border.color:
                    check = True
    return check




def append_boarders(stone):
    borders = []
    if stone.x == 0 and stone.y == 0:
        borders.append(field[stone.y][stone.x + 1])
        borders.append(field[stone.y + 1][stone.x])
        return borders
    if stone.x == 0 and stone.y == 7:
        borders.append(field[stone.y][stone.x + 1])
        borders.append(field[stone.y - 1][stone.x])
        return borders
    if stone.x == 7 and stone.y == 7:
        borders.append(field[stone.y][stone.x - 1])
        borders.append(field[stone.y - 1][stone.x])
        return borders
    if stone.x == 7 and stone.y == 0:
        borders.append(field[stone.y][stone.x - 1])
        borders.append(field[stone.y + 1][stone.x])
        return borders
    if stone.x == 0:
        borders.append(field[stone.y - 1][stone.x])
        borders.append(field[stone.y + 1][stone.x])
        borders.append(field[stone.y][stone.x + 1])
        return borders
    if stone.x == 7:
        borders.append(field[stone.y - 1][stone.x])
        borders.append(field[stone.y + 1][stone.x])
        borders.append(field[stone.y][stone.x - 1])
        return borders
    if stone.y == 0:
        borders.append(field[stone.y][stone.x - 1])
        borders.append(field[stone.y + 1][stone.x])
        borders.append(field[stone.y][stone.x + 1])
        return borders
    if stone.y == 7:
        borders.append(field[stone.y - 1][stone.x])
        borders.append(field[stone.y][stone.x - 1])
        borders.append(field[stone.y][stone.x + 1])
        return borders
    borders.append(field[stone.y - 1][stone.x])
    borders.append(field[stone.y + 1][stone.x])
    borders.append(field[stone.y][stone.x - 1])
    borders.append(field[stone.y][stone.x + 1])
    return borders


def check_free_spaces(stone):
    if stone.x == 0 and stone.y == 0:
        return is_free(stone.x + 1, stone.y) + is_free(stone.x, stone.y + 1)
    if stone.x == 0 and stone.y == 7:
        return is_free(stone.x + 1, stone.y) + is_free(stone.x, stone.y - 1)
    if stone.x == 7 and stone.y == 7:
        return is_free(stone.x - 1, stone.y) + is_free(stone.x, stone.y - 1)
    if stone.x == 7 and stone.y == 0:
        return is_free(stone.x - 1, stone.y) + is_free(stone.x, stone.y + 1)
    if stone.x == 0:
        return is_free(stone.x, stone.y - 1) + is_free(stone.x, stone.y + 1) + is_free(stone.x + 1, stone.y)
    if stone.x == 7:
        return is_free(stone.x, stone.y + 1) + is_free(stone.x, stone.y - 1) + is_free(stone.x - 1, stone.y)
    if stone.y == 0:
        return is_free(stone.x, stone.y + 1) + is_free(stone.x - 1, stone.y) + is_free(stone.x + 1, stone.y)
    if stone.y == 7:
        return is_free(stone.x, stone.y - 1) + is_free(stone.x + 1, stone.y) + is_free(stone.x - 1, stone.y)
    return is_free(stone.x, stone.y - 1) + is_free(stone.x + 1, stone.y) + is_free(stone.x - 1, stone.y) + is_free(stone.x, stone.y + 1)


def is_free(x, y):
    if field[y][x].color == "n":
        return 1
    return 0


def create_result(pre_captures):
    max_pre_capt = 0
    str_answer = ""
    set_pre_captures = []
    for pre_capture in pre_captures:
        if pre_capture[2] > max_pre_capt:
            max_pre_capt = pre_capture[2]
    for pre_capture in pre_captures:
        if pre_capture[2] == max_pre_capt:
            in_pre_captures = False
            for pre_capt in set_pre_captures:
                if pre_capt[0] == pre_capture[0] and pre_capt[1] == pre_capture[1]:
                    in_pre_captures = True
            if not in_pre_captures:
                str_answer += str(pre_capture[0] + 1) + " " + str(pre_capture[1] + 1) + " "
                pre_c = [pre_capture[0], pre_capture[1]]
                set_pre_captures.append(pre_c)
    if max_pre_capt == 0:
        str_answer = "N"
    return str_answer


def print_result(white, black):
    with open("output.txt", "w") as file:
        file.write(white + "\n" + black)


def main():
    initialize_field()
    fill_field()
    check_bests()
    white_result = create_result(white_pre_captures)
    black_result = create_result(black_pre_captures)
    print_result(white_result, black_result)


if __name__ == '__main__':
    main()
