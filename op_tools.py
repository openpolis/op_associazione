# -*- coding: utf-8 -*-

def op_aboutus():
	#http://news.google.it/news?q=openpolis+-site:openpolis.it&hl=it&prmd=imvns&tbas=0&bav=on.2,or.r_gc.r_pw.r_cp.,cf.osb&biw=1135&bih=713&um=1&ie=UTF-8&output=rss
	

def op_realtime(id, align):
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
		table_rows += u'<tr title="titolo" class="tips"><th>%s</th><td>%s</td></tr>' % (field, format(nb, ',d'))
	
	html_table = u"""
		<table id="op_realtime">
			<caption>
				<strong>Openpolis in tempo reale</strong><br />
				Le attivita nel nostro network mentre consulti questa pagina 
			</caption>
			<tbody>
			%s
			</tbody>
		</table>
	""" % table_rows
	return css_styles + html_table