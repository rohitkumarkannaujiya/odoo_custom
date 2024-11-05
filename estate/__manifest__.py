{
    'name': 'Real Estate',
    'version': '1',
    'category': 'Real Estate/Advertising',
    'summary': 'A Real Estate Advertising Module.',
    'description': "",
    'depends' : ['website' , 'base', 'web'],
    'data':[
        'security/ir.model.access.csv',
        'reports/estate_property_templates.xml',
        'reports/estate_property_reports.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menu.xml',
        'views/res_users.xml',
        'views/estate_web_template.xml',
        'views/owl_template.xml',
        'wizards/estate_wizard.xml',
    ],
    'demo':[
        'data/academy_demo.xml',
        'data/estate_property_data.xml',
        'data/estate_property_offer_data.xml',
    ],
    'assets':{
            'estate.assets_backend': [
                 # bootstrap
            ('include', 'web._assets_helpers'),
            'web/static/src/scss/pre_variables.scss',
            'web/static/lib/bootstrap/scss/_variables.scss',
            ('include', 'web._assets_bootstrap'),

            'web/static/src/libs/fontawesome/css/font-awesome.css', # required for fa icons
            'web/static/src/legacy/js/promise_extension.js', # required by boot.js
            'web/static/src/boot.js', # odoo module system
            'web/static/src/env.js', # required for services
            'web/static/src/session.js', # expose __session_info__ containing server information
            'web/static/lib/owl/owl.js', # owl library
            'web/static/lib/owl/odoo_module.js', # to be able to import "@odoo/owl"
            'web/static/src/core/utils/functions.js',
            'web/static/src/core/browser/browser.js',
            'web/static/src/core/registry.js',
            'web/static/src/core/assets.js',
            'estate/static/src/**/*.js',
            'estate/static/src/**/*.xml',]
    },
    'application': True,
}