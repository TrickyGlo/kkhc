#!/usr/bin/python
#
# Koelkast 2.0
#
# Dit programma leest de druppel van de koelkast klant in een grafische weergave.
# Hiervoor onderschiedt het programma 5 "screens"
# 
# screen1:
# 	Wacht tot er een tag wordt aangeboden en bepaal of de tag bekend is (screen 2) of niet (screen 3)
#
# screen2:
# 	verwelkom de klant en toon diens saldo. Presenteer eveneens het hoofdmenu. 
# 	Het hoofdmenu kent 3 opties, nl. Items kopen, Saldo wijzigen, en Stoppen.
#
# screen3:
# 	Indien de druppel onbekend is, wordt de registratie procedure gestart. Na de registratie wordt 
# 	gevraagd om het saldo te wijzigin (screen 5)
#
# screen4:
# 	Items kopen. Vraag om het aantal items, en past het saldo evenredig aan voor de klant. Hierna is de transactie klaar (screen 1)
#
# screen5:
# 	wijzig het saldo
# 	Het submenu toont twee opties, nl. Saldo opwaarderen en Saldo afwaarderen.
# 	Saldo opwaarderen vraagt om het bedrag wat ingelegd wordt en wijzigt het huidige saldo met de inleg
# 	Saldo afwaarderen vraagt om het bedrag (kan nooit meer zijn dan huidige saldo) en wijzigt het huidig saldo met de opname
# 	Na het aanpassen van het saldo is de transactie klaar en kunnen er aankopen gedaan worden (screen 2)
#
# Alle klantgegevens worden bijgehouden in een dataframe, en opgeslagen in een .csv bestand.
# dit maakt het eenvoudig om het bestand op te slaan, mee te nemen in een backup, te openen in een spreadsheet, etc.
# Na iedere aankoop en daarmee saldo aanpassing wordt het .csv bestand opgeslagen.
# eenmaal per etmaal wordt er een backup van het bestand gemaakt op cloudstorage (dropbox, google drive, onedrive, etc)
#
# voor de integratie met de Bunq api: https://doc.bunq.com/
# voor deze inegratie zal ook een database backend gerealiseerd moeten worden om de bank transacties bij te houden
#
#import Tkinter as tk
from Tkinter import *		# GUI Library
from pathlib2 import Path	# Filesystem access
import pandas as pd			# DataFrame Library
import time					# Time functions (sleep)
import os					# OS Calls

# Tk independent vars
csv_file = "./koelkast_administratie.csv"
tagprovided = False
klanttag = ""
null = ""
show_scrn1 = True
show_scrn2 = False
show_scrn3 = False
show_scrn4 = False
show_scrn5 = False
scrn4_keybtn = []
nr_items = ""


##### Funties:

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

def items_aankopen_adm(tag, df, nr_items, adm_file):
	item_prijs = 0.5
	uitgave = 0

	# wijzig het saldo in het dataframe met het aantal afgenomen items
	uitgave = int(nr_items) * item_prijs
	nw_saldo = df.at[tag, 'Saldo'] - uitgave
	df.at[tag, 'Saldo'] = nw_saldo
	
	# schrijf dit nieuwe saldo ook naar het csv bestand
	df.to_csv(Path(adm_file), mode='w', header=True, index=True, index_label='TAG')
	
	print(df)
		
	return

def items_aankopen():
	toggle_screen2(null, null)
	toggle_screen4()

# keypad function
def keypad_key(value):
	# inform function to use external/global variable
	global nr_items
	global klanttag
	
	if value == 'Stop':
		print("Stop")
		# clear `nr_items`
		nr_items = ""
		# clear `entry`
		scrn4_txtentry1.delete('0', 'end')
		toggle_screen4()
		toggle_screen1()
		klanttag = ""
		return None
		
	elif value == 'Corr.':
		# remove last number from `nr_items`
		nr_items = nr_items[:-1]
		# remove all from `entry` and put new `nr_items`
		scrn4_txtentry1.delete('0', 'end')
		scrn4_txtentry1.insert('end', nr_items)
		
	elif value == 'Enter':
		# check nr_items
		if nr_items > "0":
			print("Items OK")
			# verwerk administratie
			items_aankopen_adm(klanttag, df, nr_items, csv_file)
			# laat nieuw saldo zien
			# toggle screen4
			scrn4_txtentry1.delete('0', 'end')
			nr_items = ""
			toggle_screen4()
			# toogle screen1
			toggle_screen1()
			# verlaat deze functie
			return None
		else:
			print("Items ERROR!", nr_items)
			# clear `nr_items`
			nr_items = ""
			# clear `entry`
			scrn4_txtentry1.delete('0', 'end')
	
	else:
		# add number to nr+items
		nr_items += value
		# add number to `entry`
		scrn4_txtentry1.insert('end', value)
	
	print("Current:", nr_items)

# schoon scherm
def toggle_screen1():							# presenteer tag
	# verwijder scherm 
	global show_scrn1
	global show_scrn2
	if show_scrn1:
		scrn1_imagelbl.grid_remove()
		scrn1_textlbl.grid_remove()
		scrn1_tagentry.grid_remove()
		scrn1_tagbtn.grid_remove()
	else:
		scrn1_imagelbl.grid()
		scrn1_textlbl.grid()
		scrn1_tagentry.grid()
		scrn1_tagbtn.grid()
	show_scrn1 = not show_scrn1
	show_scrn2 = not show_scrn2
	
def toggle_screen2(klantnaam, klantsaldo):		# hoofdmenu
	global show_scrn2
	
	if show_scrn2:
		scrn2_select1.grid(row=0, column=0, sticky=E)
		scrn2_select2.grid(row=0, column=0, sticky=W)
		scrn2_textlbl1.config(text = klantnaam)
		scrn2_textlbl1.grid(row=0, column=0,sticky=E)
		scrn2_textlbl2.config(text = "Saldo: "+klantsaldo)
		scrn2_textlbl2.grid(row=1, column=0, sticky=E)
		scrn2_textlbl3.grid(row=0, column=0, sticky=N)
	else:
		scrn2_select1.grid_remove()
		scrn2_select2.grid_remove()
		scrn2_textlbl1.config(text = "")
		scrn2_textlbl1.grid_remove()
		scrn2_textlbl2.config(text = "")
		scrn2_textlbl2.grid_remove()
		scrn2_textlbl3.grid_remove()
	show_scrn2 = not show_scrn2
		
def toggle_screen3():							# registreer nieuwe klant
	global show_scrn3

	show_scrn3 = not show_scrn3
	if show_scrn3:
		scrn3_textlbl1.grid(row=0, column=0, sticky=E)
		scrn3_textlbl2.grid(row=1, column=0, sticky=E)
		scrn3_textlbl3.grid(row=2, column=0, sticky=E)
		scrn3_textlbl4.grid(row=3, column=0, sticky=E)
		scrn3_textlbl5.grid(row=4, column=0, sticky=E)
		scrn3_txtentry1.grid(row=2, column=1, sticky=E)
		scrn3_txtentry2.grid(row=3, column=1, sticky=E)
		scrn3_txtentry3.grid(row=4, column=1, sticky=E)
	else:
		scrn3_textlbl1.grid_remove()
		scrn3_textlbl2.grid_remove()
		scrn3_textlbl3.grid_remove()
		scrn3_textlbl4.grid_remove()
		scrn3_textlbl5.grid_remove()
		scrn3_txtentry1.grid_remove()
		scrn3_txtentry2.grid_remove()
		scrn3_txtentry3.grid_remove()
	
def toggle_screen4():							# registreer aantal af te nemen items
	global show_scrn4
	global scrn4_keybtn
	
	show_scrn4 = not show_scrn4
	
	if show_scrn4:
		scrn4_textlbl1.grid(row=0, column=0, sticky=E)
		scrn4_txtentry1.grid(row=0, column=1, sticky=E)
		i = 0
		# create buttons using `keys_keypad`
		for y, row in enumerate(keys_keypad, 1):
			for x, key in enumerate(row):
				# `lambda` inside `for` has to use `val=key:code(val)` 
				# instead of direct `code(key)`
				#scrn4_keybtn[i] = Button(BottomFrame, text=key, width=8, command=lambda val=key:keypad_key(val))
				scrn4_keybtn.append(Button(BottomFrame, text=key, width=8, command=lambda val=key:keypad_key(val)))
				scrn4_keybtn[i].grid(row=y, column=x) # b.grid(row=y, column=x, ipadx=10, ipady=10)
				i += 1
		
	else:
		scrn4_textlbl1.grid_remove()
		scrn4_txtentry1.grid_remove()
		i = 0
		# create buttons using `keys_keypad`
		for y, row in enumerate(keys_keypad, 1):
			for x, key in enumerate(row):
				scrn4_keybtn[i].grid_remove()
				i += 1
		

# read tag and confirm from csv
def bevestig_tag(tag):
	global klanttag
	global klantlabel1
	global klantlabel2
	global tagprovided
	
	tagprovided=True
	klanttag = tag
	scrn1_tagentry.delete(0, END)
	toggle_screen1()
	#output.delete(0.0, END)
	if klanttag in df.index.values:
		klantnaam = "Hallo {0}!".format(df.at[tag, 'Voornaam'])
		klantsaldo = "Je saldo is: {0:.2f} euro.".format(df.at[tag, 'Saldo'])
		klant = klantnaam + klantsaldo
		toggle_screen2(klantnaam, klantsaldo)
	else:
		toggle_screen3()
	#klantlabel1.config(text = "Klant: "+klantnaam)
	#klantlabel2.config(text = "Saldo: "+klantsaldo)
	#print (klant)
	#print (tagprovided)
	#print ("Tag is %s" % klanttag)
	#output.insert(END, klant)
	

	
	
def saldo_wijzigen():
	print("saldo wijzigen")
	
	
		

	
	
	
	
##### Main:

# Bouw dataframe met de adminstratie file
df = open_df(csv_file)
df.set_index('TAG', inplace=True)

# Bouw en arrangeer het window
window = Tk()
window.title("De Koelkast App")
window.configure(background="black")

# Tk dependent vars
tagimage1 = PhotoImage(file="RFID-tag-zwart.png")

# Frame layout
BottomFrame = Frame(window, bg="purple", bd=2, height=300)		# bg kleuren zijn gekozen om de frame layout te verduidelijken
BottomFrame.pack(side=BOTTOM, fill=X)				# tijdens het ontwikkel proces. 
TopLeftFrame = Frame(window, bg="blue", bd=2, width=100)		# deze kleuren zullen uit eindelijk aangepast worden in zwart
TopLeftFrame.pack(side=LEFT, fill=Y)
TopRightFrame = Frame(window, bg="blue", bd=2, width=100)
TopRightFrame.pack(side=RIGHT, fill=Y)
TopCenterFrame = Frame(window, bg="black", bd=2)
TopCenterFrame.pack(side=TOP, fill=X)
CenterCenterFrame = Frame(window, bg="red", bd=2)
CenterCenterFrame.pack(fill=X)

# Bouw en arrangeer screen layouts
# screen1() Presenteer Tag
scrn1_imagelbl = Label (CenterCenterFrame, image=tagimage1, bg="black")
scrn1_imagelbl.grid(row=0, column=0, sticky=N)
scrn1_textlbl = Label (TopCenterFrame, text="Presenteer je TAG:", bg="black", fg="white", font="none 12 bold")
scrn1_textlbl.grid(row=1, column=0)
scrn1_tagentry = Entry(CenterCenterFrame, width=20, relief=FLAT, bg="black", fg="white")
scrn1_tagentry.focus()
scrn1_tagentry.bind('<Return>', (lambda event: bevestig_tag(scrn1_tagentry.get())))
scrn1_tagentry.grid(row=0, column=0, sticky=S)
scrn1_tagbtn = Button (CenterCenterFrame, text="Bevestig TAG", width=12, command=(lambda: bevestig_tag(scrn1_tagentry.get())))
scrn1_tagbtn.grid(row=1, column=0, sticky=S)

# screen2() Hoofdmenu
scrn2_select1 = Button (TopLeftFrame, text="Items aankopen", width=12, command=items_aankopen)
scrn2_select2 = Button (TopRightFrame, text="Saldo wijzigen", width=12, command=saldo_wijzigen)
scrn2_textlbl1 = Label(BottomFrame, text="Klant: ", bg="purple", fg="white", font="none 12 bold")
scrn2_textlbl2 = Label(BottomFrame, text="Saldo: ", bg="purple", fg="white", font="none 12 bold")
scrn2_textlbl3 = Label(TopCenterFrame, text="Maak een keuze: ", bg="black", fg="white", font="none 12 bold")

# screen3() Tag onbekend, start registratie
scrn3_textlbl1 = Label(TopCenterFrame, text="Oeps, u bent niet bekend in het systeem", bg="red", fg="white", font="none 12 bold")
scrn3_textlbl2 = Label(CenterCenterFrame, text="Registreer u zelf...", bg="red", fg="white", font="none 12 bold")
scrn3_textlbl3 = Label(CenterCenterFrame, text="Voornaam: ", bg="red", fg="white", font="none 12 bold")
scrn3_textlbl4 = Label(CenterCenterFrame, text="Achternaam: ", bg="red", fg="white", font="none 12 bold")
scrn3_textlbl5 = Label(CenterCenterFrame, text="E-mail adres: ", bg="red", fg="white", font="none 12 bold")
scrn3_txtentry1 = Entry(CenterCenterFrame, width=40, relief=SUNKEN, bg="white", fg="black")
scrn3_txtentry2 = Entry(CenterCenterFrame, width=40, relief=SUNKEN, bg="white", fg="black")
scrn3_txtentry3 = Entry(CenterCenterFrame, width=40, relief=SUNKEN, bg="white", fg="black")

# screen4() Items kopen
scrn4_textlbl1 = Label(CenterCenterFrame, text="Hoeveel items neem je?: ", bg="red", fg="white", font="none 12 bold")
scrn4_txtentry1 = Entry(CenterCenterFrame, width=10, relief=SUNKEN, bg="white", fg="black")


keys_keypad = [
    ['1', '2', '3', 'Stop'],    
    ['4', '5', '6', 'Corr.'],    
    ['7', '8', '9', 'Enter'],    
    ['', '0', '.', ''],    
]

keys_keyboard = [
	['!', '#', '$', '%', '&', '*', '+', '-', '/', '=', '?', '^', '_', '`', '{', '|', '}', '~'],
	['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
	['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
	['a', 's', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l'],
	['z', 'x', 'c', 'v', 'b', 'n', 'm','.', '@'],
]


# screen5() Saldo wijzigen
#scrn5_select1 = radiobutton "opwaarderen"
#scrn5_select2 = radiobutton "afwaarderen"
scrn5_textlbl = Label(CenterCenterFrame, text="Euro", bg="red", fg="white", font="none 12 bold")
scrn5_txtentry1 = Entry(CenterCenterFrame, width=10, relief=SUNKEN, bg="white", fg="black")


##### BottomFrame
# create another label
#klantnaam = ""
#klantsaldo = ""
#klant = ""
#output = Text(BottomFrame, width=75, height=6, wrap=WORD, background="white").grid(columnspan=3)

##### run the main loop
window.mainloop()
