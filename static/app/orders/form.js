function initPlaceholder() {
  // workaround init select2 placeholder
  $('.select2-selection').html('<span class="select2-selection__rendered">' +
    '<span class="select2-selection__placeholder">Please Select</span></span>' +
    '<span class="select2-selection__arrow"><b role="presentation"></b></span>');
}

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
  factory.getStatus = function() {
    return $http.get('/api/status/list');
  };

  factory.view = function(id) {
    return $http.get('/api/bill/get' + (id ? '/' + id : ''));
  };

  factory.nextId = function(id) {
    return $http.get('/api/bill/next' + (id ? '/' + id : ''));
  };

  factory.prevId = function(id) {
    return $http.get('/api/bill/prev' + (id ? '/' + id : ''));
  };

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
  return factory;
});

app.controller('ctrl', function($scope, $http, appFactory) {
  // bill info
  $scope.bill           = {};
  $scope.bill_items     = [];
  $scope.statuses       = [];
  $scope.sum            = {};
  // product info
  $scope.products       = [];
  $scope.product        = {};
  // product list dialog paging
  $scope.page           = 0;
  $scope.rp             = 5;
  $scope.results        = {};
  $scope.total          = 0;
  $scope.pageCount      = 0;
  $scope.sortOrder      = 'updated_at';
  $scope.sortDesc       = true;

  $scope.currencies = [
    {id: 1, code: 'THB', name: 'Thai Baht'},
    {id: 2, code: 'JPY', name: 'Japan Yen'},
    {id: 3, code: 'USD', name: 'US Dollar'},
  ];

  $scope.getStatus = function() {
    appFactory.getStatus().success(function(data) {
      $scope.statuses = data.status;
    });
  };

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

  $scope.openProduct = function() {
    $scope.reset();
    $('#product-modal').modal('show');
  };

  $scope.selecProduct = function($index) {
    $scope.product = $scope.products[$index];
    $('#product').val($scope.product.code + ' ' + $scope.product.name);
    $('#product-modal').modal('hide');
  };

  $scope.clearProduct = function() {
    $('#product').val('');
    $scope.product = {};
  };

  $scope.addItem = function() {
    var p = $scope.product;
    if(p.id) {
      $scope.addBillItem(p.id, p.code, p.name, $('#option').val(), p.unit_price, $('#qty').val());
      $scope.clearProduct();
      $('#option').val('');
      $('#qty').val('1');
    } else {
      alert('Please select product');
    }
  };

  $scope.addBillItem = function(id, code, name, option, price, qty) {
    var isUpdated = false;
    angular.forEach($scope.bill_items, function(item) {
      if (id === item.id) {
        item.qty = parseInt((qty||0), 10);
        isUpdated = true;
      }
    });

    if (!isUpdated) {
      $scope.bill_items.push({
        'id': id,
        'code': code,
        'name': name,
        'option': option||'',
        'price': price||0,
        'qty': qty||1,
      });
    }
  };

  // watch bill re-calculate amout
  $scope.$watch('bill_items', function() {
    var totalQty = 0;
    var totalAmount = 0;
    var totalDisc = 0;
    var totalTax = 0;

    angular.forEach($scope.bill_items, function(item) {
      var qty = item.qty ? parseInt(item.qty, 10) : 0;
      item.qty = qty;
      item.amount = item.price * qty;
      totalQty += qty;
      totalAmount += item.price * qty;
    });

    // have a discount percent from config
    if ($scope.bill.discount_rate) {
      totalDisc = (totalAmount * $scope.bill.discount_rate) / 100;
    }

    // have a tax percent from config
    if ($scope.bill.tax_rate) {
      totalTax  = (totalAmount * $scope.bill.tax_rate) / 100;
    }

    var subTotal = totalAmount - totalTax;
    var grandTotal = totalAmount - totalDisc;
    $scope.sum = {
      'total_qty': totalQty,
      'total_discount': totalDisc,
      'total_tax': totalTax,
      'total_price': subTotal,
      'total_amount': grandTotal
    };
  }, true);

  $scope.deleteItem = function($index) {
    $scope.bill_items.splice($index, 1);
  };

  $scope.nextId = function() {
    if($scope.bill && $scope.bill.id) {
      appFactory.nextId($scope.bill.id).success(function(data) {
        if(data.next_id) {
          $scope.view(data.next_id);
        }
      });
    }
  };

  $scope.prevId = function() {
    if($scope.bill && $scope.bill.id) {
      appFactory.prevId($scope.bill.id).success(function(data) {
        if(data.prev_id) {
          $scope.view(data.prev_id);
        }
      });
    }
  };

  $scope.removeCustomer = function() {
    $('#cust_id').val('');
    $('#customer').siblings().find('.select2-selection__rendered').html('');
    $('#customer').siblings().find('.select2-selection__rendered').html('<span class="select2-selection__placeholder">Please Select</span>');
  };

  $scope.removeTable = function() {
    $('#table_id').val('');
    $('#table').siblings().find('.select2-selection__rendered').html('');
    $('#table').siblings().find('.select2-selection__rendered').html('<span class="select2-selection__placeholder">Please Select</span>');
  };

  $scope.view = function(id) {
    if(id) {
      $('#id').val(id);
    }
    $scope.bill = {};
    $scope.bill_items = [];
    initPlaceholder();
    appFactory.view(id).success(function(data) {
      $scope.bill = data.bill;
      $scope.receipt = data.receipt;
      // restore bill items
      var bill_items = $scope.bill.bill_items;
      angular.forEach(bill_items, function(p) {
        $scope.addBillItem(p.product_id, p.product.code, p.product.name, '', p.price, p.qty);
      });
      // bill date
      var date = new Date();
      if($scope.bill.bill_date) {
        date = new Date($scope.bill.bill_date);
      }
      $('.input-group.date').datepicker('setDate', date);
      // binding bill customer
      var repo1 = $scope.bill.customer;
      if(repo1) {
        var $cust = $('#customer').siblings().find('.select2-selection__rendered');
        $cust.html((repo1.code + ' ' + repo1.firstname + ' ' + (repo1.lastname||'')).trim());
      }
      // binding bill tables
      var repo2 = $scope.bill.tables;
      if(repo2) {
        var $table = $('#table').siblings().find('.select2-selection__rendered');
        $table.html(repo2.name||'');
      }
      // setup bill status
      if($scope.bill.status) {
        $scope.status = {id: $scope.bill.status.id};
      } else {
        $scope.status = 0;
      }
      // setup currency
      if($scope.bill.currency) {
        $scope.currency = {code: $scope.bill.currency};
      } else {
        $scope.currency = '';
      }
      $('#no').val($scope.bill.no);
      $('#cust_id').val($scope.bill.cust_id);
      $('#table_id').val($scope.bill.table_id);
      $('#user_id').val($scope.bill.user_id);
    });
  };

  $scope.submit = function() {
    angular.forEach($scope.bill_items, function(item, $index) {
      item.line_no = $index + 1;
      item.amount = item.price * parseInt(item.qty, 10);
      item.tax = 0;
      item.discount = 0;
      item.remark = '';
      item.site_id = $scope.bill.site_id;
      item.branch_id = $scope.bill.branch_id;
      item.bill_id = $scope.bill.id;
      item.product_id = item.id;
      item.tax = $scope.bill.tax_rate ? (item.amount * $scope.bill.tax_rate) / 100 : 0;
      item.discount = $scope.bill.discount_rate ? (item.amount * $scope.bill.discount_rate) / 100 : 0;
    });

    $('#total_qty').val($scope.sum.total_qty);
    $('#total_price').val($scope.sum.total_price);
    $('#total_tax').val($scope.sum.total_tax);
    $('#total_discount').val($scope.sum.total_discount);
    $('#total_amount').val($scope.sum.total_amount);
    $('#bill_items').val(JSON.stringify($scope.bill_items));
    $('#forms').submit();
  };

  $scope.$on('page', function(e, page) {
    $scope.page = page;
    if(page) { $scope.load(); }
  });

  $scope.getStatus();
  $scope.clearProduct();
  $scope.view($('#id').val()||'');
});

$(function() {
  // initialize modal dialog
  $.fn.modal.prototype.constructor.Constructor.DEFAULTS.backdrop = 'static';
  $('body').on('hidden.bs.modal', '.modal', function() {
    $(this).removeData();
    $(this).off('hidden.bs.modal');
  });

  // date picker config
  $('.input-group.date').datepicker({
    format: 'dd/mm/yyyy',
    todayBtn: 'linked',
    orientation: 'bottom auto'
  });

  // select2 customer dropdown
  $("#customer").select2({
    minimumInputLength: 1,
    width: '100%',
    ajax: {
      url: "/api/customer/term",
      dataType: 'json',
      type: 'POST',
      data: function (params) {
        return { q: params.term };
      },
      processResults: function (data, page) {
        return { results: data.customers };
      },
      cache: true
    },
    escapeMarkup: function(markup) { return markup; },
    templateResult: function(repo ) {
      if (repo.loading) return repo.text;
      return repo.code + ' ' + repo.firstname + ' ' + (repo.lastname||'')
        + '<br><span class="small">' + repo.email + '</span>';
    },
    templateSelection: function(repo) {
      if(repo.code) {
        $('#cust_id').val(repo.id);
        return (repo.code + ' ' + repo.firstname + ' ' + (repo.lastname||'')).trim();
      }
      return '';
    }
  });

  // select2 table dropdown
  $("#table").select2({
    minimumInputLength: 1,
    width: '100%',
    ajax: {
      url: "/api/table/term",
      dataType: 'json',
      type: 'POST',
      data: function (params) {
        return { q: params.term };
      },
      processResults: function (data, page) {
        return { results: data.tables };
      },
      cache: true
    },
    escapeMarkup: function(markup) { return markup; },
    templateResult: function(repo ) {
      if (repo.loading) return repo.text;
      return repo.name;
    },
    templateSelection: function(repo) {
      if(repo.name) {
        $('#table_id').val(repo.id);
        return repo.name;
      }
      return '';
    }
  });

  // init select2 placeholder
  initPlaceholder();

  // ajax submit form
  $('#forms').submit(function() {
    $(this).ajaxSubmit({
      success: function(res) {
        if(res.result) {
          alert('save success');
          window.location = '/admin/orders';
        }
      },
      error: function(xhr) {}
    });
    return false;
  });
});
