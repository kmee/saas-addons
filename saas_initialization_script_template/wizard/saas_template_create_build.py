from odoo import api, models, fields


class CreateBuildByTemplate(models.TransientModel):
    _inherit = 'saas.template.create_build'

    @api.onchange('template_id')
    def _onchange_build_post_init_ids(self):
        for rec in self:
            build_template_ids = rec.template_id.build_initialization_template_ids
            for build_template_id in build_template_ids:
                if build_template_id:
                    for line_id in build_template_id.build_post_init_line_ids:
                        vals = line_id.read()
                        line = self.env['build.post_init.line'].create(self._prepare_build_post_init_line_vals(vals[0]))
                        rec.build_post_init_ids += line

    def _prepare_build_post_init_line_vals(self, vals):
        out = {}
        out['key'] = vals['key']
        out['value'] = vals['value']
        return out



class BuildPostInit(models.TransientModel):
    _inherit = 'build.post_init.line'
    initialization_template_id = fields.Many2one(
        comodel_name='saas.initialization.template',
        readonly=True
    )
