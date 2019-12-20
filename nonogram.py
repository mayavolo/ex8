def add_allowed_row(allowed_rows, new_rows):
    for k in range(len(new_rows)):
        already_there = False
        for j in range(len(allowed_rows)):
            if allowed_rows[j] == new_rows[k]:
                already_there = True
                continue
        if not already_there:
            allowed_rows.append(new_rows[k])

    return allowed_rows


def get_row_variations(row, blocks):
    if len(blocks) == 0 or len(row) == 0:
        return [paint_white(row, 0)]

    return get_row_variations_inner(row, blocks, 0, True)


def get_row_variations_inner(row: list, blocks: list, index, is_clean):
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
        inner_rows = get_row_variations_inner(row_copy, blocks_copy, index + 1, False)
        if inner_rows:
            allowed_rows = add_allowed_row(allowed_rows, inner_rows)

    if row_copy[index] == -1:
        if is_clean:
            blocks_copy = blocks.copy()
            row_inner_copy = row_copy.copy()
            row_inner_copy[index] = 0
            inner_rows = get_row_variations_inner(row_inner_copy, blocks_copy, index + 1, is_clean)
            if inner_rows:
                allowed_rows = add_allowed_row(allowed_rows, inner_rows)

        if not must_be_white:
            row_inner_copy = row_copy.copy()
            row_inner_copy[index] = 1
            blocks_copy = blocks.copy()
            blocks_copy[0] -= 1
            inner_rows = get_row_variations_inner(row_inner_copy, blocks_copy, index + 1, False)
            if inner_rows:
                allowed_rows = add_allowed_row(allowed_rows, inner_rows)

    if row_copy[index] == 0:
        blocks_copy = blocks.copy()
        inner_rows = get_row_variations_inner(row_copy, blocks_copy, index + 1, is_clean)
        if inner_rows:
            allowed_rows = add_allowed_row(allowed_rows, inner_rows)

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


def conclude_from_constraints(board, constraints):
    if len(board) == 0:
        return None

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

    for j in range(len(board)):
        comparison_rows = [sorted_rows_board[j], sorted_col_board[j]]
        final_row = get_intersection_row(comparison_rows)
        board[j] = final_row

    return None


# conclude_from_constraints([[-1, -1, -1, -1, -1, -1]],[[[2, 1]], [[], [1], [1], [], [1], []]])


# res = get_row_variations([-1, -1, -1, -1, -1, -1, -1, -1], [2, 3, 1])
# for i in range(len(res)):
#    print(res[i])






