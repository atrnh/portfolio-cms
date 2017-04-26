/* jshint esversion: 6 */
(function(angular) {
  'use strict';

var removeItem = function(item, collection) {
  var idx = collection.indexOf(item);
  if (idx >= 0) {
    collection.splice(idx, 1);
  }
};

angular.module('dashboard', [
  'ngRoute',
  'dbService',
  'ngFileUpload',
  'ngSanitize',
  'ui.bootstrap',
])
  .config(['$routeProvider', function ($routeProvider) {

    var universalResolves = {
      'CategoriesData': function(Categories) {
        return Categories.promise;
      },
    };

    var customRouteProvider = angular.extend({}, $routeProvider, {
      when: function(path, route) {
        route.resolve = (route.resolve) ? route.resolve : {};
        angular.extend(route.resolve, universalResolves);
        $routeProvider.when(path, route);
        return this;
      }
    });

    customRouteProvider
      .when('/', {
        templateUrl: '/static/js/templates/dashboard-view-projects.html',
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

      .when('/new/page', {
        templateUrl: '/static/js/templates/new-page.html',
        controller: 'NewPageController'
      })

      .when('/new/link', {
        templateUrl: '/static/js/templates/new-link.html',
        controller: 'NewLinkController'
      })

      .when('/edit/category/:categoryId', {
          templateUrl: '/static/js/templates/edit-category.html',
          controller: 'EditCategoryController'
      })

      .when('/edit/project/:projectId', {
        templateUrl: '/static/js/templates/edit-project.html'
      })

      .when('/edit/page/:pageId', {
        templateUrl: '/static/js/templates/edit-page.html',
        controller: 'EditPageController'
      })

      .when('/edit/link/:linkId', {
        templateUrl: '/static/js/templates/edit-link.html',
        controller: 'EditLinkController'
      })
      ;
  }])

  .filter('isEmpty', [function() {
    return function(object) {
      return object ? angular.equals({}, object) ||
                      object.projects === null :
                      true;
    };
  }])

  .controller(
    'ProjectsController',
    function ($scope, $route, Categories, Project, Page, Link) {
      var toDelete;
      var undoIdx;
      var undoType;
      var projects;

      $scope.showUndo = false;
      $scope.accordion = {
        isCategoriesOpen: true,
        isPagesOpen: false,
        isLinksOpen: false
      };

      $scope.categories = Categories.all();

      $scope.pages = Page.getAll().$promise.then(function (pages) {
        $scope.pages = pages;
      });

      $scope.links = Link.getAll().$promise.then(function (links) {
        $scope.links = links;
      });

      console.log($scope.accordion.isCategoriesOpen);

      $scope.queueDelete = function (type, obj, parent=null) {
        undoType = type;

        if (type === 'category') {
          $scope.deletedName = Categories.queueDelete(obj).title;
        } else if (type === 'project') {
          toDelete = obj;
          projects = Categories.all()[parent.id].projects;
          delete projects[obj.id];
          undoIdx = projects.id;
        }

        $scope.showUndo = true;
      };

      $scope.undoDelete = function () {
        if (undoType === 'category') {
          Categories.undoDelete();
        } else if (undoType === 'project') {
          projects[toDelete.id] = toDelete;
        }

        $scope.showUndo = false;
      };

      $scope.commitDelete = function () {
        if (undoType === 'category') {
          Categories.commitDelete();
        } else if (undoType === 'project') {
          Project.delete(toDelete.id).$promise.then(function (project) {
            console.log('project deleted');
          });
        }

        $scope.showUndo = false;
      };
    }
  )

  .controller('NewProjectController', function ($scope, $location, Category, Project, Tag, Categories, Tags) {
    $scope.pendingTags = [];

    $scope.categories = Categories.all();
    $scope.thisCategory = Categories.first();

    $scope.tags = Tag.getAll().$promise.then(function (tags) {
      $scope.tags = tags;
    });

    $scope.handleTags = function(keyEvent) {
      var key = keyEvent.key;

      if (key === ',' || key === 'Enter') {
        if (typeof $scope.newTag === 'string') {
          $scope.newTag = $scope.newTag.replace(' ', '-');
          $scope.newTag = {'code': $scope.newTag};
        }

        $scope.pendingTags.push($scope.newTag);
        $scope.newTag = null;
      }
    };

    $scope.deleteTag = function(tag) {
      removeItem(tag, $scope.pendingTags);
    };

    $scope.addProject = function(title, desc, category) {
      var tagCodes = $scope.pendingTags.map(function (tag) {
        return tag.code;
      });
      var obj = {
        title: title,
        desc: desc,
        categoryId: category.id,
        tags: tagCodes,
      };

      Project.addNew(obj)
        .$promise
        .then(function (project) {
          Categories.addProjectTo(category, project);
          $location.path('/');
        })
      ;
    };
  })

  .controller('EditProjectController', function ($scope, $location, $routeParams, Project, Category, Upload, Media, Tag, Categories) {

    $scope.id = $routeParams.projectId;
    var categoryCopy;
    var projectCopy;

    $scope.tags = Tag.getAll().$promise.then(function (tags) {
      $scope.tags = tags;
    });

    Project.getById($scope.id).$promise.then(function (project) {
      var keys = Object.keys(project.categories);
      Object.keys(project.media).map(function (m) {
        project.media[m].open = false;
      });

      $scope.project = project;

      $scope.categories = Categories.all();
      categoryCopy = Categories.get(project.categories[keys[0]].id);
      projectCopy = Categories.getProjectById(categoryCopy, project.id);
      $scope.thisCategory = categoryCopy;
    });

    $scope.update = function(prop, value) {
      var obj = {};
      obj[prop] = value;
      Project.update($scope.id, obj)
        .$promise.then(function (resp) {
          if (prop === 'categoryId') {
            Categories.addProjectTo($scope.thisCategory, $scope.project);
            Categories.removeProjectFrom(categoryCopy, projectCopy);
          }
          Categories.updateProject($scope.thisCategory, $scope.project.id, prop, value);
          $scope.project[prop] = value;
        });
    };

    $scope.handleTags = function(keyEvent) {
      var key = keyEvent.key;
      if (key === ',' || key === 'Enter') {
        if (typeof $scope.newTag === 'string') {
          $scope.newTag = $scope.newTag.replace(' ', '-');
          $scope.newTag = {'code': $scope.newTag};
        }
        $scope.project.tags.push($scope.newTag);
        Project.newTag($scope.id, $scope.newTag)
          .$promise.then(function (tag) {
            $scope.newTag = null;
        });
      }
    };

    $scope.deleteTag = function(tag) {
      Project.deleteTag($scope.id, tag.code).$promise.then(function (project) {
        removeItem(tag, $scope.project.tags);
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
        removeItem(media, $scope.project.media);
      });
    };
  })

  .controller('NewCategoryController', function ($scope, Category, $location, Categories) {
    $scope.addCategory = function (title, desc) {
      Category.addNew(title, desc).$promise.then(function (category) {
        Categories.push(category);
        $location.path('/');
      });
    };
  })

  .controller('EditCategoryController', function ($scope, $routeParams, Category, Categories) {
    var id = parseInt($routeParams.categoryId, 10);
    $scope.category = Categories.get(id);

    $scope.update = function (prop, value) {
      var obj = {};
      obj[prop] = value;
      Category.update(id, obj).$promise.then(function (category) {
        $scope.category[prop] = value;
      });
    };
  })

  .controller('NewPageController', ['$scope', 'Page', '$location', function ($scope, Page, $location) {
    $scope.addPage = function(title, content) {
      Page.addNew(title, content).$promise.then(function (page) {
        $location.path('/');
      });
    };
  }])

  .controller('EditPageController', ['$scope', '$routeParams', 'Page', function ($scope, $routeParams, Page) {
    var id = parseInt($routeParams.pageId, 10);
    $scope.page = Page.getById(id);

    $scope.update = function (prop, value) {
      var obj = {};
      obj[prop] = value;
      Page.update(id, obj).$promise.then(function (project) {
        $scope.page[prop] = value;
      });
    };
  }])

  .controller('NewLinkController', ['$scope', 'Link', '$location', function ($scope, Link, $location) {
    $scope.addLink = function(title, url) {
      Link.addNew(title, url).$promise.then(function (link) {
        $location.path('/');
      });
    };
  }])

  .controller('EditLinkController', ['$scope', '$routeParams', 'Link', function ($scope, $routeParams, Link) {
    var id = parseInt($routeParams.linkId, 10);
    $scope.link = Link.getById(id);

    $scope.update = function (prop, value) {
      var obj = {};
      obj[prop] = value;
      Link.update(id, obj).$promise.then(function (link) {
        $scope.link[prop] = value;
      });
    };
  }])
;
})(window.angular);
