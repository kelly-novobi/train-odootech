import datetime
from datetime import date

from odoo import api, models, fields

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['library.book', 'mail.thread']
    
    isbn = fields.Char(
                        string='International Standard Book Number',
                        required=True)
    description = fields.Text(string='Brief introduction')
    status = fields.Selection(string='Type',selection=[('not_published','Not Published'),('available','Available'),('borrowed','Borrowed'),('lost','Lost')],
                            default='available')
    current_borrower_id = fields.Many2one('res.partner',string='Borrower',help='The current Borrower',
                                        readonly=True,tracking=True)
    return_date = fields.Datetime(string='Return Date',help='The date on which the borrower will send the book',
                                tracking=True)
    location_id = fields.Many2one('book.location',string='Location',help='The location (shelf) where we store the book')

    def lease_button(self):
        context = dict(self.env.context)
        context['default_lease_book_id'] = self.id
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'lease.book.wizard',    # name of respective model,
                'target': 'new',
                'context': context,
        }

    # future date_release changes status to not_published
    @api.onchange("date_release")
    def _onchange_status(self):
        #context_date = self.env.context['date_release']
        today = fields.Date.today()
        #now= datetime.strftime(fields.Datetime.context_timestamp(self, datetime.now()), "%Y-%m-%d %H:%M:%S")
        
        if self.date_release > today:
            self.status = 'not_published'