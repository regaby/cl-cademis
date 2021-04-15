# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MatriculateProfesion(models.Model):

	_name= 'matriculate.profesion'
	_description = 'Profesion'

	name = fields.Char(string='Nombre', required=True)

	_sql_constraints = [
		('name_uniq', 'UNIQUE (name)',  'Ya existe una profesión con el mismo nombre')
	]
