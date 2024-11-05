from odoo import api, fields, models
from datetime import datetime, timedelta

class EstateWizard(models.TransientModel):
    _name = 'estate.wizard'

    price = fields.Float()
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_validity', inverse='_inverse_date_vality')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)

    @api.depends('validity')
    def _compute_date_validity(self):
        for record in self:
            my_date = record.create_date if record.create_date else datetime.today()
            record.date_deadline = my_date + timedelta(record.validity)

    def _inverse_date_vality(self):
        for record in self:
            my_date = record.create_date.date() if record.create_date else fields.date_availability.today()
            record.validity = (record.date_deadline - my_date).days

    def action_create_offer(self):
        data = [{
            'price':self.price,
            'validity':self.validity,
            'date_deadline':self.date_deadline,
            'partner_id': self.partner_id.id,   
            'property_id':id,
        } for id in self._context.get('active_ids', False)]
        self.env['estate.property.offer'].create(data)