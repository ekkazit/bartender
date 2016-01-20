function firstDay() {
  var date = new Date();
  return '01/' + (date.getMonth() + 1) + '/' + date.getFullYear();
}

function lastDay() {
  var t = new Date();
  var date = new Date(t.getFullYear(), t.getMonth() + 1, 0, 23, 59, 59);
  return date.getDate() + '/' + (date.getMonth() + 1) + '/' + date.getFullYear();
}

$(function() {
  $('.input-group.date').datepicker({
    format: "dd/mm/yyyy",
    clearBtn: true
  });

  var report_url = '';
  var date = new Date();
  $('#from_date').val(firstDay());
  $('#to_date').val(lastDay());

  $('#rptclear').on('click', function() {
    $('#from_date').val(firstDay());
    $('#to_date').val(lastDay());
    $('#branch_id').val('');
    $('#rptexpexcel').attr('disabled', 'disabled');
    $('#rptexppdf').attr('disabled', 'disabled');
    report_url = '';
    $('#ifrm').prop('src', '');
  });

  $('#rptpreview').on('click', function() {
    if(!$('#from_date').val()) {
      $('#from_date').val(firstDay());
    }

    if(!$('#to_date').val()) {
      $('#to_date').val(lastDay());
    }

    var branch_id = $('#branch_id').val();
    var opts = '&__showtitle=false&__toolbar=true&__navigationbar=false'
    var params = '&site_id={{site_id}}&from_date=' + $('#from_date').val() + '&to_date=' + $('#to_date').val();
    if(! branch_id) {
      report_url = '{{rpt_server}}frameset?__report=salecustomer_all.rptdesign' + opts + params;
    } else {
      params = params + '&branch_id=' + branch_id;
      report_url = '{{rpt_server}}frameset?__report=salecustomer_by_branch.rptdesign' + opts + params;
    }
    $('#rptexpexcel').removeAttr('disabled');
    $('#rptexppdf').removeAttr('disabled');
    $('#ifrm').prop('src', report_url);
  });

  $('#rptexppdf').on('click', function() {
    $('#ifrm').prop('src', report_url + '&__format=pdf');
  });

  $('#rptexpexcel').on('click', function() {
    $('#ifrm').prop('src', report_url + '&__format=xls');
  });
});

var app = angular.module('app', []);
app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});
app.controller('ctrl', function($scope, $http) {});
