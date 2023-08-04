# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    traefik_operator_domain = fields.Char(string='Operator Domain', config_parameter='traefik_operator_domain')
