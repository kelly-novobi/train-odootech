from odoo.tests.common import TransactionCase, tagged

@tagged('-standard', 'booklocation')
class BookLocationTest(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(BookLocationTest, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.booklocation = cls.env['book_location'].create({'name': 'Book Location'})
        cls.authorname = cls.env['res.partner'].create({'name': 'Author Name'})
    
    def test_total_books(self):
        """Test that the total_books is increased by one, when creating a new book."""
        
        new_book = self.env['book_location'].create({
            'name': 'New Book',
            'short_name': 'nbook',
            'isbn': 'nb',
            'author_ids': 'authorname',
            'date_release': '1/1/2001',
            'location': 'self.booklocation.id'
        })
        
        self._compute_total_books()
        
        self.assertEqual(self.booklocation.total_books, 1)