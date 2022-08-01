from odoo import api, models, fields

class BookLocation(models.Model):
    _name = 'book.location'
    _description = 'Book Location'

    name = fields.Char(
        string='The name of each bookcase',
        required=True,
    )
    book_ids = fields.One2many(
        'library.book',
        'location_id',
        string='Books stored in this location',
    )
    total_available_books = fields.Integer(
        string ='The number of available books stored in this location',
    )
    total_books = fields.Integer(
        compute="_compute_total_books",
    )
                         
    def name_get(self):
        """ This method used to customize display name of the record """
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.total_available_books)
            result.append((record.id, rec_name))
        return result


    # def action_report(self):
    #     return self.env.ref('novobi_kellyhoang_library.action_report_books').report_action(self)


    @api.depends('book_ids')
    def _compute_total_books(self):
        for record in self:
            self.total_books = len(record.book_ids)