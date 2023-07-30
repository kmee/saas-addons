# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Saas Operator Traefik Provider',
    'description': """
        Traefik http provider endpoint to map builds to their respective operators""",
    'version': '14.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'KMEE',
    'website': 'https://www.kmee.com.br/',
    'depends': [
        "saas",
        "saas_operator_remote",
        "saas_operator_remote_deploy",
        "base_rest",
    ],
    'data': [
    ],
    'demo': [
    ],
}
