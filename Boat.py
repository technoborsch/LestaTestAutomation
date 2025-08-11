from typing import Tuple

from Vehicle import Vehicle


class Boat(Vehicle):
    """Базовый класс для лодок"""

    def __init__(self,
                 max_weight: float,
                 weight: float,
                 max_speed: float,
                 max_rotation: float,
                 max_force: float):
        self.max_weight = max_weight # Максимальный вес лодки в кг
        self._weight = weight # Текущий вес лодки
        self._max_speed = max_speed # Максимальная скорость лодки
        self._max_rotation = max_rotation # Максимальная скорость поворота вокруг своей оси, град/с
        self._acceleration = 0.0 # Текущее ускорение, от 0 до 1
        self._max_force = max_force # Сила двигателя, Н
        self._speed = 0.0  # Текущая скорость, м/с
        self._rotation = 0.0 # Текущее вращение, град/с. Положительное по часовой стрелке
        self._direction = 0.0  # градусы (0 - север)
        self._position = (0.0, 0.0)  # x, y координаты
        self._is_afloat = True # На плаву ли лодка

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, position: Tuple[float, float]) -> None:
        pass

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, speed: float) -> None:
        pass

    @property
    def direction(self) -> float:
        return self._direction

    @direction.setter
    def direction(self, direction: float) -> None:
        pass

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, rotation: float) -> None:
        pass

    def move(self, time_delta: float) -> None:
        """Базовая реализация движения лодки"""
        pass

    def _get_current_resistance(self):
        """
        Возвращает текущее сопротивление движению.
        Квадратичная функция, равная 1 при предельной скорости, и 0 при нулевой скорости.
        """
        pass

    def _update_position(self, time_delta: float) -> None:
        """Обновить позицию на основе скорости и направления"""
        pass
