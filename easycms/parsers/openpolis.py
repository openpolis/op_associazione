# -*- coding: utf-8 -*-
#from op_associazione.tools import op_realtime

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
    
    stats = {
        'Incarichi censiti' : 358968,
        'Politici monitorati' : 224730,
        'Emendamenti' : 148578,
        'Dichiarazioni' : 16659,
        "Votazioni d'aula" : 14723,
        'Utenti registrati' : 18181
    }
    table_rows = ''
    
    for field, nb in stats.iteritems():
        table_rows += u'<tr title="titolo" class="tips"><th>%s</th><td>%s</td></tr>' % (field, nb)
    
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