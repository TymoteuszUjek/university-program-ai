import random
wszystkieLiniePliku=open("C:\\Users\\tymot\\Desktop\\kroC100.txt").readlines()
liczbaMiast = int(wszystkieLiniePliku[0])
liczbaOsobnikowWPopulacji=60
prawdopodobienstwoKrzyzowania=0.94  #91 do 95
prawdopodobienstwoMutacji=0.07
liczbaIteracjiDlaAlgorytmu=250000
parametrKDlaTurnieju=20 #2 do 4, jak populacja 100 to tak z 20

def wczytajMacierzOdleglosci():
    macierzOdleglosci = [[0 for i in range(liczbaMiast)] for j in range(liczbaMiast)]
    aktualnyWiersz = 1
    for aktualnaLinia in wszystkieLiniePliku[2::]:
        odleglosci = list(map(int, aktualnaLinia.strip().split()))
        for aktualnaKolumna in range(len(odleglosci)):
            macierzOdleglosci[aktualnyWiersz][aktualnaKolumna] = odleglosci[aktualnaKolumna]
            macierzOdleglosci[aktualnaKolumna][aktualnyWiersz] = odleglosci[aktualnaKolumna]
        aktualnyWiersz += 1
    return macierzOdleglosci

macierzOdleglosci=wczytajMacierzOdleglosci()

def stworzOsobnika():
    osobnik = [i for i in range(liczbaMiast)]
    random.shuffle(osobnik)
    return osobnik

def stworzPopulacjePoczatkowa():
    populacja = []
    for i in range(liczbaOsobnikowWPopulacji):
        populacja.append(stworzOsobnika())
    return populacja

def obliczFunkcjePrzystosowaniaDlaOsobnika(osobnik):
    odleglosc = 0
    for i in range(len(osobnik) - 1):
        indeksPierwszegoMiasta = osobnik[i]
        indeksDrugiegoMiasta = osobnik[i + 1]
        odleglosc += macierzOdleglosci[indeksPierwszegoMiasta][indeksDrugiegoMiasta]
    odleglosc += macierzOdleglosci[osobnik[0]][osobnik[-1]]
    return odleglosc

def obliczFunkcjePrzystosowaniaDlaCalejPopulacji(populacja):
    przystosowaniePopulacji = []
    for osobnik in populacja:
        przystosowaniePopulacji.append(obliczFunkcjePrzystosowaniaDlaOsobnika(osobnik))
    return przystosowaniePopulacji


def selekcjaTurniejowa(populacja, ocena, k):
    populacjaPoSelekcji = []
    for osobnik in populacja:
        indeksNajlepszego = random.randint(0, liczbaOsobnikowWPopulacji - 1)
        for j in range(k - 1):
            indeksLosowego = random.randint(0, len(populacja) - 1)
            if ocena[indeksNajlepszego] > ocena[indeksLosowego]:
                indeksNajlepszego = indeksLosowego
        wybrany = populacja[indeksNajlepszego][:]
        populacjaPoSelekcji.append(wybrany)
    return populacjaPoSelekcji

def krzyzowaniePMX(populacja):
    populacjaPoKrzyzowaniu = []
    for i in range(0, len(populacja), 2):
        rodzic1 = populacja[i]
        rodzic2 = populacja[i + 1]
        if random.random()<prawdopodobienstwoKrzyzowania:
            pierwszyPunktKrzyzowania = random.randint(1, len(rodzic1) - 2)
            drugiPunktKrzyzowania = random.randint(pierwszyPunktKrzyzowania + 1, len(rodzic1) - 1)

            potomek1 = rodzic1[pierwszyPunktKrzyzowania:drugiPunktKrzyzowania]
            potomek2 = rodzic2[pierwszyPunktKrzyzowania:drugiPunktKrzyzowania]

            prefix1 = przepiszCzescOsobnika(rodzic2[:pierwszyPunktKrzyzowania], potomek1, potomek2)
            prefix2 = przepiszCzescOsobnika(rodzic1[:pierwszyPunktKrzyzowania], potomek2, potomek1)

            postfix1 = przepiszCzescOsobnika(rodzic2[drugiPunktKrzyzowania:], potomek1, potomek2)
            postfix2 = przepiszCzescOsobnika(rodzic1[drugiPunktKrzyzowania:], potomek2, potomek1)

            dziecko1 = prefix1 + potomek1 + postfix1
            dziecko2 = prefix2 + potomek2 + postfix2
            populacjaPoKrzyzowaniu.append(dziecko1)
            populacjaPoKrzyzowaniu.append(dziecko2)
        else:
            populacjaPoKrzyzowaniu.append(rodzic1[:])
            populacjaPoKrzyzowaniu.append(rodzic2[:])

    return populacjaPoKrzyzowaniu


def przepiszCzescOsobnika(rodzic, srodekRodzica, srodekPotomka):
    czescOsobnika = []
    for gen in rodzic:
        while gen in srodekRodzica:
            gen = srodekPotomka[srodekRodzica.index(gen)]
        czescOsobnika.append(gen)
    return czescOsobnika

def mutacja(populacja):
    for osobnik in populacja:
        if random.random()<prawdopodobienstwoMutacji:
            pierwszyPunktInwersji = random.randint(1, len(osobnik))
            drugiPunktInwersji = random.randint(1, len(osobnik))
            while drugiPunktInwersji == pierwszyPunktInwersji:
                drugiPunktInwersji = random.randint(1, len(osobnik))
            if pierwszyPunktInwersji > drugiPunktInwersji:
                pierwszyPunktInwersji, drugiPunktInwersji = drugiPunktInwersji, pierwszyPunktInwersji
            osobnik[pierwszyPunktInwersji:drugiPunktInwersji] = osobnik[drugiPunktInwersji - 1:pierwszyPunktInwersji - 1:-1]

def algorytmGenetyczny():
    populacjaPoczatkowa = stworzPopulacjePoczatkowa()
    ocena = obliczFunkcjePrzystosowaniaDlaCalejPopulacji(populacjaPoczatkowa)
    najlepszy = (populacjaPoczatkowa[0][:], ocena[0])
    for i in range(1, len(populacjaPoczatkowa)):
        if ocena[i] < najlepszy[1]:
            najlepszy = (populacjaPoczatkowa[i][:], ocena[i])

    print("Losowy:", najlepszy)


    for gen in range(liczbaIteracjiDlaAlgorytmu):
        populacjaPoSelekcji = selekcjaTurniejowa(populacjaPoczatkowa, ocena,parametrKDlaTurnieju)
        populacjaPoKrzyzowaniu = krzyzowaniePMX(populacjaPoSelekcji)
        mutacja(populacjaPoKrzyzowaniu)
        #!!!!!
        #sukcesja
        #sukcesja(populacjaPoczątkowa ....)
        populacjaPoczatkowa=populacjaPoKrzyzowaniu[:]
        ocena = obliczFunkcjePrzystosowaniaDlaCalejPopulacji(populacjaPoczatkowa)
        for i in range(liczbaOsobnikowWPopulacji):
            if ocena[i] < najlepszy[1]:
                najlepszy = (populacjaPoczatkowa[i][:], ocena[i])
    return najlepszy

print("Najlepszy osobnik z działania algorytmu genetycznego: ",algorytmGenetyczny())