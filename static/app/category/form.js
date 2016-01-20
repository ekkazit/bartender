var app = angular.module('app', []);

app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function($http) {
  var factory = {};

  factory.view = function(id) {
    return $http.get('/api/category/get' + (id ? '/' + id : ''));
  };

  return factory;
});

app.controller('ctrl', function($scope, $http, appFactory) {
  $scope.category = {};

  $scope.view = function(id) {
    $scope.category = {};
    appFactory.view(id).success(function(data) {
      $scope.category = data.category;
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
          window.location = '/admin/category';
        }
      },
      error: function(xhr) {}
    });
    return false;
  });
});
