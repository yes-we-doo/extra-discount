from odoo import models, fields, api
from odoo.exceptions import ValidationError

    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    discount = fields.Float(string="Discount (%)", digits='Discount', default=0.0, compute="_compute_discount", store=True, readonly=False, precompute=True)
    discount2 = fields.Float(string="Discount 2 (%)", digits='Discount', default=0.0, compute="_compute_discount", store=True, readonly=False, precompute=True)
    discount3 = fields.Float(string="Discount 3 (%)", digits='Discount', default=0.0, compute="_compute_discount", store=True, readonly=False, precompute=True)
    
    @api.depends('product_id', 'move_id.partner_id')
    def _compute_discount(self):
        # filter the account.move.line because its not all invoice line but could be journal item,
        # so we exclude the journal item
        invoice_line_ids = self.filtered(lambda l:l.display_type == 'product')
        for line in invoice_line_ids:
            customer_id = line.move_id.partner_id
            line.discount = customer_id.default_discount if not line.discount else line.discount
            line.discount2 = customer_id.default_second_discount if not line.discount2 else line.discount2
            line.discount3 = customer_id.default_third_discount if not line.discount3 else line.discount3

    @api.depends('quantity', 'discount', 'price_unit', 'discount2', 'discount3', 'tax_ids', 'currency_id')
    def _compute_totals(self):
        # just to add re-computation treigger based on discount changes
        super(AccountMoveLine, self)._compute_totals()


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