var app = angular.module('app', []);

app.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.factory('appFactory', function($http) {
  var factory = {};

  factory.getRoles = function() {
    return $http.get('/api/role/list');
  };

  factory.view = function(id) {
    return $http.get('/api/user/get' + (id ? '/' + id : ''));
  };

  return factory;
});

app.controller('ctrl', function($scope, $http, appFactory) {
  $scope.user = {};
  $scope.roles = [];

  $scope.view = function(id) {
    $scope.user = {};
    appFactory.view(id).success(function(data) {
      $scope.user = data.user;
      $('#na').prop('checked', true);
      if($scope.user.gender) {
        $(':radio[value=' + $scope.user.gender + ']').prop('checked', true);
      }
      if($scope.user.roles) {
        $scope.role = {id: $scope.user.roles.id};
      } else {
        $scope.role = 0;
      }
      $('#img').val($scope.user.img);
      $('#img_path').val($scope.user.img_path);
      showImage();
    });
  };

  $scope.getRoles = function() {
    appFactory.getRoles().success(function(data) {
      $scope.roles = data.roles;
    });
  };

  $scope.submit = function() {
    $('#forms').submit();
  };

  $scope.getRoles();
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
          window.location = '/admin/user';
        }
      },
      error: function(xhr) {}
    });
    return false;
  });
});
