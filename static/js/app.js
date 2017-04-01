var app = angular.module('portfolio', ['ngRoute', 'ngResource'])

  .config(function ($interpolateProvider, $routeProvider) {
    $interpolateProvider
      .startSymbol('{[{')
      .endSymbol('}]}');
  })

  // Project service for getting project data from server
  .factory('Project', function ($resource) {
    return {

      // Returns array of projects associated with given category id
      getAllInCategory: function(id) {
        return $resource('category/:categoryId/projects.json', {categoryId: id}, {
          'query': {
            method: 'GET',
            isArray: true
          },
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      }
    };
  })

  .controller('CategoryController', function ($scope, Project) {
    $scope.updateView = function(categoryId) {
      $scope.update = categoryId + '!';

      Project.getAllInCategory(categoryId)
             .$promise.then(function (projects) {
               $scope.projects = projects;
             });
    };


  })
;
