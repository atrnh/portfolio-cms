(function(angular) {
  'use strict';
angular.module('portfolio', ['dbResource', 'ngRoute', 'ngSanitize'])

  .config(function ($routeProvider) {
    $routeProvider
      .when('/category/:categoryTitle/:id', {
        templateUrl: '/static/js/templates/view-category.html',
        controller: 'CategoryViewController'
      })

      .when('/project/:projectTitle/:id', {
        templateUrl: '/static/js/templates/view-project.html',
        controller: 'ProjectViewController'
      })

      .when('/tag/:code', {
        templateUrl: '/static/js/templates/view-tag.html',
        controller: 'TagViewController'
      })
      ;
    }
  )

  .controller('CategoryViewController', function ($scope, $routeParams, Category) {
    Category.getById($routeParams.id)
      .$promise.then(function (category) {
        $scope.category = category;
      }
    );
  })

  .controller('ProjectViewController', function ($scope, $routeParams, Project) {
    Project.getById($routeParams.id)
      .$promise.then(function (project) {
        $scope.project = project;
      }
    );
  })

  .controller('TagViewController', function ($scope, $routeParams, Tag) {
    Tag.getByCode($routeParams.code)
      .$promise.then(function (tag) {
        $scope.tag = tag;
      }
    );
  })
;
})(window.angular);
