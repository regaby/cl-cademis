# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class MatriculateUniversidad(models.Model):

    _name= 'matriculate.universidad'
    _description = 'Universidad'

    name = fields.Char(string='Nombre', required=True)
    country_id = fields.Many2one('res.country',string='País', required=True)
    state_id = fields.Many2one('res.country.state', string='Provincia',required=True)

    _sql_constraints = [
      ('name_uniq', 'UNIQUE (name)',  'Ya existe una universidad con el mismo nombre')
    ]

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
        else:
            return {'domain': {'state_id': []}}
