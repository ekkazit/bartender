angular.module('pager', []).directive('paginate', function() {
  return {
    scope: {
      results: '=paginate'
    },
    template:
      '<ul class="pagination" ng-show="totalPages">' +
        '<li ng-repeat="n in pages" ng-class="{active:n==currentPage}"><a href="#" ng-bind="n" ng-click="setPage(n)">1</a></li>' +
      '</ul>',
    link: function(scope) {
      scope.nextPage = function() {
        if (scope.currentPage < scope.totalPages) {
          scope.currentPage++;
        }
      };

      scope.prevPage = function() {
        if (scope.currentPage > 1) {
          scope.currentPage--;
        }
      };

      scope.firstPage = function() {
        scope.currentPage = 1;
      };

      scope.lastPage = function() {
        scope.currentPage = scope.totalPages;
      };

      scope.setPage = function(page) {
        scope.currentPage = page;
      };

      var paginate = function(results, oldResults) {
        scope.currentPage = results.currentPage || 1;
        scope.totalPages = results.totalPages;

        scope.pages = [];
        for (var i = 1; i <= scope.totalPages; i++) {
          scope.pages.push(i);
        }
      };

      var pageChange = function(newPage, lastPage) {
        if (newPage == lastPage)
          return;
        scope.$emit('page', newPage);
      };

      scope.$watch('results', paginate);
      scope.$watch('currentPage', pageChange);
    }
  }
});
