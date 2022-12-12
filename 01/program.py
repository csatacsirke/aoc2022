

lines = None
with open("input.txt") as file:
    lines = file.readlines()


elves = [0]
for line in lines:
    if len(line.strip()) == 0:
        elves.append(0)
    else:
        elves[-1] = elves[-1] + int(line)



max = elves[0]
maxind = 0


for i in range(1, len(elves)):
    if elves[i] > max:
        max =  elves[i]
        maxind = i

print(max)


elves.sort()

print(elves[-1] + elves[-2] + elves[-3])