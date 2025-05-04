# Hány SET van az ábrán?

A játék célja, hogy a szokásos SET lapokból kiválasztunk tetszőleges darabot (legalább 6-t, de legfeljebb 27-et, mert ennyivel érdekes a játék és még egészen jól megtippelhető a válasz). Ezt amikor megnyitjunk a játék ablakot (leírás később), akkor tudjuk megadni a megfelelő mezőben, ami a “Enter the number of cards to play with:” szöveg alatt lesz. Ide csak számot tudunk beírni, hogy elfogadja, valamint ha nem megfelelő nagyságú a szám, akkor hibaüzenetet dob ki. Ezt követően a “Start Game” gombot megnyomva, vagy Entert ütve tudunk átjutni a következő ablakba. Ott annyi kártya lesz három sorban megadva, amennyit az előző ablakban kértünk. Ezeket a program véletlenül generálja ki a SET kártyák halmazából (81 lap). Ebben az ablakban a “How many sets do you see?” kérdésre kell válaszolni, a kérdés utáni mezőben. Itt is csak egy egész számot fog elfogadni. Innét a “Submit Guess” gombbal vagy Entert ütve tudunk a megoldásra továbbmenni (de ismét csak akkor, ha írtunk egy egész számot a mezőbe). Itt azonban van egy “Help” gomb is, ami a SET kártyák várható értékét adja meg (az ablak alján jelenik meg ez a szám, ha megnyomjuk a gombot). Ha átléptünk a következő ablakba, akkor ott a következő lesz látható: “The correct answer is {ide jön megoldás}. You guessed {a felhasználó előző ablakban begépelt megoldása lesz}.” Valamint azt is kiírja, jó válasz esetén, hogy “Correct\!”, rossz esetén “Try again\!”. Innét három gombbal lehet tovább menni:

- “New Game”, ezzel visszajutunk arra az oldalra, ahol a kártyák darabszámát megadhatjuk, majd onnan továbblépve ismet kapunk kártyákat és megtippelhetjük a SET-ek számát.  
- “Show Sets”, ezzel bejön egy új ablak, amin végig nézhetjük a SET-eket (3 kártya van egy sorban, és minden sorban másik SET lesz). Itt görgetni is lehet. Ha nem volt SAT (a válasz 0 volt), akkor azt írja ki, hogy “No sets found\!”. Ha ezt az ablakot becsukjuk, vagy a “Back” gombot megnyomjuk, akkor nem záródik be az egész játék ablaka, csak a SAT-ek oldala csukódik be, a játékos pedig visszajut arra az oldalra, ahol a megoldás volt kiírva. A többi ablakban, ha becsukjuk, akkor bezáródik minden ablak.  
- “Exit”, ezzel kilépünk a játékból.

## Játék futtatása

Tetszőleges python környezetből futtatható a kód.

A játék a következő python package-ket használja:
- PySimpleGUI
- random
- itertools
- matplotlib
- math

## AI használata

A kártyák kirajzolásához használtuk, illetve a játékablakok készítéséhez. Ezeket át kellett dolgoznunk.

- A kártyák konkrét kirajzolásához használtunk AI-t. Az általa visszaadott kódon többek között az alakzatok méretét, elhelyezkedését is megváltoztattuk, hogy méretarányosak legyenek és a valóságban használt kártyákhoz hasonlítsanak (amelytől végül annyiban eltértünk, hogy téglalapot használtunk és nem hullám jelet). Illetve eredetileg 4 oszlopot akartunk csinálni és n/4 felső egészrész db sort, végül 3 sorra és n/3 felső egészrész oszlopra változtattuk, hogy egyszerre kiférjenek a képernyőre.  
- Még sohasem csináltunk semmi UI-hoz hasonló dolgot, úgyhogy a UI készítés első lépésként megkérdeztük a Claude-ot, milyen python package-et érdemes használni egy ilyen projekthez (ezen a ponton a játék egy Jupiter Notebook-ban futtatható változata már készen volt, ami igazából mindent tudott, amit a végső játék, csak a tipp bekérése és a végeredmény kirajzolása is a Notebook-on belül történt). 4 javaslata volt, ezek közül a leírások alapján a PySimpleGUI-t választottuk, mert az tűnt a legegyszerűbbnek. Ezen a ponton már egy elég határozott képünk volt arról, hogy hogyan nézzen ki a játék, melyik oldalon milyen gombok és lehetőségek szerepeljenek. A 0-ról UI-t írni még így is elég nehéznek bizonyult, így végül megkértük az AI-t, hogy készítsen egy prototípust. Ez még nyilván tartalmazott hibákat, de arra mindenképp jó volt, hogy megtanultuk, hogyan lehet számokat bekérni és különböző elemeket elhelyezni a képernyőn. Ezután többek között a következőket kellett átírni:
    - A játékablak a kártyák képének mérete miatt használhatatlan volt, mert nem lehetett elérni az alján a gombokat. Ehhez végül ezt a kódrészt és a kártyák kirajzolását is módosítani kellett (emiatt lettek végül a kártyák 3 sorban kirajzolva).
    - Beraktuk a Help gombot, és magát a megjelenő segítséget.
    - A SET-ek megjelenítésének oldalán sem fért el a kép (nem túl meglepő módon), erre egy görgethető megoldást választottunk, amihez végül mégegyszer kellett az AI segítségét kérni. A megoldása egyébként nem működött, de sikerült kijavítanunk a kódját.
    - A fókuszálás és az ablakok középre igazítása is a mi munkánk volt, valamint az is, hogy a jobb felső x-re kattintva bezáródjon a játék.

## Próba futtatás

Első ablakban megadjuk, hogy 8, majd az Entert nyomjuk le. Ekkor 3 db oszlopot rajzol ki, ahol a jobb, alsó sarokban nincs kártya. Mi tippelünk egy számot a Help alapján. Beírjuk: …  
Utána Submit Guess gombra nyomunk es átmegyünk a  következő ablakba. Itt a válasz:... és megnyomjuk a Show sets gombot. Végignézzük, majd Back gombra nyomva visszajutunk az előző oldalra. Megnyomjuk a New Game gombot és újra beírunk egy számot, pl 27 (a maximumot). Amikor ismét eljutunk majd a megoldás oldalra es megnéztük a Set-eket, akkor az Exit gombbal kilépünk a játékból.