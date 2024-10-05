def cohort_m(df, customer_col, invoice_date_col):
   
    orders['InvoiceQuarter'] = ('Q' + orders['invoice_date_col'].dt.quarter.astype(str) + '/' + orders['invoice_date_col'].dt.year.astype(str))
    quarters_map = dict(zip(orders['InvoiceQuarter'].unique(), range(len(orders['InvoiceQuarter'].unique()))))
    orders['InvoiceQuarterID'] = orders['InvoiceQuarter'].map(quarters_map)

    
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
