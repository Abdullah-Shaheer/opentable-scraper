import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


def send_request(ur):
    soup = None
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    for i in range(3):
        try:
            # print(f"Trying {i + 1} time.")
            response = requests.get(ur, headers=headers)
            if response.status_code == 200:
                # print('Response success.')
                soup = BeautifulSoup(response.text, 'lxml')
                break
            else:
                print("Trying Again.")
                continue
        except:
            print('Request Failed.')
    return soup


def get_data(soup):
    data = []
    cards = soup.find_all("div", class_="card-body")

    for card in cards:
        try:
            title = card.find('h3', class_='card-title-wrap--deal-single').text.strip()
        except AttributeError:
            title = None

        try:
            location = card.find("div", class_="card-location-icon--deal-single").text.strip()
        except AttributeError:
            location = None

        try:
            rating = card.find('div', class_='card-rating--deal-single').text.strip()
        except AttributeError:
            rating = None

        try:
            image_div = card.find_parent('div').find("div", class_='card-thumbnail')
            image_url = image_div.find('img')['src'] if image_div else None
        except AttributeError:
            image_url = None

        try:
            footer = card.find_parent('div').find("div", class_='card-footer')
            link = footer.find('a', class_='card-link stretched-link--invisible')['href'] if footer else None
        except AttributeError:
            link = None
        data.append({
            "Title": title,
            "Location": location,
            "Rating": rating,
            "Image URL": image_url,
            "Link": link,
        })

    return data


def main():
    ur = "https://www.opentable.com/c/top-restaurants/top-100/"
    sou = send_request(ur)
    data = get_data(sou)
    df = pd.DataFrame(data)
    df.to_excel('top_100.xlsx', index=False)
    df.to_csv('top_100.csv', index=False)
    with open('top_100.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print("Scraping completed and output file Generated.")


def info():
    print('This scraper has been built by github.com/Abdullah-Shaheer')
    print("[+] Scrapes the top 100 restaurant's information from OpenTable")
    print('[+] Excel, CSV, JSON output')
    print('Starting scraping.')


if __name__ == "__main__":
    info()
    main()
