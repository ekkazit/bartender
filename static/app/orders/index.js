var app = angular.module('app', ['pagination', 'sorted']);

app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.filter('capitalize', function() {
  return function(token) {
    return token.charAt(0).toUpperCase() + token.slice(1);
  }
});

app.factory('appFactory', function($http) {
  var factory = {};

  factory.load = function(fromDate, toDate, status, term, sortOrder, sortDesc, page, rp) {
    return $http({
      url: '/api/bill/search',
      method: 'post',
      data: {
        'term': term,
        'from_date': fromDate,
        'to_date': toDate,
        'status': status,
        'page': page||1,
        'rp': rp||10,
        'sort': sortOrder,
        'desc': sortDesc
      }
    });
  };

  factory.remove = function(id) {
    return $http.get('/api/bill/delete/' + id);
  };

  return factory;
});

app.controller('ctrl', function($scope, $http, appFactory) {
  $scope.bills = [];
  $scope.page = 0;
  $scope.rp = 10;
  $scope.results = {};
  $scope.total = 0;
  $scope.pageCount = 0;
  $scope.sortOrder = 'status_id, bill_date';
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
    $scope.bills = [];
    $scope.load();
  };

  $scope.reset = function() {
    $('#search').val('');
    $('#from_date').val('');
    $('#to_date').val('');
    $('#status').val('');
    $scope.sortOrder = 'status_id, bill_date';
    $scope.sortDesc = true;
    $scope.search();
  };

  $scope.load = function() {
    var term = $('#search').val();
    var status = $('#status').val();
    var fromDate = $('#from_date').val();
    var toDate = $('#to_date').val();

    appFactory.load(fromDate, toDate, status, term, $scope.sortOrder, $scope.sortDesc, $scope.page, $scope.rp).then(function(out) {
      res = out.data;
      $scope.bills = res.bills;
      $scope.total = res.total;
      $scope.pageCount = res.page_count;
      $scope.results = { totalPages: res.total_pages, currentPage: $scope.page };
    });
  };

  $scope.view = function(id) {
    window.location.href = '/admin/orders/form/' + id;
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
