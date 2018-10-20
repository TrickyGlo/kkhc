#!/usr/bin/python

# Denk er aan: DRY KISS ;-=)
# DRY : Dont Repeat Yourself
# KISS : Keep It Simple Stupid

# Dit programma leest de druppel van de koelkast klant.
# Indien de druppel onbekend is, wordt de registratie procedure gestart, en anders het hoofdmenu getoont.

# Het hoofdmenu kent 3 opties, nl. Items kopen, Saldo opvragen, en Stoppen.

# Items kopen vraag om het aantal items, en past het saldo evenredig aan voor de klant. Hierna is de transactie klaar

# Saldo opvragen toont het huidige saldo, en toont een submenu.
# Het submenu toont drie opties, nl. Saldo opwaarderen, Saldo afwaarderen en Terug naar hoofdmenu.
# Saldo opwaarderen vraagt om het bedrag wat ingelegd wordt en wijzigt het huidige saldo met de inleg
# Saldo afwaarderen vraagt om het bedrag (kan nooit meer zijn dan huidige saldo) en wijzigt het huidig saldo met de opname
# Terug naar het hoofdmenu spreekt voor zich

# Stoppen spreekt voor zich

# Alle klantgegevens worden bijgehouden in een dataframe, en opgeslagen in een .csv bestand.
# dit maakt het eenvoudig om het bestand op te slaan, mee te nemen in een backup, te openen in een spreadsheet, etc.
# Na iedere aankoop en daarmee saldo aanpassing wordt het .csv bestand opgeslagen.
# eenmaal per etmaal wordt er een backup van het bestand gemaakt op cloudstorage (dropbox, google drive, onedrive, etc)

# voor de integratie met de Bunq api: https://doc.bunq.com/

import pandas as pd
#import curses
from pathlib2 import Path
import time
import os

csv_file = "./data/koelkast_administratie.csv"

# open dataframe, Creeer administratie bestand wanneer dit niet bestaat
def open_df(adm_file):
	# adm_file - Administratie file
	if Path(adm_file).is_file():
		# vul dataframe vanuit csv bestand
		dataframe = pd.read_csv(adm_file)
		return dataframe
	else:
		# creeer dataframe sla op in csv bestand
		#adm_file_layout = {'TAG','Voornaam','Achternaam','E-mail adres','Saldo'}
		#columns = ['TAG', 'Voornaam', 'Achternaam', 'E-mail adres', 'Saldo']
		dataframe = pd.DataFrame(columns = ['TAG', 'Voornaam', 'Achternaam', 'E-mail adres', 'Saldo'])
		dataframe.to_csv(Path(adm_file), index=False)
		return dataframe

		
def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
	# prompt - Vraag waarop input wordt gegeven
	# type_  - class type van de input (float, int, str, list (=range), dict, tuple)
	# min_   - Minimale waarde van de input (bij getallen)
	# max_   - Maximale waarde van de input (bij getallen)
	# range_ - lijst van keuze mogelijkheden
	#
	# 	age = sanitised_input("Enter your age: ", int, min_=1, max_=10)
	#	answer = sanitised_input("Enter your answer: ", str.lower, range_=('a', 'b', 'c', 'd'))
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ moet minder dan of gelijk zijn aan max_.")
    while True:
        ui = raw_input(prompt)
        if type_ is not None:
            try:
                ui = type_(ui)
            except ValueError:
                print("Input type moet {0} zijn.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input moet minder dan of gelijk zijn aan {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input moet groter dan of gelijk zijn aan {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, list):	
                template = "Input moet liggen tussen {0.start} en {0.stop}."
                print(template.format(range_))
            else:
                template = "Input moet {0} zijn."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    print(template.format(" of ".join((", ".join(map(str, range_[:-1])), str(range_[-1])))))
        else:
            return ui

def klant_reg(df_org,tag,adm_file):
	#Tag_ = tag
	# vraag om persoonsgegevens
	Voornaam = sanitised_input("Wat is uw voornaam?: ", str.title)
	Achternaam = sanitised_input("Wat is uw achternaam?: ", str.title)
	Email = sanitised_input("Wat is uw e-mail adres?: ",str.lower)
	Saldo = 0.00
	
	# voeg deze info toe aan temp dataframe
	df_add = pd.DataFrame([[Voornaam, Achternaam, Email, Saldo]], index = [tag], columns = ['Voornaam', 'Achternaam', 'E-mail adres','Saldo'])
	
	# schrijf deze ook naar het csv bestand
	df_add.to_csv(Path(adm_file), mode='a', header=False, index=True)
	
	# dataframe teruggeven aan main
	frames = [df_org, df_add]
	result = pd.concat(frames)
	return result

def aankopen(df_org,tag,adm_file):
	os.system('clear')
	item_prijs = 0.5
	nr_items = sanitised_input("Hoeveel items wil je?: ", int, min_=1, max_=20)
	
	# wijzig het saldo in het dataframe met het aantal afgenomen items
	nw_saldo = df_org.at[tag, 'Saldo'] - (nr_items * item_prijs)
	df_org.at[tag, 'Saldo'] = nw_saldo
	
	# schrijf dit nieuwe saldo ook naar het csv bestand
	df_org.to_csv(Path(adm_file), mode='w', header=True, index=True, index_label='TAG')
	
	print('Dank je voor de aankoop!')
	print('Je saldo is nu: \xe2\x82\xac '.decode('utf8') + '{0:.2f}.'.format(df_org.at[tag, 'Saldo']))
	time.sleep(2)
		
	return df_org
	
def saldo(df_org,tag,adm_file):
	os.system('clear')
	#Tag_ = tag
	sld_wijz = sanitised_input("Wil je je saldo op- of afwaarderen? (o/a): ", str.lower, range_=('o','a'))
	if sld_wijz == str('o'):
		sld_opw = sanitised_input("Met welk bedrag wil je je saldo opwaarderen?: ", float)
		
		# wijzig het saldo in het dataframe
		nw_saldo = df_org.at[tag, 'Saldo'] + sld_opw
		df_org.at[tag, 'Saldo'] = nw_saldo
		
		# schrijf dit saldo ook naar het csv bestand
		df_org.to_csv(Path(adm_file), mode='w', header=True, index=True, index_label='TAG')
		
		#dataframe teruggeven aan main
		return df_org
	elif sld_wijz == str('a'):
		sld_afw = sanitised_input("Met welk bedrag wil je je saldo afwaarden?: ", float)
		if sld_afw > df_org.at[tag, 'Saldo']:
			print('meer afwaarderen dan je saldo is niet mogelijk!')
			time.sleep(2)
		else:
			# wijzig het saldo in het dataframe
			nw_saldo = df_org.at[tag, 'Saldo'] - sld_afw
			df_org.at[tag, 'Saldo'] = nw_saldo
			
			# schrijf dit saldo ook naar het csv bestand
			df_org.to_csv(Path(adm_file), mode='w', header=True, index=True, index_label='TAG')
			
			# dataframe teruggeven aan main
			return df_org
	else:
		# met onverrichte zaken naar main
		return
			
def halt():
	return		

# main program start


# Bouw dataframe met de adminstratie file
df = open_df(csv_file)
df.set_index('TAG', inplace=True)

# begin hier de loop!
while True:
	os.system('clear')
	print('Welkom bij de koelkast!\n')

	# lees tag
	tag = sanitised_input("Presenteer Tag: ", str)

	# indien de tag voorkomt in de administratie,...
	if tag in df.index:
		os.system('clear')
		print('Hallo {0}!'.format(df.at[tag, 'Voornaam']))
		print('Je saldo is: \xe2\x82\xac '.decode('utf8') + '{0:.2f}.'.format(df.at[tag, 'Saldo']))
		print('\nOpties: \n')
		print('\t1\t-\tAankoop product(en).')
		print('\t2\t-\tSaldo wijzigen.')
		print('\t0\t-\tStoppen.\n')
		m_keuze = sanitised_input("\nMaak een keuze: ", str, range_=('1','2','0'))
		if m_keuze == '1':
			aankopen(df,tag,csv_file)
		elif m_keuze == '2':
			saldo(df,tag,csv_file)
		else:
			print('bye bye')
			time.sleep(2)

	# indien de tag niet voorkomt in de administratie...
	else:
		print ("Tag is niet bekend.\n")
		reg = sanitised_input("Wilt u zich registreren? (j/n): ", str.lower, range_=('j','n'))
		if reg == str('j'):
			df = klant_reg(df,tag,csv_file)
			print('Registratie voltooid!\n')
			print(df)
		else:
			print('Jammer...\n')


