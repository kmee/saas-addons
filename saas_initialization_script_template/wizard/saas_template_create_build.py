from odoo import api, models, fields


class CreateBuildByTemplate(models.TransientModel):
    _inherit = 'saas.template.create_build'

    # build_post_init_ids = fields.One2many(compute='_compute_build_post_init_ids')

    @api.onchange('template_id')
    def _onchange_build_post_init_ids(self):
        for rec in self:
            build_template_id = rec.template_id.build_initialization_template_id
            if build_template_id:
                rec.build_post_init_ids = build_template_id.build_post_init_line_ids


class BuildPostInit(models.TransientModel):
    _inherit = 'build.post_init.line'
    initializateion_template_id = fields.Many2one(
        comodel_name='saas.initialization.template',
        readonly=True
    )
