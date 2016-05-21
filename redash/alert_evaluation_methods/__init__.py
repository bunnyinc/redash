import logging

logger = logging.getLogger(__name__)

__all__ = [
    'BaseAlertEvaluationMethod',
    'register',
    'get_alert_evaluation_method',
    'import_alert_evaluation_methods'
]


class BaseAlertEvaluationMethod(object):

    @classmethod
    def name(self):
        return self.__name__.lower()

    @classmethod
    def enabled(self):
        return False

    def evaluate(self, options, data):
        raise NotImplementedError()


alert_evaluation_methods = {}


def register(alert_evaluation_method_class):
    global alert_evaluation_methods
    if alert_evaluation_method_class.enabled():
        logger.debug("Registering %s alert evaluation method.", alert_evaluation_method_class.name())
        alert_evaluation_methods[alert_evaluation_method_class.name()] = alert_evaluation_method_class
    else:
        logger.warning(
            "%s alert evaluation method enabled but not supported, not registering. Either disable or install missing dependencies.",
            alert_evaluation_method_class.name()
        )


def get_alert_evaluation_method(name):
    method_class = alert_evaluation_methods.get(name, None)
    if method_class is None:
        raise KeyError('{} is not registered'.format(name))

    return method_class()


def import_alert_evaluation_methods(imports):
    for module in imports:
        __import__(module)
