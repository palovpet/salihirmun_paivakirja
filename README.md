## Salihirmun päiväkirja
Sovelluksella kirjataan kuntosalitreenin sarjapainoja ja treenikertoja. Omia treenejä ja tilastoja voi katsella, ja vertailla omia tuloksia muiden käyttäjien tuloksiin. Sovellus optimoidaan käytettäväksi puhelimella.


### Välipalautukseen 2 valmistuneet toiminnallisuudet:

Käyttäjä voi kirjautua sovellukseen käyttäen käyttäjätunnusta ja salasanaa:
- Uusi käyttäjätunnus voidaan luoda ja salasana valita. Käyttäjätunnukseksi ei hyväksytä nimimerkkiä joka on jo käytössä, lisäksi salasana on syötettävä kaksi kertaa ja niiden on oltava samat
- Käyttäjä voi kirjautua sovellukseen käyttäen luomiaan tunnuksia
- Käyttäjä voi kirjautua ulos


Käyttäjä voi luoda max 5 pohjaa kuntosalitreenille:
- Käyttäjä voi luoda uuden saliohjelman ja muokata aiemmin luomiaan.
    - Etusivulla on lista käyttäjän saliohjelmista, jos niitä ei ole, on näkyvillä kenttä johon lisätään ensimmäisen saliohjelman nimi
    - Kun saliohjelmia on useampi, valitaan alasvetovalikosta ohjelma jota halutaan muokata, ja napsautetaan Näytä ja muokkaa
- Saliohjelmia sallitaan max 5 per käyttäjä
- Saliohjelman muokkaustilassa lisätään liikkeitä valitsemalla liike alasvetovalikosta ja antamalla sarjojen ja toistojen lukumäärä
- Saliohjelman liikkeet -osiossa näkyy suunnitelmassa olevat liikkeet, sarjat ja toistot
- Saliohjelmasta voi poistaa liikkeen napsauttamalla Saliohjelman liikkeet -osiossa Poista liike -painiketta kyseisen likkeen kohdalla
- Yhteen saliohjelmaan sallitaan max 10 liikettä
- Ohjelman keskeneräisyyden vuoksi liikkeitä on valittavissa vasta kolme, näitä tullaan lisäämään


Käyttäjä voi kirjata kuntosalitreenin:
- Kirjataan päivämäärä
- Jokaisen liikkeen kohdalla kirjataan sarjapainot.

Huom! Kuntosalitreenin kirjauksen tallennustoiminnallisuutta ei ole vielä toteutettu, mutta visuaalisia elementtejä on jo laitettu paikoilleen. Kirjaa-painikkeen painaminen ei siis vielä tee mitään.


### Keskeneräiset toiminnallisuudet:

Kuntosalitreenin kirjauksen loput toiminnallisuudet:
- Sarjapainojen tallennus
- Kuntosalikerran tallennus (pvm + mikä saliohjelma)
- Jokaisen liikkeen kohdalla oletuksena liikkeen sarjapainoksi tarjotaan edellisellä kerralla kirjattua, mutta sitä voi muokata


Käyttäjä voi katsoa tilastoja omista treeneistään. Saatavilla olevat toiminnot:
- Tilasto siitä kuinka usein treejenä on tehty viikossa / kuukaudessa / vuodessa
- Jokaisen liikeeen joka kuuluu johonkin käyttäjän treenipohjaan kohdalla voidaan tarkastella kehitystä (sarjapainojen kasvu suhteessa aikaan)


Käyttäjä voi verrata omia tilastojaan muiden käyttäjien tilastoihin. Saatavilla olevat toiminnot:
- Treenikertojen erot (kumpi on treenannut enemmän viikossa / kuukaudessa / vuodessa)
- Niiden liikkeiden osalta jotka kuuluvat kummankin johonkin treenipohjaan voi vertailla sarjapainojen max arvojen eroja, sekä kehityksen eroa
