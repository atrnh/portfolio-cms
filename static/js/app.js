var app = angular.module('portfolio', [])
  // .config( function ($interpolateProvider) {
  //   $interpolateProvider.startSymbol('{[{');
  //   $interpolateProvider.endSymbol('}]}');
  // })

  // .factory('categoriesService', function ($http) {
  //   return {
  //     getCategories: function () {
  //       return $http.get('categories.json').then(function (response) {
  //         return response.data;
  //       });
  //     }
  //   };
  // })
  //
  // .controller('NavController', function ($scope, $http) {
  //   $scope.boo = 'boo';
  // })
;

app.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});

app.controller('NavController', function ($scope, $http) {
  $scope.foo = 'bar';

  $http.get('/categories.json').then(function (response) {
    $scope.categories = response.data;
  });
});
