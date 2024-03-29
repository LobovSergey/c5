import os
from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        return uniform(self.min_damage, self.max_damage)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipments = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Optional[Weapon]:
        for weapon in self.equipments.weapons:
            if weapon_name == weapon.name:
                return weapon
        return None

    def get_armor(self, armor_name):
        for armor in self.equipments.armors:
            if armor_name == armor.name:
                return armor
        return None

    def get_weapons_names(self) -> list:
        return [weapon.name for weapon in self.equipments.weapons]

    def get_armors_names(self) -> list:
        return [armor.name for armor in self.equipments.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("E:\pro\c5\data\equipment.json", 'r', encoding='UTF-8') as file:
            data = json.load(file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
            try:
                return equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError
