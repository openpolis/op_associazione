# -*- coding: utf-8 -*-
#from op_associazione.tools import op_realtime
from django.utils.html import strip_tags
import urllib2

def parse(kwargs):
    id = kwargs.get('id')
    align = kwargs.get('align', 'left')
    css_styles = """ 
        <style type=\"text/css\">
        #op_realtime { min-width:300px; background-color: #FFF; text-align:left; margin: 15px; float:%s; }
        #op_realtime caption { text-align:left; font-size:0.8em; }
        #op_realtime caption strong { font-size:1.3em; }
        #op_realtime tr { border-bottom:1px solid #FFF; background-color: #fbec6d; }
        #op_realtime tr > * { padding: 10px 5px; }
        #op_realtime tr th { background-color: #e8da65; }
        #op_realtime tr td { text-align:right; }
        </style>
    """ % align
    

    op_url = 'http://openpolis.it/'
    opp_url = 'http://parlamento.openpolis.it/'
    stats = (
            ('Incarichi censiti', op_url + 'api/chargeNumber/', 'Incarichi censiti'),
            ('Politici monitorati', op_url + 'api/politicianNumber/', 'Politici monitorati'),
            ('Emendamenti', opp_url + 'api/getNumeroEmendamenti/', 'Emendamenti'),
            ('Dichiarazioni', op_url + 'api/declarationNumber/', 'Dichiarazioni'),
            ('Votazioni d\'aula', opp_url + 'api/getNumeroVotazioni/', 'Votazioni d\'aula'),
            ('Utenti registrati', op_url + 'api/userNumber/', 'Utenti registrati'),
        )

    table_rows = ''

    for stat in stats:
        f = urllib2.urlopen(stat[1])
        value = strip_tags(f.read())
        table_rows += u'<tr title="%s" class="tips"><th>%s</th><td>%s</td></tr>' % (stat[2], stat[0], value)
    
    html_table = u"""
        <table id="op_realtime">
            <caption>
                <strong>Openpolis in tempo reale</strong><br />
                Le attivit&agrave; nel nostro network mentre consulti questa pagina 
            </caption>
            <tbody>
            %s
            </tbody>
        </table>
    """ % table_rows
    return css_styles + html_table
    