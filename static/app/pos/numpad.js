/**/
var _instance = null;

function npDecrement() {
  var qty = parseInt($('#np-qty').val()||0, 10);
  qty -= 1;
  $('#np-qty').val(qty);
}

function npIncrement() {
  var qty = parseInt($('#np-qty').val()||0, 10);
  qty += 1;
  $('#np-qty').val(qty);
}

function npReturn() {
  if(_instance == null)
    return;
  var preval = $('#np-qty').val();
  var qty = parseFloat((preval=='.' ? preval.replace('.', '') : preval)||0, 10);
  $(_instance).val(qty);
  $(_instance).change();
  $(_instance).popover('destroy');
  _instance = null;
}

function npDel() {
  var qty = $('#np-qty').val()||'';
  if(qty != '') {
    $('#np-qty').val(qty.substring(0, qty.length-1));
  }
}

function npNumber(val) {
  if($('#np-qty').hasClass('hilight')) {
    $('#np-qty').val('');
    $('#np-qty').removeClass('hilight');
  }

  var qty = $('#np-qty').val()||'';
  if(val == '.' && qty.indexOf('.') != -1) { val = ''; }
  $('#np-qty').val(qty + val);
}

function npPlusMinus() {
  var qty = $('#np-qty').val()||'';
  if(qty) {
    if(qty[0] == '-') {
      $('#np-qty').val(qty.replace('-', ''));
    } else {
      $('#np-qty').val('-' + qty);
    }
  }
}

function npUnlock() {
  if($('#np-qty').hasClass('hilight')) {
    $('#np-qty').removeClass('hilight');
  }
}

$(function() {
  $('#bill-table').delegate('.numpad', 'click', function() {
    $(this).popover({
      placement: 'bottom',
      html:'true',
      title: $('.pop-title').html(),
      content: $('.pop-content').html(),
    });
    $(this).popover('show');

    $('#np-qty').val(parseInt($(this).val()||'0', 10));
    $('#np-qty').select();
    $('#np-qty').addClass('hilight');
    _instance = $(this);
  });
});

$('html').on('click', function (e) {
  $('.numpad').each(function () {
    if (!$(this).is(e.target) && $(this).has(e.target).length === 0 &&
      $('.popover').has(e.target).length === 0) {
      $(this).popover('destroy');
    }
  });
});
