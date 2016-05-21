from tests import BaseTestCase
from redash import models
from redash.alert_evaluation_methods.shewhart import Shewhart
from scipy import stats


class ShewhartTest(BaseTestCase):

    def test_evaluation_greater_than_ok(self):
        options = {
            'column': 'column_A',
            'value': 6,
            'op': 'greater than'
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 5.0})
        data['rows'].append({'column_A': 7.0})
        evaluation_model = Shewhart()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.OK_STATE)

    def test_evaluation_greater_than_trigger(self):
        options = {
            'column': 'column_A',
            'value': 6,
            'op': 'greater than'
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 8.0})
        data['rows'].append({'column_A': 7.0})
        evaluation_model = Shewhart()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)

    def test_evaluation_less_than_ok(self):
        options = {
            'column': 'column_A',
            'value': 6,
            'op': 'less than'
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 8.0})
        data['rows'].append({'column_A': 7.0})
        evaluation_model = Shewhart()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.OK_STATE)

    def test_evaluation_less_than_trigger(self):
        options = {
            'column': 'column_A',
            'value': 6,
            'op': 'less than'
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 5.0})
        data['rows'].append({'column_A': 7.0})
        evaluation_model = Shewhart()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)

    def test_evaluation_equals_ok(self):
        options = {
            'column': 'column_A',
            'value': 6,
            'op': 'equals'
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 8.0})
        data['rows'].append({'column_A': 7.0})
        evaluation_model = Shewhart()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.OK_STATE)

    def test_evaluation_equals_trigger(self):
        options = {
            'column': 'column_A',
            'value': 6,
            'op': 'equals'
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 6.0})
        data['rows'].append({'column_A': 7.0})
        evaluation_model = Shewhart()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)
