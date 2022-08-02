from re import S
from odoo import api, models, fields
from datetime import date
from odoo.exceptions import ValidationError
from odoo.http import request

class LibraryBook(models.Model):
    _name = 'library.book'
    _inherit = ['library.book', 'mail.thread']
    
    isbn = fields.Char(
        string='International Standard Book Number',
        required=True,
    )
    description = fields.Text(
        string='Brief introduction',
    )
    status = fields.Selection(
        string='Type',
        selection=[('not_published','Not Published'),('available','Available'),('borrowed','Borrowed'),('lost','Lost')],
        default='available',
    )
    current_borrower_id = fields.Many2one(
        'res.partner',
        string='Borrower',
        help='The current Borrower',
        readonly=True,
        tracking=True,
    )
    return_date = fields.Datetime(
        string='Return Date',
        help='The date on which the borrower will send the book',
        tracking=True,
    )
    location_id = fields.Many2one(
        'book.location',
        string='Location',
        help='The location (shelf) where we store the book',
    )
    book_url = fields.Char(
        string="Book's URL",
    )

    def action_url(self):
        self.book_url = 'https://www.odoo.com/documentation/15.0/developer/reference/backend/orm.html'

        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': self.book_url,
        }
        
    def lease_button(self):
        context = dict(self.env.context)
        context['default_lease_book_id'] = self.id
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'lease.book.wizard',    # name of respective model,
            'target': 'new',
            'context': context,
        }


    def lost_button(self):
        """
        Mark as Lost action
        """
        self.ensure_one()
        if self.status == 'lost':
            raise ValidationError('Already lost!')
        self.status = 'lost'
        self.current_borrower_id = False
        self.return_date = False
            
     
    def available_button(self):
        """
        Mark as Available action
        """
        self.ensure_one()
        if self.status == 'available':
            raise ValidationError('Already available!')
        self.status = 'available'   
        self.current_borrower_id = False # remove usre-defined value in fields
        self.return_date = False
         
         
        
    @api.constrains('isbn')
    def _check_isbn(self):
        """
        If the ISBN already exists, raise UserError
        """
        for record in self:
            books = self.env['library.book'].search([('isbn', '=', record.isbn)]) # SELECT * FROM library_book WHERE isbn = '<isbn input>';
            
            if len(books) > 1:
                raise ValidationError("Existing ISBN %s for these books: %s" % (record.isbn, ', '.join(books.mapped('short_name'))))

            # , '.join(books.mapped('short_name'))
            # OR 
            # books_name = ""
            # for book in books:
            #     if not last:
            #         books_name += book.short_name + ', '
            #     else:
            #         books_name += book.short_name
      
            
    @api.onchange('date_release')
    def _onchange_status(self):
        """
        If date release is in furture, changes status to "not published"
        """
        today = fields.Date.today()
        if self.date_release and self.date_release > today:
            self.status = 'not_published'
         
    def send_late_return_reminder(self):
        print("Executing CRON")