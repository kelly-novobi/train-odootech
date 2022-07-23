from odoo import api, models, fields

class BookLocation(models.Model):
    _name = 'book.location'
    _description = 'Book Location'

    name = fields.Char(string='The name of each bookcase', required=True)
    book_ids = fields.One2many('library.book','location_id',string='Books stored in this location')
    total_available_books = fields.Integer('The number of available books stored in this location')
    total_books = fields.Integer(compute="_compute_total_books")
                         
    def name_get(self):
        """ This method used to customize display name of the record """
        result = []
        for record in self:
            rec_name = "%s (%s)" % (record.name, record.total_available_books)
            result.append((record.id, rec_name))
        return result

    @api.depends('book_ids')
    def _compute_total_books(self):
        for record in self:
            record.total_books = len(record.book_ids)