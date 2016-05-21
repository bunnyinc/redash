import logging

from redash.alert_evaluation_methods import BaseAlertEvaluationMethod, register
from redash import models


logger = logging.getLogger(__name__)


try:
    from statsmodels.tsa.arima_model import ARIMA
    enabled = True
except ImportError, e:
    enabled = False


class Arima(BaseAlertEvaluationMethod):

    @classmethod
    def name(cls):
        return "arima"

    @classmethod
    def enabled(cls):
        return enabled

    def evaluate(self, options, data):
        order = (options['p'], options['d'], options['q'])
        if options['window_size'] + options['start_offset'] == len(data['rows']):
            return models.Alert.UNKNOWN_STATE

        time_serie = [data['rows'][i][options['column']] for i in xrange(len(data['rows']))]
        value = time_serie[0]

        if options['start_offset'] == 1:
            start_offset = 0
            end_offset = start_offset - options['window_size']
            time_serie = time_serie[-1 * options['window_size']:]
        else:
            start_offset = -1 * (options['start_offset'] - 1)
            end_offset = start_offset - options['window_size']
            time_serie = time_serie[end_offset:start_offset]

        try:
            model = ARIMA(time_serie, order=order).fit(transparams=False, disp=-1)
            _, _, conf_int = model.forecast(
                steps=len(data['rows']) + end_offset,
                alpha=(1 - options['confidence'])
            )
        except:
            logger.exception()
            return models.Alert.UNKNOWN_STATE

        conf_int = conf_int[-1]
        if value > conf_int[1] or value < conf_int[0]:
            return models.Alert.TRIGGERED_STATE
        else:
            return models.Alert.OK_STATE


register(Arima)
