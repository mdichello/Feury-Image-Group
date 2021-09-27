# -*- coding: utf-8 -*-

from odoo import tools
from odoo import api, fields, models


class ProductStyleVendorCode(models.Model):
    _name = 'product.style.vendor.code'
    _description = 'Product vendor code style'
    _auto = False

    name = fields.Char(
        string='Name'
    )

    code = fields.Char(
        string='Style Code',
    )

    vendor_code = fields.Char(
        string='Vendor Code',
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
            SELECT id, name, code, vendor_code, active
            FROM product_style
        """
        self.env.cr.execute("""
            CREATE or REPLACE VIEW %s AS (%s)
        """ % (self._table, query))
