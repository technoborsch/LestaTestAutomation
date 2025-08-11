from typing import Tuple

from Boat import Boat


class RowingBoat(Boat):
    """Класс вёсельной лодки"""

    def __init__(self,
                 max_weight: float, # кг
                 weight: float, # кг
                 number_of_rowers: int, # число гребцов
                 max_rowing_frequency, # предельная частота гребков
                 max_speed: float, # предельная скорость лодки
                 max_rotation: float, # предельные обороты в секунду вокруг своей оси
                 rower_force: float): # Сила одного гребца
        super().__init__(max_weight, weight, max_speed, max_rotation, rower_force * number_of_rowers)
        self._rowers_count = number_of_rowers
        self._max_rowing_frequency = max_rowing_frequency
        self._rowing_frequency = max_rowing_frequency * self._acceleration
        self._left_rowing_rate = 0.0
        self._right_rowing_rate = 0.0

    @property
    def rowing_rate(self) -> Tuple[float, float]:
        """Возвращает кортеж в формате: (интенсивность гребли слева, интенсивность гребли справа)"""
        return self._left_rowing_rate, self._right_rowing_rate

    @rowing_rate.setter
    def rowing_rate(self, value: Tuple[float, float]) -> None:
        """Устанавливает новые интенсивности гребли слева и справа"""
        pass

    @property
    def rotation(self) -> float:
        return self._rotation

    @rotation.setter
    def rotation(self, new_rotation: float):
        """
        Устанавливает текущую интенсивность поворота.
        Отрицательные значения поворачивают против часовой стрелки, положительные - по часовой.
        Диапазон значений - от -1 до 1.
        При значениях по модулю от (0 до 0.5] гребцы с противоположной стороны постепенно прекращают грести
        При значениях по модулю от (0.5 до 1] гребцы с противоположной стороны начинают грести в обратную сторону
        """
        pass

    @property
    def acceleration(self) -> float:
        return self._acceleration

    @acceleration.setter
    def acceleration(self, new_acceleration: float):
        """
        Устанавливает интенсивность, с которой гребут гребцы.
        Диапазон значений - от -1 до 1.
        [-1, 0) для заднего хода
        0 для прекращения гребли
        (0, 1] для движения вперед
        """
        pass

    def move(self, time_delta: float) -> None:
        """Обновить движение лодки на основе текущих мощности и вращения"""

        # Вызываем базовую реализацию для обновления позиции
        super().move(time_delta)
