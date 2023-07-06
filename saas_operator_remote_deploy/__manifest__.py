# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Saas Operator Remote Deploy',
    'description': """
        Automate remote operator deployment with Gitlab and Rancher Fleet Stack""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'KMEE',
    'website': 'https://www.kmee.com.br/',
    'depends': [
        'saas',
        'saas_operator_version',
    ],
    "data": [
        'views/res_config_settings.xml',
        'views/saas_operator.xml',
    ],
    'demo': [
    ],
}
