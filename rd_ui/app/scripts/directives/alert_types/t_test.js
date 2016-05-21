(function () {
  'use strict';

  var directives = angular.module('redash.directives');

  directives.directive('tTestAlert', [function () {
    function tTestAlertController($scope) {
      $scope.alert.options.evaluation_method = 't_test';
    };
    return {
      restrict: 'E',
      templateUrl: '/views/alerts/types/gaussian_threshold.html',
      controller: tTestAlertController,
      scope: true
    }
  }]);
})();
