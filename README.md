<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
</head>
<body lang="nl-NL" link="#000080" vlink="#800000" dir="ltr"><p align="center" style="margin-top: 0.42cm; margin-bottom: 0.21cm; line-height: 100%; page-break-after: avoid">
<font face="Liberation Sans, sans-serif"><font size="18" style="font-size: 28pt"><b>KKHC</b></font></font></p>
<h1 class="western">Koelkast Hobby Club</h1>
<p>De KKHC is een hobby project van een aantal collega's. Als IT
afdeling hebben we een koelkast waarin blikjes, repen, en koeken te
halen zijn. Ieder product kent een vaste prijs van slechts 50 cent. 
</p>
<p><br/>
De koelkast opereert op basis van goed vertrouwen. Je
schijft je naam op een lijst, doneert geld in een pot, en streept af
wat je uit de koelkast gebruikt. Negatief saldo is geen probleem,
mits het niet de spuigaten uitloopt. Na verloop van tijd vereffen je
je schuld bij de koelkast door weer geld in de pot te stoppen. <br/>
Eens
per periode wordt de balans opgemaakt en wordt de lijst ververst met
de nieuwe saldo standen. Hier worden de personen met een openstaande
schuld verzocht om deze in te lossen. 
</p>
<h1 class="western">Automatisering?</h1>
<p>Als techneuten onder elkaar leek het ons leuk, en leerzaam, om
deze lijst te automatiseren. Het is nog altijd op basis van goed
vertrouwen en je kunt nog altijd een negatief saldo opbouwen. 
</p>
<p><br/>
Omdat we niet de hele wereld in één keer willen
programmeren, dient dit programma, op basis van python, als basis en
kan en wordt er naar hartenlust aan gesleuteld al naar gelang we zelf
leuk en belangrijk vinden. 
</p>
<h1 class="western">Basis programma</h1>
<p>Dit programma leest de rfid tag van de koelkast klant. Indien de
rfid tag onbekend is, wordt de registratie procedure gestart, en
anders het hoofdmenu getoont. 
</p>
<p><br/>
De registratie vraagt om een paar gegevens, namelijk: 
</p>
<ul>
	<li><p>voornaam,</p>
	<li><p>achternaam,</p>
	<li><p>e-mail adres. <br/>
<br/>
<br/>

</ul>
<p>Het hoofdmenu kent 3 opties:</p>
<ul>
	<li><p>Items kopen, 
	</p>
	<li><p>Saldo opvragen,</p>
	<li><p>Stoppen. <br/>
<br/>
<br/>

</ul>
<p>Items kopen vraag om het aantal items, en past het saldo evenredig
aan voor de klant. Hierna is de transactie klaar.</p>
<p> <br/>
Saldo opvragen toont het huidige saldo, en biedt de klant
de mogelijkheid om op- of af te waarderen. Op basis van de keuze
wordt om een bedrag gevraagd en wordt het geregistreerde saldo
evenredig aangepast. Bij afwaarderen kan niet meer dan het
geregistreerde saldo afgewaardeerd wordt. 
</p>
<p><br/>
Stoppen spreekt voor zich 
</p>
<p><br/>
Alle klantgegevens worden bijgehouden in een dataframe, en
opgeslagen in een .csv bestand. Dit maakt het eenvoudig om het
bestand op te slaan, mee te nemen in een backup, te openen in een
spreadsheet, etc. 
</p>
<p>Na iedere aankoop en daarmee saldo aanpassing wordt het .csv
bestand opgeslagen. eenmaal per etmaal wordt er een backup van het
bestand gemaakt op cloudstorage (dropbox, google drive, onedrive,
etc) 
</p>
<h1 class="western">Verdere ideëen</h1>
<p>Er zijn ideëen voor integratie met de API's van Bunq of die van
Tikkie om het betalingsverkeer te digitaliseren. 
</p>
<p>Hiermee kunnen betaalverzoeken gedaan worden, en kan kunnen
saldo's in een database worden bijgehouden. 
</p>
<p><br/>
Voor de integratie met de Bunq api: https://doc.bunq.com/ 
</p>
</body>
</html>
