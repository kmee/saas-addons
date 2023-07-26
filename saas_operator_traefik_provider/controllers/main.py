from odoo.addons.base_rest.controllers import main
from odoo.http import route


class TraefikController(main.RestController):
    _root_path = "/traefik/"
    _collection_name = "saas_operator_traefik_provider.services"
