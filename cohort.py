def cohort_m(df, customer_col, invoice_date_col):
   
    df['InvoiceQuarter'] = ('Q' + df['invoice_date_col'].dt.quarter.astype(str) + '/' + df['invoice_date_col'].dt.year.astype(str))
    quarters_map = dict(zip(df['InvoiceQuarter'].unique(), range(len(df['InvoiceQuarter'].unique()))))
    df['InvoiceQuarterID'] = df['InvoiceQuarter'].map(quarters_map)

    
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
