# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Saas Operator Version',
    'description': """
        Adds the concept of versions to operators""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'KMEE',
    'website': 'https://www.kmee.com.br/',
    'depends': [
        'saas'
    ],
    'data': [
        'security/saas_operator_version.xml',

        'views/saas_operator.xml',
        'views/saas_operator_version.xml',
    ],
    'demo': [
        'demo/saas_operator_version.xml',
    ],
}
