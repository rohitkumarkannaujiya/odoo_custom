from odoo import models, fields, api, _


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property tag description'
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer('Color Index', default=0)

    _sql_constraints = [
        ('uniq_property_tag_name', 'unique(name)', 'A Property Tag name must be unique.'),
    ]