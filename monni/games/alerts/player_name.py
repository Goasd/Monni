from monni.games.alerts.alert import Alert


class PlayerName(Alert):

    def __init__(self, alert_method):
        super().__init__(alert_method)
        self.alert_when_player_name = ''
        self.server = None

    def check_server(self, gameserver):
        if gameserver.host+":"+str(gameserver.port) != self.server:
            return

        for player in gameserver.playerlist:
            if player.name == self.alert_when_player_name:
                self.alert_method(self)