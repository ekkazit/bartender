var app = angular.module('app', ['pagination', 'sorted']);

app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function($http) {
  var factory = {};

  factory.load = function(is_active, term, sortOrder, sortDesc, page, rp) {
    return $http({
      url: '/api/product/search',
      method: 'post',
      data: {
        'is_active': is_active,
        'term': term,
        'sort': sortOrder,
        'desc': sortDesc,
        'page': page||1, 'rp': rp||10
      }
    });
  };

  factory.remove = function(id) {
    return $http.get('/api/product/delete/' + id);
  };

  return factory;
});

app.controller('ctrl', function($scope, $http, appFactory) {
  $scope.products = [];
  $scope.page = 0;
  $scope.rp = 10;
  $scope.results = {};
  $scope.total = 0;
  $scope.pageCount = 0;
  $scope.sortOrder = 'updated_at';
  $scope.sortDesc = true;

  $scope.sortBy = function(ord) {
    $scope.sortDesc = ($scope.sortOrder == ord) ? !$scope.sortDesc : true;
    $scope.sortOrder = ord;
    $scope.search();
  };

  $scope.search = function() {
    $scope.page = 0;
    $scope.total = 0;
    $scope.pageCount = 0;
    $scope.products = [];
    $scope.load();
  };

  $scope.reset = function() {
    $('#search').val('');
    $scope.sortOrder = 'updated_at';
    $scope.sortDesc = true;
    $scope.search();
  };

  $scope.load = function() {
    var isActive = $('#is_active').val();
    var term = $('#search').val();
    appFactory.load(isActive, term, $scope.sortOrder, $scope.sortDesc, $scope.page, $scope.rp).then(function(out) {
      res = out.data;
      $scope.products = res.products;
      $scope.total = res.total;
      $scope.pageCount = res.page_count;
      $scope.results = { totalPages: res.total_pages, currentPage: $scope.page };
    });
  };

  $scope.view = function(id) {
    window.location.href = '/admin/product/form/' + id;
  };

  $scope.remove = function(id) {
    if(confirm('Are you sure to delete this item ?')) {
      appFactory.remove(id).success(function(data) {
        if(data.result) {
          alert('Delete completed');
          $scope.search();
        }
      });
    }
  };

  $scope.$on('page', function(e, page) {
    $scope.page = page;
    if(page) { $scope.load(); }
  });

  $scope.search();
});
