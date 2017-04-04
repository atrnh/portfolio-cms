angular.module("dashboard", ['ngRoute', 'ngResource'])
  .config(function ($interpolateProvider, $routeProvider) {
    $interpolateProvider
      .startSymbol('{[{')
      .endSymbol('}]}');

    $routeProvider
      .when('/', {
        templateUrl: '/static/js/templates/dashboard-projects-view.html',
        controller: 'ProjectsController'
      })
      .when('/new/project', {
        templateUrl: '/static/js/templates/new-project-form.html',
        controller: 'NewProjectController'
      })
      .when('/new/category', {
        templateUrl: '/static/js/templates/new-category-form.html',
        controller: 'NewCategoryController'
      })
      ;
  })

  // Project service for getting project data from server
  .factory('Project', function ($resource) {
    return {

      // Returns array of projects associated with given category id
      getAllInCategory: function(id) {
        return $resource('/projects.json', {categoryId: id}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      getAll: function() {
        return $resource('/projects.json', {}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      getById: function(id) {
        return $resource('/project.json', {projectId: id}, {
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
      },

      getAll: function(loadAll) {
        return $resource('/categories.json', {loadAll: loadAll}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      addNew: function(title, desc) {
        return $resource('/admin/category', {}, {
          'post': {
            method: 'POST'
          }

        }).post({}, {'title': title, 'desc': desc});
      }
    };
  })

  .controller('ProjectsController', function ($scope, Category) {
    Category.getAll('t').$promise.then(function (categories) {
      $scope.categories = categories;
    });
  })

  .controller('NewProjectController', function ($scope, Category) {
    Category.getAll().$promise.then(function (categories) {
      $scope.categories = categories;
    });
  })

  .controller('NewCategoryController', function ($scope, Category, $location) {
    $scope.addCategory = function (title, desc) {
      Category.addNew(title, desc) .$promise.then(function (categories) {
        $location.path('/');
      });
    };
  })
;
