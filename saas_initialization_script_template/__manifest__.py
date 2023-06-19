# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Saas Initialization Script Template',
    'description': """
        Initialization script templates for prepopulating template initialization and build initialization""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'KMEE',
    'website': 'https://kmee.com.br/',
    'depends': [
        'saas',
    ],
    'data': [
        "security/ir.model.access.csv",
        'views/saas_initialization_template_views.xml',
        'views/saas_template_views.xml',
        'views/saas_view.xml',
    ],
    'demo': [
    ],
}
