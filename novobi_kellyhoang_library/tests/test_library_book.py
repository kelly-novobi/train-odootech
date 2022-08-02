from odoo.tests.common import TransactionCase, tagged

@tagged('-standard', 'book')
class LibraryBookTest(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(LibraryBookTest, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.book = cls.env['library_book'].create({'name': 'Book'})
        cls.authorname = cls.env['res.partner'].create({'name': 'Author Name'})
    
    def test_mark_as_lost(self):
        """When "Mark as Lost", should change Status to Lost, and remove the Current Borrower & Return Date if any."""
        
        new_book = self.env['library_book'].create({
            'name': 'New Book',
            'short_name': 'nbook',
            'isbn': 'nb',
            'author_ids': 'authorname',
            'date_release': '1/1/2001',
            'location': 'self.location_id'
        })
        
        self.lost_button()
        
        self.assertIs(self.book.new_book.status, 'Lost')
        self.assertIsNone(self.book.new_book.current_borrower_id)
        self.assertIsNone(self.book.new_book.return_date)
        
        