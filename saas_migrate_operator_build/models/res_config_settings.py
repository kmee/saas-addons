# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    remote_operator_db_host = fields.Char(string='Remote Operator DB Host', config_parameter='remote_operator_db_host')
    remote_operator_db_port = fields.Char(string='Remote Operator DB Port', config_parameter='remote_operator_db_port')
    remote_operator_db_superuser = fields.Char(string='Remote Operator DB Superuser', config_parameter='remote_operator_db_superuser')
    remote_operator_db_superuser_password = fields.Char(string='Remote Operator DB Superuser Password', config_parameter='remote_operator_db_superuser_password')
