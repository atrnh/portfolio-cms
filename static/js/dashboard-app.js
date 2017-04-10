(function(angular) {
  'use strict';

angular.module('dashboard', ['ngRoute', 'dbResource'])
  .config(function ($interpolateProvider, $routeProvider) {

    $routeProvider
      .when('/', {
        templateUrl: '/static/js/templates/dashboard-projects-view.html',
        controller: 'ProjectsController'
      })

      .when('/new/project', {
        templateUrl: '/static/js/templates/new-project.html',
        controller: 'NewProjectController'
      })

      .when('/new/category', {
        templateUrl: '/static/js/templates/new-category.html',
        controller: 'NewCategoryController'
      })

      .when('/edit/category/:categoryId', {
          templateUrl: '/static/js/templates/edit-category.html',
          controller: 'EditCategoryController'
      })

      .when('/edit/project/:projectId', {
        templateUrl: '/static/js/templates/edit-project.html',
        controller: 'EditProjectController'
      })
      ;
  })

  .controller('ProjectsController', function ($scope, $location, Category, Project) {
    Category.getAll('true').$promise.then(function (categories) {
      $scope.categories = categories;
    });

    $scope.deleteCategory = function (id) {
      Category.delete(id).$promise.then(function (categories) {
        $scope.categories = categories;
      });
    };

    $scope.deleteProject = function (id) {
      Project.delete(id).$promise.then(function (categories) {
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

      Project.addNew(title, desc, categoryId, tags)
        .$promise
        .then(function () {
          $location.path('/');
        })
      ;
    };
  })

  .controller('EditProjectController', function ($scope, $location, $routeParams, Project, Category) {
    $scope.editTitle = false;

    $scope.id = $routeParams.projectId;
    Project.getById($scope.id).$promise.then(function (project) {
      $scope.project = project;
      $scope.currCategory = project.categories[0].id;
    });

    Category.getAll().$promise.then(function (categories) {
      $scope.categories = categories;
      $scope.currCategoryIdx = categories.findIndex(function (category) {
        return category.id === $scope.currCategory;
      });
      $scope.thisCategory = $scope.categories[$scope.currCategoryIdx];
    });

    $scope.updateProject = function(title, desc, category, rawTags, id=$scope.id) {
      var tags;
      if (rawTags) {
        tags = rawTags.split(/\s*,\s*/);
      }

      console.log(category);

      Project.update(id, title, desc, category, tags)
        .$promise.then(function (project) {
          $scope.project = project;
        });
      $scope.editTitle = false;
    };

    $scope.deleteTag = function(tagCode, id=$scope.id) {
      Project.deleteTag(id, tagCode).$promise.then(function (project) {
        $scope.project = project;
      });
    };

    $scope.startEdit = function(editTitle) {
      console.log(editTitle);
      if (editTitle) {
        $scope.editTitle = false;
      } else {
        $scope.editTitle = true;
      }

      console.log($scope.editTitle);
    };
  })

  .controller('NewCategoryController', function ($scope, Category, $location) {
    $scope.addCategory = function (title, desc) {
      Category.addNew(title, desc).$promise.then(function (categories) {
        $location.path('/');
      });
    };
  })

  .controller('EditCategoryController', function ($scope, $location, $routeParams, Category) {
    $scope.id = $routeParams.categoryId;
    $scope.category = Category.getById($scope.id);

    $scope.updateCategory = function (title, desc, id=$scope.id) {
      Category.update(id, title, desc).$promise.then(function (categories) {
        $location.path('/');
      });
    };
  })
;
})(window.angular);
