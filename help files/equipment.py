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
    weapon_equipment: List = List[Weapon]
    armor_equipment: List = List[Armor]


class Equipment:

    def __init__(self):
        self.equipments = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Optional[Weapon]:
        for weapon in self.equipments.weapon_equipment:
            if weapon_name in weapon:
                return weapon
            return None

    def get_armor(self, armor_name) -> Optional[Armor]:
        for armor in self.equipments.armor_equipment:
            if armor_name in armor:
                return armor
            return None

    def get_weapons_names(self) -> list:
        return [weapon.name for weapon in self.equipments.weapon_equipment]

    def get_armors_names(self) -> list:
        return [armor.name for armor in self.equipments.armor_equipment]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("./data/equipment.json", 'r', encoding='UTF-8') as file:
            data = json.load(file)
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
            try:
                return equipment_schema().load(data)
            except marshmallow.exceptions.ValidationError:
                raise ValueError
