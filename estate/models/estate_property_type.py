from odoo import models, fields, api, _


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'property type description'
    _order = "name,sequence"

    name = fields.Char(required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_counts = fields.Integer(compute='_compute_total_offers')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")

    _sql_constraints = [
        ('uniq_property_type_name', 'unique(name)', 'A Property Type name must be unique.'),
    ]

    @api.depends('offer_ids')
    def _compute_total_offers(self):
        for record in self:
            record.offer_counts = len(record.offer_ids)