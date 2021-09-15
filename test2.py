def process(n):
    num = [char for char in str(n)]
    count = 0
    for i in num:
        count += int(i) ** len(num)
    if count == n:
        print(n)

for i in range(10, 999):
    process(i)