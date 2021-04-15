# -*- coding: utf-8 -*-

from odoo import fields, models
from . import nivel

class MatriculateIdioma(models.Model):
    _name = 'matriculate.idioma'
    _description = 'Idioma'

    name = fields.Char('Nombre del idioma', size=50, required=True)

    _sql_constraints = [
        ('name_uniq',
         'unique (name)',
         u'El nombre del idioma debe ser único!'),
    ]
