var app = angular.module('app', []);

app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function($http) {
  var factory = {};

  factory.view = function(id) {
    return $http.get('/api/branch/get' + (id ? '/' + id : ''));
  };

  return factory;
});

app.controller('ctrl', function($scope, $http, appFactory) {
  $scope.branch = {};

  $scope.view = function(id) {
    $scope.branch = {};
    appFactory.view(id).success(function(data) {
      $scope.branch = data.branch;
      $('#is_main').prop('checked', $scope.branch.is_main=='Y');
    });
  };

  $scope.submit = function() {
    $('#forms').submit();
  };

  $scope.view($('#id').val()||'');
});

$(function() {
  $('#forms').submit(function() {
    $(this).ajaxSubmit({
      success: function(res) {
        if(res.result) {
          alert('save success');
          window.location = '/admin/branch';
        }
      },
      error: function(xhr) {}
    });
    return false;
  });
});
