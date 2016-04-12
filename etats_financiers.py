from openerp.osv import osv, fields
from openerp.addons.account import account
class analyse_balance(osv.Model):
    _name = 'analyse.balance'
    _columns = {
        'compte_financier':fields.integer('compte financier', size=20, required=True),
        'solde_balance':fields.float('Solde valance', digits=(9,4), required=True),
        'exercice': fields.date('Exercice',),
        'type': fields.char('Type', size=32, required=True, translate=True),
        'type_amort_prov':fields.char('Amort/prov',size=32,required=True, translate=True),
        'signe':fields.boulean('Signe'),
        'solde_corrige':fields.float('Solde corrige', digits=(9,4),required=True),
        'line_id':fields.many2one('account.move.line','Journal Line'),
        'period_id':fields.many2one('account.period','Periode'),
        'type_id':fields.many2one('account.account.type','Type'),
        'fiscalyear_id':fields.many2one('account.fiscalyear','Annee Fiscal'),
        
    }
    _defaults = {
        'signe': True, # le compte est tjrs en addition de son groupe  
    }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'analyse_banace')
cr.execute("""
                           CREATE OR REPLACE VIEW analyse_balance AS (
                                 
                           SELECT 
                                    account_account.code AS cmpt_financ, 
                                    account_account.name AS name,
                                    sum(account_move_line.debit) - sum(account_move_line.credit)as solde_balance,
                                    account_account.type AS type,
                                    account_account_type.name AS type_amort_prov,
                                    account_fiscalyear.name AS exerc,
                                   abs( sum(account_move_line.debit) - sum(account_move_line.credit))as solde_corrige
                                  
                            FROM 
                                public.account_move_line INNER JOIN public.account_account
                                    ON public.account_move_line.account_id = public.account_account.id
                                INNER JOIN public.account_period
                                    ON public.account_move_line.period_id = public.account_period.id
                                INNER JOIN public.account_account_type
                                    ON account_account.user_type = public.account_account_type.id
                                INNER JOIN public.account_fiscalyear
                                    ON account_period.fiscalyear_id = account_fiscalyear.id
                            GROUP BY account_account.name,account_account.code, account_account.type, account_account_type.name, account_fiscalyear.name
                            ORDER BY account_account.code
                            )""")
   