(function(angular) {
  'use strict';
angular.module('portfolio', ['dbResource', 'ngRoute', 'ngSanitize'])

  .config(function ($routeProvider) {
    $routeProvider
      .when('/:categoryTitle/:id', {
        templateUrl: '/static/js/templates/category-view.html',
        controller: 'CategoryViewController'
      })

      .when('/:categoryTitle/:categoryId/:projectTitle/:id', {
        templateUrl: '/static/js/templates/project-view.html',
        controller: 'ProjectViewController'
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
;
})(window.angular);
