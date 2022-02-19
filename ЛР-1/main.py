import os

from timeit import default_timer as timer
from nycflights13 import flights
from tqdm import tqdm
import pandas as pd
import numpy as np

from db.models.Flights import Flights
from db.session import session_manager


def main():
    parquet_file = 'flights.parquet'

    # Создаем новый .parquet файл с данными из датасета flights
    if not os.path.exists(f'{parquet_file}'):
        df = pd.DataFrame(flights)
        df.to_parquet('fligths.parquet')

    # Создаем датафрейм, читающий .parquet файл
    df = pd.read_parquet('fligths.parquet')

    # Вывод первых 5 строк .parquet файла для проверки
    print(df.head())

    # В значениях ячеек присутствует Nan, котороне нужно поменять на None, чтобы данные добавлялись в модель без ошибок
    df = df.replace(np.nan, None, regex=True)

    # Размер части датафрейма, которая будет добавлятся в модель бд
    chunk = 1000
    start = timer()

    for index in tqdm(range(0, len(df.index), chunk), desc=f'Добавление данных из {parquet_file} в бд', unit=' items'):
        # Создаем сессию и добавляем данные в модель бд
        with session_manager() as session:
            df.iloc[index:index + chunk].to_sql(Flights.__tablename__, session.bind, if_exists='append', index=True)
            # session.add(Flights(**df.loc[index].to_dict()))
    print(f'Время выполнения переноса данных из {parquet_file} в бд: {round(timer() - start),2} секунд')

    # Создаем сессию и проверяем сколько строк добавилось в бд
    with session_manager() as session:
        print(f'В базу данных добавлено {session.query(Flights).count()} из {len(df.index)} строк '
              f'({round(session.query(Flights).count() / len(df.index) * 100, 2)}%)')


if __name__ == '__main__':
    main()
