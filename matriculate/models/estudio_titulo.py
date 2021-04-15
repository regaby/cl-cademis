# -*- coding: utf-8 -*-

from odoo import fields, models
from . import nivel

class MatriculateEstudioTitulo(models.Model):
    _name = 'matriculate.estudio.titulo'
    _description = 'Titulo'

    name = fields.Char('Titulo de la estudio', size=50, required=True)
    nivel = fields.Selection(nivel.nivel, 'Nivel', required=True)

    _sql_constraints = [
        ('name_uniq',
         'unique (name)',
         u'El título de estudio debe ser único!'),
    ]
