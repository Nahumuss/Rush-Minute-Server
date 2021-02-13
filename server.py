boards = []
with open('levels.txt', 'r') as levels:
    for line in levels.readlines():
        boards.append(line[4:40])

games = []