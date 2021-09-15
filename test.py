def makedir(n):
    dir = {}
    for i in range(n):
        dir[i] = True
    return dir

def oneLeft(dir) -> bool:
    count = 0
    for i in dir:
        if dir[i]:
            count += 1
    return count == 1

def process(dir):
    kill = False
    while not oneLeft(dir):
        for i in dir:
            if dir[i]:
                if not kill:
                    kill = True
                else:
                    dir[i] = False
                    kill = False
    for i in dir:
        if dir[i]:
            return i + 1

for i in range(1, 2 ** 10):
    print(process(makedir(i)), "|", i)