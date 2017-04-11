(function(angular) {
  'use strict';
function EditableFieldController($scope, $element, $attrs) {
  var ctrl = this;
  ctrl.editMode = false;

  ctrl.handleModeChange = function() {
    if (ctrl.editMode) {
      ctrl.onUpdate({value: ctrl.fieldValue});
    }
    ctrl.editMode = !ctrl.editMode;
  };

  ctrl.$onInit = function() {
    if (!ctrl.fieldType) {
      ctrl.fieldType = 'text';
    }
  };
}

angular.module('dashboard').component('editableField', {
  templateUrl: '/static/js/templates/editable-field.html',
  controller: EditableFieldController,
  bindings: {
    fieldValue: '<',
    fieldType: '@?',
    onUpdate: '&'
  }
});
})(window.angular);
