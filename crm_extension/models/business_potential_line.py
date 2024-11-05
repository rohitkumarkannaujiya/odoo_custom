from odoo import models,fields,api,_
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    order_lines = fields.One2many('business.potential.line','partner_id',string='order lines')
    code = fields.Char(string="Code")
    code_check = fields.Boolean(string="Code Generation")


    _sql_constraints = [('code_uniq', 'unique(code)', "A code must be unique !")]

    @api.onchange('code')
    def code_check_bool(self):
        for rec in self:
            if rec.code:
                if len(rec.code) != 8:
                    raise UserError(_('Code length must be equal of 8 characters'))
            rec.code_check = False   
            if rec.code:
                rec.code_check = True
            

class BusinessLine(models.Model):     
    _name = 'business.potential.line' 

    product_id = fields.Many2one('product.product',string="Product")
    description = fields.Text(
        string="Description")

    qty = fields.Float(string="Qty", default=1.0,required=True)
    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string="UoM")
    
    price_unit = fields.Float(
        string="Unit Price")
    
    partner_id = fields.Many2one('res.partner')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.write({
            'description': self.product_id.name,
            'product_uom': self.product_id.uom_id.id,
            'price_unit' :  self.product_id.standard_price
        })