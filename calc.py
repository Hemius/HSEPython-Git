from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CalcState:
    ans: float = 0.0
    mem: float = 0.0
    history: List[str] = field(default_factory=list)
    history_limit: int = 10


def parse_number(token: str, state: CalcState) -> Optional[float]:
    """
    Возвращает число, если token можно преобразовать.
    Поддерживает ANS и MR.
    """
    token_up = token.strip().upper()

    if token_up == "ANS":
        return state.ans
    if token_up == "MR":
        return state.mem

    try:
        # Поддержка запятой как десятичного разделителя
        return float(token.replace(",", "."))
    except ValueError:
        return None


def compute(a: float, op: str, b: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("деление на ноль")
        return a / b
    if op == "**":
        return a ** b
    if op == "%":
        if b == 0:
            raise ZeroDivisionError("деление на ноль")
        return a % b

    raise ValueError("неизвестная операция")


def add_history(state: CalcState, line: str) -> None:
    state.history.append(line)
    if len(state.history) > state.history_limit:
        state.history = state.history[-state.history_limit:]


def print_help() -> None:
    print(
        "Команды:\n"
        "  <a> <op> <b>     вычисление, например: 10 + 5, ANS * 2, MR - 3\n"
        "  M+ <x>           прибавить x к памяти (x может быть ANS)\n"
        "  M- <x>           вычесть x из памяти\n"
        "  MR              показать память\n"
        "  MC              очистить память\n"
        "  ANS             показать последний ответ\n"
        "  history [N]      показать историю (по умолчанию 10)\n"
        "  help             подсказка\n"
        "  q                выход\n\n"
        "Операции: +  -  *  /  **  %"
    )


def show_history(state: CalcState, n: Optional[int] = None) -> None:
    if not state.history:
        print("История пуста.\n")
        return

    if n is None:
        n = state.history_limit

    tail = state.history[-max(0, n):]
    for i, item in enumerate(tail, start=max(1, len(state.history) - len(tail) + 1)):
        print(f"{i}) {item}")
    print()


def main() -> None:
    state = CalcState()

    print("Калькулятор с ANS, памятью и историей.")
    print("Напиши 'help' для списка команд.\n")

    while True:
        raw = input("> ").strip()
        if not raw:
            continue

        cmd = raw.strip().lower()

        if cmd in {"q", "quit", "exit"}:
            break

        if cmd in {"help", "h", "?"}:
            print_help()
            print()
            continue

        # Показать ANS / MR / MC
        if raw.strip().upper() == "ANS":
            print(state.ans, "\n")
            continue

        if raw.strip().upper() == "MR":
            print(state.mem, "\n")
            continue

        if raw.strip().upper() == "MC":
            state.mem = 0.0
            print("Memory cleared.\n")
            continue

        # История
        parts = raw.split()
        if parts and parts[0].lower() == "history":
            n = None
            if len(parts) >= 2:
                try:
                    n = int(parts[1])
                except ValueError:
                    print("Ошибка: history принимает число, например: history 5\n")
                    continue
            show_history(state, n)
            continue

        # Память M+/M-
        if parts and parts[0].upper() in {"M+", "M-"}:
            if len(parts) != 2:
                print("Ошибка: формат команд памяти: M+ <x> или M- <x>\n")
                continue

            val = parse_number(parts[1], state)
            if val is None:
                print("Ошибка: не могу распознать число. Используй число, ANS или MR.\n")
                continue

            if parts[0].upper() == "M+":
                state.mem += val
            else:
                state.mem -= val

            print(f"Memory: {state.mem}\n")
            continue

        # Вычисления: "<a> <op> <b>"
        if len(parts) == 3:
            a = parse_number(parts[0], state)
            op = parts[1]
            b = parse_number(parts[2], state)

            if a is None or b is None:
                print("Ошибка: неверные числа. Можно использовать ANS и MR.\n")
                continue

            try:
                result = compute(a, op, b)
            except ZeroDivisionError as e:
                print(f"Ошибка: {e}\n")
                continue
            except ValueError as e:
                print(f"Ошибка: {e}\n")
                continue

            state.ans = result
            line = f"{a} {op} {b} = {result}"
            add_history(state, line)

            print(result, "\n")
            continue

        print("Не понял команду. Напиши 'help' для примеров.\n")


if __name__ == "__main__":
    main()
