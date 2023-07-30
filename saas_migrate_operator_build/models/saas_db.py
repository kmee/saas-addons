# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaasDb(models.Model):

    _inherit = "saas.db"

    is_migrating = fields.Boolean(string="Is migrating", default=False)

    def action_open_migrate_wizard(self):
        return {
            'name': "Migrate Operator Build",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'saas.migrate.operator.build',
            'view_id': self.env.ref('saas_migrate_operator_build.saas_migrate_operator_build').id,
            'target': 'new',
        }

    def change_build_db_owner(self):
        cr = self._cr
        query = f'ALTER DATABASE "{self.name}" OWNER TO {self.operator_id.name}'

        cr.execute(query)
        cr.commit()

    def auto_update_modules(self):
        return self.operator_id.auto_update_modules(self.name)
