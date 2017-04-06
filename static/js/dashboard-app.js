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

  .controller('EditProjectController', function ($scope, $location, $routeParams, Project, Category) {
    $scope.id = $routeParams.projectId;
    $scope.project = Project.getById($scope.id);
    var tags = [];

    console.log($scope.project.tags);

    if ($scope.project.tags) {
      for (let tag in $scope.project.tags) {
        tags.push(tag.code);
      }
    }

    $scope.tags = tags.join(', ');

    Category.getAll().$promise.then(function (categories) {
      $scope.categories = categories;
    });

    $scope.updateProject = function(title, desc, categoryId, rawTags, id=$scope.id) {
      var tags;
      if (rawTags) {
        tags = rawTags.split(/\s*,\s*/);
      }

      Project.update(id, title, desc, categoryId, tags)
        .$promise.then(function (categories) {
          $location.path('/');
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
