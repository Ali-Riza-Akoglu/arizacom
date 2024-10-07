import pandas as pd
import plotly.graph_objects as go
def cohort(df, customer_id, invoice_date):
    df['InvoiceQuarter'] = ('Q' + df[invoice_date].dt.quarter.astype(str) + 
                            '/' + df[invoice_date].dt.year.astype(str))
    
    quarters_map = dict(zip(df['InvoiceQuarter'].unique(), 
                            range(len(df['InvoiceQuarter'].unique()))))
    
    df['InvoiceQuarterID'] = df['InvoiceQuarter'].map(quarters_map)
    df['CohortQuarterID'] = df.groupby(customer_id)['InvoiceQuarterID'].transform('min')
    df['CohortQuarter'] = df['CohortQuarterID'].map(dict(zip(quarters_map.values(), quarters_map.keys())))
    df['CohortIndex'] = df['InvoiceQuarterID'] - df['CohortQuarterID']
    
    cohort_retention = df.groupby(['CohortQuarterID', 'CohortIndex'])[customer_id].apply(pd.Series.nunique).reset_index()
    cohort_retention.rename(columns={customer_id: 'Customer Count'}, inplace=True)
    
    cohort_retention_count = cohort_retention.pivot_table(index='CohortQuarterID', 
                                                          columns='CohortIndex', 
                                                          values='Customer Count')
    cohort_retention_count['CohortQuarter'] = cohort_retention_count.index.map(dict(zip(quarters_map.values(), 
                                                                                        quarters_map.keys())))
    cohort_retention_count = cohort_retention_count.set_index('CohortQuarter')
    cohort_size = cohort_retention_count.iloc[:, 0]
    retention = cohort_retention_count.divide(cohort_size, axis=0)
    retention = (retention * 100).round(2)
    retention = retention.iloc[::-1]
    
    fig = go.Figure(data=go.Heatmap(
                    z=retention,
                    y=retention.index,
                    colorscale='Greens',
                    text=retention,
                    texttemplate="%{text}%",
                    colorbar_title='Retention Rate, %',
                    xgap=3,
                    ygap=3))
    
    fig.update_xaxes(side="top")
    
    fig.update_layout(title="Cohort Analysis: Retention Rate",
                      xaxis_title="Cohorts",
                      yaxis_title="Quarters",
                      title_x=0.5,
                      title_y=0.99,
                      plot_bgcolor='white')
    
    fig.show()