from monni.games.alerts.alert import Alert


class Players(Alert):

    def __init__(self, alert_method):
        super().__init__(alert_method)
        self.alert_when_over_players = 0
        self.server = None

    def check_server(self, gameserver):
        if gameserver.host+":"+str(gameserver.port) != self.server:
            return

        if gameserver.players > self.alert_when_over_players:
            self.alert_method(self)