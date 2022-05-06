### Salihirmun päiväkirja
Salihirmun päiväkirjassa käyttäjä voi luoda itselleen saliohjelmia, kirjata tehtyjä treenejä ja tarkastella statistiikkaa omasta kehityksestä. Sovellus on optimoitu käytettäväksi älypuhelimella, jonka vuoksi visuaalinen ilme ei tietokoneen näytöllä ole yhtä miellyttävä kuin älypuhelimen.

Sovellus on käytettävissä [herokussa](https://salihirmun-paivakirja.herokuapp.com/).

*Sovellus on totetutettu Helsingin yliopiston tietojenkäsittelytieteen aineopintojen kurssin TKT20011: Tietokantasovellus harjoitustyönä.*


### Kuvaus sovelluksen toiminnallisuuksista

#### Käyttäjä voi luoda itselleen tunnukset ja kirjautua sovellukseen käyttäen käyttäjätunnusta ja salasanaa.

#### Käyttäjä voi luoda itselleen enintään 5 saliohjelmaa:
- Saliohjelman luominen:
    - Luo uusi saliohjelma -osioon annetaan saliohjelman nimi, ja napsautetaan  Tallenna
- Saliohjelman muokkaaminen:
    - Saliohjelmien luonti ensimmäistä kertaa ja muokkaus myöhemmin tehdään valitsemalla haluttu saliohjelma Muokkaa saliohjelmaa -osion alasvetovalikosta ja napsauttamalla Näytä ja muokkaa
    - Yhteen saliohjelmaan voi lisätä enintään kymmenen eri liikettä, liikkeet valitaan alasvetovalikosta ja niille on annettava sarja- ja toistomäärät
    - Saliohjelmaan kuuluvat liikkeet näkyvät muokkaustilan osiossa Saliohjelman liikkeet
    - Liikkeen voi poistaa napsauttamalla halutun liikkeen kohdalla Poista liike -paniketta
    
Mikäli jo käytössä olevaan saliohjelmaan tulee suuria muutoksia on suositeltavaa luoda uusi saliohjelma, koska saliohjelmakohtaisessa statistiikassa näytetään myös liikkeet jotka ovat aiemmin olleen osana saliohjelmaa.
    
#### Käyttäjä voi kirjata kuntosalitreenin:
- Valitaan päivämäärä (oletuksena on kuluva päivä) ja mikä saliohjelma on suoritettu
- Jokaisen liikkeen kohdalla kirjataan sarjapainot, kehonpainolla tehtävän liikkeen painoksi kirjataan 0kg
- Jokaisen liikkeen kohdalla oletuksena liikkeen sarjapainoksi tarjotaan edellisellä kerralla kirjattua, liikkeen kohdalla näytetään myös milloin kyseinen kirjaus on tehty (mikäli tieto on tallennettu aiemmin)
- Kirjattavaa painoa voi muokata, painoksi hyväksytään arvot 0-300kg kahden desimaalin tarkkuudella (tai kokonaislukuna)

Tietyn saliohjelman ja sitä myötä siihen kuuluvien liikkeiden sarjapainot voi kirjata vain kerran yhdelle vuorokaudelle.

#### Käyttäjä voi katsoa tilastoja omista treeneistään läpi saliohjelmien:
- Tilastot aukeavat Tilastot kaikista saliohjelmista -osion Näytä tilastot -painikkeesta
- Tilastoissa näytetään ensimmäinen treenikerta, viimeisin treenikerta, treenikertojen kokonaismäärä, kirjattujen liikkeiden korkeimmat sarjapainot, sekä tilastot treenikerroista kuukausittain ja vuosittain

#### Käyttäjä voi katsella yksittäisen saliohjelman tilastoja:
- Saliohjelma valitaan tarkasteltavaksi Tilastot yksittäisistä saliohjelmista -osion alasvetovalikosta ja näytetään kun Näytä tilastot -painiketta napsautetaan
- Tilastoissa näytetään ensimmäinen treenipäivä, viimeisin treenipäivä, montako treenikirjausta on tehty ja liikkeiden sarjapainojen kehitys

#### Käyttäjä voi katsoa tilastoa yksittäisen liikkeen sarjapainojen kehityksestä:
- Liike valitaan tarkasteluun Tilastot yksittäisestä liikkeestä -osion alasvetovalikosta
- Tilastoissa näytetään kyseisen liikkeen kirjattuja painoja, sekä tiedot saliohjelmasta johon kirjaus kuuluu

## Kommentti sovelluksen teknisestä laadusta
Sovellus on kirjoitettu noudattaen Python-koodin ohjelmointityyliä, ja laatua on tarkistetty käyttäen Pylint-työkalua. Routes-luokkaan jäi muutamia rivejä, jotka ovat yli sallitun rivipituuden. Näissä tapauksissa rivit olisi saatu lyhyemmäksi vain luomalla metodeihin välitallennusta varten muutoin turhia muuttujia. Kyseisen luokan kaikki metodit noudattavat yhtenäisesti tapaa, että muuttujiin tallennetaan tietoja metodin sisällä vain mikäli ne saadaan käyttäjältä esim. lomakkeen kautta, ja muutoin taas muilta python-luokilta kysyttävät tiedot annetaan suoraan render_templane -metodeille.
