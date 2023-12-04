import random
import csv

def option_maker_A(num):
    rand = random.random()
    if rand <= 0.25:
        return [num, num + 1, num + 2, num + 3]
    elif rand <= 0.5:
        return [num - 1, num, num + 1, num + 2]
    elif rand <= 0.75:
        return [num - 2, num - 1, num, num + 1]
    else:
        return [num - 3, num - 2, num - 1, num]

# 1.2 square problem
def exponentiation_type_1_problem_maker(trial):
    total_array = []
    j = 0
    while j < trial:
        array = []
        number = random.randrange(2, 30)
        power = random.randrange(2, 7)

        string = f"{number}"

        for i in range(power-1):
            string += f' \\times {number}'

        string += ' = {\msquare} ^ {\ssquare}'
        array.append(string)
        array.append(str(number) + ", " + str(power))
        array.append("[" + str(option_maker_A(number)) + ', ' + str(option_maker_A(power)) + ']')

        if array not in total_array:
            total_array.append(array)
            j += 1

    return total_array

def exponentiation_type_2_problem_maker(trial):
    total_array = []
    j = 0
    while j < trial:
        array = []
        number = random.randrange(2, 10)
        power = random.randrange(2, 11)

        if number ** power > 1100:
            continue

        opt = option_maker_A(power)

        if opt[0] <= 0:
            continue

        string = f"{number ** power}"
        array.append(string + "=" + f"{number}" + "^{\ssquare}")
        array.append(power)
        array.append(str(opt))

        if array not in total_array:
            total_array.append(array)
            j += 1
    return total_array


def exponentiation_type_3_problem_maker(trial):
    total_array = []
    j = 0
    while j < trial:
        array = []
        number = random.randrange(2, 20)
        power = random.randrange(2, 11)

        if number ** power > 1100:
            continue

        string = f"{number ** power}"
        array.append(string + "=" + "{\msquare}" + "^{\ssquare}")
        array.append(str(number) + ', ' + str(power))

        if array not in total_array:
            total_array.append(array)
            j += 1
    return total_array


# main
result = exponentiation_type_3_problem_maker(25)

with open("exponentiation_type_3.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(result)