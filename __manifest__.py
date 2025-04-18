{
    'name': 'Extra Discount',
    'version': '1.0',
    'summary': 'Adding second discount and third discount fields',
    'category': 'Sales',
    'author': 'François Dewaste & Stephane Roux',
    'depends': ['sale_management', 'account'],
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/report_templates.xml'
    ],
    'installable': True,
    'application': False,
}
