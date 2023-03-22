from classes import unit_classes
from flask import Flask, render_template, redirect, url_for, request
from base import Arena
from equipment import Equipment
from unit import PlayerUnit, BaseUnit, EnemyUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template("index.html", )


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        response = arena.player_hit()
    else:
        response = arena.battle_result
    return render_template("fight.html", result=response, heroes=heroes)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        response = arena.player_use_skill()
    else:
        response = arena.battle_result
    return render_template("fight.html", result=response, heroes=heroes)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        response = arena.next_turn()
    else:
        response = arena.battle_result
    return render_template("fight.html", result=response, heroes=heroes)


@app.route("/fight/end-fight")
def end_fight():
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
        player = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        player.equip_weapon(equip.get_weapon(weapon))
        player.equip_armor(equip.get_armor(armor))
        heroes["player"] = player
        print(player.weapon)
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['GET', 'POST'])
def choose_enemy():
    if request.method == 'GET':
        result = {
            "header": "Выбор вашего врага",
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
        enemy = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        enemy.equip_weapon(equip.get_weapon(weapon_name=weapon))
        enemy.equip_armor(equip.get_armor(armor_name=armor))
        print(enemy.name)
        heroes["enemy"] = enemy
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run(debug=True)
