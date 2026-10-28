import flet as ft
import pandas as pd
import joblib
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="logs.txt",
    filemode="a",  # dopisuje do pliku
)


model = joblib.load("../model.pkl")
df = pd.read_csv("../../data/all_cars_cleaned.csv")

# Zakresy do walidacji
year_min, year_max = df["Year"].min(), df["Year"].max()
mileage_min, mileage_max = df["Mileage_km"].min(), df["Mileage_km"].max()
power_min, power_max = df["real_power_hp_din"].min(), df["real_power_hp_din"].max()

def main(page: ft.Page):
    page.title = "Car Price Predictor"
    page.scroll = ft.ScrollMode.AUTO
    page.window_min_width = 400
    page.window_width = 500
    page.padding = 20

    result = ft.Text("Wprowadź dane samochodu, aby uzyskać prognozowaną cenę.", size=16)


    fuel = ft.Dropdown(label="Paliwo", options=[ft.dropdown.Option(v) for v in sorted(df['Fuel'].dropna().unique())], width=400)
    gearbox = ft.Dropdown(label="Skrzynia biegów", options=[ft.dropdown.Option(v) for v in sorted(df['Gearbox'].dropna().unique())], width=400)
    type = ft.Dropdown(label="Rodzaj pojazdu", options=[ft.dropdown.Option(v) for v in sorted(df['Type'].dropna().unique())], width=400)

    year = ft.TextField(label=f"Rok produkcji ({year_min}-{year_max})", width=400, keyboard_type=ft.KeyboardType.NUMBER)
    mileage = ft.TextField(label=f"Przebieg (km) ({mileage_min}-{mileage_max})", width=400, keyboard_type=ft.KeyboardType.NUMBER)
    power = ft.TextField(label=f"Moc KM ({power_min}-{power_max})", width=400, keyboard_type=ft.KeyboardType.NUMBER)

    # Walidatory zakresów
    def validate_range(textfield, value, min_val, max_val):
        try:
            v = int(value)
            if v < min_val or v > max_val:
                textfield.border_color = "red"
            else:
                textfield.border_color = None
        except:
            textfield.border_color = "red"
        page.update()

    year.on_change = lambda e: validate_range(year, year.value, year_min, year_max)
    mileage.on_change = lambda e: validate_range(mileage, mileage.value, mileage_min, mileage_max)
    power.on_change = lambda e: validate_range(power, power.value, power_min, power_max)

    def predict_price(e):
        try:
            y = int(year.value)
            m = int(mileage.value)
            p = int(power.value)

            if not (year_min <= y <= year_max):
                result.value = f"Błąd: Rok poza zakresem {year_min}-{year_max}"
                return
            if not (mileage_min <= m <= mileage_max):
                result.value = f"Błąd: Przebieg poza zakresem {mileage_min}-{mileage_max}"
                return
            if not (power_min <= p <= power_max):
                result.value = f"Błąd: Moc poza zakresem {power_min}-{power_max}"
                return

            input_data = pd.DataFrame([{
                'Fuel': fuel.value,
                'Gearbox': gearbox.value,
                'Type': type.value,
                'Year': y,
                'Mileage_km': m,
                'real_power_hp_din': p,
            }])
            price_pred = model.predict(input_data)[0]
            result.value = f"Szacowana cena: {round(price_pred)} EUR"
            logging.info(
                f"Input: year={y}, mileage={m}, power={p}, fuel={fuel.value}, gearbox={gearbox.value}, type={type.value}")
            logging.info(f"Prediction result: {round(price_pred)} EUR")

        except Exception as ex:
            result.value = f"Błąd: {ex}"
            logging.error(f"Prediction failed: {ex}")

        page.update()

    predict_btn = ft.ElevatedButton("Oblicz cenę", on_click=predict_price, width=200)

    page.add(
        ft.Column([
            ft.Text("🧮 Przewidywanie ceny samochodu", size=22, weight="bold", text_align=ft.TextAlign.CENTER),
            fuel,
            gearbox,
            type,
            year,
            mileage,
            power,
            predict_btn,
            result
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    )
# ft.app(main)
ft.app(target=main, view=ft.WEB_BROWSER)
