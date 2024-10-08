import pandas as pd

def rf(df, customer_col, invoice_date_col, total_col):
    # 1. Maximum tarih (today) belirle
    today = df[invoice_date_col].max()

    # 2. RFM hesaplama
    df_rfm = df.groupby(customer_col).agg({
        invoice_date_col: lambda x: (today - x.max()).days,  # Recency
        'Invoice': lambda x: x.nunique(),  # Frequency
        total_col: 'sum'  # Monetary
    })

    # 3. Sütunları yeniden adlandır
    df_rfm.rename(columns={
        invoice_date_col: 'Recency',
        'Invoice': 'Frequency',
        total_col: 'Monetary'
    }, inplace=True)

    # 4. R, F ve M değerlerini hesapla
    df_rfm['R'] = pd.qcut(df_rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])
    df_rfm['F'] = pd.qcut(df_rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    df_rfm['M'] = pd.qcut(df_rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

    # 5. Recency, Frequency ve Monetary sütunlarını kaldır
    df_rfm.drop(['Recency', 'Frequency', 'Monetary'], axis=1, inplace=True)

    # 6. RF Skoru oluştur
    df_rfm['RF_Score'] = df_rfm['R'].astype(str) + df_rfm['F'].astype(str)

    # 7. Müşteri segmentlerini belirle
    segment_map = {
        r'[1-2][1-2]': 'low_value',
        r'[1-2][3-5]': 'at_risk',
        r'3[1-3]': 'needs_attention',
        r'[3-4][4-5]': 'loyal',
        r'4[1-3]': 'promising',
        r'5[1-3]': 'new_customers',
        r'5[4-5]': 'champions'
    }

    df_rfm['result'] = df_rfm['RF_Score'].replace(segment_map, regex=True)

    return df_rfm
