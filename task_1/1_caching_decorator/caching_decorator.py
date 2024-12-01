import functools
from collections import OrderedDict


def caching_decorator(max_cache_size=None):
    """
    Декоратор для кэширования результатов выполнения функции с возможностью задания глубины кэша.

    :param max_cache_size: Максимальное количество элементов в кэше (None - без ограничения).
    """

    def decorator(func):
        cache = OrderedDict()  # Для сохранения порядка добавления элементов

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                # Перемещаем используемый элемент в конец (как недавно использованный)
                cache.move_to_end(key)
                print(f"Fetching from cache for {func.__name__}: {key}")
                return cache[key]
            else:
                print(f"Computing result for {func.__name__}: {key}")
                result = func(*args, **kwargs)
                cache[key] = result
                # Если кэш превышает максимальный размер, удаляем самый старый элемент
                if max_cache_size is not None and len(cache) > max_cache_size:
                    oldest_key = next(iter(cache))
                    print(f"Removing oldest cached result: {oldest_key}")
                    cache.pop(oldest_key)
                return result

        def clear_cache():
            nonlocal cache
            cache.clear()
            print(f"Cache cleared for {func.__name__}")

        wrapper.clear_cache = clear_cache
        return wrapper

    return decorator
