# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ResConfigSettings(models.TransientModel):

    _inherit = "res.config.settings"

    operator_env = fields.Char(string='Operator Env', config_parameter='operator_env')
    gitlab_url = fields.Char(string='GitLab URL', config_parameter='gitlab_url')
    gitlab_private_token = fields.Char(string='GitLab Private Token', config_parameter='gitlab_private_token')
    gitlab_deployment_repo = fields.Char(string='GitLab Deplyment Repo', config_parameter='gitlab_deployment_repo')
    deployment_repo_branch = fields.Char(string='Deployment Repo Branch', config_parameter='deployment_repo_branch')
    deployment_folder_prefix = fields.Char(string='Deployment Folder Prefix', config_parameter='deployment_folder_prefix')
    deployment_committer_name = fields.Char(string='Deployment Committer Name', config_parameter='deployment_committer_name')
    deployment_committer_email = fields.Char(string='Deployment Committer E-mail', config_parameter='deployment_committer_email')
