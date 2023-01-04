import random

numbers = []
for i in range(6):
    number = random.randint(1, 60)
    numbers.append(number)

for number in numbers:
    if number in [19, 7, 8, 9, 13, 21, 39, 44, 54, 28, 48]:
        if random.randint(1, 10) <= 3:
            numbers.append(number)

print(numbers)
