from odoo import models, fields

class HelloModel(models.Model):
    _name = 'hello.world'
    _description = 'Hello World Model'

    name = fields.Char(string='Name')
    message = fields.Text(string='Message')