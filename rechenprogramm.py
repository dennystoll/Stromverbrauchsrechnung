import json

def neue_verbrauchsdaten():
    with open("C:/datei/pfad/daten.json", "r")as datei:
        daten = json.load(datei)
        neuverbrauch = daten["neuverbrauch"]
    while True:
        global neuer_verbraucher
        neuer_verbraucher = 0
        inp = input("Existiert ein neuer verbraucher? J|Ja, N|Nein: ")
        if inp == "J":
            neuer_verbraucher += 1
            while True:
                inp = input("Nachname des neuverbrauchers: ")
                if inp.isdigit():
                    print("Ungültige Eingabe!")
                    continue
                else:
                    global neuverbraucher_name
                    neuverbraucher_name = inp
                    break

            existierender_verbrauch = input(f"Hat familie {neuverbraucher_name} schon Strom verbraucht? J|Ja N|Nein: ")
            while True:
                if existierender_verbrauch == "J":
                    while True:
                        neuverbraucher_verbrauch = input(f"Stromverbrauch der familie {neuverbraucher_name} in kWh: ")
                        if neuverbraucher_verbrauch.isdigit():
                            neuverbraucher_verbrauch = int(neuverbraucher_verbrauch)
                            break
                        else:
                            print("Ungültige Eingabe!")
                            continue
                    break

                elif existierender_verbrauch == "N":
                    neuverbraucher_verbrauch = 0
                    break

                else:
                    print("Ungültige Eingabe!")
                    continue

            neuer_verbrauch = {}
            for familie in neuverbrauch:
                while True:
                    inp = input(f"Bitte geben sie den neuen verbrauchswert des folgenden zählers an. {familie}: ")
                    if inp.isdigit():
                        inp = int(inp)
                        neuer_verbrauch[familie] = inp
                        break

                    else:
                        print("Ungültige Eingabe!")
                        continue

            neuer_verbrauch[neuverbraucher_name] = neuverbraucher_verbrauch
            break

        elif inp == "N":
            neuer_verbrauch = {}
            for familie in neuverbrauch:
                while True:
                    inp = input(f"Bitte geben sie den neuen verbrauchswert des folgenden zählers an. {familie}: ")
                    if inp.isdigit():
                        inp = int(inp)
                        neuer_verbrauch[familie] = inp
                        break
                    else:
                        print("Ungültige Eingabe!")
                        continue
            break
        else:
            print("Ungültige Eingabe!")
            continue
    return neuer_verbrauch

def daten_überschreibung(neuer_verbrauch):
    with open("C:/datei/pfad/daten.json", "r")as datei:
        daten = json.load(datei)
        if neuer_verbraucher == 1:
            addition = daten["neuverbrauch"]
            addition[neuverbraucher_name] = 0
            print(addition)
            daten["altverbrauch"] = addition
        else:
            daten["altverbrauch"] = daten["neuverbrauch"]
        daten["neuverbrauch"] = neuer_verbrauch 

    with open("C:/datei/pfad/daten.json", "w")as f:
        json.dump(daten, f, indent = 4)

def rechnung():

    with open("C:/datei/pfad/daten.json", "r")as datei:
        daten = json.load(datei)
        mtl_verb = (daten["neuverbrauch"]["Haptz\u00e4hler"]) - (daten["altverbrauch"]["Haptz\u00e4hler"])
        einz_alt_verb = []
        einz_neu_verb = []
        altverbrauch = daten["altverbrauch"]
        neuverbrauch = daten["neuverbrauch"]
        for verbrauch in altverbrauch.values():
            verbrauch = int(verbrauch)
            einz_alt_verb.append(verbrauch)

        index = 0

        for verbrauch in neuverbrauch.values():
            verbrauch -= einz_alt_verb[index]
            verbrauch = int(verbrauch)
            einz_neu_verb.append(verbrauch)
            index+= 1

    stoll_verb = mtl_verb - sum(einz_neu_verb[1:])
    tarif = 1485
    rest = tarif - mtl_verb
    einz_verb_in_proz = {}
    einz_endsummen = {}
    endsumme = 0
    einz_verbrauch = {}
    comission = 14000/len(daten["neuverbrauch"])


    if mtl_verb < tarif:

        zähler = 0
        hauptzähler = 0
        for familie, verbrauch in neuverbrauch.items():
            if zähler == hauptzähler:
                hauptzähler = verbrauch
                stoll_verb_in_proz = (stoll_verb/mtl_verb) * 100
                stoll_endsumme = (((stoll_verb + ((rest/100) * stoll_verb_in_proz)) *1.1) *310+comission)
                einz_verb_in_proz["Stoll"] = round(stoll_verb_in_proz, 1)
                einz_endsummen["Stoll"] = round(stoll_endsumme)
                einz_verbrauch["Stoll"] = stoll_verb
                continue
            else:
                verb_in_proz = ((verbrauch - altverbrauch[familie])/mtl_verb) * 100
                einz_endsumme = ((((verbrauch - altverbrauch[familie]) + ((rest/100) * verb_in_proz)) *1.1)*310+comission)
                einz_verb_in_proz[familie] = round(verb_in_proz, 1)
                einz_endsummen[familie] = round(einz_endsumme)
                einz_verbrauch[familie] = (verbrauch - altverbrauch[familie])
        print(f"\n\n\n\n\n    Der jeweilige verbrauch in prozent ist {einz_verb_in_proz}")
    else:
        zähler_0 = 0
        hauptzähler_0 = 0
        for familie, verbrauch in neuverbrauch.items():
            if zähler_0 == hauptzähler_0:
                hauptzähler_0 = verbrauch
                stoll_endsumme = ((stoll_verb * 1.1) * 310+comission)
                einz_endsummen["Stoll"] = round(stoll_endsumme)
                einz_verbrauch["Stoll"] = stoll_verb
                continue
            else:
                endsummen = (((verbrauch - altverbrauch[familie]) * 1.1) * 310+comission)
                einz_verbrauch[familie] = (verbrauch - altverbrauch[familie])
                einz_endsummen[familie] = round(endsummen)
    for einzel_endsumme in einz_endsummen.values():
        endsumme += einzel_endsumme
    print(f"\n\n    Die endsummen in Gs. sind{einz_endsummen}\n\n\n\n\n\n\n\n\n\n    Total final: Gs. {endsumme}\n\n    Consumo Individual en kWh:{einz_verbrauch}\n\n\n")

def main():
    while True:
        inp = input("Wollen sie die monantliche Stromrechnung durchführen? J|Ja N|Nein: ")
        if inp == "J":
            daten_überschreibung(neue_verbrauchsdaten())
            rechnung()
            break
        elif inp == "N":
            break
        else:
            print("\nUngültige Eingabe!\n")
            continue

main()
