import requests
from bs4 import BeautifulSoup
import tkinter as tk

url = "https://www.worldometers.info/coronavirus/" #address


def get_base_data(url_country=None):
    if url_country is None:
        main_data = requests.get(url)
    else:
        main_data = requests.get(url_country)

    soup = BeautifulSoup(main_data.text, "html.parser")
    cases = soup.find("div", class_="content-inner")
    content = cases.find_all("div", id="maincounter-wrap")
    numbers = []
    for container in content:
        value = container.find('span', class_=None)
        if value:
            numbers.append(value.get_text())

    return numbers


def get_data_for_country():
    global var_cases, var_deaths, var_recov     #global var
    country: str = country_search_name.get()
    if country:  # если значение country непустое
        url_country = url + f'/country/{country}/'
        cases, deaths, recov = get_base_data(url_country)
        var_cases.set(cases)
        var_deaths.set(deaths)
        var_recov.set(recov)
        cases_label['text'] = f"{country.capitalize()} All Cases"
        deaths_label['text'] = f"{country.capitalize()} Deaths Cases"
        recov_label['text'] = f"{country.capitalize()} Recovered Cases"


window = tk.Tk()

cases, deaths, recov = get_base_data()
var_cases = tk.StringVar(window, value=cases)
var_deaths = tk.StringVar(window, value=deaths)
var_recov = tk.StringVar(window, value=recov)

window.geometry("700x500")
window.title('Covid Tracker')
font = ("arial", 20, "bold")

banner = tk.PhotoImage(file = "covid png.png")
bannerlabel = tk.Label(window,image=banner)
bannerlabel.grid(row=4, column=0, columnspan=2)


cases_label = tk.Label(window, text="World Cases", font=font)
cases_label.grid(row=0, column=0)
deaths_label = tk.Label(window, text="World Deaths", font=font)
deaths_label.grid(row=1, column=0)
recov_label = tk.Label(window, text="World Recovered", font=font)
recov_label.grid(row=2, column=0)

cases_entry = tk.Entry(window, textvariable=var_cases, state='readonly')
deaths_entry = tk.Entry(window, textvariable=var_deaths)
recov_entry = tk.Entry(window, textvariable=var_recov)

cases_entry.grid(row=0, column=1)
deaths_entry.grid(row=1, column=1)
recov_entry.grid(row=2, column=1)

country_search_name = tk.Entry(window, width=50)
country_search_name.grid(row=3, column=0)

btn_country = tk.Button(window, text="Get data", font=font, relief="solid", command=get_data_for_country)
btn_country.grid(row=3, column=1)

window.mainloop()
