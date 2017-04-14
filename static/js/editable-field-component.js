(function(angular) {
  'use strict';
function EditableFieldController($scope, $element, $attrs) {
  var ctrl = this;
  ctrl.editMode = false;

  ctrl.handleModeChange = function(evt) {
    if (evt.type === 'click' || evt.key === 'Enter') {

      if (ctrl.editMode) {
          ctrl.onUpdate({value: ctrl.fieldValue});
      }

      ctrl.editMode = !ctrl.editMode;
    }
  };

  ctrl.$onInit = function() {
    if (!ctrl.fieldType) {
      ctrl.fieldType = 'text';
    }
  };
}

function EditMediaController($scope, $element, $attrs) {
  var ctrl = this;

  ctrl.update = function(prop, value) {
    ctrl.onUpdate({media: ctrl.media, prop: prop, value: value});
  };

  ctrl.delete = function() {
    ctrl.onDelete({media: ctrl.media});
  };
}

angular.module('dashboard')
  .component('editableField', {
    templateUrl: '/static/js/templates/editable-field.html',
    controller: EditableFieldController,
    bindings: {
      fieldValue: '<',
      fieldType: '@?',
      enableHtml: '<?',
      onUpdate: '&'
    }
  })

  .component('editMedia', {
    templateUrl: '/static/js/templates/edit-media.html',
    controller: EditMediaController,
    bindings: {
      media: '<',
      onUpdate: '&',
      onDelete: '&'
    }
  })
;
})(window.angular);
