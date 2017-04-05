angular.module('dashboard', ['ngRoute', 'dbResource'])
  .config(function ($interpolateProvider, $routeProvider) {
    // $interpolateProvider
    //   .startSymbol('{[{')
    //   .endSymbol('}]}');

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

  .controller('ProjectsController', function ($scope, $location, Category) {
    Category.getAll('true').$promise.then(function (categories) {
      $scope.categories = categories;
    });

    $scope.deleteCategory = function (id) {
      Category.delete(id).$promise.then(function (categories) {
        $scope.categories = categories;
      });
    };
  })

  .controller('NewProjectController', function ($scope, $location, Category, Project) {
    Category.getAll().$promise.then(function (categories) {
      $scope.categories = categories;
    });

    $scope.addProject = function(title, desc, categoryId, rawTags) {
      var re = /\s*,\s*/;
      var tags = rawTags.split(re);

      // try {
      //   tags = rawTags.split(re);
      // } catch (e) {
      //   if (e instanceof TypeError) {
      //     tags = [];
      //   }
      // }

      Project.addNew(title, desc, categoryId, tags)
        .$promise
        .then(function () {
          $location.path('/');
        })
      ;
    };
  })

  .controller('NewCategoryController', function ($scope, Category, $location) {
    $scope.addCategory = function (title, desc) {
      Category.addNew(title, desc).$promise.then(function (categories) {
        $location.path('/');
      });
    };
  })
;
