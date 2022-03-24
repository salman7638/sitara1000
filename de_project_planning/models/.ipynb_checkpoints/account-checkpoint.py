# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class HrTimesheet(models.Model):
    _inherit = 'account.analytic.line'

    job_type_id = fields.Many2one('project.job.type', string='Job Type', change_default=True, ondelete='restrict') 
