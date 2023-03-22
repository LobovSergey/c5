from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Weapon, Armor
from random import randint


class BaseUnit(ABC):

    def __init__(self, name, unit_class):

        self.name: str = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used: bool = False

    @property
    def health_points(self):
        return self.hp

    @property
    def stamina_points(self):
        return self.stamina

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        target_diffence = 0
        self.stamina -= self.weapon.stamina_per_hit
        unit_damage = self.weapon.damage * self.unit_class.attack

        if target.stamina > target.armor.stamina_per_turn:
            target.stamina -= target.armor.stamina_per_turn
            target_diffence = target.unit_class.armor * target.armor.defence

        damage = round(unit_damage - target_diffence, 1)
        target.get_damage(damage=damage)
        return damage

    def get_damage(self, damage: float) -> None:
        self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        if not self._is_skill_used:
            self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)
        return "Навык использован"


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target=target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит " \
                   f"{damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, " \
               f"но {target.armor.name} cоперника его останавливает."


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        if not self._is_skill_used and randint(0, 99) < 10 and self.stamina >= self.unit_class.skill.stamina:
            return self.use_skill(target=target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target=target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит " \
                   f"{damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар," \
               f" но {target.armor.name} cоперника его останавливает."
