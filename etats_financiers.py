from openerp.osv import osv, fields
from openerp.addons.account import account
class etats_financiers(osv.Model):
    _name = 'analyse.balance'
    _columns = {
        'account':fields.integer('Account', size=20, required=True),
        'solde_init_d':fields.float('Solde initial debit', digits=(9,4), required=True),
        'solde_init_c':fields.float('solde initial credit', digits=(9,4), required=True),
        'mouv_debit':fields.float('mouvement debit', digits=(9,4), required=True),
        'mouv_credit':fields.float('mouvement credit', digits=(9,4), required=True),
        'solde_Balance':fields.char('Solde Balance', size=128, required=True),
        'type':fields.char('type', size=128, required=True),
        
    }
   
    
   
