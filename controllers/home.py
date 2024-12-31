from odoo import models, _


class IrConfigParameter(models.Model):
    _inherit = "ir.config_parameter"

    def write(self, vals):
        data = super(IrConfigParameter, self).write(vals)
        if data and self.key == 'web.base.sorturl':
            self.env['ir.http'].env.registry.clear_cache("routing")
            self.env['ir.attachment'].regenerate_assets_bundles()
        return {'type': 'ir.actions.client', 'tag': 'soft_reload'}
