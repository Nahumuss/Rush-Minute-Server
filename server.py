with open('levels.txt', 'r') as levels:
    boards = [line[3:40] for line in levels.readlines()]

print(boards[5])