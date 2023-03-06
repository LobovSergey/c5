from marshmallow_dataclass import dataclass
from skills import Bash, Garrote, FrostBolt, Skill


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    attack: float
    stamina: float
    armor: float
    skill: Skill


WarriorClass: UnitClass = UnitClass(
    name="Hellscream",
    max_health=10.0,
    max_stamina=6.0,
    attack=3.2,
    armor=5.5,
    skill=Bash()
)

ThiefClass = UnitClass(
    name="Valira",
    max_health=8.0,
    max_stamina=10.0,
    attack=4.1,
    armor=4.0,
    skill=Garrote()
)

MageClass = UnitClass(
    name="Khadgar",
    max_health=6.0,
    max_stamina=20.0,
    attack=6.7,
    armor=3.0,
    skill=FrostBolt()
)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass,
    MageClass.name: MageClass
}
