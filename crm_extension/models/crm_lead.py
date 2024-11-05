from odoo import models,fields,api,_
from odoo.exceptions import UserError


class Lead(models.Model):     
    _inherit = 'crm.lead' 

    
    requirnment_ids = fields.One2many('lead.requirnment','crm_lead_id',string="Requirnment")
    is_mandatory = fields.Boolean(string="is Mandatory?", compute="_compute_state", store=True)
    check_stage = fields.Boolean(string="check_stage?", compute="_compute_check_stage", store=True)


    def _cron_create_record(self):
        print("hii")


    @api.depends('stage_id')
    def _compute_state(self):
        for rec in self:
            rec.is_mandatory= False
            if rec.stage_id.name == 'Qualification':
                rec.is_mandatory = True
                

    @api.depends('stage_id')
    def _compute_check_stage(self):
        stage = self.env.ref('crm.stage_lead4')
        for data in self:
            data.check_stage = False
            if data.stage_id.id == stage.id:
                data.check_stage = True


    @api.depends(lambda self: ['stage_id', 'team_id'] + self._pls_get_safe_fields())
    def _compute_probabilities(self):
        for lead in self:
            lead.probability = lead.stage_id.probability

    
    @api.onchange('stage_id') 
    def check_requirnment(self):
        stage = self.env.ref('crm.stage_lead1')
        if not self.requirnment_ids and self.stage_id.id != stage.id:
            raise UserError(_("Requirements is Mandatory"))
        
    @api.onchange('expected_revenue', 'stage_id')
    def check_expected_revenue(self):
        if self.expected_revenue == 0.0 and self.stage_id.name != 'Qualification':
            raise UserError(_("Expected Revenue is Mandatory"))



    def write(self, values):
        type = self.type
        result = super(Lead, self).write(values)
        for rec in self:
            stage = self.env.ref('crm.stage_lead1')
            if self.stage_id.id != stage.id:
                if not rec.country_id:
                    raise UserError(_('Country is required.'))
                if not rec.state_id:
                    raise UserError(_('State is required.'))
                if not rec.date_deadline:
                    raise UserError(_('Expected Closing is required.'))
                if not rec.city:
                    raise UserError(_('City is required.'))
                if not rec.partner_name:
                    raise UserError(_('Company Name is required.'))
            
                if not rec.contact_name:
                    raise UserError(_('Contact Name is required.'))
                if not rec.medium_id:
                    raise UserError(_('Medium is required.'))
                if not rec.source_id:
                    raise UserError(_('Source is required.'))
                if not rec.mobile:
                    raise UserError(_('Mobile is required.'))
                if not rec.email_from:
                    raise UserError(_('Email is required.'))
                

    # def action_new_quotation_custom(self):
    #     action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
    #     action['context'] = self._prepare_opportunity_quotation_context_custom()
    #     action['context']['search_default_opportunity_id'] = self.id
    #     print('\n\n================ss', )
    #     return action

    def action_new_quotation_custom(self):
        """ Prepares the context for a new quotation (sale.order) by sharing the values of common fields """
        
        self.ensure_one()
        quotation_context = {
            'opportunity_id': self.id,
            'partner_id': self.partner_id.id,
            'campaign_id': self.campaign_id.id,
            'medium_id': self.medium_id.id,
            'origin': self.name,
            'source_id': self.source_id.id,
            'company_id': self.company_id.id or self.env.company.id,
            'tag_ids': [(6, 0, self.tag_ids.ids)],
            'team_id': self.team_id.id,
            'user_id': self.user_id.id,

        }
        x = self.env['sale.order'].sudo().create(quotation_context)
        return {
            'name': ('Sale Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': x.id,
            'view_type': 'form',
            'view_mode': 'form',                
            'context': self.env.context,
            # 'target': 'new',
        }
      



class LeadRequirment(models.Model):
    _name = 'lead.requirnment'

    fluid = fields.Char(string="Fluid")
    pipe_size = fields.Char(string="Pipe Size")
    flow_range = fields.Char(string=" Flow Range")
    application = fields.Char(string="Application")
    temperature = fields.Char(string="Temperature")
    accuracy = fields.Char(string="Accuracy")
    pressure = fields.Char(string="Pressure")
    qty = fields.Float(string="Qty")
    product_id = fields.Many2one('product.product', string="Recommended Product")
    crm_lead_id = fields.Many2one('crm.lead')

class CrmStage(models.Model):
    _inherit = 'crm.stage'

    probability = fields.Float(string="Probability", store=True)
    crm_lead_id = fields.Many2one("crm.lead",string="lead")



   
