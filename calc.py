def calc(a, op, b):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        if b == 0:
            return "Ошибка: деление на ноль"
        return a / b
    elif op == "**":
        return a ** b
    elif op == "%":
        if b == 0:
            return "Ошибка: деление на ноль"
        return a % b
    else:
        return "Ошибка: неизвестная операция"


print("Калькулятор. Операции: +  -  *  /  **  %")
print("Чтобы выйти: введите 'q'\n")

while True:
    a_inp = input("Введите первое число: ")
    if a_inp.lower() == "q":
        break

    op = input("Введите операцию: ")
    if op.lower() == "q":
        break

    b_inp = input("Введите второе число: ")
    if b_inp.lower() == "q":
        break

    try:
        a = float(a_inp)
        b = float(b_inp)
    except ValueError:
        print("Ошибка: нужно вводить числа.\n")
        continue

    result = calc(a, op, b)
    print("Результат:", result, "\n")
