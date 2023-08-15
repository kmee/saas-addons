from odoo import models, fields, api


class SAASTemplate(models.Model):
    _inherit = 'saas.template'

    template_initialization_template_id = fields.Many2one(
        comodel_name='saas.initialization.template',
        string='Initialization Template'
    )

    build_initialization_template_ids = fields.Many2many(
        comodel_name='saas.initialization.template',
        string='Build Initialization Template'
    )

    @api.onchange('template_initialization_template_id')
    def onchange_initialization_template(self):
        if self.template_initialization_template_id:
            template_code = self.template_initialization_template_id.template_post_init
            self.template_post_init = template_code

    @api.onchange('build_initialization_template_ids')
    def onchange_build_initialization_template(self):
        if self.build_initialization_template_ids:
            template_code = ""
            for template in self.build_initialization_template_ids:
                template_code += template.build_post_init + "\n"
            self.build_post_init = template_code