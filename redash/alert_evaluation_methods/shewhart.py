from redash.alert_evaluation_methods import BaseAlertEvaluationMethod, register
from redash import models


class Shewhart(BaseAlertEvaluationMethod):

    @classmethod
    def name(cls):
        return "shewhart"

    @classmethod
    def enabled(cls):
        return True

    def evaluate(self, options, data):
        value = data['rows'][0][options['column']]
        op = options['op']
        if op == 'greater than' and value > options['value']:
            return models.Alert.TRIGGERED_STATE
        elif op == 'less than' and value < options['value']:
            return models.Alert.TRIGGERED_STATE
        elif op == 'equals' and value == options['value']:
            return models.Alert.TRIGGERED_STATE
        else:
            return models.Alert.OK_STATE


register(Shewhart)
