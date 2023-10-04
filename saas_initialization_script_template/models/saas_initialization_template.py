from odoo import models, fields

DEFAULT_TEMPLATE_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - Warning: Warning Exception to use with raise
# To return an action, assign: action = {...}\n\n\n\n"""

DEFAULT_BUILD_PYTHON_CODE = """# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - Warning: Warning Exception to use with raise
# To return an action, assign: action = {{...}}
# You can specify places for variables that can be passed when creating a build like this:
# env['{key_name_1}'].create({{'subject': '{key_name_2}', }})
# When you need curly braces in build post init code use doubling for escaping\n\n\n\n"""


INITIALIZATION_TYPE_SELECTION = [
    ('template', 'Template'),
    ('build', 'Build'),
]


class SAASInitializationTemplate(models.Model):
    _name = 'saas.initialization.template'
    _description = 'Initialization Template'

    name = fields.Char(
        string='Name'
    )

    initialization_type = fields.Selection(
        string='Initialization Type',
        selection=INITIALIZATION_TYPE_SELECTION,
        default='build'
    )

    template_post_init = fields.Text(
        'Template Initialization',
        default=DEFAULT_TEMPLATE_PYTHON_CODE,
        help='Python code to be executed once db is created and modules are installed')

    build_post_init = fields.Text(
        'Build Initialization',
        default=DEFAULT_BUILD_PYTHON_CODE,
        help='Python code to be executed once build db is created from template')

    build_post_init_line_ids = fields.One2many(
        'build.post_init.line.persistent', 'initialization_template_id',
        string="Build Initialization Values",
        help="These values will be used on execution template's Build Initialization code"
    )

class BuildPostInitPersistent(models.Model):
    _name = 'build.post_init.line.persistent'
    _description = 'Build post init line persistent'
    key = fields.Char()
    value = fields.Char()
    initialization_template_id = fields.Many2one(
        comodel_name='saas.initialization.template',
        readonly=True
    )