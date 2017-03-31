var app = angular.module('portfolio', ['ngRoute'])

  .factory('categoryService', function() {
    return {
      getProjects: function (categoryId) {
        console.log(categoryId);
        return categoryId;
      }
    };
  })

  .config(function ($interpolateProvider, $routeProvider) {
    $interpolateProvider
      .startSymbol('{[{')
      .endSymbol('}]}');

    $routeProvider
      .when('/', {
        controller: 'CategoryController',
        resolve: {
          categoryService: function(categoryService) {
            return categoryService;
          }
        }
      });
  })

  .controller('CategoryController', function ($scope, categoryService) {
    $scope.updateView = function(categoryId) {
      $scope.update = categoryId + '!';
    };

    $scope.test = 'test';
  })
;
