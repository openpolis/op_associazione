# -*- coding: utf-8 -*-
#from op_associazione.tools import op_realtime
from django.utils.html import strip_tags
import urllib2

def parse(kwargs):
    id = kwargs.get('id')
    align = kwargs.get('align', 'left')
    css_styles = """ 
        <style type=\"text/css\">
        div#op_realtime { font-family:Arial; width:270px; background-color: #FFF; text-align:left; margin: 15px; float:%s; }
        div#op_realtime h1 { color:#333; font-family: Georgia; font-size: 24px; line-height: 30px; margin:0; }
        div#op_realtime h2 { font-size: 14px; line-height: 16px; color:#333; margin:0; }
        div#op_realtime table { width:100%% ; margin-top: 5px; }
        div#op_realtime tr { border-bottom:1px solid #FFF; background-color: #fbec6d; }
        div#op_realtime tr > * { padding: 0 5px; }
        div#op_realtime tr th { font-size:12px; background-color: #e8da65; }
        div#op_realtime tr td { font-weight:bold; line-height: 24px; font-size: 18px; text-align:right; }
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
        value = strip_tags(f.read()).strip() # Remove xml tags and spaces
        table_rows += u'<tr title="%s" class="tips"><th>%s</th><td>%s</td></tr>' % (stat[2], stat[0], splitthousands(value))
    
    html_table = u"""
        <div id="op_realtime">
            <h1>Openpolis in tempo reale</h2>
            <h2>Le attivit&agrave; nel nostro network mentre consulti questa pagina </h2>
            <table>
                <tbody>
                %s
                </tbody>
            </table>
        </div>
    """ % table_rows
    return css_styles + html_table
    
    
def splitthousands(s, sep='.'):  
    if len(s) <= 3: return s  
    return splitthousands(s[:-3], sep) + sep + s[-3:]
    