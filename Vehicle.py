from abc import ABC, abstractmethod, abstractproperty
from typing import Tuple


class Vehicle(ABC):
    """Абстрактный базовый класс для транспортных средств"""

    @abstractmethod
    def move(self, time_delta: float) -> None:
        """Обновить положение транспортного средства"""
        pass

    @abstractmethod
    @property
    def position(self) -> Tuple[float, float]:
        """Получить текущие координаты"""
        pass

    @abstractmethod
    @position.setter
    def position(self, position: Tuple[float, float]) -> None:
        """Установить новую позицию"""
        pass

    @abstractmethod
    @property
    def speed(self) -> float:
        """Получить текущую скорость"""
        pass

    @abstractmethod
    @speed.setter
    def speed(self, speed: float) -> None:
        """Установить новую скорость"""
        pass

    @abstractmethod
    @property
    def direction(self) -> float:
        """Получить текущее направление движения в градусах"""
        pass

    @abstractmethod
    @direction.setter
    def direction(self, direction: float) -> None:
        """Задать новое направление движения в градусах"""
        pass

    @abstractmethod
    @property
    def rotation(self) -> float:
        """Получить текущее значение скорости поворота"""
        pass

    @abstractmethod
    @rotation.setter
    def rotation(self, new_rotation: float) -> None:
        """Задать новую скорость поворота"""
        pass
