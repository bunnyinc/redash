#encoding: utf8
from tests import BaseTestCase
from redash import models
from tests.factories import time_serie
from redash.alert_evaluation_methods.arima import *

 
class BasicExponentialSmoothingTest(BaseTestCase):

    def test_evaluation_value_in_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10,
            'p': 0, 'd': 1, 'q': 1
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 100.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.OK_STATE)
        
    def test_evaluation_value_over_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10,
            'p': 0, 'd': 1, 'q': 1
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 108.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)

    def test_evaluation_value_under_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10 ,
            'p': 0, 'd': 1, 'q': 1
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 66.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)


class DoubleExponentialSmoothingTest(BaseTestCase):

    def test_evaluation_value_in_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10,
            'p': 0, 'd': 2, 'q': 2
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 100.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.OK_STATE)
        
    def test_evaluation_value_over_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10,
            'p': 0, 'd': 2, 'q': 2
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 114.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)

    def test_evaluation_value_under_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10,
            'p': 0, 'd': 2, 'q': 2
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 70.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)


class ArimaTest(BaseTestCase):

    def test_evaluation_value_in_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10,
            'p': 2, 'd': 1, 'q': 0
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 95.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.OK_STATE)
        
    def test_evaluation_value_over_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10,
            'p': 2, 'd': 1, 'q': 0
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 97.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)

    def test_evaluation_value_under_interval(self):
        options = {
            'column': 'column_A',
            'confidence': 0.1,
            'window_size': 120,
            'start_offset': 10,
            'p': 2, 'd': 1, 'q': 0
        }
        data = {'rows':[]}
        data['rows'].append({'column_A': 63.0})
        for val in time_serie:
            data['rows'].append({'column_A': val})

        evaluation_model = Arima()
        self.assertEquals(evaluation_model.evaluate(options, data), models.Alert.TRIGGERED_STATE)
