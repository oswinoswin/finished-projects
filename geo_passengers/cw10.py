import requests
import pandas as pd
from pathlib import Path
import time

BDL_BASE = "https://bdl.stat.gov.pl/api/v1"
HEADERS = {
    "Accept": "application/json",
    "X-ClientId": "99105788-dab2-47c2-f06b-08dd6c852151"  # opcjonalnie
}

YEAR = 2024

VAR_POP = "LUDNOŚĆ_ID"          # liczba ludności
VAR_FIRMY_JR = "PODMIOTY_JR_ID" # podmioty J-R na 1000 ludności
VAR_BEZROBOCIE = "BEZROBOCIE_ID"# stopa bezrobocia
VAR_WYZSZE = "WYKSZT_WYZSZE_ID" # ludność z wykształceniem wyższym
VARIABLES = [VAR_POP, VAR_FIRMY_JR, VAR_BEZROBOCIE, VAR_WYZSZE]



# słownik: nazwa województwa -> kod TERYT/BDL województwa (level=2)
VOIVODESHIP_CODES = {
    "dolnośląskie": "02",
    "kujawsko-pomorskie": "04",
    "lubelskie": "06",
    "lubuskie": "08",
    "łódzkie": "10",
    "małopolskie": "12",
    "mazowieckie": "14",
    "opolskie": "16",
    "podkarpackie": "18",
    "podlaskie": "20",
    "pomorskie": "22",
    "śląskie": "24",
    "świętokrzyskie": "26",
    "warmińsko-mazurskie": "28",
    "wielkopolskie": "30",
    "zachodniopomorskie": "32",
}

def search_powiat_code(name, voivodship_name=None, year=2024, sleep=0.2):
    """
    Zwraca kod TERYT (unitId) powiatu o podanej nazwie
    oraz (opcjonalnie) w zadanym województwie.
    """
    params = {
        "name": name,
        "level": 6, #6 - gminy, 5 - powiaty
        "year": year,
        "format": "json"
    }
    url = f"{BDL_BASE}/units/search"
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    time.sleep(sleep)

    if not results:
        return None

    # jeśli nie podano województwa – bierz pierwszy wynik
    if voivodship_name is None:
        return results[0].get("id")

    # normalizacja nazwy województwa
    vname = voivodship_name.strip().lower()
    woj_code2 = VOIVODESHIP_CODES.get(vname)
    if woj_code2 is None:
        # nieznane województwo w słowniku
        return None

    # kody jednostek w BDL dla województw mają postać np. "020000000000"
    woj_full_prefix = woj_code2 + "0000"

    # filtruj po parentId lub prefiksie id (w zależności od struktury zwrotki)
    for r in results:
        parent_id = r.get("parentId") or ""
        unit_id = r.get("id") or ""

        if parent_id.startswith(woj_full_prefix) or unit_id.startswith(woj_code2):
            return unit_id

    # jeśli nic nie pasowało po województwie – zwróć pierwszy wynik
    return results[0].get("id")

def add_teryt_codes_from_excel(xlsx_in="2024.xlsx"):
    df = pd.read_excel(xlsx_in)
    df["gminaId"] = None
    for idx, row in df.iterrows():
        gmina = str(row["gmina"])
        woj = str(row["województwo"])
        code = search_powiat_code(gmina, voivodship_name=woj)
        df.at[idx, "gminaId"] = code
        print(f"{gmina} ({woj}) -> {code}")
    return df

def fetch_bdl_data_for_vars(units, variables, year=YEAR):
    rows = []
    for var in variables:
        params = {
            "unit-ids": ",".join(u for u in units if pd.notna(u)),
            "var-id": var,
            "year": year,
            "format": "json"
        }
        url = f"{BDL_BASE}/data/by-unit"
        resp = requests.get(url, headers=HEADERS, params=params)
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("results", []):
            unit_id = item.get("id")
            for val in item.get("values", []):
                rows.append({
                    "unitId": unit_id,
                    "variableId": var,
                    "year": val.get("year"),
                    "value": val.get("val")
                })
    return pd.DataFrame(rows)

def pivot_variables(df):
    mapping = {
        VAR_POP: "liczba_ludnosci",
        VAR_FIRMY_JR: "podmioty_uslugi_wyzszego_rzedu_na_1000",
        VAR_BEZROBOCIE: "stopa_bezrobocia",
        VAR_WYZSZE: "ludnosc_wyksztalcenie_wyzsze"
    }
    df["variableName"] = df["variableId"].map(mapping)
    out = df.pivot_table(
        index=["unitId", "year"],
        columns="variableName",
        values="value"
    ).reset_index()
    return out

if __name__ == "__main__":
    # print(search_powiat_code("Ustrzyki Dolne"))
    df = add_teryt_codes_from_excel()
    print(df)
    df.to_csv("2024_gminy.csv")
    # df = pd.read_csv("2024_with_codes.csv")
