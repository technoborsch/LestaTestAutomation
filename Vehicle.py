from abc import ABC, abstractmethod
from typing import Tuple


class Vehicle(ABC):
    """Абстрактный базовый класс для транспортных средств"""

    @abstractmethod
    def move(self, time_delta: float) -> None:
        """Обновить положение транспортного средства"""
        pass

    @property
    @abstractmethod
    def position(self) -> Tuple[float, float]:
        """Получить текущие координаты"""
        pass

    @position.setter
    @abstractmethod
    def position(self, position: Tuple[float, float]) -> None:
        """Установить новую позицию"""
        pass

    @property
    @abstractmethod
    def speed(self) -> float:
        """Получить текущую скорость"""
        pass

    @speed.setter
    @abstractmethod
    def speed(self, speed: float) -> None:
        """Установить новую скорость"""
        pass

    @property
    @abstractmethod
    def direction(self) -> float:
        """Получить текущее направление движения в градусах"""
        pass

    @direction.setter
    @abstractmethod
    def direction(self, direction: float) -> None:
        """Задать новое направление движения в градусах"""
        pass

    @property
    @abstractmethod
    def rotation(self) -> float:
        """Получить текущее значение скорости поворота"""
        pass

    @rotation.setter
    @abstractmethod
    def rotation(self, new_rotation: float) -> None:
        """Задать новую скорость поворота"""
        pass
