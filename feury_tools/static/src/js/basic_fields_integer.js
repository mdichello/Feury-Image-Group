odoo.define('feury_tools.WidgetInteger', function (require) {
    "use strict";
    
    var basic_fields = require('web.basic_fields');

    basic_fields.FieldInteger.include({
        _render: function () {
            this.$el.on('keypress', function (event) {
                var keyCode = event.which;
                if ( (keyCode != 8 || keyCode ==32 ) && (keyCode < 48 || keyCode > 57)) {
                    return false;
                }
            });
            return this._super();
        },
    });

    basic_fields.FieldFloat.include({
        _render: function () {
            this.$el.on('keypress', function (event) {
                var keyCode = event.which;
                if ( (keyCode != 44 && keyCode != 46 ) && (keyCode != 8 || keyCode ==32 ) && (keyCode < 48 || keyCode > 57)) {
                    return false;
                }
            });
            return this._super();
        },
    });

    basic_fields.FieldMonetary.include({
        _render: function () {
            this.$el.on('keypress', function (event) {
                var keyCode = event.which;
                if ( (keyCode != 44 && keyCode != 46 ) && (keyCode != 8 || keyCode ==32 ) && (keyCode < 48 || keyCode > 57)) {
                    return false;
                }
            });
            return this._super();
        },
    });
});
