import csv
import random


def prime_factors(n):
    factors = []
    # 2부터 n까지의 소수 중에서만 검사
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def count_elements(lst):
    element_count = {}
    for element in lst:
        if element in element_count:
            element_count[element] += 1
        else:
            element_count[element] = 1
    return element_count


def factorization(num):
    result = count_elements(prime_factors(num))
    return result


def greatest_common_factor(num1, num2):
    fac1 = factorization(num1)
    fac2 = factorization(num2)
    gcd = 1

    for divisor1 in fac1.keys():
        value = min(fac1[divisor1], fac2[divisor1]) if divisor1 in fac2.keys() else 0
        gcd *= divisor1 ** value

    return gcd

def greatest_common_factor_3(num1, num2, num3):
    return greatest_common_factor(num3, greatest_common_factor(num1, num2))


# 1.1 Prime Number
def prime_number_problem_maker(num):
    if len(prime_factors(num)) == 1:
        prime = 1
    else:
        prime = 0
    if prime:
        string1 = "    \item $"
        string2 = "$\n    \\begin{enumerate}\n        \item Prime*\n        \item Composite\n    \end{enumerate}"
    else:
        string1 = "    \item $"
        string2 = "$\n    \\begin{enumerate}\n        \item Prime\n        \item Composite*\n    \end{enumerate}"

    print(string1 + str(num) + string2)



# 1.7 Greatest Common Factor Type 1
def greatest_common_factor_problems_maker(trial):
    record = []
    total_array = []
    while len(total_array) < trial:
        array = []
        g = random.randrange(2, 16)
        parts1 = random.randrange(1, 10)
        parts2 = random.randrange(1, 10)
        if parts1 != parts2 and (g*parts1, g*parts2) not in record:
            num1 = g * min(parts1, parts2)
            num2 = g * max(parts1, parts2)
            record.append((num1, num2))

            gcd = greatest_common_factor(num1, num2)

            array.append(f"Find the greatest common factor of {num1} and {num2}")
            array.append(str(gcd))
        if array:
            total_array.append(array)
    return total_array


# 1.7.2 Common Factor Type 2
def greatest_common_factor_problems_maker2(trial):
    record = []
    total_array = []
    while len(record) < trial:
        array = []
        g = 1
        parts1 = random.randrange(10, 50)
        parts2 = random.randrange(10, 50)
        if parts1 != parts2 and (g*parts1, g*parts2) not in record and greatest_common_factor(g*parts1, g*parts2) == 1:
            num1 = g * min(parts1, parts2)
            num2 = g * max(parts1, parts2)
            record.append((num1, num2))

            gcd = greatest_common_factor(num1, num2)

            gcd = greatest_common_factor(num1, num2)

            array.append(f"Find the greatest common factor of {num1} and {num2}")
            array.append(str(gcd))
        if array:
            total_array.append(array)
    return total_array


def greatest_common_factor_3_problems_maker(trial):
    record = []
    total_array = []
    while len(total_array) < trial:
        array = []
        g = random.randrange(1, 16)
        parts1 = random.randrange(1, 10)
        parts2 = random.randrange(1, 10)
        parts3 = random.randrange(1, 10)
        num1 = g * parts1
        num2 = g * parts2
        num3 = g * parts3
        if len({parts1, parts2, parts3}) == 3 and (num1, num2, num3) not in record:
            record.append({num1, num2, num3})

            gcd = greatest_common_factor_3(num1, num2, num3)

            array.append(f"Find the greatest common factor of {num1}, {num2} and {num3}")
            array.append(str(gcd))

        if array:
            total_array.append(array)
    return total_array



# main
result = greatest_common_factor_3_problems_maker(50)

with open("gcd_problem.csv", "w+") as my_csv:
    csvWriter = csv.writer(my_csv, delimiter= ',')
    csvWriter.writerows(result)