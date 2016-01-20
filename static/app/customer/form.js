var app = angular.module('app', []);

app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function($http) {
  var factory = {};

  factory.view = function(id) {
    return $http.get('/api/customer/get' + (id ? '/' + id : ''));
  };

  return factory;
});

app.controller('ctrl', function($scope, $http, appFactory) {
  $scope.customer = {};

  $scope.view = function(id) {
    $scope.customer = {};
    appFactory.view(id).success(function(data) {
      $scope.customer = data.customer;
      $('#na').prop('checked', true);
      if($scope.customer.gender) {
        $(':radio[value=' + $scope.customer.gender + ']').prop('checked', true);
      }
      $('#img').val($scope.customer.img);
      $('#img_path').val($scope.customer.img_path);
      showImage();
    });
  };

  $scope.submit = function() {
    $('#forms').submit();
  };

  $scope.view($('#id').val()||'');
});

function showImage() {
  if($('#img_path').val()) {
    $('#pic').attr('src', $('#img_path').val());
    $('#pic').show();
    $('#no-pic').hide();
  } else {
    $('#pic').removeAttr('src');
    $('#pic').hide();
    $('#no-pic').show();
  }
}

$(function() {
  $('#removeimg').on('click', function() {
    $('#img').val('');
    $('#img_path').val('');
    showImage();
  });

  $('#addimg').click(function() {
    $('input[type=file]').click();
    return false;
  });

  $('input[type=file]').change(function() {
    $('#uploadform').submit();
  });

  $('#uploadform').submit(function() {
    $(this).ajaxSubmit({
      success: function(res) {
        if(res.img) {
          $('#img').val(res.img);
          $('#img_path').val(res.img_path);
        }
        showImage();
      },
      error: function(xhr) {}
    });
    return false;
  });

  showImage();

  $('#forms').submit(function() {
    $(this).ajaxSubmit({
      success: function(res) {
        if(res.result) {
          alert('save success');
          window.location = '/admin/customer';
        }
      },
      error: function(xhr) {}
    });
    return false;
  });
});
