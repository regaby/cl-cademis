# -*- coding: utf-8 -*-

from odoo import fields, models
from . import nivel

class MatriculateEstudio(models.Model):
    _name = 'matriculate.estudio'
    _descripion = 'Estudio'

    universidad_id = fields.Many2one('matriculate.universidad', string='Universidad', required=True)
    titulo_id = fields.Many2one('matriculate.estudio.titulo', 'Titulo', required=True,
                                ondelete='restrict')
    nivel = fields.Selection(nivel.nivel, related='titulo_id.nivel', string='Nivel')
    inicio = fields.Date('Fecha de Inicio', required=False)
    fin = fields.Date('Fecha de Cierre', required=False)
    duracion = fields.Integer('Duracion', required=False)
    estado = fields.Selection([('1', 'Completo'),
                               ('2', 'Incompleto'),
                               ('3', 'En Curso')], 'Estado', required=True)
    partner_id = fields.Many2one('res.partner', 'Matriculado', ondelete='restrict')
    partner_curso_id = fields.Many2one('res.partner', 'Matriculado', ondelete='restrict')
