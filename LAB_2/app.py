#!/usr/bin/env python3
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def fetch_exchange_rates():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        rates_df = pd.DataFrame([
            {'currency': curr, 'rate_to_usd': rate}
            for curr, rate in data['rates'].items()
        ])
        print("Загружены курсы валют (первые 5):")
        print(rates_df.head(5).to_string(index=False))
        return rates_df
    except Exception as e:
        print(f"Ошибка загрузки курсов: {e}")
        return pd.DataFrame()

def generate_supply_chain_data(n=150):
    routes = ['Moscow-SPb', 'Berlin-Paris', 'Shanghai-LA', 'Dubai-Mumbai', 'NYC-Chicago']
    transports = ['truck', 'train', 'ship', 'air']
    return pd.DataFrame({
        'route': [random.choice(routes) for _ in range(n)],
        'transit_hours': np.random.uniform(2, 120, n),
        'cost_usd': np.random.uniform(100, 5000, n),
        'cargo_weight_kg': np.random.uniform(50, 20000, n),
        'transport_type': [random.choice(transports) for _ in range(n)],
        'date': [datetime.now() - timedelta(days=random.randint(0, 30)) for _ in range(n)]
    })

def main():
    print("Запуск Supply Chain Analytics...")
    rates = fetch_exchange_rates()
    df = generate_supply_chain_data()

    print("\n" + "="*50)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("="*50)
    print(f"Всего записей: {len(df)}")
    print(f"Период: {df['date'].min().date()} — {df['date'].max().date()}")

    for col, label in [('cost_usd','Стоимость'), ('transit_hours','Время в пути'), ('cargo_weight_kg','Вес груза')]:
        mx = df.loc[df[col].idxmax()]
        mn = df.loc[df[col].idxmin()]
        print(f"\n{label}:")
        print(f"  MAX: {mx[col]:.2f} | {mx['route']} ({mx['transport_type']})")
        print(f"  MIN: {mn[col]:.2f} | {mn['route']} ({mn['transport_type']})")

    print(f"\n Средняя стоимость по транспорту:")
    print(df.groupby('transport_type')['cost_usd'].mean().sort_values(ascending=False).round(2).to_string())
    print("\n Готово!")

if __name__ == '__main__':
    main()
