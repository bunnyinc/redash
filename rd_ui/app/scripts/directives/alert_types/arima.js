(function () {
  'use strict';

  var directives = angular.module('redash.directives');

  directives.directive('arimaAlert', [function () {
    function arimaAlertController($scope) {
      $scope.alert.options.evaluation_method = 'arima';
    };
    return {
      restrict: 'E',
      templateUrl: '/views/alerts/types/arima.html',
      controller: arimaAlertController,
      scope: true
    }
  }]);
})();
