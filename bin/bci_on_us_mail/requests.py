import datetime
today = datetime.datetime.now().strftime("%d/%m/%y")

sql_request_bci = (  # Requete pour selectionner les AC en attente pour la SG TODO change to today
    """
    select sum(m.ch_mt_brut_centimes)  from tbob_retrait_mvt m
    left join tbob_gab g on g.id = m.id_gab
    left join tbob_porteur p on p.id = m.id_porteur
    where m.dh_compens between to_date ('""" + today + """', 'DD/MM/YY HH24:MI:SS') and to_date ('""" + today + """ 23:59:59', 'DD/MM/YY HH24:MI:SS')
    and g.id_banque = '11'
    and p.in_jade <> '1'
    and p.id_banque = '11' """)

sql_request_hors_bci = (  # Requete pour selectionner les AC en attente pour la SG TODO change to today
    """
    select sum(nb_montant) from tbob_stat_categorie_cpt
    where da_stat = '""" + today + """'
    and id_banque = '11'
    and id_categorie = '1'
    and ch_critere1 != 'JADE'
    and ch_critere2 not in ('ETRANGER', 'INTERNE')""")

sql_request_etranger = (  # Requete pour selectionner les AC en attente pour la SG TODO change to today
    """
    select sum(nb_montant) from tbob_stat_categorie_cpt
    where da_stat = '""" + today + """'
    and id_banque = '11'
    and ch_critere1 != 'JADE'
    and ch_critere2 = 'ETRANGER' """)
