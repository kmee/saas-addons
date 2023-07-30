# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Saas Migrate Operator Build',
    'description': """
        Performs the migration of operator builds""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'KMEE',
    'website': 'https://kmee.com.br/',
    'depends': [
        'saas',
        'saas_operator_remote',
        'saas_operator_traefik_provider',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/job_queue.xml',
        'views/saas_db.xml',
        'wizard/saas_migrate_operator_build.xml',
    ],
    'demo': [
    ],
}
