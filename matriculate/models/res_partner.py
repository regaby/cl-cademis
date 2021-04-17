# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import date
from datetime import datetime
from dateutil import relativedelta
import time
from odoo.exceptions import ValidationError

class Partner(models.Model):

    _name = 'res.partner'
    _inherit = 'res.partner'

    is_matriculado = fields.Boolean(string='Matriculado')
    matricula_number = fields.Integer(string='N° de Matrícula')
    matricula_date = fields.Date(string='Fecha de Inscripción')
    marital = fields.Selection(
        string='Estado Civil',
        selection=
        [('single', 'Soltero/a'),
         ('married', 'Casado/a'),
         ('divorced', 'Divorciado/a'),
         ('widower', 'Viudo/a')],
        default='single'
    )
    dni = fields.Char(string='DNI', size=8)
    # city_id = fields.Many2one('res.city', string='Ciudad')
    #datos laborales
    job_street = fields.Char()
    job_city = fields.Many2one('res.city', string='Ciudad')
    job_phone = fields.Char(string="Teléfono Profesional")
    street_number = fields.Char()
    street_floor = fields.Char()
    street_depto = fields.Char()
    state = fields.Selection(
        [('pendiente','Pendiente'),
         ('activo','Activo'),
         ('activo_honorario','Activo Honorario'),
         ('advertido','Advertido'),
         ('suspendido','Suspendido Morosidad'),
         ('suspendido_voluntario','Suspendido Voluntariamente'),
         ('baja','Cancelado/Baja'),
         ('fallecido','Fallecido'),
         ('incompatibilidad','Incompatibilidad'),
        ],
        string='Status',
        default='pendiente',
        readonly=True
    )
    #datos de estudio
    estudio_ids = fields.One2many('matriculate.estudio', 'partner_id', string='Estudios')
    curso_ids = fields.One2many('matriculate.estudio', 'partner_curso_id', string='Capacitaciones')
    idioma_ids = fields.Many2many('matriculate.idioma', string='Idiomas',  ondelete='restrict')
    profesion_id = fields.Many2one('matriculate.profesion', string='Profesión', ondelete='restrict')
    #datos de familiares
    familiar_ids = fields.One2many('matriculate.familiar', 'partner_id', string='Familiares')

    #Datos sobre los motivos de la última suspensión o de la última baja para ser mostrado en el res_partner
    issue_lines = fields.One2many('matriculate.issue', 'partner_id', help="Incidencias.")
    motivo_cambio_estado_id =fields.Many2one('matriculate.motivo',string='Motivo del Estado')
    date_cambio_estado = fields.Date(string='Fecha del último Estado')
    #Datos sobre empleo o actividades profesionales
    empleo_ids = fields.One2many('matriculate.empleo', 'partner_id', string='Cargos o empleos')
    #Datos sobre los aportes
    obra_social_id = fields.Many2one('matriculate.obra.social', string='Obra Social', ondelete='restrict')
    caja_jubilatoria_id = fields.Many2one('matriculate.caja.jubilatoria', string='Caja Jubilatoria', ondelete='restrict')

    def _onchange_state_id(self):
        if self.state_id:
            return {'domain': {'city_id': [('state_id', '=', self.state_id.id)],'job_city': [('state_id', '=', self.state_id.id)]},
            'value': {'country_id': self.state_id.country_id}}
        else:
            return {'domain': {'city_id': [], 'job_city':[] }}

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id.id:
            country = self.city_id.state_id.country_id
            self.city = self.city_id.name
            return {'value': {'state_id': self.city_id.state_id, 'zip':self.city_id.codigo_postal, 'country_id' : country}}
            print ("---------------------------------------------------_>>>>", city)

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.country_id:
            return {'domain': {'state_id': [('country_id', '=', self.country_id.id)]}}
        else:
            return {'domain': {'state_id': []}}

    @api.constrains('matricula_number')
    def _check_matricula_number(self):
        for record in self:
            if record.matricula_number == 0 and self.state == 'pendiente':
                return True
            if record.matricula_number == 0 and self.state != 'pendiente':
                raise ValidationError("No se puede asignar 0 a un matriculado que este en un estado distinto a pendiente.")
            else:
                partner = self.env['res.partner'].search([('matricula_number', '=', record.matricula_number)])
                if partner.id != record.id:
                    raise ValidationError("Ya existe un matriculado con la matrícula %s" % record.matricula_number)
                else:
                    return True


    def print_carnet(self):
        datas = {
            'ids': [self.id],
            'model': 'res.partner',
            'form': self.id,
        }
        ids_ret = [self.id]
        ctx = dict(self.env.context)
        ctx.update({'active_id': ids_ret[0],
                    'active_ids': ids_ret,
                    'active_model': 'res.partner',
                   })
        return {
            'type': 'ir.actions.report',
            'report_name': 'carnet.matriculado',
            'report_type': 'aeroo',
            'datas': datas,
            'context': ctx,
            'target': 'current',
            }

    def get_matricula(self):
        matriculados = self.env['res.partner'].search([('is_matriculado', '=', True)], order='matricula_number desc', limit=1)
        mat = matriculados.matricula_number + 1
        return mat


    #Genera el código secuencial para el laboratorio
    def get_cod_lab(self):
        laboratorios = self.env['res.partner'].search([('is_laboratory', '=', True)], order='cod_number_lab desc', limit=1)
        print ('########################', laboratorios.cod_number_lab)
        cod = laboratorios.cod_number_lab + 1
        print ('########################', cod)
        return cod


    def button_alta(self):
        #Cambiar al estado activo
        if self.state == 'pendiente':
            self.write({'state': 'activo'})
            if (self.is_matriculado):
                #Asigna el número de matricula
                self.matricula_number = self.get_matricula()
            #Cargar la fecha del dia en la fecha de inscripcion de la matricula
            self.matricula_date = datetime.now()
        if self.state == 'suspendido':
            description = "Cambio de estado Suspendido a Activo"
        elif self.state == 'advertido':
            description = "Cambio de estado Advertido a Activo"
        elif self.state == 'baja':
            description = "Cambio de estado Baja a Activo"
        self.write({'state': 'activo'})
        self.motivo_cambio_estado_id = None
        issue_obj = self.env['matriculate.issue']
        issue_obj.create({
            'partner_id': self.id,
            'descripcion': description,
            'motivo_id': False,
            'date_issue': datetime.now(),
            'state':'activo'})
        return True

    def button_suspendido(self,motivo_id,descripcion,partner_id):
        self.write({'state': 'suspendido'})
        self.motivo_cambio_estado_id = motivo_id
        self.date_cambio_estado = datetime.now()
        issue_obj = self.env['matriculate.issue']
        issue_obj.create({
            'partner_id': partner_id,
            'descripcion': descripcion,
            'motivo_id': motivo_id[0],
            'date_issue': datetime.now(),
            'state':'suspension'})
        return {}

    def button_advertido(self,motivo_id,descripcion,partner_id):
        self.write({'state': 'advertido'})
        self.motivo_cambio_estado_id = motivo_id
        self.date_cambio_estado = datetime.now()
        issue_obj = self.env['matriculate.issue']
        issue_obj.create({
            'partner_id': partner_id,
            'descripcion': descripcion,
            'motivo_id': motivo_id[0],
            'date_issue': datetime.now(),
            'state':'advertido'})
        return {}

    def button_baja(self, motivo_id, descripcion,partner_id):
        self.write({'state': 'baja'})
        self.motivo_cambio_estado_id = motivo_id
        self.date_cambio_estado = datetime.now()
        issue_obj = self.env['matriculate.issue']
        issue_obj.create({
            'partner_id': partner_id,
            'descripcion': descripcion,
            'motivo_id': motivo_id[0],
            'date_issue': datetime.now(),
            'state':'baja'})
        return {}

    #Método automatizado para el envío de mails automatizados
    def send_automatic_email_deuda(self):
        today = datetime.now().date()
        #Cantidad de meses necesarios para enviar mail de deuda
        number_months_debt = 3
        res_partners = self.env['res.partner'].search([('state', '=', 'activo'), ('is_matriculado', '=', True)])
        for partner in res_partners:
                invoice = self.env['account.invoice'].search([('partner_id', '=', partner.id), ('state', '=', 'paid')], order='date_due desc', limit=1)
                if invoice:
                    if invoice.date_due < today.strftime('%Y-%m-%d'):
                        date_due = datetime.strptime(invoice.date_due , '%Y-%m-%d')
                        month_diff = abs( int(today.strftime("%m")) - int(date_due.strftime("%m") ))
                        if month_diff > number_months_debt:
                            #Envia el Mail
                            template = self.env.ref('matriculate.aviso_deuda_template')
                            self.env['mail.template'].browse(template.id).send_mail(partner.id, force_send=True)
                            if partner.state == 'activo':
                                #Cambia de estado al partner
                                partner.write({'state': 'suspendido'})
                                descripcion = 'Cambio de estado automático por adeudar cuotas'
                                motivo_cambio_estado = self.env['matriculate.motivo'].search([('name', '=', 'Falta de pago')])
                                print(motivo_cambio_estado.id)
                                partner.date_cambio_estado = datetime.now()
                                issue_obj = self.env['matriculate.issue']
                                issue_obj.create({
                                    'partner_id': partner.id,
                                    'descripcion': descripcion,
                                    'motivo_id': motivo_cambio_estado.id,
                                    'date_issue': datetime.now(),
                                    'state':'suspension'})

   #Dejo por defecto como tipo de documento al CUIT
    def _get_default_category(self):
        res = self.env['l10n_latam.identification.type'].search([('name', '=', 'CUIT')])
        return res and res[0] or False
    main_id_category_id = fields.Many2one('l10n_latam.identification.type', required=False, default=_get_default_category)

    #Dejo por defecto como responsabilidad de afip a Consumidor Final
    def _get_default_category_afip(self):
        res = self.env['l10n_ar.afip.responsibility.type'].search([('code', '=', '5')])
        return res and res[0] or False
    afip_responsability_type_id = fields.Many2one('l10n_ar.afip.responsibility.type', required=False, default=_get_default_category_afip)




    @api.constrains('cod_number_lab')
    def _check_cod_number_lab(self):
        for record in self:
            if record.cod_number_lab == 0 and self.state == 'pendiente':
                return True
            if record.cod_number_lab == 0 and self.state != 'pendiente':
                raise ValidationError("No se puede asignar 0 como código a un laboratorio que este en un estado distinto a pendiente.")
            else:
                partner = self.env['res.partner'].search([('cod_number_lab', '=', record.cod_number_lab)])
                if partner.id != record.id:
                    raise ValidationError("Ya existe un laboratorio con con el mismo código %s" % record.cod_number_lab)
                else:
                    return True

    #No permite que un matriculado sea director técnico de mas de un laboratorio.
    @api.constrains('dt')
    def _check_dt_unique(self):
        if self.is_matriculado == True: return True
        res = self.env['res.partner'].search([('is_laboratory', '=', True)])
        for r in res:
            if r.dt:
                if r.dt.id == self.dt.id and r.id != self.id:
                    raise ValidationError("El director técnico que está intentando asignar ya se encuentra asignado al laboratorio %s" %r.name)
         #Acá asigno el laboratorio recien creado al director técnico para que sea mostrado en matriculados
        if self.dt: self.dt.lab = self.id
        return True



