# Copyright 2023 KMEE
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import os
import glob
import logging
import tempfile
import urllib.request
import urllib.error
from string import Template
from shutil import copytree
from datetime import datetime
from unicodedata import normalize
import gitlab

from odoo import _, api, fields, models, exceptions
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)

DEPLOYMENT_TEMPLATE_PATH = get_module_resource(
    'saas_operator_remote_deploy', 'static/template', 'operator_deployment_template')

CONFIG_PARAMS = [
    'gitlab_url',
    'gitlab_private_token',
    'gitlab_deployment_repo',
    'deployment_repo_branch',
    'deployment_folder_prefix',
    'deployment_committer_name',
    'deployment_committer_email'
]

STATES = [
    ('draft', 'Draft'),
    ('offline', 'Offline'),
    ('online', 'Online'),
    ('error', 'Error')
]

def sanitize_string(string):
    string = string.replace(' ', '-')
    string = string.replace('.', '-')
    string = normalize('NFKD', string)
    return string


class SaasOperator(models.Model):

    _inherit = "saas.operator"

    state = fields.Selection(
        string='State',
        default='draft',
        selection=STATES,
    )

    state_message = fields.Char(
        string='State Message',
    )

    last_state_update = fields.Datetime(
        string='Last State Update'
    )

    def create_operator_deployment(self):
        """
        Deploys a new Odoo instance using a deployment GitLab repository
            monitored by Rancher Fleet
        """

        values = {
            'version': sanitize_string(self.name),
            'image_tag': self.version_id.image_tag,
        }

        if not self._is_all_config_params_valid():
            raise exceptions.UserError(_("All 'Operator Remote Deployment' configuration parameters must be filled in SaaS settings"))

        deploy_repo = self._get_gitlab_deploy_repo()
        changes_action = self._prepare_deployment(values)
        self._commit_deployment(deploy_repo, changes_action, values)
        self.update_remote_operator_status()

    def _is_all_config_params_valid(self):
        for param in CONFIG_PARAMS:
            config_params = self.env['ir.config_parameter']
            value = config_params.get_param(param, '')
            if not value:
                return False
        return True

    def _get_gitlab_deploy_repo(self):
        config_params = self.env['ir.config_parameter']
        gitlab_url = config_params.get_param('gitlab_url', '')
        gitlab_private_token = config_params.get_param('gitlab_private_token', '')
        gitlab_deployment_repo = config_params.get_param('gitlab_deployment_repo', '')

        gitlab_conn = gitlab.Gitlab(
            url=gitlab_url,
            private_token=gitlab_private_token,
        )
        return gitlab_conn.projects.get(gitlab_deployment_repo)

    def _prepare_deployment(self, values):
        """
        The file structure for deploying a new operator is generated from a template
            that will be used to calculate the necessary changes actions to generate the
            commit in the GitLab repository
        """
        with tempfile.TemporaryDirectory() as temp_dir:

            deploy_path = self._clone_deploy_template(temp_dir, values)

            return self._prepare_deployment_changes(temp_dir, deploy_path, values)

    def _clone_deploy_template(self, temp_dir, values):
        config_params = self.env['ir.config_parameter']
        deployment_folder_prefix = config_params.get_param('deployment_folder_prefix', '')

        deployment_folder = f'{deployment_folder_prefix}-{values.get("version")}'
        deploy_path = os.path.join(temp_dir, deployment_folder)
        copytree(DEPLOYMENT_TEMPLATE_PATH, deploy_path)
        return deploy_path

    def _prepare_deployment_changes(self, temp_dir, deploy_path, values):
        values_file_path = os.path.join(deploy_path, 'values.yaml')

        with open(values_file_path, 'r+') as values_file:
            self._fill_in_tamplate_values(values_file, values)

        action_changes = self._generate_actions_changes(temp_dir, deploy_path)

        return action_changes

    def _fill_in_tamplate_values(self, values_file, values):
        values_file.seek(0)
        file_content = values_file.read()

        template_obj = Template(file_content)
        new_file_content = template_obj.safe_substitute(
            TAG=values.get('image_tag'),
            OPERATOR_NAME=values.get('version')
        )

        # Override file content
        values_file.seek(0)
        values_file.truncate()
        values_file.write(new_file_content)

    def _generate_actions_changes(self, temp_dir, deploy_path):
        action_changes = []
        paths = glob.glob(deploy_path + '/**/*', recursive=True)
        for path in paths:
            if os.path.isfile(path):
                repo_file_path = path.replace(temp_dir + '/', '')

                with open(path) as file_to_commit:
                    action_changes.append(
                        {
                            'action': 'create',
                            'file_path': repo_file_path,
                            'content': file_to_commit.read(),
                        }
                    )
        return action_changes

    def _commit_deployment(self, deploy_repo, changes_action, values):
        config_params = self.env['ir.config_parameter']
        deployment_repo_branch = config_params.get_param('deployment_repo_branch', '')
        deployment_committer_name = config_params.get_param('deployment_committer_name', '')
        deployment_committer_email = config_params.get_param('deployment_committer_email', '')

        commit_data = {
            'branch': deployment_repo_branch,
            'commit_message': f'Deploy Operator: {values.get("version")}',
            'author_name': deployment_committer_name,
            'author_email': deployment_committer_email,
            'actions': changes_action,
        }

        try:
            commit = deploy_repo.commits.create(commit_data)
        except Exception as error:
            _logger.error("Error committing deploy of new operator in Gitlab: %s", error)
        else:
            _logger.info("New operator deployed %s. Commit: %s", values.get("version"), commit)

    def update_remote_operator_status(self):
        state = self.check_remote_operator_status()

        self.state = state[0]
        self.state_message = state[1]
        self.last_state_update = fields.Datetime.now()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def check_remote_operator_status(self):
        """
        Check if an operator is online through a request in the URL where it should resolve
        :return (str): Operator status
        """
        try:
            response = urllib.request.urlopen(f"http://{self.remote_instance_url}")
        except (urllib.error.HTTPError, urllib.error.URLError) as error:
            message = f"Operator is not online (Error:{error}). Operator: {self.name}. URL: {self.remote_instance_url}."
            _logger.info(message)
            return ("offline", message)
        except Exception as error:
            message = f"Error checking if operator is online: {error}. Probably because it is still offline. Operator: {self.name}. URL: {self.remote_instance_url}."
            _logger.error(message)
            return ("error", message)

        if response.getcode() == 200:
            message = f"Operator {self.name} Online. URL: {self.remote_instance_url}."
            _logger.info(message)
            return ("online", message)
        else:
            message = f"Operator is not online (Response Code: {response.getcode()}). Operator: {self.name}. URL: {self.remote_instance_url}."
            _logger.info(message)
            return ("offline", message)

