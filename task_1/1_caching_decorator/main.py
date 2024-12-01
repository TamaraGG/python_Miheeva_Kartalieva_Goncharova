from caching_decorator import caching_decorator

@caching_decorator(max_cache_size=3)
def multiply(a, b):
    # Имитация долгого вычисления
    from time import sleep
    sleep(2)
    return a * b

@caching_decorator(max_cache_size=2)
def add(a, b):
    # Другая функция с долгим вычислением
    from time import sleep
    sleep(1)
    return a + b

if __name__ == "__main__":
    print(multiply(2, 3))  # Вычисление результата
    print(multiply(2, 3))  # Повторный вызов, берется из кэша
    print(multiply(4, 5))  # Новый вызов
    print(multiply(6, 7))  # Новый вызов, кэш переполняется
    print(multiply(2, 3))  # Старое значение удалено, пересчет

    print(add(1, 2))       # Вычисление результата
    print(add(3, 4))       # Новый вызов
    print(add(1, 2))       # Берется из кэша
    print(add(5, 6))       # Новый вызов, кэш переполняется
    print(add(3, 4))       # Берется из кэша
    print(add(1, 2))       # Старое значение удалено, пересчет
