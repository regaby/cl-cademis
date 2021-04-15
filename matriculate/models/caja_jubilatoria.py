# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

#Se definen las cajas jubilatorias para los matriculados
class MatriculateCajaJubilatoria(models.Model):

    _name = 'matriculate.caja.jubilatoria'
    _description = 'matriculate.caja.jubilatoria'

    name = fields.Char(string='Caja Jubilatoria', required=True)
    tipo = fields.Selection(string='Tipo', selection=[('nacional', 'Nacional'),
    													('provincial', 'Provincial')],
                                required=True)
