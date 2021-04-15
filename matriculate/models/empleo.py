# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MatriculateEmpleo(models.Model):

	_name= 'matriculate.empleo'
	_description = 'matriculate.empleo'

	#name = fields.Char(string='Particular')
	particular_id = fields.Many2one('matriculate.particular', 'Cargo particular')
	especialidad_id = fields.Many2one('matriculate.especialidad', 'Especialidad a la que se dedica')
	actuacion_cientifica = fields.Char(string='Actuación científica')
	actuacion_didactica = fields.Char(string='Actuación didáctica')
	actuacion_entidades = fields.Char(string='Actuación en entidades profesionales')
	partner_id = fields.Many2one('res.partner', 'Matriculado')




class MatriculateEspecialidad(models.Model):
	_name='matriculate.especialidad'
	_description = 'Especialidad'

	name = fields.Char(string='Especiaidad a la que se dedica')

class MatriculateParticular(models.Model):
	_name='matriculate.particular'
	_description = 'Particular'

	name = fields.Char(string='Cargo Particular')
