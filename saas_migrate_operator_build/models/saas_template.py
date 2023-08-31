# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons.saas_operator_remote.models.saas_operator import jsonrpc


class SaasTemplate(models.Model):

    _inherit = "saas.template"

    def _on_template_created(self):
        super(SaasTemplate, self)._on_template_created()
        self.operator_id.with_delay().save_checksums(self.operator_db_name)
