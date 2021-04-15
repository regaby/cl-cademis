# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

#Se definen las obras sociales para los matriculados
class MatriculateObraSocial(models.Model):

    _name= 'matriculate.obra.social'
    _description = 'Obra Social'

    name = fields.Char(string='Obra Social', required=True)
    prepaga = fields.Selection(string='Prepaga', selection=[('si', 'Si'),
    													('no', 'No')],
                                required=True)
