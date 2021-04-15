# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

#Se definen los motivos de porque se suspende, se advierte o se da de baja a un matriculado o un laboratorio
class MatriculateMotivo(models.Model):

    _name = 'matriculate.motivo'
    _description = 'Motivo'


    name = fields.Char(string='Descripción', required=True)
    state = fields.Selection(
    	string='Estado',
    	selection=[
    	 ('baja', 'Baja'),
    	 ('advertencia', 'Advertencia'),
         ('suspension', 'Suspensión')],
        required=True)
