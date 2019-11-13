import urllib.request as q
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date as dt


def set_url(base_url):
    """
        各ページのURLを生成

    :param base_url: 基本となるURL　これを加工
    :return: 　加工されたURL
    """
    urls = [base_url+str(i) for i in range(1, 11)]
    return urls


def getData():
    base_url = "https://kabutan.jp/stock/kabuka?code=6093&page="
    urls = set_url(base_url)
    # データを格納する空リストを設置
    write_data = []
    for url in urls:
        res = q.urlopen(url)
        soup = BeautifulSoup(res, "html.parser")
        date = [i.get_text() for i in soup.select("#stock_kabuka_table > table.stock_kabuka1 > tbody > tr > th")]
        start = [i.get_text().replace(',', '') for i in soup.select("#stock_kabuka_table > table.stock_kabuka1 > "
                                                                    "tbody > tr > td:nth-child(2)")]
        max_p = [i.get_text().replace(',', '') for i in soup.select("#stock_kabuka_table > table.stock_kabuka1 > "
                                                                    "tbody > tr > td:nth-child(3)")]
        min_p = [i.get_text().replace(',', '') for i in soup.select("#stock_kabuka_table > table.stock_kabuka1 > "
                                                                    "tbody > tr > td:nth-child(4)")]
        end = [i.get_text().replace(',', '') for i in soup.select("#stock_kabuka_table > table.stock_kabuka1 > "
                                                                  "tbody > tr > td:nth-child(5)")]
        hi = [i.get_text().replace(',', '') for i in soup.select("#stock_kabuka_table > table.stock_kabuka1 > "
                                                                 "tbody > tr > td:nth-child(6)")]
        hiper = [i.get_text().replace(',', '') for i in soup.select("#stock_kabuka_table > table.stock_kabuka1 > "
                                                                    "tbody > tr > td:nth-child(7)")]
        daka = [i.get_text().replace(',', '') for i in soup.select("#stock_kabuka_table > table.stock_kabuka1 > "
                                                                   "tbody > tr > td:nth-child(8)")]
        week = [i.replace('19/', '2019/') for i in date]
        ss = [z.split('/') for z in week]
        week_data = []
        week_name_list = '月火水木金土日'
        for v in ss:
            d = dt(int(v[0]), int(v[1]), int(v[2]))
            date_week = week_name_list[d.weekday()]
            week_data.append(date_week)
        zip_date = list(zip(date, week_data))
        new_date = [','.join(i).replace(',', '(')+')' for i in zip_date]
        csv_data = list(zip(new_date, week_data, start, max_p, min_p, end, hi, hiper, daka))
        write_data += [list(i) for i in csv_data]

    # CSV書き出し
    df = pd.DataFrame(write_data)
    df.to_csv("u_data.csv",
        header=['date', 'week','start', 'max_p', 'min_p', 'end', 'hi', 'hiper', 'daka'],
        index = False,
        encoding='UTF-8'
    )
    return True