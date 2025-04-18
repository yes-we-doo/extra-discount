from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    default_discount = fields.Float(string="Remise 1 (%)", digits=(3, 3), default=0)
    default_second_discount = fields.Float(string="Remise 2 (%)", digits=(3, 3), default=0)
    default_third_discount = fields.Float(string="Remise 3 (%)", digits=(3, 3), default=0)
