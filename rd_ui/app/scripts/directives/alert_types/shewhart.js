(function () {
  'use strict';

  var directives = angular.module('redash.directives');

  directives.directive('shewhartAlert', [function () {
    function shewhartAlertController($scope) {
      $scope.ops = ['greater than', 'less than', 'equals'];
      $scope.alert.options.evaluation_method = 'shewhart';
    };
    return {
      restrict: 'E',
      templateUrl: '/views/alerts/types/shewhart.html',
      controller: shewhartAlertController,
      scope: true
    }
  }]);
})();
