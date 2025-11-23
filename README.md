# Mediebias-analys av Dagens Nyheters rapportering av kriget i Gaza

Kodbas för koden och resultatet som använts i medieanalysen av Dagens Nyheters rapportering av kriget i Gaza. Länkas till här: [Stark pro-israelisk bias i Dagens Nyheters rapportering av kriget i Gaza](https://ellenhelkernygren.substack.com/p/stark-pro-israelisk-bias-i-dagens?utm_source=profile&utm_medium=reader2).

## Resultat
Tre Excel-dokument har inkluderats som visar våra resultat:
 - [`DN_medieanalys_alla_meningar_dodsfall.xlsx`](DN_medieanalys_alla_meningar_dodsfall.xlsx): Inkluderar alla meningar där palestinska och israeliska dödsfall nämns.
 - [`DN_medieanalys_alla_meningar_ordanalys.xlsx`](DN_medieanalys_alla_meningar_ordanalys.xlsx): Inkluderar alla meningar med känsloladdade ord för att beskriva palestinska och israeliska dödsfall, olika termer för tillfångatagande, samt antisemitism och islamofobi.
 - [`DN_medieanalys_resultat_sammanfattning.xlsx`](DN_medieanalys_resultat_sammanfattning.xlsx): Inkluderar en sammanfattning av alla resultat.

## Rådata

All rådata som använts i den här analysen kan inte läggas upp på grund av upphovsrättsskäl med DN. Om du vill reproducera resultaten, skicka ett e-mail till mig på: [ellen.helkernygren@gmail.com](ellen.helkernygren@gmail.com).

## Metod
 
Vi analyserade 233 DN-artiklar mellan den 7:e oktober – 7 november för att få en översikt av de mönster som genomsyrar DN:s medierapportering i det senaste kriget i Gaza. 

Denna analys gjordes i två delar: 
 1. Vi undersökte hur ofta israeliska och palestinska dödsfall nämns.
 2. Vi granskade hur ofta olika känsloladdade ord används för att beskriva israeliska och palestinska dödsfall (t ex ”blodig,” ”brutal,” ”massaker”), samt hur ofta andra relevanta ord nämns, inklusive ”antisemitism” och ”islamofobi.”

För att få en inblick i hur ofta DN rapporterar om israeliska och palestinska dödsfall utförde vi fyra separata steg.
 1. Först samlade vi ihop alla relevanta artiklar under ämnet ”Israel-Palestina-konflikten” genom DN:s ämnesfunktion. På grund av det stora antalet artiklar så valde vi att begränsa vår analys till den första månaden av kriget, 7:e oktober-7:e november. Eftersom vi var mest intresserade av att få en inblick i DN:s rapportering av konflikten så valde vi att exkludera debattinlägg av utomstående skribenter, dvs. debattartiklar och insändare som inte var skrivna av DN:s medarbetare. Krönikor, ledarartiklar och andra kommenterande texter av DN:s medarbetare inkluderades. Detta resulterade i 233 stycken artiklar.
 2. Vi sammanställde alla meningar som innehöll följande ord och ordderivat genom att använda en "RegEx"-sökning implementerad i Python-kod:
    ```
    words = ['dör?', 'död', 'dog', 'dötts?', 'dödats?', 'dödades?', 'döds\w{1,15}', 'döda', 'mörda\w{0,3}', 'mord\w{0,2}','massak\w{0,8}','massmord\w{0,2}', 'slakt\w{0,5}']
    ```
    Detta kompilerades till ett enda Regex-uttryck:
    ```
    (?<=^)([^.\n]*?(dör?|död|dog|dötts?|dödats?|dödades?|döds\w{1,15}|döda|mörda\w{0,3}|mord\w{0,2}|massak\w{0,8}|massmord\w{0,2}|slakt\w{0,5})(?:[ ,;:][^.\n]+?)?[.?!])
    ```
    Detta mönster letar efter nyckelorden i en mening samtidigt som den tillhandahåller "capture groups," både för hela meningen och det matchade ordet. Uttrycket 'lookbehind' säkerställer att meningen föregås av `\n`, `^`, eller `. `.

3. Efter att dessa meningar samlats ihop (totalt 603 stycken) gick vi igenom dem manuellt och taggade dem baserat på om de refererade till israeliska eller palestinska dödsfall, eller både och. Om fler än ett relevant ord identifieras i samma mening står flera identiska meningar efter varandra, men orden som analyseras är olika. Den här processen involverade även att sålla bort meningar som var irrelevanta. Fyra regler formulerades för att gallra ut irrelevanta meningar och ord: 
   - Offret måste vara palestinier eller israel, och dödsfallet måste ha skett i Israel eller Palestina (Gaza eller Västbanken).
   - Meningarna måste beröra specifika händelser mellan den 7:e oktober – 7:e november som redan har skett (spekulationer räknas inte)
   - Ord eller meningar som står inom citattecken exkluderas
   - Textboxar och annan typ av grafik exkluderas
4. Dessa siffror jämfördes sedan med de faktiska dödstalen mellan den 7:e oktober – 7:e november.

För att få en djupare uppfattning om hur olika relevanta ord användes i relation till israeler och palestinier fortsatte vi med en separat ordanalys.
 
1. Steg 1 ovan. 
2. Vi sammanställde alla meningar som innehöll följande ord och ordderivat genom att använda en "RegEx"-sökning implementerad i Python-kod:
    ```
    words = ['mörda\w{0,3}', 'mord\w{0,3}', 'massak\w{0,8}', 'massmord\w{0,3}', 'slakt\w{0,5}','blodig\w{0,4}', 'brutal\w{0,6}', 'antisemit\w{0,5}', 'judehat\w{0,4}', 'islamofob\w{0,4}', 'muslimhat\w{0,4}', 'gisslan\w{0,14}', 'kidnapp\w{0,14}', '\w{0,4}fånga\w{0,7}', 'frihetsberöv\w{0,5}', 'förvar', 'interner\w{0,4}']
    ```
3. Efter att dessa meningar samlats ihop (totalt 613 stycken) gick vi igenom dem manuellt och taggade dem baserat på om orden refererade till israeliska eller palestinska dödsfall, gisslan, eller om det handlade om antisemitism eller islamofobi. Om fler än ett relevant ord identifieras i samma mening står flera identiska meningar efter varandra, men orden som analyseras är olika. Den här processen involverade även att sålla bort meningar som av olika anledningar var irrelevanta. Fem regler formulerades för att gallra ut irrelevanta meningar och ord: 
   - De känsloladdade orden/termerna för frihetsberövade måste referera till israeliska eller palestinska dödsfall/bortföranden som skett i Israel eller Palestina (Gaza eller Västbanken)
   - De känsloladdade orden och termerna för frihetsberövade måste beröra specifika händelser mellan den 7:e oktober – 7:e november som redan har skett (spekulationer räknas inte)
   - Orden antisemitism och islamofobi inkluderas oavsett var i världen händelserna refererar till och de behöver inte beröra specifika händelser mellan den 7:e oktober – 7:e november (antisemitism eller islamofobi som diskuteras i generella termer inkluderas) 
   - Ord eller meningar som står inom citattecken exkluderas
   - Textboxar och annan typ av grafik exkluderas
4. Ordfrekvensen lades sedan ihop i en tabell och jämfördes med varandra.

## Referens och användning av arbete

Om du använder vårt arbete, citera oss gärna på följande sätt:
```
[Helker-Nygren, Ellen., Lloyd Steffan. (2024) Stark pro-israelisk bias i Dagens Nyheters rapportering av kriget i Gaza: En mediebias-analys mellan den 7:e oktober – 7 november 2023].
```
