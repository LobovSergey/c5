class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1.5
    player = None
    enemy = None
    game_is_running = False

    def __init__(self):
        self.battle_result = None

    def start_game(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
        elif self.player.hp <= 0:
            self.battle_result = f"{self.enemy.name} выиграл битву"
        elif self.enemy.hp <= 0:
            self.battle_result = f"{self.player.name} выиграл битву"
        return self._end_game()

    def _stamina_regeneration(self):
        players = (self.player, self.enemy)

        for unit in players:
            unit.stamina += self.STAMINA_PER_ROUND
            if unit.stamina > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina

    def next_turn(self):

        if result := self._check_players_hp() is not None:
            return result

        if self.game_is_running:
            self._stamina_regeneration()
            return self.enemy.hit(self.player)

    def _end_game(self):
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        result = self.player.hit(self.enemy)
        enemy_result = self.next_turn()
        return f"Player:{result}" \
               f"\n\nEnemy:{enemy_result}"

    def player_use_skill(self):
        player_skill = self.player.use_skill(self.enemy)
        enemy_result = self.next_turn()
        return f"Player:{player_skill}\nEnemy:{enemy_result}"
