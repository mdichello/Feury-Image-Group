from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_composite_line_data(self, composite_line_id, company_id):
        lines_values = []
        product_tmpl_id = composite_line_id.product_id.product_tmpl_id

        for line_id in product_tmpl_id.composite_line_ids:
            # TODO call default_get
            values = {
                'product_id': line_id.product_id.id,
                'product_uom_qty': composite_line_id.product_uom_qty * line_id.quantity,
                'order_id': composite_line_id.order_id.id,
                'sequence': composite_line_id.sequence + 1,
            }
            lines_values.append(values)

        return lines_values

    def _auto_deploy_composite_products(self):
        SALE_ORDER_LINE = self.env['sale.order.line']

        self.ensure_one()

        # 1- Looking for composition lines in current offer
        composite_quotation_line = self.order_line.filtered(
            lambda l: (
                l.product_id and
                l.product_id.product_tmpl_id and
                l.product_id.product_tmpl_id.is_composite_product and
                l.product_id.deployment == 'auto'
            )
        )

        if not self.order_line or not composite_quotation_line:
            # No composition line, no need to go further
            return
    
        # 2- That way, we won't need to implement the same methods again and again on models inheriting this one
        new_lines = []
        old_lines = SALE_ORDER_LINE
        company_id = self.company_id

        # 3- Building data for each composition line retrieved
        for composite_line_id in composite_quotation_line:
            lines_values = self._get_composite_line_data(
                composite_line_id=composite_line_id,
                company_id=company_id
            )
            if lines_values:
                new_lines.extend(lines_values)
            old_lines += composite_line_id

        # 4- Creating new lines
        SALE_ORDER_LINE.create(new_lines)

        # 5- Archiving composed lines.
        if old_lines:
            old_lines.update({'active': False})
    
    def write(self, values):
        res = super(SaleOrder, self).write(values)

        for order in self:
            order._auto_deploy_composite_products()
        
        return res
