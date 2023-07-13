from odoo import api, models, fields


class CreateBuildByTemplate(models.TransientModel):
    _inherit = 'saas.template.create_build'

    # build_post_init_ids = fields.One2many(compute='_compute_build_post_init_ids')

    @api.onchange('template_id')
    def _onchange_build_post_init_ids(self):
        for rec in self:
            build_template_id = rec.template_id.build_initialization_template_id
            if build_template_id:
                for line_id in build_template_id.build_post_init_line_ids:
                    rec.build_post_init_ids += line_id.copy({
                        "initialization_template_id" : False,
                    })


class BuildPostInit(models.TransientModel):
    _inherit = 'build.post_init.line'
    initialization_template_id = fields.Many2one(
        comodel_name='saas.initialization.template',
        readonly=True
    )
