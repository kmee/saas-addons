import logging
from jinja2 import Environment, FileSystemLoader

from odoo.http import route, request
from odoo.addons.component.core import Component
from odoo.modules.module import get_module_resource
from odoo.addons.web.controllers.main import content_disposition

from odoo.addons.base_rest import restapi

_logger = logging.getLogger(__name__)

DYNAMIC_CONFIG_PATH = get_module_resource(
    'saas_operator_traefik_provider', 'templates')
environment = Environment(loader=FileSystemLoader(DYNAMIC_CONFIG_PATH))
template = environment.get_template("traefik_dynamic_config")


def render_template(operators, builds, remote_domain):
    return template.render(
        operators=operators,
        builds=builds,
        remote_domain=remote_domain,
    )


class HTTPProviderService(Component):
    _inherit = "base.rest.service"
    _name = "http.provider.service"
    _usage = "http_provider"
    _collection = "saas_operator_traefik_provider.services"

    @restapi.method(
        [(["/"], "GET")],
        auth="public",
    )
    def get(self):
        operator_ids = self.env['saas.operator'].sudo().search([('type', '=', 'remote'), ('state', '=', 'online')])
        operators = operator_ids.mapped(
            lambda record: (record.name, record.remote_instance_url)
        )

        build_ids = self.env['saas.db'].sudo().search([('type', '=', 'build')])
        builds = build_ids.mapped(
            lambda record: (record.name, record.operator_id.name)
        )

        config_params = self.env['ir.config_parameter'].sudo()
        remote_domain = config_params.get_param('traefik_operator_domain', '')
        file_content = render_template(operators, builds, remote_domain)

        content_type = ('Content-Type', 'application/octet-stream')
        disposition_content = ('Content-Disposition', content_disposition('dynamic_config.yaml'))
        return request.make_response(file_content, [content_type, disposition_content])


