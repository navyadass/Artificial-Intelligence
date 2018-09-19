import sys

# Reading Input from the file
inputFile = open("input.txt", "r")
# inputFile = open(sys.argv[2], "r")

outputFile = open("output.txt", "w")

day = inputFile.readline().strip().upper()

player = inputFile.readline().strip().upper()

region_list = inputFile.readline().strip().upper()[1:-1].split("),(")
y = 0
for x in region_list:
    region_list[y] = x.split(',')
    y = y + 1
region_length = len(region_list)

adj_mat = []
for x in range(0, region_length):
    temp = inputFile.readline().strip()[1:-1]
    adj_mat.append(temp.split(","))

regions_so_far = inputFile.readline().strip().upper().split(",")

max_depth = int(inputFile.readline().strip().upper())

heuristic_values = []
final_best_move = []
final_utilities = []
alpha = float('-inf')
beta = float('inf')
# End of reading

# All Functions


def calculate_heuristic():
    total_regions = 0
    for r in region_list:
        total_regions = total_regions + float(r[1])
    total_regions = total_regions / region_length
    for l in range(0, region_length):
        region_list[l][1] = (total_regions + float(region_list[l][1])) / 2


def get_profit(region):
    r = None
    for r in range(0, region_length):
        if region_list[r][0] == region:
            break
    return region_list[r][1]


def get_opponent(curr):
    if curr == "R1":
        return "R2"
    else:
        return "R1"


def get_index(region):
    i = None
    for i in range(0, region_length):
        if region_list[i][0] == region:
            break
    return i


def get_available_regions(visited, last_move):
    possible_choices = []
    if last_move == "PASS":
        possible_choices = []
    elif last_move is None:
        for r in range(0, region_length):
            if region_list[r][0] in visited:
                continue
            else:
                possible_choices.append(region_list[r][0])
    else:
        cur_mov = get_index(last_move)
        for r in range(0, region_length):
            if region_list[r][0] in visited:
                continue
            else:
                if adj_mat[r][cur_mov] == "1":
                    possible_choices.append(region_list[r][0])
    return possible_choices


def get_last_move(current_player, r1_v, r2_v):
    if current_player == "R1":
        if len(r1_v) == 0:
            last_move = None
        else:
            last_move = r1_v[-1]
    else:
        if len(r2_v) == 0:
            last_move = None
        else:
            last_move = r2_v[-1]
    return last_move


def compare(reg1, reg2):
    if reg1 == "PASS":
        return 0
    elif reg2 == "PASS":
        return 1

    if get_index(reg1) <= get_index(reg2):
        return 1
    elif get_index(reg2) < get_index(reg1):
        return 0


def max_cal(visited, current_player, r1_v, r1_u, r2_v, r2_u, depth, alpha, beta):
    available_regions = get_available_regions(visited, get_last_move(current_player, r1_v, r2_v))
    best_move = []
    r1_v_c = r1_v[:]
    r1_u_c = r1_u
    r2_v_c = r2_v[:]
    r2_u_c = r2_u
    visited_c = visited[:]
    if len(available_regions) == 0:
        if current_player == "R1":
            if r1_v[:-1] != "PASS":
                r1_v.append("PASS")
                r1_v_c = r1_v[:]
        else:
            if r2_v[:-1] != "PASS":
                r2_v.append("PASS")
                r2_v_c = r2_v[:]
        if (depth == 0) or (r1_v[-1] == "PASS" and r2_v[-1] == "PASS"):
            best_move.append("PASS")
            if player == "R1":
                best_move.append(r1_u)
            else:
                best_move.append(r2_u)
            final_utilities.append(int(round(best_move[1])))
        else:
            score = min_cal(visited_c, get_opponent(current_player), r1_v_c, r1_u_c, r2_v_c, r2_u_c, depth - 1, alpha*1, beta*1)
            best_move.append("PASS")
            best_move.append(score[1])
            if score[1] > alpha:
                alpha = score[1]
        return best_move
    else:
        for ar in available_regions:
            r1_v_c = r1_v[:]
            r1_u_c = r1_u
            r2_v_c = r2_v[:]
            r2_u_c = r2_u
            visited_c = visited[:]
            visited_c.append(ar)
            if current_player == "R1":
                r1_v_c.append(ar)
                r1_u_c = r1_u_c + float(get_profit(ar))
            else:
                r2_v_c.append(ar)
                r2_u_c = r2_u_c + float(get_profit(ar))
            if depth == 0:
                if player == "R1":
                    value1 = r1_u_c
                else:
                    value1 = r2_u_c
                if len(best_move) == 0:
                    best_move.append(ar)
                    best_move.append(value1)
                elif value1 > best_move[1]:
                    best_move[0] = ar
                    best_move[1] = value1
                final_utilities.append(int(round(value1)))
                if player == 'R1' and r1_u_c > alpha :
                    alpha = r1_u_c
                elif player == 'R2' and r2_u_c > alpha  :
                    alpha = r2_u_c
                if alpha >= beta:
                    break
            else:
                score = min_cal(visited_c, get_opponent(current_player), r1_v_c, r1_u_c, r2_v_c, r2_u_c, depth - 1, alpha*1, beta*1)
                if len(best_move) == 0:
                    best_move.append(ar)
                    best_move.append(score[1])
                elif score[1] > best_move[1]:
                    best_move[0] = ar
                    best_move[1] = score[1]
                elif score[1] == best_move[1]:
                    if compare(ar, best_move[0]) == 1:
                        best_move[0] = ar
                        best_move[1] = score[1]
                if score[1] > alpha:
                    alpha = score[1]
                if alpha >= beta:
                    break
        return best_move


def min_cal(visited, current_player, r1_v, r1_u, r2_v, r2_u, depth, alpha, beta):
    available_regions = get_available_regions(visited, get_last_move(current_player, r1_v, r2_v))
    best_move = []
    r1_v_c = r1_v[:]
    r1_u_c = r1_u
    r2_v_c = r2_v[:]
    r2_u_c = r2_u
    visited_c = visited[:]
    if len(available_regions) == 0:
        if current_player == "R1":
            if r1_v[:-1] != "PASS":
                r1_v.append("PASS")
                r1_v_c = r1_v[:]
        else:
            if r2_v[:-1] != "PASS":
                r2_v.append("PASS")
                r2_v_c = r2_v[:]
        if (depth == 0) or (r1_v[-1] == "PASS" and r2_v[-1] == "PASS"):
            best_move.append("PASS")
            if player == "R1":
                best_move.append(r1_u)
            else:
                best_move.append(r2_u)
            final_utilities.append(int(round(best_move[1])))
        else:
            score = max_cal(visited_c, get_opponent(current_player), r1_v_c, r1_u_c, r2_v_c, r2_u_c, depth - 1, alpha*1, beta*1)
            best_move.append("PASS")
            best_move.append(score[1])
            if score[1] < beta:
                beta = score[1]
        return best_move
    else:
        for ar in available_regions:
            r1_v_c = r1_v[:]
            r1_u_c = r1_u
            r2_v_c = r2_v[:]
            r2_u_c = r2_u
            visited_c = visited[:]
            visited_c.append(ar)
            if current_player == "R1":
                r1_v_c.append(ar)
                r1_u_c = r1_u_c + float(get_profit(ar))
                value1 = r1_u_c
            else:
                r2_v_c.append(ar)
                r2_u_c = r2_u_c + float(get_profit(ar))
                value1 = r2_u_c
            if depth == 0:
                if player == "R1":
                    value1 = r1_u_c
                else:
                    value1 = r2_u_c
                if len(best_move) == 0:
                    best_move.append(ar)
                    best_move.append(value1)
                elif value1 < best_move[1]:
                    best_move[0] = ar
                    best_move[1] = value1
                final_utilities.append(int(round(value1)))
                if player == 'R1' and r1_u_c < beta :
                    beta = r1_u_c
                elif player == 'R2' and r2_u_c < beta :
                    beta = r2_u_c
                if alpha >= beta:
                    break
            else:
                score = max_cal(visited_c, get_opponent(current_player), r1_v_c, r1_u_c, r2_v_c, r2_u_c, depth - 1, alpha*1, beta*1)
                if len(best_move) == 0:
                    best_move.append(ar)
                    best_move.append(score[1])
                elif score[1] < best_move[1]:
                    best_move[0] = ar
                    best_move[1] = score[1]
                elif score[1] == best_move[1]:
                    if compare(ar, best_move[0]) == 1:
                        best_move[0] = ar
                        best_move[1] = score[1]
                if score[1] < beta:
                    beta = score[1]
                if alpha >= beta:
                    break
        return best_move


# End of Functions

# Code


if day == "YESTERDAY":
    calculate_heuristic()

r1_visited = []
r1_utility = 0
r2_visited = []
r2_utility = 0
if regions_so_far[0] != "*":
    curr_player = player
    regions_visited = regions_so_far

    for v in range(len(regions_visited), 0, -1):
        curr_player = get_opponent(curr_player)
        if curr_player == "R1":
            r1_visited.insert(0, regions_visited[-1])
            regions_visited = regions_visited[:-1]
        else:
            r2_visited.insert(0, regions_visited[-1])
            regions_visited = regions_visited[:-1]

    if len(r1_visited) != 0:
        for u in range(0, len(r1_visited)):
            r1_utility = r1_utility + float(get_profit(r1_visited[u]))

    if len(r2_visited) != 0:
        for u in range(0, len(r2_visited)):
            r2_utility = r2_utility + float(get_profit(r2_visited[u]))
    max_depth = max_depth - len(regions_so_far)
else:
    regions_so_far = []


if max_depth >= 0:
    ava_regions = get_available_regions(regions_so_far, get_last_move(player, r1_visited, r2_visited))
    if len(ava_regions) == 0:
        if player == "R1":
            r1_visited.append("PASS")
        else:
            r2_visited.append("PASS")

        if max_depth == 0:
            final_best_move.append("PASS")
            if player == "R1":
                final_best_move.append(r1_utility)
            else:
                final_best_move.append(r2_utility)
            final_utilities.append(int(round(final_best_move[1])))
        else:
            final_score = max_cal(regions_so_far, get_opponent(player), r1_visited, r1_utility, r2_visited, r2_utility,
                                  max_depth - 1, alpha*1, beta*1)
            final_best_move.append("PASS")
            final_best_move.append(final_score[1])
    else:
        for arl in ava_regions:
            r1_visited_c = r1_visited[:]
            r1_utility_c = r1_utility
            r2_visited_c = r2_visited[:]
            r2_utility_c = r2_utility
            regions_so_far_c = regions_so_far[:]
            regions_so_far_c.append(arl)
            if player == "R1":
                r1_visited_c.append(arl)
                r1_utility_c = r1_utility_c + float(get_profit(arl))
            else:
                r2_visited_c.append(arl)
                r2_utility_c = r2_utility_c + float(get_profit(arl))

            if max_depth == 0:
                value = 0
                if player == "R1":
                    value = r1_utility_c
                else:
                    value = r2_utility_c
                if len(final_best_move) == 0:
                    final_best_move.append(arl)
                    final_best_move.append(value)
                else:
                    if value > int(final_best_move[1]):
                        final_best_move[0] = arl
                        final_best_move[1] = value
                if alpha >= beta :
                    break
                final_utilities.append(int(round(value)))
            else:
                final_score = min_cal(regions_so_far_c, get_opponent(player), r1_visited_c, r1_utility_c, r2_visited_c,
                                      r2_utility_c, max_depth - 1, alpha*1, beta*1)
                if final_score[1] > alpha :
                    alpha = final_score[1]
                if alpha >= beta :
                    break
                if len(final_best_move) == 0:
                    final_best_move.append(arl)
                    final_best_move.append(final_score[1])
                elif int(final_score[1]) > int(final_best_move[1]):
                    final_best_move[0] = arl
                    final_best_move[1] = final_score[1]
                elif int(final_score[1]) == int(final_best_move[1]):
                    if compare(arl, final_best_move[0]) == 1:
                        final_best_move[0] = arl
                        final_best_move[1] = final_score[1]

    outputFile.write(final_best_move[0]+"\n")
    for utilities in range(0, len(final_utilities)):
        outputFile.write(str(final_utilities[utilities]))
        if utilities != len(final_utilities)-1:
            outputFile.write(",")
