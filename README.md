<h1>KKHC</h1>
<h2>Koelkast Hobby Club</h2>

De KKHC is een hobby project van een aantal collega's.
Als IT afdeling hebben we een koelkast waarin blikjes, repen, en koeken te halen zijn.
Ieder product kent een prijs van slechts 50 cent.

De koelkast opereert op basis van goed vertrouwen. Je schijft je naam op een lijst, doneert geld in een pot, en streept af wat je
uit de koelkast gebruikt. Negatief saldo is geen probleem, mits het niet de spuigaten uitloopt. Na verloop van tijd vereffen je 
je schuld bij de koelkast door weer geld in de pot te stoppen.

Eens per periode wordt de balans opgemaakt en wordt de lijst ververst met de nieuwe saldo standen. Hier worden de personen met een openstaande schuld verzocht om deze in te lossen.

<h1>Automatisering?</h1>
Als techneuten onder elkaar leek het ons leuk, en leerzaam, om deze lijst te automatiseren. Het is nog altijd op basis van goed 
vertrouwen en je kunt nog altijd een negatief saldo opbouwen.

Omdat we niet de hele wereld in één keer willen programmeren, dient dit programma, op basis van python, als basis en kan en wordt er naar hartelust aan gesleuteld al naar gelang we zelf leuk en belangrijk vinden.

<h1>Basis programma</h1>
Dit programma leest de tag/druppel van de koelkast klant.
Indien de tag/druppel onbekend is, wordt de registratie procedure gestart, en anders het hoofdmenu getoont.

Het hoofdmenu kent 3 opties, nl. Items kopen, Saldo opvragen, en Stoppen.

Items kopen vraag om het aantal items, en past het saldo evenredig aan voor de klant. Hierna is de transactie klaar

Saldo opvragen toont het huidige saldo, en vraagt of de klant wil op- of afwaarderen.
Op basis van de keuze wordt om een bedrag gevraagd en wordt het geregistreerde saldo evenredig aangepast. 
Bij afwaarderen kan niet meer dan het geregistreerde saldo afgewaardeerd wordt.

Stoppen spreekt voor zich

Alle klantgegevens worden bijgehouden in een dataframe, en opgeslagen in een .csv bestand.
dit maakt het eenvoudig om het bestand op te slaan, mee te nemen in een backup, te openen in een spreadsheet, etc.
Na iedere aankoop en daarmee saldo aanpassing wordt het .csv bestand opgeslagen.
eenmaal per etmaal wordt er een backup van het bestand gemaakt op cloudstorage (dropbox, google drive, onedrive, etc)

</h1>Verdere ideëen</h1>
Er zijn ideëen voor integratie met de API's van Bunq of die van Tikkie om het betalingsverkeer te digitaliseren. 
voor de integratie met de Bunq api: https://doc.bunq.com/
