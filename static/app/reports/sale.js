$(function() {
  var report_url = '';
  var date = new Date();
  $('#month').val(date.getMonth() + 1);
  $('#year').val(date.getFullYear());

  $('#rptclear').on('click', function() {
    $('#month').val(date.getMonth() + 1);
    $('#year').val(date.getFullYear());
    $('#branch_id').val('');
    $('#rptexpexcel').attr('disabled', 'disabled');
    $('#rptexppdf').attr('disabled', 'disabled');
    report_url = '';
    $('#ifrm').prop('src', '');
  });

  $('#rptpreview').on('click', function() {
    if(!$('#month').val()) {
      $('#month').val(date.getMonth() + 1);
    }

    if(!$('#year').val()) {
      $('#year').val(date.getFullYear());
    }
    var branch_id = $('#branch_id').val();
    var opts = '&__showtitle=false&__toolbar=true&__navigationbar=false'
    var params = '&site_id={{site_id}}&month=' + $('#month').val() + '&year=' + $('#year').val();
    if(! branch_id) {
      report_url = '{{rpt_server}}frameset?__report=salemargin_all.rptdesign' + opts + params;
    } else {
      params = params + '&branch_id=' + branch_id;
      report_url = '{{rpt_server}}frameset?__report=salemargin_by_branch.rptdesign' + opts + params;
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
