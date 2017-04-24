/* jshint esversion: 6 */
(function(angular) {
  'use strict';

angular.module('dbResource', ['ngResource'])

  .config(function ($interpolateProvider, $locationProvider) {
    $interpolateProvider
      .startSymbol('~*~*')
      .endSymbol('*~*~');

    $locationProvider.hashPrefix('');
  })

  .factory('Project', function ($resource) {
    return {

      // Return array of projects associated with given category id
      getAllInCategory: function(id) {
        return $resource('/projects.json', {categoryId: id}, {
          'get': {
            method: 'GET'
          }
        }).get();
      },

      // Return array of all projects in database
      getAll: function() {
        return $resource('/projects.json', {}, {
          'get': {
            method: 'GET'
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

      // Add a new project
      addNew: function(obj) {
        return $resource('/admin/project', {}, {
          'post': {
            method: 'POST'
          }
        }).post({}, obj);
      },

      // Delete a project
      delete: function(id) {
        return $resource('/admin/project/:projectId', {projectId: id}, {
          'delete': {
            method: 'DELETE'
          }
        }).delete();
      },

      // Update a project
      update: function(id, obj) {
        return $resource('/admin/project/:projectId', {projectId: id}, {
          'post': {
            method: 'POST'
          }
        }).post({}, obj);
      },

      // Add a new tag to a project
      newTag: function(id, tag) {
        return $resource('/admin/project/:projectId/new_tag', {projectId: id}, {
          'post': {
            method: 'POST'
          }
        }).post({}, tag);
      },

      // Delete a tag from a project
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
          }
        }).get();
      },

      getAllList: function(loadAll) {
        return $resource('/categories_list.json', {loadAll: loadAll}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      // Add a new category
      addNew: function(title, desc) {
        return $resource('/admin/category', {}, {
          'post': {
            method: 'POST'
          }
        }).post({}, {'title': title, 'desc': desc});
      },

      // Delete a category
      delete: function(id) {
        return $resource('/admin/category/:categoryId', {categoryId: id}, {
          'delete': {
            method: 'DELETE',
          }
        }).delete();
      },

      // Update a category
      update: function(id, obj) {
        return $resource('/admin/category/:categoryId', {categoryId: id}, {
          'post': {
            method: 'POST'
          }
        }).post({}, obj);
      }
    };
  })

  .factory('Media', function ($resource) {
    return {

      // Update media
      update: function(pId, mId, obj) {
        return $resource('/admin/project/:projectId/media/:mediaId', {projectId: pId, mediaId: mId}, {
          'post': {
            method: 'POST'
          }
        }).post({}, obj);
      },

      // Delete media
      delete: function(pId, mId) {
        return $resource('/admin/project/:projectId/media/:mediaId', {projectId: pId, mediaId: mId}, {
          'delete': {
            method: 'DELETE'
          }
        }).delete();
      },

      // Get media JSON by ID
      getById: function(id) {
        return $resource('/media.json', {mediaId: id}, {
          'get': {
            method: 'GET'
          }
        }).get();
      },

      getAll: function() {
        return $resource('/all_media.json', {}, {
          'get': {
            method: 'GET'
          }
        }).get();
      }
    };
  })

  .factory('Tag', function ($resource) {
    return {

      // Get all tags in JSON array
      getAll: function() {
        return $resource('/tags.json', {}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      // Get individual tag JSON
      getByCode: function(code) {
        return $resource('tag.json', {tagCode: code}, {
          'get': {
            method: 'GET'
          }
        }).get();
      },
    };
  })

  .factory('Page', ['$resource', function ($resource) {
    return {
      getAll: function() {
        return $resource('/pages.json', {}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      // Get page JSON by ID
      getById: function(id) {
        return $resource('/page.json', {pageId: id}, {
          'get': {
            method: 'GET'
          }
        }).get();
      },

      addNew: function(title, content) {
        return $resource('/admin/page', {}, {
          'post': {
            method: 'POST'
          }
        }).post({}, {'title': title, 'content': content});
      },

      delete: function(id) {
        return $resource('/admin/page/:pageId', {pageId: id}, {
          'delete': {
            method: 'DELETE'
          }
        }).delete();
      },

      update: function(id, obj) {
        return $resource('/admin/page/:pageId', {pageId: id}, {
          'post': {
            method: 'POST'
          }
        }).post({}, obj);
      },
    };
  }])

  .factory('Link', ['$resource', function ($resource) {
    return {
      getAll: function() {
        return $resource('/links.json', {}, {
          'get': {
            method: 'GET',
            isArray: true
          }
        }).get();
      },

      // Get link JSON by ID
      getById: function(id) {
        return $resource('/link.json', {linkId: id}, {
          'get': {
            method: 'GET'
          }
        }).get();
      },

      addNew: function(title, url) {
        return $resource('/admin/link', {}, {
          'post': {
            method: 'POST'
          }
        }).post({}, {'title': title, 'url': url});
      },

      delete: function(id) {
        return $resource('/admin/link/:linkId', {pageId: id}, {
          'delete': {
            method: 'DELETE'
          }
        }).delete();
      },

      update: function(id, obj) {
        return $resource('/admin/link/:linkId', {pageId: id}, {
          'post': {
            method: 'POST'
          }
        }).post({}, obj);
      },
    };
  }])
;
})(window.angular);
