$(function() {
  var report_url = '';

  $('#orders').select2({
    width: '200',
  });

  $('#branch_id').on('change', function() {
    var id = $(this).val()||'';
    if(id != '') {
      window.location.href='/report/orders/' + id;
    } else {
      window.location.href='/report/orders';
    }
  });

  $('#rptclear').on('click', function() {
    $('#orders').select2('val', '');
    $('#rptexpexcel').attr('disabled', 'disabled');
    $('#rptexppdf').attr('disabled', 'disabled');
    report_url = '';
    $('#ifrm').prop('src', '');
  });

  $('#rptpreview').on('click', function() {
    var order_id = $('#orders').val()||'';
    if(order_id=='') {
      alert('Please select sale number');
      return;
    }
    var opts = '&__showtitle=false&__toolbar=true&__navigationbar=false'
    var params = '&site_id={{site_id}}&bill_id=' + order_id;
    report_url = '{{rpt_server}}frameset?__report=receipt.rptdesign' + opts + params;
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
