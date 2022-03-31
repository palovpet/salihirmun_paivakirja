## Salihirmun päiväkirja
Sovelluksella kirjataan kuntosalitreenin sarjapainoja ja treenikertoja. Omia treenejä ja tilastoja voi katsella, ja vertailla omia tuloksia muiden käyttäjien tuloksiin. Sovellus optimoidaan käytettäväksi puhelimella.

### Välipalautukseen 2 valmistuneet toiminnallisuudet:

Käyttäjä voi kirjautua sovellukseen käyttäen käyttäjätunnusta ja salasanaa.
- Uusi käyttäjätunnus voidaan luoda ja salasana valita. Käyttäjätunnukseksi ei hyväksytä nimimerkkiä joka on jo käytössä, lisäksi salasana on syötettävä kaksi kertaa ja niiden on oltava samat
- Käyttäjä voi kirjautua sovellukseen käyttäen luomiaan tunnuksia
- Käyttäjä voi kirjautua ulos

Käyttäjä voi luoda max 5 pohjaa kuntosalitreenille. 
- Käyttäjä voi luoda uuden saliohjelman ja muokata aiemmin luomiaan.
    - Etusivulla on lista käyttäjän saliohjelmista, jos niitä ei ole, on näkyvillä kenttä johon lisätään ensimmäisen saliohjelman nimi
    - Kun saliohjelmia on useampi, valitaan alasvetovalikosta ohjelma jota halutaan muokata, ja napsautetaan Näytä ja muokkaa
- Saliohjelmia sallitaan max 5 per käyttäjä
- Saliohjelman muokkaustilassa lisätään liikkeitä valitsemalla liike alasvetovalikosta ja antamalla sarjojen ja toistojen lukumäärä
- Saliohjelman liikkeet -osiossa näkyy suunnitelmassa olevat liikkeet, sarjat ja toistot
- Saliohjelmasta voi poistaa liikkeen napsauttamalla Saliohjelman liikkeet -osiossa Ppoista-painiketta kyseisen likkeen kohdalla
- Yhteen saliohjelmaan sallitaan max 10 liikettä
- Ohjelman keskeneräisyyden vuoksi liikkeitä on valittavissa vasta kolme, ja sarjapainot on aina 0 kg.

### Keskeneräiset toiminnallisuudet:

Käyttäjä voi kirjata kuntosalitseenin. Saatavilla olevat toiminnot on:
- Kirjataan päivämäärä
- Jokaisen liikkeen kohdalle kirjataan sarjapainot, oletuksena liikkeen sarjapainoksi tarjotaan edellisellä kerralla kirjattua, mutta sitä voi muokata

Käyttäjä voi katsoa tilastoja omista treeneistään. Saatavilla olevat toiminnot:
- Tilasto siitä kuinka usein treejenä on tehty viikossa / kuukaudessa / vuodessa
- Jokaisen liikeeen joka kuuluu johonkin käyttäjän treenipohjaan kohdalla voidaan tarkastella kehitystä (sarjapainojen kasvu suhteessa aikaan)

Käyttäjä voi verrata omia tilastojaan muiden käyttäjien tilastoihin. Saatavilla olevat toiminnot:
- Treenikertojen erot (kumpi on treenannut enemmän viikossa / kuukaudessa / vuodessa)
- Niiden liikkeiden osalta jotka kuuluvat kummankin johonkin treenipohjaan voi vertailla sarjapainojen max arvojen eroja, sekä kehityksen eroa
