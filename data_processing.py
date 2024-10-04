# arizacom/data_processing.py

import pandas as pd

def trend(order_purchase_timestamp):
    # order_purchase_timestamp'ı datetime formatına çevir
    order_purchase_timestamp = pd.to_datetime(order_purchase_timestamp)

    orders = pd.DataFrame({'order_purchase_timestamp': order_purchase_timestamp})

    # Tarih özelliklerini çıkarma
    orders['order_purchase_year'] = orders['order_purchase_timestamp'].dt.year
    orders['order_purchase_month'] = orders['order_purchase_timestamp'].dt.month
    orders['order_purchase_month_name'] = orders['order_purchase_timestamp'].dt.strftime('%b')
    orders['order_purchase_year_month'] = orders['order_purchase_timestamp'].dt.strftime('%Y%m')
    orders['order_purchase_date'] = orders['order_purchase_timestamp'].dt.strftime('%Y%m%d')
    orders['order_purchase_day'] = orders['order_purchase_timestamp'].dt.day
    orders['order_purchase_dayofweek'] = orders['order_purchase_timestamp'].dt.dayofweek
    orders['order_purchase_dayofweek_name'] = orders['order_purchase_timestamp'].dt.strftime('%a')
    orders['order_purchase_hour'] = orders['order_purchase_timestamp'].dt.hour

    orders['InvoiceQuarter'] = ('Q' + orders['InvoiceDate_DT'].dt.quarter.astype(str) + '/' + orders['order_purchase_timestamp'].dt.year.astype(str))
    quarters_map = dict(zip(orders['InvoiceQuarter'].unique(), range(len(orders['InvoiceQuarter'].unique()))))
    orders['InvoiceQuarterID'] = orders['InvoiceQuarter'].map(quarters_map)


    # Saat dilimlerine ayırma
    hours_bins = [-0.1, 6, 12, 18, 24]  # 23 yerine 24
    hours_labels = ['Dawn', 'Morning', 'Afternoon', 'Night']
    orders['order_purchase_time_day'] = pd.cut(orders['order_purchase_hour'], bins=hours_bins, labels=hours_labels)

    # Mevsim belirleme
    order_season_agg = {
        'Spring': ['Mar', 'Apr', 'May'],
        'Summer': ['Jun', 'Jul', 'Aug'],
        'Autumn': ['Sep', 'Oct', 'Nov'],
        'Winter': ['Dec', 'Jan', 'Feb']
    }

    def season_agg(s):
        for season, months in order_season_agg.items():
            if s in months:
                return season
        return None

    orders['order_purchase_season'] = orders['order_purchase_month_name'].apply(season_agg)

    return orders