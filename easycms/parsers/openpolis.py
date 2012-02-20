# -*- coding: utf-8 -*-
#from op_associazione.tools import op_realtime
from django.utils.html import strip_tags
import urllib2

def parse(kwargs):
    id = kwargs.get('id')
    align = kwargs.get('align', 'left')
    css_styles = """ 
        <style type=\"text/css\">
        aside#op_realtime { font-family:'Helvetica Neue', Helvetica, Arial, sans-serif; width:270px; background-color: #FFF; text-align:left; margin: 15px; float:%s; }
        aside#op_realtime caption { text-align: left; padding: 0.5em; padding-top: 0 }
        aside#op_realtime h1 { color:#333; font-size: 22px; margin:0; }
        aside#op_realtime h2 { font-size: 14px; line-height: 16px; color:#333; margin:0; letter-spacing: 0; }
        aside#op_realtime table { width:94%% ; margin-top: 5px; }
        aside#op_realtime tr { border-bottom:1px solid #FFF; background-color: #fbec6d; }
        aside#op_realtime th, aside#op_realtime td { padding: 10px; }
        aside#op_realtime tr th { font-size:12px; background-color: #e8da65; text-transform: uppercase }
        aside#op_realtime tr td { font-weight:bold; line-height: 24px; font-size: 18px; text-align:right; }
        </style>
    """ % align
    

    op_url = 'http://politici.openpolis.it/'
    opp_url = 'http://parlamento.openpolis.it/'
    stats = (
            ('Incarichi censiti', op_url + 'api/chargeNumber/', 
             '&Egrave; il numero delle cariche istituzionali presenti e passate che sono memorizzate nei nostri database.'),
            ('Politici monitorati', op_url + 'api/politicianNumber/', 
             '&Egrave; il numero dei politici censiti, dal piccolo comune fino al parlamento europeo.'),
            ('Emendamenti', opp_url + 'api/getNumeroEmendamenti/', 
             '&Egrave; il numero di emendamenti presentati in Parlamento nella XVI Legislatura. Di ognuno forniamo tutti i dettagli.'),
            ('Dichiarazioni', op_url + 'api/declarationNumber/', 
             '&Egrave; il numero delle dichiarazioni dei politici pubblicate dai nostri utenti. Tutte le dichiarazioni hanno il link alla fonte, per avere memoria collettiva delle cose dette e promesse.'),
            ('Votazioni d\'aula', opp_url + 'api/getNumeroVotazioni/', 
             '&Egrave; il numero di votazioni elettroniche d\'aula svolte in Parlamento della XVI Legislatura. Di ognuna forniamo tutti i dettagli.'),
            ('Utenti registrati', op_url + 'api/userNumber/', 
             'Sono i numeri della nostra community. Senza, openpolis non esisterebbe.'),
        )

    table_rows = ''

    for stat in stats:
        f = urllib2.urlopen(stat[1])
        value = strip_tags(f.read()).strip() # Remove xml tags and spaces
        table_rows += u'<tr title="%s" class="popoverable" rel="popover" data-content="%s"><th>%s</th><td>%s</td></tr>' % (stat[0], stat[2], stat[0], splitthousands(value))
    
    html_table = u"""
        <aside id="op_realtime">
            <table>
                <caption>
                    <h1>Openpolis in tempo reale</h2>
                    <h2>Le attivit&agrave; nel nostro network mentre consulti questa pagina </h2>
                </caption>
                <tbody>
                %s
                </tbody>
            </table>
        </aside>
    """ % table_rows
    return css_styles + html_table
    
    
def splitthousands(s, sep='.'):  
    if len(s) <= 3: return s  
    return splitthousands(s[:-3], sep) + sep + s[-3:]
    