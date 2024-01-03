import random
import csv
import math


def minus_type_1_problem_maker(trial):
    total_array = []
    j = 0
    while j < trial:
        array = []
        num1 = round((7 * random.random()) ** 2 * (2 * random.random() > 0.5 - 1))
        num2 = round((7 * random.random()) ** 2 * (2 * random.random() > 0.5 - 1))

        str_num_1 = '+' + str(num1) if num1 > 0 else str(num1)
        str_num_2 = '+' + str(num2) if num2 > 0 else str(num2)

        array.append("(" + str_num_1 + ")" + "-" + "(" + str_num_2 + ")={\msquare}")
        array.append(num1 - num2)

        if array not in total_array:
            total_array.append(array)
            j += 1

    return total_array


def multiply_type_1_problem_maker(trial):
    total_array = []
    j = 0
    while j < trial:
        array = []
        num1 = math.ceil((4 * random.random()) ** 2) * (1 if random.random() > 0.5 else -1)
        num2 = math.ceil((4 * random.random()) ** 2) * (1 if random.random() > 0.5 else -1)

        str_num_1 = '+' + str(num1) if num1 > 0 else str(num1)
        str_num_2 = '+' + str(num2) if num2 > 0 else str(num2)

        array.append("(" + str_num_1 + ")" + "×" + "(" + str_num_2 + ")={\msquare}")
        array.append(num1 * num2)

        if array not in total_array:
            total_array.append(array)
            j += 1

    return total_array


result = multiply_type_1_problem_maker(50)


with open("minus_type_1.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv,delimiter=',')
    csvWriter.writerows(result)