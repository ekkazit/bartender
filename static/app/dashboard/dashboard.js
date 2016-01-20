function renderChart(type) {
  $.ajax({
    url: '/api/dashboard/' + type,
    type: 'post',
    success: function(data) {
      var chartingOptions = {
        chart: {
          renderTo: 'container',
          defaultSeriesType: 'line'
        },
        title: {
          text: data.title,
        },
        subtitle: {
          text: data.subtitle,
        },
        xAxis: {
          categories: data.categories
        },
        yAxis: {
          title: {
            text: 'Sale Amount (THB)'
          },
        },
        tooltip: {
          valueSuffix: ' THB'
        },
        series: data.series
      };
      chart = new Highcharts.Chart(chartingOptions);
    }
  });
}

$(function() {
  $('#weekly').on('click', function() {
    $('#weekly').addClass('active');
    $('#monthly').removeClass('active');
    $('#yearly').removeClass('active');
    renderChart('weeklychart');
  });

  $('#monthly').on('click', function() {
    $('#weekly').removeClass('active');
    $('#monthly').addClass('active');
    $('#yearly').removeClass('active');
    renderChart('monthlychart');
  });

  $('#yearly').on('click', function() {
    $('#weekly').removeClass('active');
    $('#monthly').removeClass('active');
    $('#yearly').addClass('active');
    renderChart('yearlychart');
  });

  renderChart('weeklychart');
  $('#weekly').addClass('active');
});

var app = angular.module('app', []);
app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function($http) {
  var factory = {};
  factory.getSummary = function() {
    return $http.get('/api/dashboard/summary');
  };

  factory.getTopBranch = function() {
    return $http.get('/api/dashboard/topbranch');
  };

  factory.getTopProduct = function() {
    return $http.get('/api/dashboard/topproduct');
  };

  return factory;
});

app.controller('ctrl', function($scope, $http, $interval, appFactory){
  $scope.summary = { 'total_amount': 0, 'total_orders': 0, 'total_customer': 0, 'total_revenue': 0};
  $scope.branches = [];
  $scope.products = [];

  $scope.getSummary = function() {
    appFactory.getSummary().success(function(data) {
      $scope.summary.total_amount = data.total_amount;
      $scope.summary.total_revenue = data.total_amount - data.total_cost;
      $scope.summary.total_orders = data.total_orders;
      $scope.summary.total_customer = data.total_customer;
    });
  };

  $scope.getTopBranch = function() {
    appFactory.getTopBranch().success(function(data) {
      $scope.branches = data.branches;
    });
  };

  $scope.getTopProduct = function() {
    appFactory.getTopProduct().success(function(data) {
      $scope.products = data.products;
    });
  };

  $interval(function() { $scope.getSummary() }, 20000);
  $interval(function() { $scope.getTopBranch() }, 30000);
  $interval(function() { $scope.getTopProduct() }, 30000);

  $scope.getSummary();
  $scope.getTopBranch();
  $scope.getTopProduct();
});
