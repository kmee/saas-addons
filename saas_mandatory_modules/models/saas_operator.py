# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaasOperatorMandatoryModules(models.Model):

    _inherit = "saas.operator"

    mandatory_modules_ids = fields.Many2many('saas.module', string="Mandatory Modules")

    def get_mandatory_modules(self):
        mandatory_modules = super().get_mandatory_modules()
        for record in self.mandatory_modules_ids:
            mandatory_modules.append(record.name)
        return mandatory_modules
    