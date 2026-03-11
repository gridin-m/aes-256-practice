"""
# todo пока что неправильно)
if __name__ == "__main__":
    test = list(range(16))
    s = bytes_to_state(test)
    print("Матрица:")
    for row in s:
        print(row)
    b = state_to_bytes(s)
    print(f"Обратно: {b}")
    assert bytes(test) == b, "ошибка преобразлвания"
    print("преобразования происходят корректно")
"""