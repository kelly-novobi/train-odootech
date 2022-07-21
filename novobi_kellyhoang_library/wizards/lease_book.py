from odoo import api, models, fields

class LeaseBook(models.TransientModel):
    _name = 'lease.book.wizard'
    _description = 'Lease Book'

    lease_book_id = fields.Many2one('library.book', string='Leased Book', required=True, invisible=True)
    borrower_id = fields.Many2one('res.partner', string='Borrower', required=True)
    return_date = fields.Datetime(string='Return Date', required=True)
    
    # update the current borrower of the book
    # update the status of the book: available -> borrowed
    # add a log to the chatter
    def confirm_lease_action(self):
        for wiz in self:
            wiz.lease_book_id.ensure_one()
            wiz.lease_book_id.current_borrower_id = wiz.borrower_id
            wiz.lease_book_id.status = 'borrowed'
            



