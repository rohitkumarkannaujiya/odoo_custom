from odoo import models,fields,api,_


class Product(models.Model):     
    _name = 'term.product' 

    product_term = fields.Text(string="Products Term & Condition:")


class Services(models.Model):     
    _name = 'term.services' 

    services_term = fields.Text(string="Services Term & Condition:")

class Export(models.Model):     
    _name = 'term.export' 

    export_term = fields.Text(string="Export Term & Condition:")


