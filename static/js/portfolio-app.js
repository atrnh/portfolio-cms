(function(angular) {
  'use strict';
angular.module('portfolio', ['dbResource', 'ngRoute', 'ngSanitize', 'ui.bootstrap'])

  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: '/static/js/templates/view-portfolio-main.html',
        controller: 'MainViewController'
      })

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

      .when('/page/:pageTitle/:id', {
        templateUrl: '/static/js/templates/view-page.html',
        controller: 'PageViewController'
      })
      ;
    }
  )

  .controller('IndexViewController', ['$scope', 'Category', 'Page', 'Link', '$window', function ($scope, Category, Page, Link, $window) {
    var self = this;
    Category.getAllList().$promise.then(function (categories) {
      for (let i = 0; i < categories.length; i++) {
        categories[i].open = true;
      }

      self.categories = categories;
      console.log(categories);
    });

    Page.getAll().$promise.then(function (pages) {
      self.pages = pages;
    });

    Link.getAll().$promise.then(function (links) {
      self.links = links;
    });

    self.goTo = function(url) {
      $window.open(url);
    };
  }])

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
        var tags = project.tags.map(function (tag) {
          return tag.code;
        });
        $scope.lastTag = tags.pop();
        $scope.tags = tags;
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

  .controller('MainViewController', function ($scope, Media) {
    Media.getAll().$promise.then(function (media) {
      $scope.recentMedia = media;
    });
  })

  .controller('PageViewController', function ($scope, $routeParams, Page) {
    Page.getById($routeParams.id).$promise.then(function (page) {
      $scope.page = page;
    });
  })
;
})(window.angular);
