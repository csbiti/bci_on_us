import datetime
today = datetime.datetime.now().strftime("%d/%m/%y")

sql_request_bci = (  # Requete pour selectionner les AC en attente pour la SG TODO change to today
    """
        select sum(m.ch_mt_brut_centimes)  from tbob_retrait_mvt m
        left join tbob_gab g on g.id = m.id_gab
        left join tbob_porteur p on p.id = m.id_porteur
        where m.dh_compens between to_date ('05/08/20 00:00:00', 'DD/MM/YY HH24:MI:SS') and to_date ('""" + today + """ 23:59:59', 'DD/MM/YY HH24:MI:SS')
        and g.id_banque = '11'
        and p.in_jade <> '1'
        and p.id_banque = '11' """)

sql_request_hors_bci = (  # Requete pour selectionner les AC en attente pour la SG TODO change to today
    """
        select sum(m.ch_mt_brut_centimes)  from tbob_retrait_mvt m
        left join tbob_gab g on g.id = m.id_gab
        left join tbob_porteur p on p.id = m.id_porteur
        where m.dh_compens between to_date ('05/08/20 00:00:00', 'DD/MM/YY HH24:MI:SS') and to_date ('""" + today + """ 23:59:59', 'DD/MM/YY HH24:MI:SS')
        and g.id_banque = '11'
        and p.in_jade <> '1'
        and p.id_banque = '11' """)

sql_request_etranger = (  # Requete pour selectionner les AC en attente pour la SG TODO change to today
    """
    select sum(m.ch_mt_brut_centimes)  from tbob_retrait_mvt m
    left join tbob_gab g on g.id = m.id_gab
    left join tbob_porteur p on p.id = m.id_porteur
    where m.dh_compens between to_date ('05/08/20 00:00:00', 'DD/MM/YY HH24:MI:SS') and to_date ('""" + today + """ 23:59:59', 'DD/MM/YY HH24:MI:SS')
    and g.id_banque = '11'
    and p.in_jade <> '1'
    and p.id_banque = '11' """)
