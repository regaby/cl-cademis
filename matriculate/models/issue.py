# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

#Se definen los motivos de porque se suspende, se advierte o se da de baja a un matriculado o un laboratorio
class MatriculadoIssue(models.Model):

    _name = 'matriculate.issue'
    _description = 'Issue'

    partner_id = fields.Many2one('res.partner', 'Matriculado')
    descripcion = fields.Char(string='Descripcion del Cambio')
    motivo_id =fields.Many2one('matriculate.motivo',string='Motivo del Cambio')
    date_issue = fields.Date(string='Fecha del Cambio')
    state = fields.Selection(
    	string='Estado del Matriculado',
    	selection=[
    	 ('baja', 'Baja'),
         ('advertido','Advertido'),
         ('suspension', 'Suspensión'),
         ('activo', 'Activo')
        ],
        default='baja',
        required=True
    )
