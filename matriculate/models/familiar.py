from odoo import models, fields, api, _


class MatriculateFamiliar(models.Model):

    _name= 'matriculate.familiar'
    _description = 'matriculate.familiar'

    name = fields.Char(string='Nombre', required=True)
    apellido = fields.Char(string='Apellido', required=True)
    parentesco = fields.Selection([('mother', 'Madre'),
                                   ('father', 'Padre'),
                                   ('spouse', 'Cónyuge'),
                                   ('son', 'Hijo/a')], 'Parentesco', required=True)
    partner_id = fields.Many2one('res.partner', 'Matriculado', ondelete='restrict')
