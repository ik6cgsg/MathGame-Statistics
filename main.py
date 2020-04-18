from data_base import MathDataBase
from scenarios import StatisticsScenarios


if __name__ == '__main__':
    math_base = MathDataBase()
    try:
        math_base.connect()
        scenarios = StatisticsScenarios(math_base, 0.38)
        scenarios.pick_valuable_players()
    except Exception as e:
        print("Exception caught: %s" % str(e))
