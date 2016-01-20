var app = angular.module('app', []);

app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function($http) {
  var factory = {};

  factory.view = function(id) {
    return $http.get('/api/table/get' + (id ? '/' + id : ''));
  };

  return factory;
});

app.controller('ctrl', function($scope, $http, appFactory) {
  $scope.table = {};

  $scope.view = function(id) {
    $scope.table = {};
    appFactory.view(id).success(function(data) {
      $scope.table = data.table;
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
          window.location = '/admin/table';
        }
      },
      error: function(xhr) {}
    });
    return false;
  });
});
