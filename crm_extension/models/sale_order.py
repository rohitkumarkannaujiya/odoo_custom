from odoo import models,fields,api,_
from odoo.exceptions import UserError
from odoo.tools import  float_compare
from markupsafe import Markup
from datetime import timedelta, date, datetime


class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    attachment_ids2 = fields.Many2many(
        'ir.attachment', 'mail_compose_message_ir_attachments_rel',
        'wizard_id', 'attachment_id', string='Attachments',readonly=False, store=True)



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tracking_status = fields.Selection([
        ("order_confirmed", "Order Confirmed"),
        ("awaiting_advance_payment", "Awaiting Advance Payment"),
        ("advance_received", "Advance Received"),
        ("production_started", "Production Started"),
        ("ready_for_dispatch", "Raccess_term_exporteady for Dispatch"),
        ("awaiting_delivery_payment", "Awaiting Delivery Payment"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"), 
        ], string="Order Tracking Status")
    
    sales_type  = fields.Selection([
        ("products", "products"),
        ("services", "services"),
        ("export", "export"),
        ], string="Sales Type")
    
    SALE_ORDER_STATE = [
        ('draft', "Quotation"),
        ('approval', "Awaiting Approval"),
        ('approved', "Quotation Approved"),
        ('sent', "Quotation Sent"),
        ('sale', "Sales Order"),
        ('cancel', "Cancelled"),
        ]
    
    deviation = fields.Text(string="Deviation")
    state = fields.Selection(selection_add=SALE_ORDER_STATE)
    is_subs = fields.Boolean() 

    def action_confirm_quotation(self):
        pass


    @api.onchange('company_id')
    def _onchange_company_id_warning(self):
        pass


    # def crete_opportunity(self):
    #     validity = date.today() + timedelta(days=30)
    #     order = self.env['sale.order'].search([('state',in,['sale']),('validity_date', '=', validity)])
    #     for rec in order:
    #         vals = {
    #         'name' : ,
    #         'partner_id' : rec.partner_id.id,
    #         'type' : 'opportunity',
    #         'user_id' : rec.user_id.id,
    #         'team_id' : rec.team_id.id,
    #         'name' : ,
    #         'name' : ,
    #         }

    @api.onchange('sales_type')
    def _onchange_condition(self):
        product = self.env['term.product'].search([])
        services = self.env['term.services'].search([])
        export = self.env['term.export'].search([])

        for rec in self:
            for data in product:
                if rec.sales_type == 'products':
                    rec.note = data.product_term
                
                for data in services:
                    if rec.sales_type == 'services':
                        rec.note = data.services_term

                for data in export:
                    if rec.sales_type == 'export':
                        rec.note = data.export_term

            
   
    def action_approval(self):
        self.state = 'approved'

    def action_reset_to_draft(self):
        self.state = 'draft'

    def action_quatation_approval(self):
        data_price=self.env['product.pricelist'].search([])
        f=0
        for data in  data_price.item_ids:
            for rec in self.order_line:
                if rec.product_template_id.id == data.product_tmpl_id.id:
                    price_unit =  rec.price_subtotal/rec.product_uom_qty
                    if data.selling_price > price_unit:
                        f=1
                        break
                else:
                    continue
            
        if f==1:
            self.state = 'approval'
        else:
            self.state='approved'



    def action_quotation_send(self):
        """ Opens a wizard to compose an email, with relevant mail template loaded by default """
        self.ensure_one()
        self.order_line._validate_analytic_distribution()
        lang = self.env.context.get('lang')
        mail_template = self._find_mail_template()

        if mail_template and mail_template.lang:
            lang = mail_template._render_lang(self.ids)[self.id]
        attachments = self.env['ir.attachment'].search([('res_model', '=', 'product.category'), ('res_id', 'in', self.order_line.product_id.categ_id.mapped('id'))])

        ctx = {
            'default_model': 'sale.order',
            'default_res_ids': self.ids,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
            'default_attachment_ids2' : [(6, 0, attachments.ids)]
            }
        if self.state == 'approved':
            self.state = 'sent'
    
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
    
            
    def action_confirm(self):
        self.order_line._validate_analytic_distribution()

        for order in self:
            order.validate_taxes_on_sales_order()
            if order.partner_id in order.message_partner_ids:
                continue
            order.message_subscribe([order.partner_id.id])

        self.write(self._prepare_confirmation_values())

        # Context key 'default_name' is sometimes propagated up to here.
        # We don't need it and it creates issues in the creation of linked records.
        context = self._context.copy()
        context.pop('default_name', None)

        self.with_context(context)._action_confirm()

        self.filtered(lambda so: so._should_be_locked()).action_lock()

        if self.env.context.get('send_email'):
            self._send_order_confirmation_mail()
        
        template = self.env.ref('crm_extension.email_template_sale_order')
        template.send_mail(self.id, force_send=True)   
      

        return True  

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.opportunity_id:
            for rec in res.opportunity_id.requirnment_ids:
                line = {
                        'order_id' : res.id,
                        'product_id': rec.product_id.id,
                        'name':rec.product_id.name,
                        'price_unit':rec.product_id.lst_price,
                        'product_uom_qty': rec.qty,
                    }
                x = self.env['sale.order.line'].create(line)   
        return res
        
class SaleOrderLine(models.Model):
    _inherit= 'sale.order.line'


    def write(self, values): 
        if 'display_type' in values and self.filtered(lambda line: line.display_type != values.get('display_type')):
            raise UserError(_("You cannot change the type of a sale order line. Instead you should delete the current line and create a new line of the proper type."))

        if 'product_uom_qty' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            self.filtered(
                lambda r: r.state == 'sale' and float_compare(
                    r.product_uom_qty,
                    values['product_uom_qty'],
                    precision_digits=precision
                ) != 0
            )._update_line_quantity(values)

        if 'price_unit' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            self.filtered(
                lambda r: r.state == 'sale' and float_compare(
                    r.price_unit,
                    values['price_unit'],
                    precision_digits=precision
                ) != 0
            )._update_line_price_unit(values)

        if 'discount' in values:
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            self.filtered(
                lambda r: r.state == 'sale' and r.discount !=  values['discount'] )._update_line_discount(values)
            
        # Prevent writing on a locked SO.
        protected_fields = self._get_protected_fields()
        if any(self.order_id.mapped('locked')) and any(f in values.keys() for f in protected_fields):
            protected_fields_modified = list(set(protected_fields) & set(values.keys()))

            if 'name' in protected_fields_modified and all(self.mapped('is_downpayment')):
                protected_fields_modified.remove('name')

            fields = self.env['ir.model.fields'].sudo().search([
                ('name', 'in', protected_fields_modified), ('model', '=', self._name)
            ])
            if fields:
                raise UserError(
                    _('It is forbidden to modify the following fields in a locked order:\n%s',
                      '\n'.join(fields.mapped('field_description')))
                )

        result = super().write(values)

        # Don't recompute the package_id if we are setting the quantity of the items and the quantity of packages
        if 'product_uom_qty' in values and 'product_packaging_qty' in values and 'product_packaging_id' not in values:
            self.env.remove_to_compute(self._fields['product_packaging_id'], self)

        return result
    
    
    def _update_line_price_unit(self, values):
        orders = self.mapped('order_id')
        for order in orders:
            order_lines = self.filtered(lambda x: x.order_id == order)
            msg = Markup("<b>%s</b><ul>") % _("The ordered Unit Price has been updated.")

            for line in order_lines:
                if 'product_id' in values and values['product_id'] != line.product_id.id:
                    # tracking is meaningless if the product is changed as well.
                    continue
                msg += Markup("<li> %s: <br/>") % line.product_id.display_name
                msg  += _(
                    "Ordered Unit Price: %(old_price)s -> %(new_price)s",
                    old_price=line.price_unit,
                    new_price=values["price_unit"]
                ) + Markup("<br/>")

            msg += Markup("</ul>")
            order.message_post(body=msg)
    
    def _update_line_discount(self, values):
        orders = self.mapped('order_id')
        for order in orders:
            order_lines = self.filtered(lambda x: x.order_id == order)
            msg = Markup("<b>%s</b><ul>") % _("The ordered Disc. has been updated.")

            for line in order_lines:
                if 'product_id' in values and values['product_id'] != line.product_id.id:
                    # tracking is meaningless if the product is changed as well.
                    continue
                msg += Markup("<li> %s: <br/>") % line.product_id.display_name
                msg  += _(
                    "Ordered Discount: %(old_disc)s -> %(new_disc)s",
                    old_disc=line.discount,
                    new_disc=values["discount"]
                ) + Markup("<br/>")

            msg += Markup("</ul>")
            order.message_post(body=msg)
    

class ProductPricelist(models.Model):
    _inherit="product.pricelist.item"

    selling_price = fields.Float(string="Minimum Selling Price")


class ProductCategory(models.Model):
    _name = 'product.category'
    _inherit = ['product.category', 'mail.thread', 'mail.activity.mixin']


