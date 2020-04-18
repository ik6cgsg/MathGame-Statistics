from typing import Dict

from prettytable import PrettyTable

from data_base import MathDataBase, MathDataBaseException


class StatisticsScenarios(object):
    levels_count = 21

    def __init__(self, math_db: MathDataBase, value_coeff: float):
        """

        :param math_db: database with "math_game_log" table from https://bitbucket.org/vkatsman/mathhelperserver/src/master/
        :param value_coeff: coefficient 'levels_passed / levels_count' for picking the most valuable players
        """
        self.math_db = math_db
        self.value_coeff = value_coeff
        self.valuable_players = None

    def user_marks(self) -> bool:
        name = "Check user marks"
        print("%s scenario started!" % name)
        try:
            res = self.math_db.execute("\
                select user_game_identifier, user_mark, user_comment from math_game_log where action='mark'\
            ", output=True)
        except MathDataBaseException as e:
            print("%s scenario failed ( :( ) : %s" % (name, e))
            return False
        total: float = 0
        for record in res:
            total += float(record['user_mark'])
        print("%s users marked game!" % len(res))
        print("Summary mark = %s" % (total / len(res)))
        return True

    def pick_valuable_players(self) -> bool:
        name = "Pick most valuable players"
        print("%s scenario started!" % name)
        try:
            res = self.math_db.execute("""
                select user_game_identifier, task_id, count(*) from math_game_log 
                where 
                    ip not in (
                        '178.71.128.254', 
                        '81.200.120.104', 
                        '', 
                        '92.100.108.227', 
                        '78.140.203.202', 
                        '81.200.120.52', 
                        '217.66.159.130', 
                        '81.200.120.34', 
                        '93.185.30.8', 
                        '146.120.75.64'
                    ) and
                    hardware_device_id not in (
                        '8e5604af-99db-47a5-b5e9-465040486690', 
                        '392b661b-f6c8-4686-928a-30318a870343', 
                        'be7125c7-c1a9-44b1-b1e8-f46e27b3b07e', 
                        '', 
                        'fd85bf04-e899-441d-a2e6-cc26ca7360b7', 
                        'd6ce40ec-93af-4b85-82f4-bac4860fffa2', 
                        'be24a7a4-d904-48ad-b08d-f1bb5bd96523', 
                        '2750bc42-702e-4cbe-bae5-798f171389e1', 
                        'ca02a2c6-1202-4d45-9a76-3a20f8333a41', 
                        '781d80dd-810d-42cc-bc98-fccbf16a3e38', 
                        'd520c7a8-421b-4563-b955-f5abc56b97ec'
                    ) and
                    action='win' and
                    game = 'MathGame_IK_an'
                group by user_game_identifier, task_id 
            """, output=True)
        except MathDataBaseException as e:
            print("%s scenario failed ( :( ) : %s" % (name, e))
            return False
        players: Dict[str: int] = dict()
        for record in res:
            if players.get(record["user_game_identifier"]) is not None:
                players[str(record["user_game_identifier"])] += 1
            else:
                players[str(record["user_game_identifier"])] = 1
        delete_users = [user for user in players
                        if float(players[user]) / self.levels_count < self.value_coeff]
        for user in delete_users:
            del players[user]
        print("Most valuables players:")
        table = PrettyTable(["User game id", "Levels passed", "User coefficient"])
        for user in players:
            table.add_row([user, players[user], float(players[user]) / self.levels_count])
        print(table)
        return True
