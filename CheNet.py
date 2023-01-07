from bs4 import BeautifulSoup
from requests import *
import csv
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

year2018 = {
    'january': ['01', 31],
    'february': ['02', 28],
    'march': ['03', 31],
    'april': ['04', 30],
    'may': ['05', 31],
    'june': ['06', 30],
    'july': ['07', 31],
    'august': ['08', 31],
    'september': ['09', 30],
    'october': ['10', 31],
    'november': ['11', 30],
    'december': ['12', 31]
}

year2019 = {
    'january': ['01', 31],
    'february': ['02', 28],
    'march': ['03', 31],
    'april': ['04', 30],
    'may': ['05', 31],
    'june': ['06', 30],
    'july': ['07', 31],
    'august': ['08', 31],
    'september': ['09', 30],
    'october': ['10', 31],
    'november': ['11', 30],
    'december': ['12', 31]
}

year2020 = {
    'january': ['01', 31],
    'february': ['02', 29],
    'march': ['03', 31],
    'april': ['04', 30],
    'may': ['05', 31],
    'june': ['06', 30],
    'july': ['07', 31],
    'august': ['08', 31],
    'september': ['09', 30],
    'october': ['10', 31],
    'november': ['11', 30],
    'december': ['12', 31]
}

year2021 = {
    'january': ['01', 31],
    'february': ['02', 28],
    'march': ['03', 31],
    'april': ['04', 30],
    'may': ['05', 31],
    'june': ['06', 30],
    'july': ['07', 31],
    'august': ['08', 31],
    'september': ['09', 30],
    'october': ['10', 31],
    'november': ['11', 30],
    'december': ['12', 31]
}

year2022 = {
    'january': ['01', 31],
    'february': ['02', 28],
    'march': ['03', 31],
    'april': ['04', 30],
    'may': ['05', 31],
    'june': ['06', 30],
    'july': ['07', 31],
    'august': ['08', 12]
}

years = [year2018, year2019, year2020, year2021, year2022]
yr = 2018

x = []
y = []


def parse():
    global yr
    for i in range(len(years)):
            for j in years[i].keys():
                for d in range(years[i][j][1]):
                    if d + 1 < 10:
                        day = f'0{d + 1}'
                    else:
                        day = f'{d + 1}'
                    url = f'https://pogoda1.ru/chernovtsy-2/{day}-{years[i][j][0]}-{str(yr)}/'
                    u = get(str(url))
                    p = BeautifulSoup(u.text, 'html.parser')
                    t = str(p.find_all(class_='weather-now-temp'))
                    if t != '[]':
                        t = int(t.split('°')[0].split('>')[-1])
                        print(f'{day}-{years[i][j][0]}-{str(yr)[2:]}:', t)
                        x.append([yr, int(years[i][j][0]), int(day)])
                        y.append(t)
            yr += 1
            print(' ')


def save():
    with open('data.csv', 'w') as f:
        c = csv.writer(f)
        c.writerow(['year', 'month', 'day', 't'])
        for i in range(len(x)):
            c.writerow(x[i] + [y[i]])


def show(c):
    df = pd.read_csv('data.csv')
    d = pd.DataFrame({'year': df['year'], 'month': df['month'], 'day': df['day']})
    df['date'] = pd.to_datetime(d, dayfirst=True)
    df = df.drop(columns=['year', 'month', 'day'], axis=1)
    print(df.head())
    plt.scatter(df['date'], df['t'], color=c)


# добавляем месяц и день
df = pd.read_csv('data.csv')
for i in range(len(df['day'])):
    if df['year'][i] == 2021:
        x.append([int(df['month'][i]), int(df['day'][i])])
        y.append(df['t'][i])


dx, dy = x, y
poly_reg = PolynomialFeatures(degree=2)
X_poly = poly_reg.fit_transform(dx)
lin_reg = LinearRegression()
lin_reg.fit(X_poly, dy)
print(lin_reg.score(X_poly, dy))

plt.plot(x, y, color='blue')
plt.plot(dx, lin_reg.predict(poly_reg.fit_transform(dx)), color='red')
plt.show()

while True:
    month = int(input('Input number of month: '))
    day = int(input('Input day: '))
    print(str(round(lin_reg.predict(poly_reg.fit_transform([[month, day]]))[0]))+'°')
    q = input('quit?: ')
    if q.lower() == 'y' or q.lower() == 'yes':
        exit()
