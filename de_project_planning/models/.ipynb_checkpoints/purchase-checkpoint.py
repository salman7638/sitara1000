# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
   
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    project_id = fields.Many2one('project.project', string='Project', ondelete='cascade', index=True, copy=False)
    task_id = fields.Many2one('project.task', string='Task', ondelete='cascade', index=True, copy=False, domain="[('project_id', '=', project_id)]")
    
    
    @api.onchange('task_id')
    def _onchange_task_id(self):
        if not self.task_id:
            self.task_id = self.requisition_id.task_id
            return
        
    @api.onchange('project_id')
    def _onchange_project_id(self):
        if not self.project_id:
            self.project_id = self.requisition_id.project_id
            return    
        
#         ab = self.with_company(self.company_id)
        
        
#         self.project_id = self.requisition_id.project_id.id
#         self.company_id = task.company_id.id
#         name = self.name