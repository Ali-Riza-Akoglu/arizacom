def cohort_m(df, customer_col, invoice_date_col):
    # InvoiceDate sütununu trend fonksiyonuna gönder
    from .data_processing import trend
    trend_df = trend(df[invoice_date_col])
    
    # trend fonksiyonundan dönen DataFrame'deki invoice_quarter_col sütununu kullan
    df['InvoiceQuarterID'] = trend_df['InvoiceQuarter']
    
    # Her müşteri için ilk fatura çeyrek kimliğini bul
    df['CohortQuarterID'] = df.groupby(customer_col)['InvoiceQuarterID'].transform('min')
    
    # Çeyrek kimlikleriyle çeyrek isimlerini eşleştir
    unique_quarters = df['InvoiceQuarterID'].unique()
    quarters_map = dict(zip(unique_quarters, range(len(unique_quarters))))
    
    # İlk fatura çeyreğini bul ve çeyrek ismine dönüştür
    df['CohortQuarter'] = df['CohortQuarterID'].map({v: k for k, v in quarters_map.items()})
    
    # Kohort indeksini hesapla (ilk fatura ile mevcut fatura arasındaki çeyrek farkı)
    df['CohortIndex'] = df['InvoiceQuarterID'] - df['CohortQuarterID']
    
    return df
