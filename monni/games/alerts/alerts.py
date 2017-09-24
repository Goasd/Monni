import subprocess
import sys

from monni.games.alerts.player_name import PlayerName
from monni.games.alerts.players import Players


class Alerts:
    def __init__(self):
        self.alerts = []

    def new_alert(self, alert_type, alert_variable, server):
        if alert_type == 'over_player':
            alert = Players(self.call_alert)
            alert.alert_when_over_players = alert_variable
            alert.server = server
            self.alerts.append(alert)
            print('ok')
        elif alert_type == 'name_player':
            alert = PlayerName(self.call_alert)
            alert.alert_when_player_name = alert_variable
            alert.server = server
            self.alerts.append(alert)
            print('ok')
        else:
            print('fail')

    def check_server(self, gameserver):
        for alert in self.alerts:
            alert.check_server(gameserver)

    def call_alert(self, alert):
        subprocess.Popen(['play','/usr/share/sounds/ubuntu/ringtones/Bliss.ogg'],
                       shell=False,
                       stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL)
