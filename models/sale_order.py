from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount2 = fields.Float(string="Discount 2 (%)", digits='Discount', default=0.0, compute="_compute_discount", store=True, readonly=False, precompute=True)
    discount3 = fields.Float(string="Discount 3 (%)", digits='Discount', default=0.0, compute="_compute_discount", store=True, readonly=False, precompute=True)

    # so the discount from SO carried over to invoice
    def _prepare_invoice_line(self, **optional_values):
        invoice_line = super()._prepare_invoice_line(**optional_values)
        invoice_line.update({
            'discount2': self.discount2,
            'discount3': self.discount3,
        })
        return invoice_line
    
    # this logic will not take into account the tax, we inherit another function on account.tax = _prepare_base_line_for_taxes_computation instead
    # so we just playinh with the discount amount and let odoo base logic handle the rest
    # that one function is used on sale order and invoice
    # we inherit this to only add re-computation trigger based on discount fields
    @api.depends('product_uom_qty', 'price_unit', 'discount', 'discount2', 'discount3', 'tax_id')
    def _compute_amount(self):
        super(SaleOrderLine, self)._compute_amount()
        
    
    @api.depends('product_id', 'product_uom', 'product_uom_qty', 'order_id.partner_id')
    def _compute_discount(self):
        super()._compute_discount()
        for line in self:
            customer_id = line.order_id.partner_id
            line.discount = customer_id.default_discount or 0
            line.discount2 = customer_id.default_second_discount or 0
            line.discount3 = customer_id.default_third_discount or 0

        

    @api.constrains('discount', 'discount2', 'discount3')
    def _check_discount_values(self):
        for line in self:
            if not (0 <= line.discount <= 100):
                raise ValidationError("The discount must be between 0 and 100.")
            if not (0 <= line.discount2 <= 100):
                raise ValidationError("The discount 2 must be between 0 and 100.")
            if not (0 <= line.discount3 <= 100):
                raise ValidationError("The discount 3 must be between 0 and 100.")

           # Checking the total amount of discounts
            total_discount = line.discount + line.discount2 + line.discount3
            if total_discount > 100:
                raise ValidationError("The total discount cannot exceed 100%.")

