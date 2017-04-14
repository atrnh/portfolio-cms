(function(angular) {
  'use strict';

angular.module('dashboard', ['ngRoute', 'dbResource', 'ngFileUpload', 'ngSanitize'])
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
        templateUrl: '/static/js/templates/edit-project.html'
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

  .controller('EditProjectController', function ($scope, $location, $routeParams, Project, Category, Upload, Media) {

    $scope.id = $routeParams.projectId;

    Project.getById($scope.id).$promise.then(function (project) {
      $scope.project = project;

      Category.getAll().$promise.then(function (categories) {
        $scope.categories = categories;
        var idx = categories.findIndex(function (category) {
          return category.id === project.categories[0].id;
        });
        $scope.thisCategory = $scope.categories[idx];
      });
    });

    $scope.update = function(prop, value) {
      var obj = {};
      obj[prop] = value;
      Project.reUpdate($scope.id, obj)
        .$promise.then(function (resp) {
          $scope.project[prop] = value;
        });
    };

    $scope.handleTags = function(keyEvent) {
      var key = keyEvent.key;
      if (key === ',') {
        $scope.project.tags.push({'code': $scope.rawTag});
        Project.newTag($scope.id, $scope.rawTag)
          .$promise.then(function (tag) {
            $scope.rawTag = null;
          });
      }
    };

    $scope.deleteTag = function(tag) {
      Project.deleteTag($scope.id, tag.code).$promise.then(function (project) {
        var idx = $scope.project.tags.indexOf(tag);
        if (idx >= 0) {
          $scope.project.tags.splice(idx, 1);
        }
      });
    };

    $scope.upload = function(imageFile) {
      Upload.upload({
        url: '/upload',
        data: {'imageFile': imageFile, 'projectId': $scope.id}
      }).then(function (resp) {
        $scope.project.media.push(resp.data);
      });
    };

    $scope.updateMedia = function(media, prop, value) {
      var obj = {};
      obj[prop] = value;
      Media.update($scope.id, media.id, obj)
        .$promise.then(function (resp) {
          media[prop] = value;
        });
    };

    $scope.deleteMedia = function(media) {
      Media.delete($scope.id, media.id).$promise.then(function (resp) {
        var idx = $scope.project.media.indexOf(media);
        if (idx >= 0) {
          $scope.project.media.splice(idx, 1);
        }
      });
    };
  })

  .controller('NewCategoryController', function ($scope, Category, $location) {
    $scope.addCategory = function (title, desc) {
      Category.addNew(title, desc).$promise.then(function (categories) {
        $location.path('/');
      });
    };
  })

  .controller('EditCategoryController', function ($scope, $routeParams, Category) {
    $scope.id = $routeParams.categoryId;
    $scope.category = Category.getById($scope.id);

    $scope.update = function (prop, value) {
      var obj = {};
      obj[prop] = value;
      Category.update($scope.id, obj).$promise.then(function (category) {
        $scope.category[prop] = value;
      });
    };
  })
;
})(window.angular);
