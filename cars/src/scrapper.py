import pandas as pd
import requests
import time
import bs4


url = 'https://www.autosphere.be/en/car?size=24&from=0' #po 24 samochody na stronie, max 1032
base_link = "https://www.autosphere.be"

def get_car_details(detail_url):
    print(detail_url)
    car_page = requests.get(detail_url)
    soup = bs4.BeautifulSoup(car_page.text, 'html.parser')
    ul_tag = soup.find("ul", {"class": "single-vehicle-description__tab-pane__list"})
    details = dict()

    for el in ul_tag.find_all("li"):

        prop = el.find("span", {"class": {"single-vehicle-description__tab-pane__prop"}})
        value = el.find("span", {"class": {"single-vehicle-description__tab-pane__value"}})
        details[prop.text.strip().replace(" :","")] = value.text.strip()

    equipments_tag = soup.find("ul", {"class": "single-vehicle-description__tab-pane__list-checks single-vehicle-description__tab-pane__list--see-more list-checks col-lg-9"})
    equipments_list = None
    if equipments_tag:
        equipments_list = []
        for el in equipments_tag.find_all("li"):
            equipments_list.append(el.text)
    details["equipments"] = equipments_list
    return details




def download_sites():
    links = []
    for i in range(40,52):
        print(i)
        url = f"https://www.autosphere.be/en/car?size=24&from={i*24}"
        req = requests.get(url)

        soup = bs4.BeautifulSoup(req.text, 'html.parser')

        details = soup.find_all("a", {"class": "ss_link"})
        tmp_links =  [base_link + x.get("href") for x in details]
        links += tmp_links

        car_df = pd.DataFrame()
        for link in tmp_links:
            s = pd.Series(get_car_details(link))
            car_df = pd.concat([car_df, s.to_frame().T], ignore_index=True)
        car_df.to_csv(f"../data/{i}.csv", index=False)
        time.sleep(2)


    return links


if __name__ == "__main__":
    # links = download_sites()

    df = pd.DataFrame()
    for i in range(0, 52):
         print(i)
         tmp = pd.read_csv(f"../data/{i}.csv")
         df = pd.concat([df, tmp], ignore_index=True)
    df = df.drop(df.columns[0], axis=1)
    df.to_csv("../data/all_cars.csv")
