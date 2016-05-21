import logging

from redash.alert_evaluation_methods import BaseAlertEvaluationMethod, register
from redash import models


logger = logging.getLogger(__name__)


try:
    import numpy as np, scipy.stats as st
    enabled = True
except ImportError, e:
    enabled = False


class Ttest(BaseAlertEvaluationMethod):

    @classmethod
    def name(cls):
        return "t_test"

    @classmethod
    def enabled(cls):
        return enabled

    def evaluate(self, options, data):
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

        l, u = st.t.interval(
            options['confidence'],
            len(time_serie)-1,
            loc=np.mean(time_serie),
            scale=st.sem(time_serie)
        )

        if value > u or value < l:
            return models.Alert.TRIGGERED_STATE
        else:
            return models.Alert.OK_STATE


register(Ttest)
