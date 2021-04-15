# -*- coding: utf-8 -*-

from odoo import models, fields, api
import time
from openerp.tools import misc, DEFAULT_SERVER_DATETIME_FORMAT

class SuspensionWizard(models.TransientModel):

    _name = 'suspension.wizard'
    _description = 'Suspension Wizard'

    motivo_id = fields.Many2one('matriculate.motivo',string='Motivo', required=True)
    descripcion = fields.Char('Descripcion', required=False)

    def makeSuspension(self):
        partner_obj = self.env['res.partner']
        partner_id = self._context['active_ids'][0]
        partner = partner_obj.browse(partner_id)
        wizard = self.read(['motivo_id'])[0]
        wizard2 = self.read(['descripcion'])[0]
        partner.button_suspendido(wizard['motivo_id'],wizard2['descripcion'],partner_id)
        return True
