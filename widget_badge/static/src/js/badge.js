odoo.define("widget_badge.badge_fields", function (require) {
    "use strict";
    // Var AbstractField = require("web.AbstractField");
    var basic_fields = require("web.basic_fields");
    var FieldChar = basic_fields.FieldChar;
    var core = require("web.core");
    var fieldRegistry = require("web.field_registry");

    var _lt = core._lt;

    var FieldBadge = FieldChar.extend({
        template: "web.FieldBadge",
        supportedFieldTypes: ["selection", "many2one", "char"],

        //   _setDecorationClasses
        _applyDecorations() {
            var self = this;
            this.attrs.decorations.forEach(function (dec) {
                var isToggled = py.PY_isTrue(py.evaluate(dec.expression, self.record.evalContext));
                var className = `badge-${dec.className.split("-")[1]}`;
                self.$el.toggleClass(className, isToggled);
            });
        },
    });

    fieldRegistry.add("badge", FieldBadge);

    return FieldBadge;
});
