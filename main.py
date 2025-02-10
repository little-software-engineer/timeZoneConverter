import pytz
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import relativedelta


class VremenskaZonaKonverter:
    def __init__(self):
        self.sve_zone = pytz.all_timezones
        self.organizovane_zone = self._organizuj_zone()

    def _organizuj_zone(self):
        zone_po_regionima = {
            'Europe': [],
            'America': [],
            'Asia': [],
            'Africa': [],
            'Australia': [],
            'Pacific': [],
            'Indian': [],
            'Atlantic': [],
            'Antarctica': []
        }

        for zona in self.sve_zone:
            region = zona.split('/')[0]
            if region in zone_po_regionima:
                zone_po_regionima[region].append(zona)

        return zone_po_regionima

    def prikazi_meni(self):
        print("\n=== KONVERTER VREMENSKIH ZONA ===")
        print("1. Prikaži trenutno vreme u zoni")
        print("2. Konvertuj specifično vreme")
        print("3. Prikaži razliku između zona")
        print("4. Informacije o letnjem računanju vremena")
        print("5. Izlaz")
        return input("Izaberite opciju (1-5): ")

    def prikazi_zone(self):
        print("\nDostupne vremenske zone:")
        for region, zone in self.organizovane_zone.items():
            if zone:  # Prikazujemo samo regione koji imaju zone
                print(f"\n=== {region.upper()} ===")
                for i, zona in enumerate(zone, 1):
                    print(f"{i}. {zona}")

    def izaberi_zonu(self, poruka="Izaberite region i zonu: "):
        print("\nDostupni regioni:")
        regioni = list(self.organizovane_zone.keys())
        for i, region in enumerate(regioni, 1):
            print(f"{i}. {region}")

        try:
            izbor_regiona = int(input("\nIzaberite broj regiona: ")) - 1
            if 0 <= izbor_regiona < len(regioni):
                region = regioni[izbor_regiona]
                zone = self.organizovane_zone[region]

                print(f"\nZone u regionu {region}:")
                for i, zona in enumerate(zone, 1):
                    print(f"{i}. {zona}")

                izbor_zone = int(input("Izaberite broj zone: ")) - 1
                if 0 <= izbor_zone < len(zone):
                    return zone[izbor_zone]
        except ValueError:
            pass

        print("Nevažeći izbor!")
        return None

    def trenutno_vreme_u_zoni(self):
        zona = self.izaberi_zonu()
        if zona:
            try:
                tz = pytz.timezone(zona)
                trenutno = datetime.now(pytz.UTC).astimezone(tz)
                print(f"\nTrenutno vreme u {zona}:")
                print(trenutno.strftime("%Y-%m-%d %H:%M:%S %Z"))
            except Exception as e:
                print(f"Greška pri dobavljanju vremena: {e}")
        else:
            print("Nevažeća zona!")

    def konvertuj_specificno_vreme(self):
        izvorna_zona = self.izaberi_zonu("Izaberite izvornu zonu: ")
        if not izvorna_zona:
            print("Nevažeća izvorna zona!")
            return

        ciljna_zona = self.izaberi_zonu("Izaberite ciljnu zonu: ")
        if not ciljna_zona:
            print("Nevažeća ciljna zona!")
            return

        try:
            unos = input("Unesite datum i vreme (npr. 2024-03-20 15:30): ")
            vreme = parser.parse(unos)

            izvorna_tz = pytz.timezone(izvorna_zona)
            vreme_sa_zonom = izvorna_tz.localize(vreme)

            ciljna_tz = pytz.timezone(ciljna_zona)
            konvertovano = vreme_sa_zonom.astimezone(ciljna_tz)

            print(f"\nVreme u {izvorna_zona}: {vreme_sa_zonom.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"Vreme u {ciljna_zona}: {konvertovano.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        except Exception as e:
            print(f"Greška pri konverziji vremena: {e}")

    def razlika_izmedju_zona(self):
        zona1 = self.izaberi_zonu("Izaberite prvu zonu: ")
        zona2 = self.izaberi_zonu("Izaberite drugu zonu: ")

        if zona1 and zona2:
            try:
                tz1 = pytz.timezone(zona1)
                tz2 = pytz.timezone(zona2)

                trenutno_utc = datetime.now(pytz.UTC)
                vreme1 = trenutno_utc.astimezone(tz1)
                vreme2 = trenutno_utc.astimezone(tz2)

                razlika_offset = (vreme2.utcoffset() - vreme1.utcoffset()).total_seconds() / 3600

                if razlika_offset > 0:
                    print(f"\n{zona2} je {abs(razlika_offset)} sati ispred {zona1}")
                elif razlika_offset < 0:
                    print(f"\n{zona2} je {abs(razlika_offset)} sati iza {zona1}")
                else:
                    print(f"\n{zona1} i {zona2} su u istoj vremenskoj zoni")

                print(f"\nTrenutno vreme u {zona1}: {vreme1.strftime('%H:%M')}")
                print(f"Trenutno vreme u {zona2}: {vreme2.strftime('%H:%M')}")

            except Exception as e:
                print(f"Greška pri računanju razlike: {e}")
        else:
            print("Nevažeće zone!")

    def informacije_o_letnjem_racunanju(self):
        zona = self.izaberi_zonu()
        if zona:
            try:
                tz = pytz.timezone(zona)
                trenutno = datetime.now(tz)

                datum_leto = datetime(trenutno.year, 7, 1)
                datum_zima = datetime(trenutno.year, 1, 1)

                vreme_leto = tz.localize(datum_leto)
                vreme_zima = tz.localize(datum_zima)

                koristi_dst = vreme_leto.dst().total_seconds() != vreme_zima.dst().total_seconds()

                print(f"\nInformacije o letnjem računanju vremena za {zona}:")

                if koristi_dst:
                    trenutno_vreme = tz.localize(datetime.now())
                    dst_status = "letnje" if trenutno_vreme.dst().total_seconds() > 0 else "zimsko"

                    print(f"Ova zona KORISTI letnje računanje vremena")
                    print(f"Trenutno je {dst_status} računanje vremena")
                    print(f"DST pomak: {trenutno_vreme.dst()}")

                    if zona.startswith('Europe'):
                        godina = trenutno.year

                        mart_datum = datetime(godina, 3, 31)
                        while mart_datum.weekday() != 6:
                            mart_datum -= relativedelta(days=1)

                        okt_datum = datetime(godina, 10, 31)
                        while okt_datum.weekday() != 6:
                            okt_datum -= relativedelta(days=1)

                        mart_promena = tz.localize(mart_datum.replace(hour=2))
                        okt_promena = tz.localize(okt_datum.replace(hour=3))

                        trenutno_vreme = datetime.now(tz)

                        if trenutno_vreme < mart_promena:
                            print(
                                f"Sledeća promena (početak letnjeg vremena): {mart_datum.strftime('%d.%m.%Y')} u 02:00")
                        elif trenutno_vreme < okt_promena:
                            print(f"Sledeća promena (kraj letnjeg vremena): {okt_datum.strftime('%d.%m.%Y')} u 03:00")
                        else:
                            sledeca_godina = godina + 1
                            mart_datum = datetime(sledeca_godina, 3, 31)
                            while mart_datum.weekday() != 6:
                                mart_datum -= relativedelta(days=1)
                            print(
                                f"Sledeća promena (početak letnjeg vremena): {mart_datum.strftime('%d.%m.%Y')} u 02:00")
                    else:
                        print("Datumi promene variraju za ovu vremensku zonu.")
                else:
                    print(f"Ova zona NE KORISTI letnje računanje vremena")

            except Exception as e:
                print(f"Greška pri dobavljanju informacija o DST: {e}")
        else:
            print("Nevažeća zona!")


def main():
    print("=== DOBRODOŠLI U KONVERTER VREMENSKIH ZONA ===")
    konverter = VremenskaZonaKonverter()

    while True:
        izbor = konverter.prikazi_meni()

        if izbor == '1':
            konverter.trenutno_vreme_u_zoni()
        elif izbor == '2':
            konverter.konvertuj_specificno_vreme()
        elif izbor == '3':
            konverter.razlika_izmedju_zona()
        elif izbor == '4':
            konverter.informacije_o_letnjem_racunanju()
        elif izbor == '5':
            print("\nHvala što ste koristili konverter vremenskih zona!")
            break
        else:
            print("Nevažeća opcija! Molimo izaberite broj između 1 i 5.")

        input("\nPritisnite Enter za nastavak...")


if __name__ == "__main__":
    main()