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
    standard_boat.rotation = -1.1
    assert standard_boat.rotation == -1.0

    standard_boat.rotation = 33
    assert standard_boat.rotation == 1.0


def test_rowing_rate_changes(standard_boat):
    """TC-FUNC-04: Проверка rowing_rate при разных rotation"""
    standard_boat.rotation = 0.3
    left1, right1 = standard_boat.rowing_rate
    assert right1 > left1

    standard_boat.rotation = 0.8
    left2, right2 = standard_boat.rowing_rate
    assert left2 < 0  # Отрицательное значение означает обратную греблю
