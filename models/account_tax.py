from odoo import models, fields, api

class AccountTax(models.Model):
    _inherit = "account.tax"
    def _prepare_base_line_for_taxes_computation(self, record, **kwargs):
        # main logic to only play with discount
        results = super()._prepare_base_line_for_taxes_computation(record, **kwargs)
        if record and record._name in ['account.move.line', 'sale.order.line']:
            results['discount'] = record.discount + record.discount2 + record.discount3
        return results