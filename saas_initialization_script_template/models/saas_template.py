from odoo import models, fields, api


class SAASTemplate(models.Model):
    _inherit = 'saas.template'

    template_initialization_template_ids = fields.Many2many(
        'saas.initialization.template',
        'template_initialization_template_rel',
        'template_id',
        'initialization_template_id',
        string='Initialization Template'
    )

    build_initialization_template_ids = fields.Many2many(
        'saas.initialization.template',
        'temp_build_initialization_template_rel',
        'template_id',
        'initialization_template_id',
        string='Build Initialization Template'
    )

    @api.onchange('template_initialization_template_ids')
    def onchange_initialization_template(self):
        if self.template_initialization_template_ids:
            template_code = ""
            for template in self.template_initialization_template_ids:
                template_code += template.template_post_init + "\n"
            self.template_post_init = template_code

    @api.onchange('build_initialization_template_ids')
    def onchange_build_initialization_template(self):
        if self.build_initialization_template_ids:
            template_code = ""
            for template in self.build_initialization_template_ids:
                template_code += template.build_post_init + "\n"
            self.build_post_init = template_code