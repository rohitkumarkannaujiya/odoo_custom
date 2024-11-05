from odoo import models, fields, api, _
from datetime import datetime
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class estateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property Model'
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=datetime.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False )
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(string='Garden Orientation',
                    selection=[('n', 'North'), ('w', 'West'), ('s', 'South'), ('e', 'East')])
    active = fields.Boolean('active' , default=True)
    state = fields.Selection(
        string='state',copy=False,
        selection=[
            ('new', 'New'), 
            ('received', 'Offer Received'), 
            ('accepted', 'Offer Accepted'),
            ('sold', 'sold'),
            ('cancelled', 'Cancelled')],
        default='new',)
    buyer_id = fields.Many2one('res.partner',string ='buyer', copy = False) 
    property_type_id = fields.Many2one('estate.property.type') 
    salesperson_id = fields.Many2one('res.users',string ='salesperson', default=lambda self:self.env.user)
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    tag_ids = fields.Many2many('estate.property.tag')
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_offer')
    image = fields.Binary()

    _sql_constraints = [
        ('check_positive_selling_price', 'CHECK(selling_price >= 0)', "The Selling Price must be Positive."),
        ('check_positive_expected_price', 'CHECK(expected_price > 0)', "The Expected price must be  strictly Positive."), 
    ]
    
    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for row in self:
            row.total_area = row.garden_area + row.living_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for row in self:
            if row.offer_ids:
                row.best_price = max(row.offer_ids.mapped('price'))
            else:
                row.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = 'n'
            self.garden_area = 10
        else:
            self.garden_orientation = ''
            self.garden_area = 0

    def sell_property(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(_('A Cancelled property cannot be Sold.'))
            else:
                record.state = 'sold'
        return True

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError(_('A Sold property cannot be cancelled.'))
            else:
                record.state = 'cancelled'
        return True

    @api.constrains('selling_price','expected_price')
    def _check_prices(self):
        for record in self:
            if record.selling_price < (0.9 * record.expected_price) and record.state == 'accepted':
                raise ValidationError("A selling Price Cannot be Less than 90% of expectation.")

    @api.ondelete(at_uninstall=False)
    def _unlink_estate_property(self):
        if self.filtered(lambda x:x.state not in ('new', 'cancelled')):
            raise ValidationError("Only new and cancelled property can be deleted !!! ")


    # method to show wizard.
    def show_wizard(self):
        
        return {'type': 'ir.actions.act_window',
               'name': _('Make offer'),
               'res_model': 'estate.wizard',
               'binding_view_types': 'list',
               'target': 'new',
               'view_mode': 'form',
               }

