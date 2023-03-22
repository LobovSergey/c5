from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from marshmallow_dataclass import dataclass

if TYPE_CHECKING:
    from unit import BaseUnit

@dataclass
class Skill(ABC):
    """
    Базовый класс умения
    """
    user = None
    target = None

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def stamina(self):
        pass

    @property
    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def skill_effect(self) -> str:
        pass

    def _is_stamina_enough(self):
        return self.user.stamina > self.stamina

    def use(self, user: BaseUnit, target: BaseUnit) -> str:
        """
        Проверка, достаточно ли выносливости у игрока для применения умения.
        Для вызова скилла везде используем просто use
        """
        self.user = user
        self.target = target
        if self._is_stamina_enough():
            return self.skill_effect()
        return f"{self.user.name} попытался использовать {self.name} но у него не хватило выносливости."


class Bash(Skill):
    name = 'Стан'
    stamina = 15.0
    damage = 17.0

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.get_damage(damage=Bash.damage)
        return f"{self.user.name}  использовал {self.name}"


class Garrote(Skill):
    name = "Гаррота"
    stamina = 5.0
    damage = 10.0

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.get_damage(damage=Garrote.damage)
        return f"{self.user.name}  использовал {self.name}"


class FrostBolt(Skill):
    name = "Ледяной шар"
    stamina = 70.0
    damage = 30.0

    def skill_effect(self):
        self.user.stamina -= self.stamina
        self.target.get_damage(damage=FrostBolt.damage)
        return f"{self.user.name}  использовал {self.name}"
