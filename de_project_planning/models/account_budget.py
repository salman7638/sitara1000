# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class CrossoveredBudgetLines(models.Model):
    _inherit = 'crossovered.budget.lines'

    project_cost_sheet_id = fields.Many2one('project.cost.sheet', string='Cost Sheet', change_default=True, ondelete='restrict')
    job_type_id = fields.Many2one('project.job.type', string='Job Type', change_default=True, ondelete='restrict', required=True) 

