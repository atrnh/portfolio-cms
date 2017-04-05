var app = angular.module('portfolio', ['dbResource'])

  // .config(function ($interpolateProvider) {
  //   $interpolateProvider
  //     .startSymbol('{[{')
  //     .endSymbol('}]}');
  // })

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
