import os

from nycflights13 import flights
import pandas as pd
from tqdm import tqdm
import numpy as np

from db.models.Flights import Flights
from db.session import session_manager

parquet_file = 'flights.parquet'


# Создаем новый .parquet файл с данными из датасета flights
if not os.path.exists(f'{parquet_file}'):
    df = pd.DataFrame(flights)
    df.to_parquet('fligths.parquet')

# Создаем датафрейм, читающий .parquet файл
df = pd.read_parquet('fligths.parquet')

# Вывод первых 5 строк .parquet файла
print(pd.read_parquet('fligths.parquet').head())
df = df.replace(np.nan, None, regex=True)

# Создаем новую сессию и добавляем данные в модель бд
for index in tqdm(df.index, desc=f'Добавление данных из {parquet_file} в бд'):
    with session_manager() as session:
        session.add(Flights(**df.loc[index].to_dict()))

# Создаем сессию и проверяем сколько строк добавилось в бд
with session_manager() as session:
    print(f'В базу данных добавлено {session.query(Flights).count()} из {len(df.index)} строк '
          f'({round(session.query(Flights).count()/len(df.index)*100, 2)}%)')


