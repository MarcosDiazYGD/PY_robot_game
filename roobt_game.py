import random

robot_art = r"""
      0: {head_name}
      Is available: {head_status}
      Attack: {head_attack}                              
      Defense: {head_defense}
      Energy consumption: {head_energy_consump}
              ^
              |                  |1: {weapon_name}
              |                  |Is available: {weapon_status}
     ____     |    ____          |Attack: {weapon_attack}
    |oooo|  ____  |oooo| ------> |Defense: {weapon_defense}
    |oooo| '    ' |oooo|         |Energy consumption: {weapon_energy_consump}
    |oooo|/\_||_/\|oooo|          
    `----' / __ \  `----'           |2: {left_arm_name}
   '/  |#|/\/__\/\|#|  \'           |Is available: {left_arm_status}
   /  \|#|| |/\| ||#|/  \           |Attack: {left_arm_attack}
  / \_/|_|| |/\| ||_|\_/ \          |Defense: {left_arm_defense}
 |_\/    O\=----=/O    \/_|         |Energy consumption: {left_arm_energy_consump}
 <_>      |=\__/=|      <_> ------> |
 <_>      |------|      <_>         |3: {right_arm_name}
 | |   ___|======|___   | |         |Is available: {right_arm_status}
// \\ / |O|======|O| \  //\\        |Attack: {right_arm_attack}
|  |  | |O+------+O| |  |  |        |Defense: {right_arm_defense}
|\/|  \_+/        \+_/  |\/|        |Energy consumption: {right_arm_energy_consump}
\__/  _|||        |||_  \__/        
      | ||        || |          |4: {left_leg_name} 
     [==|]        [|==]         |Is available: {left_leg_status}
     [===]        [===]         |Attack: {left_leg_attack}
      >_<          >_<          |Defense: {left_leg_defense}
     || ||        || ||         |Energy consumption: {left_leg_energy_consump}
     || ||        || || ------> |
     || ||        || ||         |5: {right_leg_name}
   __|\_/|__    __|\_/|__       |Is available: {right_leg_status}
  /___n_n___\  /___n_n___\      |Attack: {right_leg_attack}
                                |Defense: {right_leg_defense}
                                |Energy consumption: {right_leg_energy_consump}

"""

# OBJETOS
colors = {
    'black': '\x1b[90m',
    'blue': '\x1b[94m',
    'cyan': '\x1b[96m',
    'green': '\x1b[92m',
    'magenta': '\x1b[95m',
    'red': '\x1b[91m',
    'white': '\x1b[97m',
    'yellow': '\x1b[93m'
}


# CREACION DE CLASES
# Se crea la clase magic cards, con la cual crearemos las cartas con atributos nombre y habilidad(cantidad numerica que afecta al robot) y una breve descripción de la funcionalidad de la carta
class MagicCard:
    def __init__(self, name, hability, description):
        self.name = name
        self.hability = hability
        self.part_to_attack = None
        self.description = description
        self.uses = 2 # Por julio este es el numero de usos


cards = {
    'cure': MagicCard('cure', 10, 'recover 10 defense points in the chosen part'),  # recupera defensa
    'critic_attack': MagicCard('critic_attack', 30, 'deals 30 damage without spending energy'),  # ataque sin gastar energia
    'short_circuit': MagicCard('short_circuit', 5, 'reduces energy by 5 points for 3 rounds'),  # efecto por 3 rondas
    'invulnerable': MagicCard('invulnerable', True, 'is immune to any rival attack for 1 round'),  # inmuidad al daño por 1 turno
    'turn_jump': MagicCard('turn_jump', 2, "skip the opponent's next turn") #salta el turno del rival
}


class Robot:
    def __init__(self, name, color_code):
        self.name = name
        self.color_code = color_code
        self.energy = 100
        self.cards = {}
        self.get_random_cards()
        self.is_short_circuit = False
        self.is_invulnerable = False
        self.parts = [
            Part('Head', attack_level=5, defense_level=20, energy_consumption=5),

            Part('weapon', attack_level=20, defense_level=40, energy_consumption=20),

            Part('left_arm', attack_level=15, defense_level=60, energy_consumption=15),
            Part('right_arm', attack_level=15, defense_level=60, energy_consumption=15),

            Part('left_leg', attack_level=10, defense_level=80, energy_consumption=10),
            Part('right_leg', attack_level=10, defense_level=80, energy_consumption=10)
        ]

    def greet(self):
        print('HI, mi name is', self.name)

    def amount_energy(self):
        print('the energy level is:', self.energy)

    def is_on(self):
        return self.energy <= 0

    def attack(self, enemy, part_to_use, part_to_attack):
        enemy.parts[part_to_attack].defense_level -= self.parts[part_to_use].attack_level
        self.energy -= self.parts[part_to_use].energy_consumption

    def is_there_available_parts(self):
        for part in self.parts:
            if part.is_available():
                return True
            else:
                return False

    def print_status(self):
        print(self.color_code)
        str_robot = robot_art.format(**self.get_part_status())

        self.greet()
        self.amount_energy()
        print(str_robot)

    def print_cards_availables(self):
        list_cards = list(self.cards.keys())

        card_1 = self.cards[list_cards[0]]
        card_2 = self.cards[list_cards[1]]

        print(self.color_code)
        print('AVAILABLE_CARDS\n')
        print('| 6:', card_1.name)
        print('|', card_1.description)
        print('\n')
        print('| 7:', card_2.name)
        print('|', card_2.description)

        print(colors['white'])

    def get_part_status(self):
        part_status = {}
        for part in self.parts:
            status_dict = part.get_status_dict()
            part_status.update(status_dict)

        return part_status

    def short_circuit(self, hability):
        self.energy -= hability

    # metodo para asignar 2 cartas de forma aleatoria a cada robot
    def get_random_cards(self):
        list_cards = list(cards.keys())
        num_cards = 0
        while num_cards < 2:
            rand = random.choice(list_cards)
            if rand in cards and rand not in self.cards:
                self.cards.update({rand: cards[rand]})
                num_cards = len(self.cards)

class Part:
    def __init__(self, name, attack_level=0, defense_level=0, energy_consumption=0):
        self.name = name
        self.attack_level = attack_level
        self.defense_level = defense_level
        self.energy_consumption = energy_consumption

    def get_status_dict(self):
        formatted_name = self.name.replace(" ", "_").lower()
        return {
            "{}_name".format(formatted_name): self.name.upper(),
            "{}_status".format(formatted_name): self.is_available(),
            "{}_attack".format(formatted_name): self.attack_level,
            "{}_defense".format(formatted_name): self.defense_level,
            "{}_energy_consump".format(formatted_name): self.energy_consumption
        }

    def is_available(self):
        return self.defense_level > 0

    # metodo al que recurre la carta sanar
    def cure(self, hability):
        self.defense_level += hability

    # metodo al que recurre la carta de ataque critico
    def critic_attack(self, hability):
        self.defense_level -= hability


class Play:
    def __init__(self):
        self.robot_1 = Robot('Jarvis', colors['cyan'])
        self.robot_2 = Robot('Friday', colors['red'])
        self.playing = True
        self.round_name = 0
        self.counter = 0
        print('welcome to the game')

    def play(self):
        while self.playing:
            if self.round_name % 2 == 0:
                current_robot = self.robot_1
                enemy_robot = self.robot_2
            else:
                current_robot = self.robot_2
                enemy_robot = self.robot_1

            if enemy_robot.is_invulnerable:
                print(colors['red'])
                print('the enemy is invulnerable')

                self.round_name += 1

            else:
                if current_robot.is_short_circuit:
                    if self.counter < 3:
                        current_robot.short_circuit(cards['short_circuit'].hability)

                        self.counter += 1

                    if self.counter == 2:
                        print('the short_circuit is over')
                        current_robot.is_short_circuit = False

                current_robot.print_status()
                current_robot.print_cards_availables()
                print('choose the part or the card to use')

                part_to_use = input('choose a number part or card: ')
                part_to_use = int(part_to_use)

                if part_to_use < 6:

                    enemy_robot.print_status()
                    print('what part of the enemy should we attack?')
                    part_to_attack = int(input('choose a part of enemy to attack: '))

                    current_robot.attack(enemy_robot, part_to_use, part_to_attack)

                    self.round_name += 1


                elif part_to_use > 5:
                    self.use_card(current_robot, part_to_use, enemy_robot)

                else:
                    print('Wrong number')
                    self.playing = False

        if not enemy_robot.is_on() or enemy_robot.is_there_available_parts() == False:
            self.playing = False
            print('Congratulations, you won', current_robot.name)

            # metodo para acceder a las funcionalidades de cada carta

    def use_card(self, current_robot, card_to_use, enemy_robot):
        list_cards = list(current_robot.cards.keys())
        card_selected = None

        if card_to_use == 6:
            card_selected = current_robot.cards[list_cards[0]]

        if card_to_use == 7:
            card_selected = current_robot.cards[list_cards[1]]

        if card_selected.uses > 0:
            card_selected.uses -= 1  

            if card_selected.name == 'cure':
                print(current_robot.print_status())
                part_to_cure = int(input('choose the part to cure: '))
    
                current_robot.parts[part_to_cure].cure(card_selected.hability)
    
                print(current_robot.parts[part_to_cure].defense_level)
    
                self.round_name += 1
    
            if card_selected.name == 'critic_attack':
                print(enemy_robot.print_status())
                part_to_affect = int(input('choose a part of enemy to attack: '))
                enemy_robot.parts[part_to_affect].critic_attack(card_selected.hability)
    
                self.round_name += 1
    
            if card_selected.name == 'short_circuit':
                enemy_robot.is_short_circuit = True
                print(enemy_robot.print_status())
                print("The enemy is having a short circuit")
    
                self.round_name += 1
    
            if card_selected == 'invulnerable':
                current_robot.is_invulnerable = card_selected.hability
    
                self.round_name += 1
    
            if card_selected.name == 'turn_jump':
                print('The enemy robot miss his turn')
                part_to_use = input('choose a number part: ')
                part_to_use = int(part_to_use)
                enemy_robot.print_status()
                print('what part of the enemy should we attack?')
                part_to_attack = input('choose a part of enemy to attack: ')
                part_to_attack = int(part_to_attack)
                current_robot.attack(enemy_robot, part_to_use, part_to_attack)
    
                self.round_name += card_selected.hability
            
        else:
            print("This card can no longer be used.")
          

play = Play()
play.play()

# crear las cartas y agregarlas al robot
#

