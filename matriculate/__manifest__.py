# -*- coding: utf-8 -*-
{
    'name': 'Professional College Matriculate',
    'version': '0.1',
    'author': 'Ing. Gabriela Rivero',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'partner_contact_birthdate',
        'partner_contact_nationality',
        'partner_contact_gender',
        # este modulo es para definir el circulo
        'partner_contact_department',
        'base_address_city',
        'base_location',
        'l10n_latam_invoice_document',
        'l10n_ar',
    ],
    'data': [
        'security/matriculate_security.xml',
        'security/ir.model.access.csv',
        'wizard/suspension_wizard_view.xml',
        'wizard/baja_wizard_view.xml',
        'wizard/advertencia_wizard_view.xml',
        'views/res_partner_view.xml',
        "views/universidad_view.xml",
        "views/estudio_titulo_view.xml",
        "views/idioma_view.xml",
        "views/motivo_view.xml",
        "views/empleo_view.xml",
        "views/profesion_view.xml",
        "views/obra_social_view.xml",
        "views/caja_jubilatoria_view.xml",
        'views/menues.xml',
    ],
    'qweb': [
    ],
    'installable': True,
}
