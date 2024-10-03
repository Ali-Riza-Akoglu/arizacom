# arizacom/visualization.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings

def plot_ecommerce_analysis(order_purchase_timestamp, order_id_column=None):
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)

    # İlk fonksiyon olan extract_time_features'i burada çağırıyoruz
    from .data_processing import extract_time_features
    orders = extract_time_features(order_purchase_timestamp)

    # Eğer order_id sütunu verilmişse, onu kullan
    if order_id_column is not None:
        orders['order_id'] = orders[order_id_column]
    else:
        # Benzersiz order_id oluşturma
        orders['order_id'] = range(1, len(orders) + 1)

    # NaN ve inf değerlerini temizleme
    orders.replace([float('inf'), -float('inf')], pd.NA, inplace=True)  # inf değerleri pd.NA ile değiştirilir
    orders.dropna(inplace=True)  # NaN değerleri düşürülür

    # Zaman serisine göre sipariş miktarlarını hesaplama
    orders_count = orders.groupby('order_purchase_year_month').agg({'order_id': 'count'}).reset_index()

    # Şekli oluşturma ve GridSpec ayarları
    fig = plt.figure(constrained_layout=True, figsize=(15, 10))
    gs = GridSpec(3, 2, figure=fig)

    # Alt grafiklerin yerleşimi
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, 0])
    ax3 = fig.add_subplot(gs[1, 1])
    ax4 = fig.add_subplot(gs[2, 0])
    ax5 = fig.add_subplot(gs[2, 1])

    # Zaman serisine göre sipariş miktarları
    sns.lineplot(x='order_purchase_year_month', y='order_id', data=orders_count, ax=ax1)
    sns.barplot(x='order_purchase_year_month', y='order_id', data=orders_count, ax=ax1, alpha=0.1)

    # Haftanın günlerine göre siparişler
    day_order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    sns.countplot(x='order_purchase_dayofweek_name', data=orders, order=day_order, ax=ax2)

    # Günün saatlerine göre siparişler
    sns.countplot(x='order_purchase_time_day', data=orders, ax=ax3)

    # Mevsimlere göre siparişler
    sns.countplot(x='order_purchase_season', data=orders, ax=ax4)

    # Saatlere göre siparişler
    sns.countplot(x='order_purchase_hour', data=orders, ax=ax5)

    # Dikey eksen için görünüm ayarları
    for ax in [ax1, ax2, ax3, ax4, ax5]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    plt.tight_layout()  # Uyarıyı önlemek için layout ayarlarını burada yapıyoruz
    plt.show()