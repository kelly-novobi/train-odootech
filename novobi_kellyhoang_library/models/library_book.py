from odoo import api, models, fields
from datetime import date
from odoo.exceptions import ValidationError

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['library.book', 'mail.thread']
    
    isbn = fields.Char(string='International Standard Book Number', required=True)
    description = fields.Text(string='Brief introduction')
    status = fields.Selection(string='Type',selection=[('not_published','Not Published'),('available','Available'),('borrowed','Borrowed'),('lost','Lost')], default='available')
    current_borrower_id = fields.Many2one('res.partner',string='Borrower',help='The current Borrower', readonly=True,tracking=True)
    return_date = fields.Datetime(string='Return Date',help='The date on which the borrower will send the book', tracking=True)
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

    # 
    @api.onchange('date_release')
    def _onchange_status(self):
        """
        If date release is in furture, changes status to "not published"
        """
        today = fields.Date.today()
        if self.date_release and self.date_release > today:
            self.status = 'not_published'
         
    @api.constrains('isbn')
    def _check_isbn(self):
        """
        If the ISBN already exists, raise UserError
        """
        for record in self:
            books = self.env['library.book'].search([('isbn', '=', record.isbn)])
            # SELECT * FROM library_book WHERE isbn = '<isbn input>';
            
            if books:
                # raise ValidationError("Existing ISBN ",record.isbn, "for these books: ",','.join(books.mapped('short_name')))
                raise ValidationError("Existing ISBN %s for these books: %s", record.isbn, ', '.join(books.mapped('short_name')))
            # , '.join(books.mapped('short_name'))
            # OR 
            # books_name = ""
            # for book in books:
            #     if not last:
            #         books_name += book.short_name + ', '
            #     else:
            #         books_name += book.short_name