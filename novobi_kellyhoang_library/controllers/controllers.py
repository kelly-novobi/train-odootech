from odoo.http import request

from odoo import http


class BookController(http.Controller):
    
    """
    Retrieve an existing book's details → Returns ID, Name and ISBN upon successfully found
    """ 
    @http.route('/novobi_kelly_library/books', methods=['GET'], type='json', auth='none')
    def list_books(self, **kw):
        books = request.env['library.book'].sudo().search([])
        return books.read(['id', 'name', 'isbn'])


    # @http.route('/novobi_kelly_library/books/<int:book_id>', methods=['GET'], type='json', auth='none')
    # def get_book_id(self, book_id, **kw):
    #     book = request.env['library.book'].sudo().browse([book_id])
    #     return book.read(['id', 'name', 'isbn'])

   
    # @http.route('/novobi_kelly_library/books', methods=['POST'], type='json', auth='none')
    # def create_book(self, **kw):
    #     request.env['library.book'].sudo().create(request.jsonrequest)
    #     return True

    """ 
    Update an existing book → Returns the updated book's ID upon successfully updated
    """ 
    @http.route('/novobi_kelly_library/books/<int:book_id>', methods=['PUT'], type='json', auth='none')
    def update_book(self, book_id, **kw):
        book = request.env['library.book'].sudo().browse([book_id])
        book.write(request.jsonrequest)
        return True

    """ 
    Delete an existing book → Returns the deleted book's ID upon successfully deleted
    """ 
    @http.route('/novobi_kelly_library/books/<int:book_id>', methods=['DELETE'], type='json', auth='none')
    def delete_book(self, book_id, **kw):
        book = request.env['library.book'].sudo().browse([book_id])
        book.unlink()
        return True