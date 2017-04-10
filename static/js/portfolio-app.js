(function(angular) {
  'use strict';
angular.module('portfolio', ['dbResource'])

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
})(window.angular);
