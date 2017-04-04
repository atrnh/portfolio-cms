var app = angular.module('portfolio', ['ngResource'])

  .config(function ($interpolateProvider) {
    $interpolateProvider
      .startSymbol('{[{')
      .endSymbol('}]}');
  })

  // Project service for getting project data from server
  .factory('Project', function ($resource) {
    return {

      // Returns array of projects associated with given category id
      getAllInCategory: function(id) {
        return $resource('/projects.json', {categoryId: id}, {
          'query': {
            method: 'GET',
            isArray: true
          },
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      getAll: function() {
        return $resource('/projects.json', {}, {
          'query': {
            method: 'GET',
            isArray: true
          },
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      getById: function(id) {
        return $resource('/project.json', {projectId: id}, {
          'query': {
            method: 'GET'
          },
          'get': {
            method: 'GET'
          }
        }).get();
      }

    };
  })

  .factory('Category', function ($resource) {
    return {
      getById: function(id) {
        return $resource('/category.json', {categoryId: id}, {
          'query': {
            method: 'GET'
          },
          'get': {
            method: 'GET'
          }
        }).get();
      }
    };
  })

  .controller('PortfolioController', function ($scope, Project, Category) {
    $scope.viewCategory = function(categoryId) {
      Category.getById(categoryId)
              .$promise.then(function (category) {
                $scope.title = category.title;
                $scope.content = category.projects;
              });
    };

    $scope.viewProject = function(projectId) {
      Project.getById(projectId)
             .$promise.then(function (project) {
               $scope.title = project.title;
               $scope.content = project.media;
             });
    };


  })
;
