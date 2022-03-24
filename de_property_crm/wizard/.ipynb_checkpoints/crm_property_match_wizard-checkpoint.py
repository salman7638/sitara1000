# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrmPropertyMatchWizard(models.TransientModel):
    _name = "crm.property.match.wizard"
    _description = "CRM Property Matched Wizard"