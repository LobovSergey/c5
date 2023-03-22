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


WarriorClass = UnitClass(
    name="Hellscream",
    max_health=10.0,
    max_stamina=80.0,
    stamina=0.9,
    attack=1.1,
    armor=1.1,
    skill=Bash()
)

ThiefClass = UnitClass(
    name="Valira",
    max_health=50.0,
    max_stamina=70.0,
    attack=1.3,
    stamina=0.8,
    armor=0.9,
    skill=Garrote()
)

MageClass = UnitClass(
    name="Khadgar",
    max_health=60.0,
    max_stamina=100.0,
    attack=0.8,
    stamina=1.1,
    armor=1.1,
    skill=FrostBolt()
)

unit_classes = {
    ThiefClass.name: ThiefClass,
    WarriorClass.name: WarriorClass,
    MageClass.name: MageClass
}
