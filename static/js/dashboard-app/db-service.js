/* jshint esversion: 6 */
(function(angular) {
  'use strict';

  var dbService = angular.module('dbService', ['dbResource']);

  dbService.service('Tags', ['Tag', function (Tag) {
    var all;

    var promise = Tag.getAll().$promise.then(function (tags) {
      all = tags;
    });

    return {
      promise: promise,

      all: function() {
        return all;
      }
    };
  }]);

  dbService.service('Categories', ['Category', function (Category) {
    var self = this;
    var all;
    var undoIdx;
    var toDelete = [];

    var promise = Category.getAll('true').$promise.then(function (categories) {
      all = categories;
    });

    return {
      promise: promise,

      all: function() {
        return all;
      },

      addNew: function(category) {
        all.push(category);
      },

      queueDelete: function(category) {
        undoIdx = all.indexOf(category);
        toDelete.push(category);

        // If toDelete has more than one object in it, delete the oldest item
        if (toDelete.length > 1) {
          this.commitDelete();
        }

        if (undoIdx >= 0) {
          all.splice(undoIdx, 1);
        }

        console.log(toDelete[toDelete.length - 1]);

        return toDelete[toDelete.length - 1];
      },

      undoDelete: function() {
        all.splice(undoIdx, 0, toDelete[toDelete.length - 1]);
      },

      commitDelete: function() {
        Category.delete(toDelete.shift().id);
      },

      remove: function(category) {
        var idx = all.indexOf(category);
        if (idx >= 0) {
          all.splice(idx, 1);
        }
      },

      insertAt: function(idx, category) {
        all.splice(idx, 0, category);
      },

      push: function(category) {
        all.push(category);
      },

      get: function(id) {
        var found = all.find(function (category) {
          return category.id === id;
        });

        return found;
      },

      addProjectTo: function(category, project) {
        var idx = all.indexOf(category);
        if (idx >= 0) {
          all[idx].projects.push(project);
        }
      },

      removeProjectFrom: function(category, project) {
        var cIdx = all.indexOf(category);
        var pIdx = all[cIdx].projects.indexOf(project);

        if (pIdx >= 0) {
          all[cIdx].projects.splice(pIdx, 1);
        }
      }
    };
  }]);

  // dbService.service('Undo', function () {
  //
  // });

})(window.angular);
