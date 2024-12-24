import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

'''fan_speed = ctrl.Antecedent(np.arange(0, 11.1, 1), 'fan_speed')
battery_drainage = ctrl.Consequent(np.arange(0, 11, 1), 'battery_drainage')
cleaning_rate = ctrl.Consequent(np.arange(0, 21, 2), 'cleaning_rate')

fan_speed['low'] = fuzz.zmf(fan_speed.universe, 1, 3)
fan_speed['medium'] = fuzz.trapmf(fan_speed.universe, [2, 3, 6, 8])
fan_speed['high'] = fuzz.smf(fan_speed.universe, 8, 10)

battery_drainage['low'] = fuzz.zmf(battery_drainage.universe, 1, 3)
battery_drainage['medium'] = fuzz.trapmf(battery_drainage.universe, [2, 3, 6, 8])
battery_drainage['high'] = fuzz.smf(battery_drainage.universe, 7, 9)

cleaning_rate['low'] = fuzz.zmf(cleaning_rate.universe, 2, 6)
cleaning_rate['medium'] = fuzz.trapmf(cleaning_rate.universe, [4, 6, 12, 16])
cleaning_rate['high'] = fuzz.smf(cleaning_rate.universe, 14, 18)

# fan_speed.view()

rule1 = ctrl.Rule(fan_speed['low'], battery_drainage['low'])
rule2 = ctrl.Rule(fan_speed['medium'], battery_drainage['medium'])
rule3 = ctrl.Rule(fan_speed['high'], battery_drainage['high'])

rule4 = ctrl.Rule(fan_speed['low'], cleaning_rate['low'])
rule5 = ctrl.Rule(fan_speed['medium'], cleaning_rate['medium'])
rule6 = ctrl.Rule(fan_speed['high'], cleaning_rate['high'])

speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
speed_sim = ctrl.ControlSystemSimulation(speed_ctrl)

speed_sim.input['fan_speed'] = 2.5

speed_sim.compute()'''


def calc_cleaning(fan):
    fan_speed = ctrl.Antecedent(np.arange(0, 101.1, 1), 'fan_speed')
    cleaning_rate = ctrl.Consequent(np.arange(0, 21, 2), 'cleaning_rate')

    fan_speed['low'] = fuzz.zmf(fan_speed.universe, 0, 25)
    fan_speed['medium'] = fuzz.trapmf(fan_speed.universe, [20, 30, 60, 80])
    fan_speed['high'] = fuzz.smf(fan_speed.universe, 75, 100)

    cleaning_rate['low'] = fuzz.zmf(cleaning_rate.universe, 2, 6)
    cleaning_rate['medium'] = fuzz.trapmf(cleaning_rate.universe, [4, 6, 12, 16])
    cleaning_rate['high'] = fuzz.smf(cleaning_rate.universe, 14, 18)

    rule1 = ctrl.Rule(fan_speed['low'], cleaning_rate['low'])
    rule2 = ctrl.Rule(fan_speed['medium'], cleaning_rate['medium'])
    rule3 = ctrl.Rule(fan_speed['high'], cleaning_rate['high'])

    speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    speed_sim = ctrl.ControlSystemSimulation(speed_ctrl)

    # cleaning_rate.view()

    speed_sim.input['fan_speed'] = fan

    speed_sim.compute()

    return speed_sim.output['cleaning_rate']


def calc_battery(fan):
    fan_speed = ctrl.Antecedent(np.arange(0, 101.1, 1), 'fan_speed')
    battery_drainage = ctrl.Consequent(np.arange(0, 11, 1), 'battery_drainage')

    fan_speed['low'] = fuzz.zmf(fan_speed.universe, 0, 25)
    fan_speed['medium'] = fuzz.trapmf(fan_speed.universe, [20, 30, 60, 80])
    fan_speed['high'] = fuzz.smf(fan_speed.universe, 75, 100)

    battery_drainage['low'] = fuzz.zmf(battery_drainage.universe, 1, 3)
    battery_drainage['medium'] = fuzz.trapmf(battery_drainage.universe, [2, 3, 6, 8])
    battery_drainage['high'] = fuzz.smf(battery_drainage.universe, 7, 9)

    rule1 = ctrl.Rule(fan_speed['low'], battery_drainage['low'])
    rule2 = ctrl.Rule(fan_speed['medium'], battery_drainage['medium'])
    rule3 = ctrl.Rule(fan_speed['high'], battery_drainage['high'])

    speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
    speed_sim = ctrl.ControlSystemSimulation(speed_ctrl)

    speed_sim.input['fan_speed'] = fan

    speed_sim.compute()

    return speed_sim.output['battery_drainage']


# print(calc_battery(35))

# print(speed_sim.output['cleaning_rate'], speed_sim.output['battery_drainage'])

# fan_speed.view(sim=speed_sim)
