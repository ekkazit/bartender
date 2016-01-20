function custPlaceholder() {
  $('.select2-selection').html('<span class="select2-selection__rendered">' +
    '<span class="select2-selection__placeholder">Please Select</span></span>' +
    '<span class="select2-selection__arrow"><b role="presentation"></b></span>');
}

// beginning an AngularJS module
var app = angular.module('app', ['pager']);
app.config(function($interpolateProvider, $compileProvider) {
  $compileProvider.debugInfoEnabled(false);
  $interpolateProvider.startSymbol('@{').endSymbol('}');
});

app.config(['$compileProvider', function ($compileProvider) {
  $compileProvider.debugInfoEnabled(false);
}]);

app.factory('billFactory', function($http) {
  var factory = {};

  factory.getAllCategories = function() {
    return $http.get('/api/category/list');
  };

  factory.getProduct = function(page, rp, terms, cate_id) {
    return $http({
      url: '/api/product/search',
      method: 'post',
      headers: {'Content-Type': 'application/json'},
      data: {page: page||1, rp: rp||10, term: terms||'', cate_id: cate_id||''}
    });
  };

  factory.newBill = function() {
    return $http.get('/api/bill/new');
  };

  factory.openBill = function(id) {
    return $http.get('/api/bill/open/' + id);
  };

  factory.saveBill = function(bill) {
    return $http({
      url: '/api/bill/save',
      method: 'post',
      data: {'bill': bill}
    })
  };

  factory.holdBill = function() {
    return $http.get('/api/bill/hold');
  };

  factory.checkoutBill = function(bill, checkout) {
    return $http({
      url: '/api/bill/checkout',
      method: 'post',
      data: {'bill': bill, 'checkout': checkout}
    });
  };

  factory.emailBill = function(custId) {
    return $http.get('/api/customer/get/' + custId)
  };

  factory.completeBill = function(bill_id, email) {
    return $http({
      url: '/report/bill/email',
      method: 'post',
      data: {'bill_id': bill_id, 'receiver': email}
    });
  };

  factory.markCompleteBill = function(id) {
    return $http.get('/api/bill/complete/' + id);
  };

  factory.deleteBill = function(id) {
    return $http.get('/api/bill/delete/' + id);
  };

  factory.saveCustomer = function(cust) {
    return $http({
      url: '/api/customer/add',
      method: 'post',
      data: {'customer': cust}
    });
  };

  return factory;
});


app.controller('ctrl', function($scope, $http, billFactory) {
  // JSON data list & object
  $scope.categories     = [];
  $scope.products       = [];
  $scope.billItems      = [];
  $scope.cust           = {};
  // search & pagination
  $scope.page           = 0;
  $scope.rp             = 5;
  $scope.terms          = '';
  $scope.results        = {};
  $scope.total          = 0;
  $scope.pageCount      = 0;
  // category selected
  $scope.cate_id        = 0;
  $scope.cate_name      = '';
  // bill
  $scope.bill           = {};
  $scope.sum            = {};
  // bill on-hold
  $scope.holdBills      = [];
  $scope.holdBillCount  = 0;
  // customer info
  $scope.checkout       = {};
  $scope.customer       = {};

  // load all active categories
  $scope.getAllCategories = function() {
    billFactory.getAllCategories().success(function(data) {
      $scope.categories = data.categories;
    });
  };

  // reset all bill data
  $scope.reset = function() {
    $scope.page = 0;
    $scope.total = 0;
    $scope.pageCount = 0;
    $scope.cate_id = 0;
    $scope.cate_name = '';
    $scope.products = [];
  };

  // interface function to search a product
  $scope.searchProduct = function() {
    $scope.reset();
    $scope.getProduct();
  };

  // interface function to search product by category id
  $scope.searchByCategory = function(id, name) {
    $scope.reset();
    $scope.terms = '';
    $scope.cate_id = id;
    $scope.cate_name = name;
    $scope.getProduct();
  };

  // implements function to search all product display per page
  $scope.getProduct = function() {
    billFactory.getProduct($scope.page, $scope.rp, $scope.terms, $scope.cate_id).then(function(out) {
      var data = out.data;
      $scope.products = data.products;
      if(data.total_pages > 1) {
        $scope.total = data.total;
        $scope.pageCount = data.page_count;
        $scope.results = {totalPages: data.total_pages, currentPage: $scope.page};
      } else {
        $scope.results = {};
      }
    });

    if (!$scope.cate_id) {
      $scope.cate_name = 'All Products';
    }

    $('.dropdown-toggle:first-child').html($scope.cate_name + ' ' + '<span class="caret"></span>');
  };

  // detect page changing listener
  $scope.$on('page', function(e, page) {
    $scope.page = page;
    if (page) {
      $scope.getProduct();
    }
  });

  // add product to bill item
  $scope.addBillItem = function(id, name, price, qty) {
    var isUpdated = false;
    angular.forEach($scope.billItems, function(item) {
      if (id === item.id) {
        item.qty = parseInt(item.qty, 10) + 1;
        isUpdated = true;
      }
    });

    if (!isUpdated) {
      // insert new bill item
      $scope.billItems.push({'id': id, 'name': name, 'price': price, 'qty': qty});
    }
  };

  // delete bill item
  $scope.deleteBillItem = function(index) {
    $scope.billItems.splice(index, 1);
  };

  // watch bill on-change and then re-calculate bill's amount
  $scope.$watch('billItems', function() {
    var totalQty = 0;
    var totalAmount = 0;
    var totalDisc = 0;
    var totalTax = 0;

    angular.forEach($scope.billItems, function(item) {
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

  // reset bill item
  $scope.resetBill = function() {
    $scope.reset();
    $scope.bill = {};
    $scope.billItems = [];
    $scope.customer = {};
    $scope.searchByCategory();
    $('#cust_id').val('');
    $('#customer').select2('val', '');
  };

  // renew bill and cancel old bill data
  $scope.voidBill = function() {
    $scope.resetBill();
    $scope.newBill();
  };

  // initial new bill
  $scope.newBill = function() {
    billFactory.newBill().success(function(data) {
      custPlaceholder();
      $scope.bill = data.bill;
      $scope.holdBillCount = data.hold_bill_count;
    });
  };

  // load on-hold bills
  $scope.holdBill = function() {
    billFactory.holdBill().success(function(data) {
      $scope.holdBills = data.hold_bills;
      $('#holdbill-modal').modal('show');
    });
  };

  // selected customer item
  $scope.bindCustomer = function() {
      $('#cust_id').val($scope.bill.cust_id);
      var ctm = $scope.bill.customer;
      if(ctm) {
        var $cust = $('#customer').siblings().find('.select2-selection__rendered');
        $cust.html((ctm.code + ' ' + ctm.firstname + ' ' + (ctm.lastname||'')).trim());
      }
  };

  // open existing bill by id
  $scope.openBill = function(id) {
    billFactory.openBill(id).success(function(data) {
      $scope.resetBill();
      $scope.bill = data.bill;
      // add bill item
      angular.forEach($scope.bill.bill_items, function(item) {
        $scope.addBillItem(item.product_id, item.product.name, item.product.unit_price, item.qty);
      });
      // rebinding customer
      custPlaceholder();
      $scope.bindCustomer();
    });
    $('#holdbill-modal').modal('hide');
  };

  // open from on-hold bill
  $scope.openHoldBill = function() {
    $scope.holdBill();
  };

  // prepare to save bill
  $scope.prepareBill = function() {
    angular.forEach($scope.billItems, function(item, $index) {
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

    $scope.bill.bill_items = $scope.billItems;
    $scope.bill.total_qty = $scope.sum.total_qty;
    $scope.bill.total_price = $scope.sum.total_price;
    $scope.bill.total_tax = $scope.sum.total_tax;
    $scope.bill.total_discount = $scope.sum.total_discount;
    $scope.bill.total_amount = $scope.sum.total_amount;
    $scope.bill.remark = '';
    $scope.bill.cust_id = $('#cust_id').val();
  };

  // call API to execute saved
  $scope.saveBill = function() {
    $scope.prepareBill();
    billFactory.saveBill($scope.bill).then(function(output) {
      if (output.data.result) {
        alert('Save completed');
        $scope.voidBill();
      }
    });
  };

  // delete bill by its id
  $scope.deleteBill = function(id) {
    billFactory.deleteBill(id).success(function(data) {
      if(data.result) {
        $scope.resetBill();
        $scope.newBill();
      }
    });
    $('#holdbill-modal').modal('hide');
  };

  // clear customer dropdown
  $scope.clearCustomer = function() {
    $scope.cust = {gender: ''};
  };

  // cal API to execute saving customer
  $scope.saveCustomer = function() {
    var errormsg = '';
    var cust = $scope.cust;

    if (!cust.firstname)
      errormsg += 'Enter customer name\n';

    if (!cust.email)
      errormsg += 'Enter customer email\n';

    if (errormsg) {
      alert(errormsg); return;
    }

    billFactory.saveCustomer($scope.cust).then(function(output) {
      if (output.data.result) {
        alert('Save completed');
        // after add new customer
        // re assign value in current bill
        var cust = output.data.result;
        $scope.bill.cust_id = cust.id;
        $scope.bill.customer = cust;
        $scope.bindCustomer();
      }
    });
    $('#customer-modal').modal('hide');
  };

  // open customer dialog
  $scope.openCustomer = function() {
    $scope.clearCustomer();
    $('#customer-modal').modal('show');
  };

  // watch the bill amount to checkout (payment)
  $scope.$watch('checkout ', function() {
    var total_amount = parseFloat($scope.sum.total_amount || 0);
    var total_charge = parseFloat($scope.checkout.total_charge || 0);
    var total_return = total_charge > total_amount ? (total_charge - total_amount) : 0;
    $scope.checkout = {total_amount: total_amount, total_charge: total_charge, total_return: total_return};
  }, true);

  // open checked-out bill dialog
  $scope.openCheckout = function() {
    if (!$scope.sum.total_amount)
      return;
    $scope.checkout = {total_amount: $scope.sum.total_amount, total_charge: 0, total_return: 0};
    $('#checkout-modal').modal('show');
  };

  // execute save checkout bill
  $scope.checkoutBill = function() {
    $scope.prepareBill();
    billFactory.checkoutBill($scope.bill, $scope.checkout).then(function(output) {
      if (output.data.result) {
        var id = output.data.result;
        $scope.openBill(id);
        $scope.bill.id = id;
        $('#checkout-modal').modal('hide').on('hidden.bs.modal', function(e) {
          $('#receipt-modal').modal('show');
        });
      }
    });
  };

  // show customer email dialog
  $scope.emailBill = function() {
    if ($scope.bill.cust_id <= 0)
      return;
    $scope.customer = {};
    billFactory.emailBill($scope.bill.cust_id).success(function(data) {
      $scope.customer = data.customer;
      $('#btnSendMail').prop('disabled', false);
      $('#btnSendMail').html('Send');
      $('#receipt-modal').modal('hide').on('hidden.bs.modal', function(e) {
        $('#email-modal').modal('show');
      });
    });
  };

  // back to checkout dialog
  $scope.backToCheckoutBill = function() {
    $('#receipt-modal').modal('hide').on('hidden.bs.modal', function(e) {
      $('#checkout-modal').modal('show');
    });
  };

  // back to receipt dialog
  $scope.backToReceiptBill = function() {
    $('#email-modal').modal('hide').on('hidden.bs.modal', function(e) {
      $('#receipt-modal').modal('show');
    });
  };

  // print bill payment slip (receipt)
  $scope.printBill = function() {
    $scope.viewBillPdf();
    $('#receipt-modal').modal('hide').on('hidden.bs.modal', function(e) {
      $('#complete-modal').modal('show');
    });
  };

  // complete bill processing
  $scope.completeBill = function() {
    $('#btnSendMail').prop('disabled', true);
    $('#btnSendMail').html('Sending...');
    billFactory.completeBill($scope.bill.id, $scope.customer.email).then(function(output) {
      if (output.data.result) {
        $scope.markCompleteBill('complete_with_receipt');
      }
      $('#btnSendMail').prop('disabled', false);
    });
  };

  // complete bill without receipt slip
  $scope.completeNoReceipt = function() {
    $scope.markCompleteBill('complete_no_receipt');
  };

  // complete bill and continue to new sale
  $scope.closeCompleteBill = function() {
    $('#complete-modal').modal('hide').on('hidden.bs.modal', function(e) {
      $scope.voidBill();
    });
  };

  // mark bill as a completed
  $scope.markCompleteBill = function(choice) {
    var id = $scope.bill.id;
    if (!id)
      return;
    billFactory.markCompleteBill(id).success(function(data) {
      if (data.result) {
        if(choice === 'complete_with_receipt') {
          $('#email-modal').modal('hide').on('hidden.bs.modal', function(e) {
            $('#complete-modal').modal('show');
          });
        } else {
          $('#receipt-modal').modal('hide').on('hidden.bs.modal', function(e) {
            $('#complete-modal').modal('show');
          });
        }
      }
    });
  };

  // view bill slip as PDF
  $scope.viewBillPdf = function() {
    if(!$scope.bill.id)
      return;
    var w = 700;
    var h = 450;
    var l = Number((screen.width / 2) - (w / 2));
    var t = Number((screen.height / 2) - (h / 2));
    var props = 'directories=0,location=0,menubar=0,resizable=0,scrollbars=0,status=0,width=' + w + ',height=' + h + ',top=' + t + ',left=' + l;
    window.open('/report/bill/pdf/' + $scope.bill.id, 'Report Viewer', props);
  };

  $scope.newBill();
  $scope.searchByCategory();
  $scope.getAllCategories();
});

$(function() {
  $.fn.modal.prototype.constructor.Constructor.DEFAULTS.backdrop = 'static';
  $('body').on('hidden.bs.modal', '.modal', function() {
    $(this).removeData();
    $(this).off('hidden.bs.modal');
  });

  $("#customer").select2({
    minimumInputLength: 1,
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
      return repo.code + ' ' + repo.firstname + ' ' + (repo.lastname||'') + '<br><span class="small">' + repo.email + '</span>';
    },
    templateSelection: function(repo) {
      if(repo.code) {
        $('#cust_id').val(repo.id);
        return (repo.code + ' ' + repo.firstname + ' ' + (repo.lastname||'')).trim();
      }
      return '';
    }
  });
  // clear customer icon
  $('#clearcust').on('click', function() {
    $('#cust_id').val('');
    $('#customer').select2('val', '');
    custPlaceholder();
  });
});
