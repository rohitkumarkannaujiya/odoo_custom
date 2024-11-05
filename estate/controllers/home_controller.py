from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import pager as portal_pager

class TeacherData(http.Controller):

    @http.route('/home/', type='http', auth='public', website=True)
    def home(self, **kwargs):
        return request.render('estate.playground')


    @http.route('/home/<model("academy.teachers"):teacher>/', type='http', auth='public', website=True)
    def teacher_data(self, teacher):
        return request.render('estate.teacher_template', {"teacher_data" :teacher})

    @http.route(['/property/','/property/page/<int:page>'], type='http', auth='public', website=True)
    def property_data(self,page=1, **kwargs):
        page_limit = 6
        EstateProperty = request.env["estate.property"]
        domain = [('state','not in',('sold','cancelled'))]
        properties = EstateProperty.search(
                                domain = domain , 
                                offset=(page - 1) * page_limit, 
                                limit=page_limit)
        pager = portal_pager(
            url='/property/',
            total=EstateProperty.search_count(domain),
            page=page,
            step=page_limit,
        )
        return request.render('estate.property_template', {
                        "property_data" :properties,
                        'pager' : pager})

        
    @http.route('/property/<model("estate.property"):property_data>/', type='http', auth='public', website=True)
    def property_profile(self,property_data, **kwargs):
        return request.render('estate.property_profile_template', {
                        "property_profile" :property_data})        
