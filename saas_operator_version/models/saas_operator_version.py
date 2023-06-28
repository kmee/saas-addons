# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaasOperatorVersion(models.Model):

    _name = "saas.operator.version"
    _description = "Saas Operator Version"

    name = fields.Char(
        string='Name',
        required=True,
    )
    description = fields.Text(
        string="Description",
    )
    image_tag = fields.Char(
        string='Image Tag',
        required=True,
    )
    external_link = fields.Char(
        string="External Link",
        help="Link to external resources associated with this release. Ex: release page of the version in the git repository",
    )
    operator_ids = fields.One2many(
        string="Operators",
        comodel_name="saas.operator",
        inverse_name="version_id",
    )
