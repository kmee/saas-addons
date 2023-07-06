# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaasOperator(models.Model):

    _inherit = "saas.operator"

    version_id = fields.Many2one(
        string="Version",
        comodel_name="saas.operator.version",
        ondelete="restrict",
    )
