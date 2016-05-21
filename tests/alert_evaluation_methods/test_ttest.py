#encoding: utf8
from tests import BaseTestCase
from redash import models
from redash.alert_evaluation_methods.t_test import Ttest
from tests.factories import time_serie


class TtestTest(BaseTestCase):

    def test_evaluation_value_in_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.95,
            'window_size': 120,
            'start_offset': 10
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 280.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Ttest()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.OK_STATE)

    def test_evaluation_value_over_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.95,
            'window_size': 120,
            'start_offset': 10
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 301.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Ttest()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)

    def test_evaluation_value_under_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.95,
            'window_size': 120,
            'start_offset': 10
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 250.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Ttest()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)
