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
   
    
    def init(self, cr):
        tools.drop_table_if_exists(cr, 'analyse_balance')
        cr.execute("""
                           INSERT INTO analyse_balance VALUES (
                                 
                           select  
                                    account_account.code , 
                                    account_journal.default_debit_account_id ,
                                    account_journal.default_credit_account_id ,
                                    account_move_line.debit ,
                                    account_move_line.credit ,
                                    CASE WHEN account_move.balance>0 THEN 'Debit'
                                    ELSE 'Credit'
                                    END AS balance,
                                   account_account.type 
                                  
                            FROM 
                                public.account_move_line INNER JOIN public.account_account
                                    ON public.account_move_line.account_id = public.account_account.id
                                INNER JOIN public.account_journal
                                    ON public.account_move_line.period_id = public.account_journal.id
                                INNER JOIN public.account_move
                                    ON account_account.id = public.account_move.id
                                
                            GROUP BY account_account.code, account_account.type, account_journal.default_debit_account_id, account_journal.default_credit_account_id, account_move_line.debit, account_move_line.credit, account_move.balance 
                            ORDER BY account_account.code
                            
                            )""")

   
