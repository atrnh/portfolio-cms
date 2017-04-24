/* jshint esversion: 6 */
(function(angular) {
  'use strict';

  var dbService = angular.module('dbService', ['dbResource']);

  dbService.service('Tags', ['Tag', function (Tag) {
    var all;
    var addQueue = [];

    var promise = Tag.getAll().$promise.then(function (tags) {
      all = tags;
    });

    return {
      promise: promise,

      all: function() {
        return all;
      },

      enqueueAdd: function(tag) {
        addQueue.push(tag);
      },

      commitAdd: function(arr) {
        all = all.concat(addQueue);
      }
    };
  }]);

  dbService.service('Categories', ['Category', function (Category) {
    var self = this;
    var all;
    var undoIdx;
    var toDelete = [];
    var ids;

    var promise = Category.getAll('true').$promise.then(function (categories) {
      all = categories;
      ids = Object.keys(all);
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
        toDelete.push(category);

        // If toDelete has more than one object in it, delete the oldest item
        if (toDelete.length > 1) {
          this.commitDelete();
        }

        this.remove(category);

        return toDelete[toDelete.length - 1];
      },

      undoDelete: function() {
        var toUndo = toDelete[toDelete.length - 1];
        all[toUndo.id] = toUndo;
      },

      commitDelete: function() {
        Category.delete(toDelete.shift().id);
      },

      remove: function(category) {
        delete all[category.id];
      },

      insertAt: function(idx, category) {
        all.splice(idx, 0, category);
      },

      push: function(category) {
        all[category.id] = category;
      },

      get: function(id) {
        return all[id];
      },

      addProjectTo: function(category, project) {
        all[category.id].projects[project.id] = project;
        console.log('project added');
      },

      removeProjectFrom: function(category, project) {
        delete all[category.id].projects[project.id];
        console.log('project deleted');
      },

      getProjectById: function(category, pId) {
        return all[category.id].projects[pId];
      },

      first: function() {
        return all[ids[0]];
      }
    };
  }]);

  // dbService.service('Undo', function () {
  //
  // });

})(window.angular);
