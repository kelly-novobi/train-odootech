# Copyright © 2022 Novobi, LLC
# See LICENSE file for full copyright and licensing details.

{
    "name": "Novobi: Library Book Extension",
    "summary": "Novobi: Library Book Extension",
    "version": "15.0.1",
    "category": "Tools",
    "website": "https://novobi.com",
    "author": "Novobi, LLC",
    "license": "OPL-1",
    "depends": [
        "novobi_library_book"
    ],
    "excludes": [],
    "data": [
        # ============================== DATA =================================

        # ============================== VIEWS ================================
        'wizards/lease_book_wizard.xml',
        'views/library_book_views.xml',
        'views/book_location_views.xml',
        
        # ============================== SECURITY ================================
        'security/security_rules.xml',
        'security/library_book_groups.xml',
        'security/ir.model.access.csv',
        # ============================== REPORT =============================
        
        # ============================== WIZARDS =============================  
    ],
    "installable": True,
}
