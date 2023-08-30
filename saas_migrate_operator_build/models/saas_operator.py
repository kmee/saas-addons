# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.addons.saas_operator_remote.models.saas_operator import jsonrpc


class SaasOperator(models.Model):

    _inherit = "saas.operator"

    def get_mandatory_modules(self):
        return super(SaasOperator, self).get_mandatory_modules() + ["module_auto_update"]

    def auto_update_modules(self, db_name):
        if self.type != "remote":
            return

        jsonrpc(
            self.remote_instance_url + "/saas_operator/auto_update_modules",
            {
                "master_pwd": self.remote_master_pwd,
                "db_name": db_name,
            },
        )

    def close_db_connection(self, db_name):
        if self.type != "remote":
            return

        jsonrpc(
            self.remote_instance_url + "/saas_operator/close_db_connection",
            {
                "master_pwd": self.remote_master_pwd,
                "db_name": db_name,
            },
        )
