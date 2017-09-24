class Alert:

    def __init__(self, alert_method):
        self.alert_method = alert_method

    def check_server(self, gameserver):
        return NotImplementedError