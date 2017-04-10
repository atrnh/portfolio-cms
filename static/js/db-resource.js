(function(angular) {
  'use strict';
angular.module('dbResource', ['ngResource'])

  .config(function ($interpolateProvider) {
    $interpolateProvider
      .startSymbol('{[{')
      .endSymbol('}]}');
  })

  // Project service for getting project data from server
  .factory('Project', function ($resource) {
    return {

      // Return array of projects associated with given category id
      getAllInCategory: function(id) {
        return $resource('/projects.json', {categoryId: id}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      // Return array of all projects in database
      getAll: function() {
        return $resource('/projects.json', {}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      // Return JSON object of a single project
      getById: function(id) {
        return $resource('/project.json', {projectId: id}, {
          'get': {
            method: 'GET'
          }
        }).get();
      },

      addNew: function(title, desc, categoryId, tags) {
        return $resource('/admin/project', {}, {
          'post': {
            method: 'POST'
          }
        }).post({}, {
          'title': title,
          'desc': desc,
          'categoryId': categoryId,
          'tags': tags
        });
      },

      delete: function(id) {
        return $resource('/admin/project/:projectId', {projectId: id}, {
          'delete': {
            method: 'DELETE',
            isArray: true
          }
        }).delete();
      },

      update: function(id, title, desc, categoryId, tags) {
        return $resource('/admin/project/:projectId', {projectId: id}, {
          'post': {
            method: 'POST'
          }
        }).post({}, {
          'title': title,
          'desc': desc,
          'categoryId': categoryId,
          'tags': tags
        });
      },

      deleteTag: function(id, tagCode) {
        return $resource(
          '/admin/project/:projectId/tag/:tagCode',
          {projectId: id, tagCode: tagCode}, {
            'delete': {
              method: 'DELETE'
            }
          }
        ).delete();
      }

    };
  })

  .factory('Category', function ($resource) {
    return {

      // Return JSON object of single category
      getById: function(id) {
        return $resource('/category.json', {categoryId: id}, {
          'get': {
            method: 'GET'
          }
        }).get();
      },

      // Return JSON array of all categories.
      // Set loadAll to true to greedily load all nested objects.
      // Value of loadAll is sent to server as JSON.
      getAll: function(loadAll) {
        return $resource('/categories.json', {loadAll: loadAll}, {
          'get': {
            method: 'GET',
            isArray: true,
          }
        }).get();
      },

      addNew: function(title, desc) {
        return $resource('/admin/category', {}, {
          'post': {
            method: 'POST'
          }
        }).post({}, {'title': title, 'desc': desc});
      },

      delete: function(id) {
        return $resource('/admin/category/:categoryId', {categoryId: id}, {
          'delete': {
            method: 'DELETE',
            isArray: true
          }
        }).delete();
      },

      update: function(id, title, desc) {
        return $resource('/admin/category/:categoryId', {categoryId: id}, {
          'post': {
            method: 'POST',
            isArray: true
          }
        }).post({}, {'title': title, 'desc': desc});
      }
    };
  })
;
})(window.angular);
