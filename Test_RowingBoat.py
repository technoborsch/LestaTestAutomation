import pytest
from RowingBoat import RowingBoat


@pytest.fixture
def standard_boat():
    """Фикстура для стандартной лодки с 4 гребцами"""
    return RowingBoat(
        max_weight=500,
        weight=300,
        number_of_rowers=4,
        max_rowing_frequency=2.0,
        max_speed=10.0,
        max_rotation=90.0,
        rower_force=150.0
    )


### Системные тесты ###

def test_moving(standard_boat):
    """TC-SYS-01: Проверка движения"""
    standard_boat.acceleration = 1.0
    standard_boat.move(1.0)

    assert standard_boat.speed > 0
    assert standard_boat.position[0] != 0
    assert standard_boat.position[1] != 0


def test_weight_capacity_effect(standard_boat):
    """TC-SYS-02: Затопление при превышении максимального веса"""
    heavy_boat = RowingBoat(
        max_weight=500,
        weight=550,  # Перегруз
        number_of_rowers=4,
        max_rowing_frequency=2.0,
        max_speed=10.0,
        max_rotation=90.0,
        rower_force=150.0
    )

    heavy_boat.acceleration = 1.0
    heavy_boat.move(1.0)

    assert heavy_boat.speed == 0
    assert heavy_boat.position[0] == 0
    assert heavy_boat.position[1] == 0
    assert heavy_boat._is_afloat == False


def test_max_speed_achievement(standard_boat):
    """TC-SYS-03: Достижение максимальной скорости при длительном ускорении"""
    standard_boat.acceleration = 1.0
    for _ in range(100):
        standard_boat.move(1.0)

    assert standard_boat.speed == pytest.approx(standard_boat._max_speed)


def test_moving_turn(standard_boat):
    """TC-SYS-04: Возможность осуществления поворота в движении"""
    standard_boat.acceleration = 1.0
    standard_boat.rotation = 0.1
    standard_boat.move(1.0)

    assert standard_boat.position[0] > 0
    assert standard_boat.position[1] < 0
    assert standard_boat.speed > 0


def test_in_place_turn(standard_boat):
    """TC-SYS-05: Возможность осуществления поворота на месте"""
    standard_boat.rotation = 1.0
    standard_boat.move(1.0)

    assert standard_boat.position[0] == 0
    assert standard_boat.position[1] == 0
    assert standard_boat.speed == 0
    assert standard_boat.direction > 0


def test_inertia_movement(standard_boat):
    """TC-SYS-06: Движение по инерции"""
    standard_boat.acceleration = 1.0
    for _ in range(10):
        standard_boat.move(1.0)
    standard_boat.acceleration = 0.0
    standard_boat.move(1.0)

    assert standard_boat.speed > 0

### Интеграционные тесты ###

def test_rowing_and_steering_interaction(standard_boat):
    """TC-INT-01: Взаимодействие гребли и поворота"""
    initial_direction = standard_boat.direction

    standard_boat.acceleration = 1.0
    standard_boat.rotation = 0.5  # Поворот вправо
    standard_boat.move(1.0)

    assert standard_boat.direction > initial_direction
    assert standard_boat.speed > 0
    assert standard_boat.position[0] > 0  # Должны сместиться вправо


def test_rowing_frequency_impact(standard_boat):
    """TC-INT-02: Влияние частоты гребли на скорость"""
    standard_boat.acceleration = 0.5
    for _ in range(100):
        standard_boat.move(1.0)
    speed1 = standard_boat.speed

    standard_boat.acceleration = 1.0
    for _ in range(100):
        standard_boat.move(1.0)
    speed2 = standard_boat.speed

    assert speed2 > speed1


def test_rowing_in_sync(standard_boat):
    """TC-INT-03: Синхронная гребля с двух сторон"""
    standard_boat.acceleration = 1.0
    standard_boat.rotation = 0.1
    for _ in range(10):
        standard_boat.move(1.0)

    assert standard_boat.rowing_rate[0] == standard_boat.rowing_rate[1]
    assert standard_boat.direction == 0.0


def test_async_rowing(standard_boat):
    """TC-INT-04: Асинхронная гребля при повороте в движении"""
    standard_boat.acceleration = 1.0
    standard_boat.rotation = 0.1
    for _ in range(10):
        standard_boat.move(1.0)

    assert standard_boat.rowing_rate[0] > standard_boat.rowing_rate[1]
    assert standard_boat.rowing_rate[0] > 0
    assert standard_boat.rowing_rate[1] > 0

### Функциональные тесты ###

def test_rotation_setting(standard_boat):
    """TC-FUNC-01: Проверка установки скорости поворота"""
    standard_boat.rotation = 0.7
    assert standard_boat.rotation == pytest.approx(0.7)

    left_rate, right_rate = standard_boat.rowing_rate
    assert right_rate > left_rate  # Больше гребков справа для поворота вправо


def test_reverse_movement(standard_boat):
    """TC-FUNC-02: Проверка заднего хода"""
    initial_position = standard_boat.position

    standard_boat.acceleration = -0.5
    standard_boat.move(1.0)

    assert standard_boat.speed < 0
    assert standard_boat.position[0] < initial_position[0]


def test_rotation_boundaries(standard_boat):
    """TC-FUNC-03: Проверка граничных значений rotation"""
    standard_boat.rotation = -90.1
    assert standard_boat.rotation == -90.0

    standard_boat.rotation = 333
    assert standard_boat.rotation == 90.0


def test_rowing_rate_changes(standard_boat):
    """TC-FUNC-04: Проверка rowing_rate при разных rotation"""
    standard_boat.rotation = 0.3
    left1, right1 = standard_boat.rowing_rate
    assert right1 > left1

    standard_boat.rotation = 0.8
    left2, right2 = standard_boat.rowing_rate
    assert left2 < 0  # Отрицательное значение означает обратную греблю


def test_max_weight_0_is_impossible():
    """TC-FUNC-05: Невозможность создать лодку с максимальным весом 0"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=0,
            weight=0,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_weight_acceleration_impact(standard_boat):
    """TC-FUNC-06: Влияние веса на ускорение"""
    light_boat = standard_boat
    heavy_boat = RowingBoat(
        max_weight=1000,
        weight=600,  # Перегруз
        number_of_rowers=4,
        max_rowing_frequency=2.0,
        max_speed=10.0,
        max_rotation=90.0,
        rower_force=150.0
    )

    light_boat.acceleration = 1.0
    light_boat.move(1.0)
    heavy_boat.acceleration = 1.0
    heavy_boat.move(1.0)

    assert light_boat.speed > heavy_boat.speed


def test_acceleration_boundaries(standard_boat):
    """TC-FUNC-07: Проверка граничных условий acceleration"""
    standard_boat.acceleration = -1.6
    acceleration1 = standard_boat.acceleration
    standard_boat.acceleration = 1000
    acceleration2 = standard_boat.acceleration

    assert acceleration1 == -1.0
    assert acceleration2 == 1.0


def test_direction_360_degrees_passing(standard_boat):
    """TC-FUNC-08: Проверка прохождения direction через 360 градусов"""
    standard_boat.rotation = 359
    standard_boat.move(1.0)
    direction1 = standard_boat.direction
    standard_boat.rotation = 2
    direction2 = standard_boat.direction

    assert direction1 == 359
    assert direction2 == 1


def test_no_movement_without_rowers():
    """TC-FUNC-09: Без гребцов лодка не движется"""
    no_rowers_boat = RowingBoat(
        max_weight=500,
        weight=300,
        number_of_rowers=0, # Ноль тут
        max_rowing_frequency=2.0,
        max_speed=10.0,
        max_rotation=90.0,
        rower_force=150.0
    )

    no_rowers_boat.acceleration = 1.0
    no_rowers_boat.move(1.0)

    assert no_rowers_boat.speed == 0
    assert no_rowers_boat.position[0] == 0
    assert no_rowers_boat.position[1] == 0


def test_no_movement_with_zero_max_rowing_frequency():
    """TC-FUNC-10: С предельной частотой гребков 0 лодка не движется"""
    no_rowing_boat = RowingBoat(
        max_weight=500,
        weight=300,
        number_of_rowers=4,
        max_rowing_frequency=0, # Ноль тут
        max_speed=10.0,
        max_rotation=90.0,
        rower_force=150.0
    )

    no_rowing_boat.acceleration = 1.0
    no_rowing_boat.move(1.0)

    assert no_rowing_boat.speed == 0
    assert no_rowing_boat.position[0] == 0
    assert no_rowing_boat.position[1] == 0

def test_no_movement_with_zero_max_speed():
    """TC-FUNC-11: С предельной скоростью 0 лодка не движется"""
    no_speed_boat = RowingBoat(
        max_weight=500,
        weight=300,
        number_of_rowers=4,
        max_rowing_frequency=2.0,
        max_speed=0, # Ноль тут
        max_rotation=90.0,
        rower_force=150.0
    )

    no_speed_boat.acceleration = 1.0
    no_speed_boat.move(1.0)

    assert no_speed_boat.speed == 0
    assert no_speed_boat.position[0] == 0
    assert no_speed_boat.position[1] == 0


def test_no_rotation_without_rowers():
    """TC-FUNC-12: Без гребцов лодка не вращается"""
    no_rowers_boat = RowingBoat(
        max_weight=500,
        weight=300,
        number_of_rowers=0,  # Ноль тут
        max_rowing_frequency=2.0,
        max_speed=10.0,
        max_rotation=90.0,
        rower_force=150.0
    )

    no_rowers_boat.rotation = 1.0
    no_rowers_boat.move(1.0)

    assert no_rowers_boat.direction == 0


def test_no_movement_with_zero_rower_force():
    """TC-FUNC-13: С предельной силой гребцов 0 лодка не движется"""
    no_force_boat = RowingBoat(
        max_weight=500,
        weight=300,
        number_of_rowers=4,
        max_rowing_frequency=2.0,
        max_speed=10.0,
        max_rotation=90.0,
        rower_force=0.0  # Ноль тут
    )

    no_force_boat.acceleration = 1.0
    no_force_boat.move(1.0)

    assert no_force_boat.speed == 0
    assert no_force_boat.position[0] == 0
    assert no_force_boat.position[1] == 0


def test_no_rotation_with_zero_rower_force():
    """TC-FUNC-14: С предельной силой гребцов 0 лодка не вращается"""
    no_force_boat = RowingBoat(
        max_weight=500,
        weight=300,
        number_of_rowers=4,
        max_rowing_frequency=2.0,
        max_speed=10.0,
        max_rotation=90.0,
        rower_force=0.0  # Ноль тут
    )

    no_force_boat.rotation = 1.0
    no_force_boat.move(1.0)

    assert no_force_boat.direction == 0


def test_impossible_initialization_with_negative_max_weight():
    """TC-FUNC-16: Невозможность создать лодку с отрицательным max_weight"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=-1,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_negative_weight():
    """TC-FUNC-17: Невозможность создать лодку с отрицательным weight"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=-1,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_negative_number_of_rowers():
    """TC-FUNC-18: Невозможность создать лодку с отрицательным number_of_rowers"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=-1,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_negative_max_rowing_frequency():
    """TC-FUNC-19: Невозможность создать лодку с отрицательным max_rowing_frequency"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=-1,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_negative_max_speed():
    """TC-FUNC-20: Невозможность создать лодку с отрицательным max_speed"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=-1,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_negative_max_rotation():
    """TC-FUNC-21: Невозможность создать лодку с отрицательным max_rotation"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=-1,
            rower_force=150.0
        )


def test_impossible_initialization_with_negative_rower_force():
    """TC-FUNC-22: Невозможность создать лодку с отрицательным rower_force"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=-1
        )


def test_impossible_initialization_with_string_max_weight():
    """TC-FUNC-16: Невозможность создать лодку со строковым max_weight"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight="a",
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_string_weight():
    """TC-FUNC-17: Невозможность создать лодку со строковым weight"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight="a",
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_string_number_of_rowers():
    """TC-FUNC-18: Невозможность создать лодку со строковым number_of_rowers"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers="a",
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_string_max_rowing_frequency():
    """TC-FUNC-19: Невозможность создать лодку со строковым max_rowing_frequency"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency="a",
            max_speed=10.0,
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_string_max_speed():
    """TC-FUNC-20: Невозможность создать лодку со строковым max_speed"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed="a",
            max_rotation=90.0,
            rower_force=150.0
        )


def test_impossible_initialization_with_string_max_rotation():
    """TC-FUNC-21: Невозможность создать лодку со строковым max_rotation"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation="a",
            rower_force=150.0
        )


def test_impossible_initialization_with_string_rower_force():
    """TC-FUNC-22: Невозможность создать лодку со строковым rower_force"""
    with pytest.raises(ValueError):
        _ = RowingBoat(
            max_weight=500,
            weight=300,
            number_of_rowers=4,
            max_rowing_frequency=2.0,
            max_speed=10.0,
            max_rotation=90.0,
            rower_force="a"
        )
