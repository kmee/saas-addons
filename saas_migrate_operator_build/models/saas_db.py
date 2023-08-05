# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import os
import psycopg2


from odoo import _, api, fields, models
from odoo.addons.http_routing.models.ir_http import slugify


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
        self._change_database_owner(self.name, self.operator_id.name)

    def auto_update_modules(self):
        return self.operator_id.auto_update_modules(self.name)

    def _change_database_owner(self, db_name, new_owner):

        new_owner = slugify(new_owner)
        conn = self._create_superadmin_db_connection(db_name)
        try:
            cursor = conn.cursor()
            querys = [
                "SELECT quote_ident(schemaname) || '.' || quote_ident(tablename) FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog';",
                "SELECT quote_ident(sequence_schema) || '.' || quote_ident(sequence_name) FROM information_schema.sequences WHERE sequence_schema != 'pg_catalog';",
                "SELECT quote_ident(table_schema) || '.' || quote_ident(table_name) FROM information_schema.views WHERE table_schema != 'pg_catalog';"
            ]

            for query in querys:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    query = f'ALTER TABLE {row[0]} OWNER TO "{new_owner}"'
                    cursor.execute(query)

            query = "SELECT DISTINCT quote_ident(table_schema) FROM information_schema.tables WHERE table_schema != 'pg_catalog';"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                query = f'ALTER SCHEMA {row[0]} OWNER TO "{new_owner}"'
                cursor.execute(query)

            query = "SELECT quote_ident(n.nspname) || '.' || quote_ident(p.proname) || '(' || pg_catalog.pg_get_function_identity_arguments(p.oid) || ')' FROM pg_catalog.pg_proc p JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace WHERE n.nspname != 'pg_catalog';"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                query = f'ALTER FUNCTION {row[0]} OWNER TO "{new_owner}"'
                cursor.execute(query)

            query = f'ALTER DATABASE "{db_name}" OWNER TO "{new_owner}"'
            cursor.execute(query)

            conn.commit()

        except psycopg2.DatabaseError as error:

            raise error

        finally:
            cursor.close()
            conn.close()

    def _create_superadmin_db_connection(self, db_name):
        config_params = self.env['ir.config_parameter']
        db_host = config_params.get_param('remote_operator_db_host', '')
        db_port = config_params.get_param('remote_operator_db_port', '')
        user = config_params.get_param('remote_operator_db_superuser', '')
        password = config_params.get_param('remote_operator_db_superuser_password', '')

        conn = psycopg2.connect(
            database=db_name,
            host=db_host,
            port=db_port,
            user=user,
            password=password,
        )

        return conn
