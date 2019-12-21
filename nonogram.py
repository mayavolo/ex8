def verify_blacks(new_row, total_black):
    blacks = 0
    for i in range(len(new_row)):
        if new_row[i] == 1:
            blacks += 1
    if blacks > total_black:
        return False
    return True


def add_allowed_row(allowed_rows, new_rows, total_black):
    for k in range(len(new_rows)):
        already_there = False
        for j in range(len(allowed_rows)):
            if allowed_rows[j] == new_rows[k]:
                already_there = True
                continue
        if not already_there:
            if verify_blacks(new_rows[k], total_black):
                allowed_rows.append(new_rows[k])

    return allowed_rows


def get_row_variations(row, blocks):
    if len(blocks) == 0 or len(row) == 0:
        return [paint_white(row, 0)]

    total_black = sum_black(blocks)
    return get_row_variations_inner(row, blocks, 0, True, total_black)


def get_row_variations_inner(row: list, blocks: list, index, is_clean, total_black):
    # print(f"row: {row}, blocks: {blocks}, index: {index}, is_clean: {is_clean}")
    row_copy = row.copy()
    if len(blocks) == 1 and blocks[0] == 0 and index <= len(row):
        return [paint_white(row_copy, index)]

    if index >= len(row) and ((len(blocks) != 0 and blocks[0] != 0) or len(blocks) > 1):
        return None
    if not is_clean and row[index] == 0 and blocks[0] != 0:
        return None
    if blocks[0] == 0 and row[index] == 1 and blocks[0] != 0:
        return None

    must_be_white = False
    if blocks[0] == 0:
        blocks = blocks.copy()[1:]
        is_clean = True
        must_be_white = True

    allowed_rows = []
    if row_copy[index] == 1:
        blocks_copy = blocks.copy()
        blocks_copy[0] -= 1
        inner_rows = get_row_variations_inner(row_copy, blocks_copy, index + 1, False, total_black)
        if inner_rows:
            allowed_rows = add_allowed_row(allowed_rows, inner_rows, total_black)

    if row_copy[index] == -1:
        if is_clean:
            blocks_copy = blocks.copy()
            row_inner_copy = row_copy.copy()
            row_inner_copy[index] = 0
            inner_rows = get_row_variations_inner(row_inner_copy, blocks_copy, index + 1, is_clean, total_black)
            if inner_rows:
                allowed_rows = add_allowed_row(allowed_rows, inner_rows, total_black)

        if not must_be_white:
            row_inner_copy = row_copy.copy()
            row_inner_copy[index] = 1
            blocks_copy = blocks.copy()
            blocks_copy[0] -= 1
            inner_rows = get_row_variations_inner(row_inner_copy, blocks_copy, index + 1, False, total_black)
            if inner_rows:
                allowed_rows = add_allowed_row(allowed_rows, inner_rows, total_black)

    if row_copy[index] == 0:
        blocks_copy = blocks.copy()
        inner_rows = get_row_variations_inner(row_copy, blocks_copy, index + 1, is_clean, total_black)
        if inner_rows:
            allowed_rows = add_allowed_row(allowed_rows, inner_rows, total_black)

    return allowed_rows


def paint_white(row, index):
    for i in range(index, len(row)):
        if row[i] == -1:
            row[i] = 0
    return row


def get_intersection_row(rows):
    if len(rows) == 0:
        return []

    intersection_list = []
    for index in range(len(rows[0])):
        start = rows[0][index]
        same = True
        for row in rows:
            if row[index] != start:
                same = False
        if same:
            intersection_list.append(start)
        else:
            intersection_list.append(-1)
    return intersection_list


def get_a_column(board, col_index):
    new_col = []
    for row in board:
        new_col.append(row[col_index])
    return new_col


def make_columns_into_rows(columns):
    board = []
    for k in range(len(columns[0])):
        row = []
        for i in range(len(columns)):
            row.append(columns[i][k])
        board.append(row)
    return board


def conclude_constrains_from_rows_and_columns(sorted_columns_board, sorted_rows_board, board):
    conclusive = True
    something_changed = False
    for row in range(len(sorted_rows_board)):
        for col in range(len(sorted_rows_board[0])):
            prev = board[row][col]
            if sorted_rows_board[row][col] == -1:
                board[row][col] = sorted_columns_board[row][col]
            else:
                board[row][col] = sorted_rows_board[row][col]
            if board[row][col] == -1:
                conclusive = False
            if prev != board[row][col]:
                something_changed = True

    if not something_changed:
        conclusive = True
    return conclusive


# def conclude_constrains_from_rows_and_columns(sorted_columns_board, sorted_rows_board):
#     final_board = sorted_rows_board.copy()
#     for row in range(len(sorted_rows_board)):
#         for col in range(len(sorted_rows_board[0])):
#             if sorted_rows_board[row][col] == -1:
#                 final_board[row][col] = sorted_columns_board[row][col]
#     return final_board

def sum_black(blocks):
    sum = 0;
    for i in range(len(blocks)):
        sum += blocks[i]
    return sum


def conclude_from_constraints(board, constraints):
    if len(board) == 0:
        return None

    conclusive = False

    while not conclusive:

        sorted_rows_board = board.copy()
        all_columns = []
        for row_index in range(len(board)):
            starting_rows = get_row_variations(board[row_index], constraints[0][row_index])
            semi_final_row = get_intersection_row(starting_rows)
            sorted_rows_board[row_index] = semi_final_row

        for col_index in range(len(board[0])):
            col = get_a_column(board, col_index)
            starting_columns = get_row_variations(col, constraints[1][col_index])
            semi_final_col = get_intersection_row(starting_columns)
            all_columns.append(semi_final_col)
        sorted_col_board = make_columns_into_rows(all_columns)

        conclusive = conclude_constrains_from_rows_and_columns(sorted_col_board, sorted_rows_board, board)
        print(f'the board is: {board}')

    return None

# conclude_from_constraints([[-1, -1, -1, -1, -1, -1]], [[[2, 1]], [[], [1], [1], [], [1], []]])
# conclude_constrains_from_rows_and_columns(
#     [[-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, -1]],
#     )
# res = get_row_variations([-1, 1, 1, 1, 0], [4])
# print(res)
# print(get_intersection_row(res))
# for i in range(len(res)):
#    print(res[i])
