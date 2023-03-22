from flask import Flask, render_template, redirect, url_for, request
from base import Arena
from equipment import EquipmentData, Equipment
from classes import unit_classes
from unit import PlayerUnit, BaseUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def hit():
    # TODO кнопка нанесения удара
    # TODO обновляем экран боя (нанесение удара) (шаблон fight.html)
    # TODO если игра идет - вызываем метод player.hit() экземпляра класса арены
    # TODO если игра не идет - пропускаем срабатывание метода (простот рендерим шаблон с текущими данными)
    pass


@app.route("/fight/use-skill")
def use_skill():
    # TODO кнопка использования скилла
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    pass


@app.route("/fight/pass-turn")
def pass_turn():
    # TODO кнопка пропус хода
    # TODO логика пркатикчески идентична предыдущему эндпоинту
    # TODO однако вызываем здесь функцию следующий ход (arena.next_turn())
    pass


@app.route("/fight/end-fight")
def end_fight():
    # TODO кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['GET', 'POST'])
def choose_hero():
    if request.method == 'GET':
        result = {
            "header": "Выбор вашего героя",
            "classes": unit_classes,
            "weapons": Equipment().get_weapons_names(),
            "armors": Equipment().get_armors_names(),
        }
        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        name = request.form["name"]
        unit_class = request.form["unit_class"]
        weapon = request.form["weapon"]
        armor = request.form["armor"]
        equip = Equipment()
        player_unit = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        player_unit.equip_weapon(equip.get_weapon(weapon))
        player_unit.equip_armor(equip.get_armor(armor))
        heroes["player"] = player_unit
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['GET', 'POST'])
def choose_enemy():
    if request.method == 'GET':
        result = {
            "header": "Выбор вашего героя",
            "classes": unit_classes,
            "weapons": Equipment().get_weapons_names(),
            "armors": Equipment().get_armors_names(),
        }
        return render_template('hero_choosing.html', result=result)
    elif request.method == 'POST':
        name = request.form["name"]
        unit_class = request.form["unit_class"]
        weapon = request.form["weapon"]
        armor = request.form["armor"]
        enemy_unit = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        enemy_unit.equip_weapon(Equipment().get_weapon(weapon_name=weapon))
        enemy_unit.equip_armor(Equipment().get_armor(armor_name=armor))
        heroes["player"] = enemy_unit
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run(debug=True)
