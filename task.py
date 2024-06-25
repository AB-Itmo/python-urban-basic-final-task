import csv


INPUT_FILE_HOUSING = "housing_data.csv"
SMALL = 5
MEDIUM = 16


def read_file(filename: str) -> list[dict]:
    """Читает данные из CSV файла и преобразует их в список словарей.

    :param filename: Название файла, содержащего данные.
    :return: Список словарей с данными о домах.
    """
    with open(filename, encoding="utf-8") as f_i:
        reader = csv.DictReader(f_i)
        data = list(reader)
    for row in data:
        row["floor_count"] = int(row["floor_count"])
        row["population"] = int(row["population"])
        row["heating_value"] = float(row["heating_value"])
        row["area_residential"] = float(row["area_residential"])
    return data


def classify_house(floor_count: int) -> str:
    """Классифицирует дом на основе количества этажей.

    Проверяет, является ли количество этажей целым числом и положительным значением.
    Возвращает категорию дома в зависимости от количества этажей.

    :param floor_count: Количество этажей в доме.
    :return: Категория дома в виде строки:
        "Малоэтажный", "Среднеэтажный" или "Многоэтажный".
    """
    # Ловим ошибки
    if not isinstance(floor_count, int):
        error_str = f"Число этажей {floor_count} должно быть целочисленным значением"
        raise TypeError(error_str)
    if floor_count <= 0:
        error_str = f"Число этажей {floor_count} должно быть положительным значением"
        raise ValueError(error_str)
    # Возвращаем категорию
    if 0 < floor_count <= SMALL:
        return "Малоэтажный"
    if SMALL < floor_count <= MEDIUM:
        return "Среднеэтажный"
    return "Многоэтажный"


def get_classify_houses(houses: list[dict]) -> list[str]:
    """Классифицирует дома на основе количества этажей.

    :param houses: Список словарей с данными о домах.
    :return: Список категорий домов.
    """
    return [classify_house(x["floor_count"]) for x in houses]


def get_count_house_categories(categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество домов в каждой категории.

    Если домов в конкретной категории нет, то в выводе данной категории не будет

    :param categories: Список категорий домов.
    :return: Словарь с количеством домов в каждой категории.
    """
    count_categories = {}
    for entry in categories:
        if entry in count_categories:
            count_categories[entry] += 1
        else:
            count_categories[entry] = 1
    return count_categories


def min_area_residential(houses: list[dict]) -> str:
    """Находит адрес нужного дома (см. описание).

    Находит адрес дома с наименьшим средним количеством
    квадратных метров жилой площади на одного жильца.

    :param houses: Список словарей с данными о домах.
    :return: Адрес дома с наименьшим средним количеством
        квадратных метров жилой площади на одного жильца.
    """
    list_key_val = [
        (x["house_address"], x["area_residential"] / x["population"]) for x in houses
    ]
    key, val = min(list_key_val, key=lambda x: x[1])
    return key


if __name__ == "__main__":
    housing_data = read_file(INPUT_FILE_HOUSING)
    # Информация о количестве домов каждого типа
    print(get_count_house_categories(get_classify_houses(housing_data)))
    # Адрес дома с наименьшим средним количеством
    #   квадратных метров жилой площади на одного жильца
    print(min_area_residential(housing_data))
