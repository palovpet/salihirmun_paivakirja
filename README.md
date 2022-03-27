## Salihirmun päiväkirja
Sovelluksella kirjataan kuntosalitreenin sarjapainoja ja treenikertoja. Omia treenejä ja tilastoja voi katsella, ja vertailla omia tuloksia muiden käyttäjien tuloksiin. Sovellus optimoidaan käytettäväksi puhelimella.

### Toimintojen määrittelyt

Käyttäjä voi kirjautua sovellukseen käyttäen käyttäjätunnusta ja pin-koodia. Tarvittavat toiminnot:
- Käyttäjä kirjautuu syöttämällä käyttäjätunnuksen ja salasanan
- Uuden käyttäjätunnuksen voi luoda, jolloin tarkistetaan ettei samannimistä käyttäjää ole jo

Käyttäjä voi luoda max 5 pohjaa kuntosalitreenille. Treenipohjalla on:
- Nimi
- 1-10 liikettä, jotka valitaan listasta
- Jokaisella liikkeellä on toistomäärä ja sarjamäärä

Käyttäjä voi kirjata kuntosalitseenin. Saatavilla olevat toiminnot on:
- Kirjataan päivämäärä
- Jokaisen liikkeen kohdalle kirjataan sarjapainot, oletuksena liikkeen sarjapainoksi tarjotaan edellisellä kerralla kirjattua, mutta sitä voi muokata

Käyttäjä voi katsoa tilastoja omista treeneistään. Saatavilla olevat toiminnot:
- Tilasto siitä kuinka usein treejenä on tehty viikossa / kuukaudessa / vuodessa
- Jokaisen liikeeen joka kuuluu johonkin käyttäjän treenipohjaan kohdalla voidaan tarkastella kehitystä (sarjapainojen kasvu suhteessa aikaan)

Käyttäjä voi verrata omia tilastojaan muiden käyttäjien tilastoihin. Saatavilla olevat toiminnot:
- Treenikertojen erot (kumpi on treenannut enemmän viikossa / kuukaudessa / vuodessa)
- Niiden liikkeiden osalta jotka kuuluvat kummankin johonkin treenipohjaan voi vertailla sarjapainojen max arvojen eroja, sekä kehityksen eroa
