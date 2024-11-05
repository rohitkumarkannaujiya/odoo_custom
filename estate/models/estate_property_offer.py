from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property offer description'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string='status', copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused'), ],
        )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property',string='Property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_validity', inverse='_inverse_date_validity')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_positive_offer_price', 'CHECK(price > 0 )', 'A Offer Price must be strictly positive.'),
    ]

    @api.model
    def create(self,vals):
        # get the property object using browse method
        property = self.env['estate.property'].browse(vals.get('property_id'))
        current_max_offer = max(property.offer_ids.mapped('price')) if property.offer_ids else 0
        # if offer price is less than current offer, raise error.
        current_offer = vals.get('price')
        if float_compare(current_offer, current_max_offer, precision_digits=1) <= 0:
            raise UserError(
                f'Offer Price should be greater than {current_max_offer}. ')
        # set property state to 'received' i.e. offer received
        property.state = 'received'
        res = super().create(vals)
        return res

    @api.depends('validity')
    def _compute_date_validity(self):
        for record in self:
            my_date = record.create_date if record.create_date else datetime.today()
            record.date_deadline = my_date + timedelta(record.validity)

    def _inverse_date_validity(self):
        for record in self:
            my_date = record.create_date.date() if record.create_date else datetime.today()
            record.validity = (record.date_deadline - my_date).days

    def accept_offer(self):
        for record in self:
            if record.property_id.state in ('sold','cancelled'):
                raise UserError("A Sold or Cancelled property cannot accept Offer.")
            # refuse every offer
            for offer in record.property_id.offer_ids:
                offer.status = 'refused'
            # accept the current one
            record.status = 'accepted'
            record.property_id.state = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def reject_offer(self):
        for record in self:
            if record.property_id.state in ('sold','cancelled'):
                raise UserError("A Sold or Cancelled property cannot reject Offer.")
            record.status = 'refused'
            record.property_id.state = 'received'
            record.property_id.selling_price = 0
            record.property_id.buyer_id = None
        return True