import time
import logging

from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class MigrateOperatorBuild(models.TransientModel):
    _name = 'saas.migrate.operator.build'

    operator_id = fields.Many2one(
        comodel_name='saas.operator',
        string='Operator',
        domain="[('state', '=', 'online'), ('type', '=', 'remote')]",
    )

    def start_migration(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_builds_ids = self.env['saas.db'].browse(selected_ids)

        for build in selected_builds_ids:
            self.with_delay(channel="root.migrate_operator_build").migrate_job(build)

    def migrate_job(self, build):
        _logger.info("Migrating build %s to operator %s", build.name, self.operator_id.name)
        build.is_migrating = True

        build.operator_id = self.operator_id.id

        # Ensures that Traefik's HTTP Provider has already polled the updated
        # build mapping with operators
        time.sleep(5)

        build.change_build_db_owner()

        build.auto_update_modules()

        build.is_migrating = False

        _logger.info("Build %s migrated to operator %s", build.name, self.operator_id.name)
