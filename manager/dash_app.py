import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
from members.models import Order  # ปรับเปลี่ยนชื่อแอปของคุณ

# สร้างแอป Dash
app = DjangoDash('SalesDashboard')

# ดึงข้อมูลจากโมเดล Order
orders = Order.objects.all().values('product_category__name', 'appt_date', 'total_price')
df = pd.DataFrame(list(orders))

# แปลงข้อมูลวันที่
df['year'] = df['appt_date'].dt.year
df['month'] = df['appt_date'].dt.month

# จัดกลุ่มข้อมูลตามหมวดหมู่ ปี และเดือน
grouped_df = df.groupby(['product_category__name', 'year', 'month']).agg({'total_price': 'sum'}).reset_index()

app.layout = html.Div([
    dcc.RangeSlider(
        id='year-slider',
        min=grouped_df['year'].min(),
        max=grouped_df['year'].max(),
        value=[grouped_df['year'].min(), grouped_df['year'].max()],
        marks={str(year): str(year) for year in grouped_df['year'].unique()},
        step=None
    ),
    dcc.Graph(id='category-sales-graph')
])

@app.callback(
    dash.dependencies.Output('category-sales-graph', 'figure'),
    [dash.dependencies.Input('year-slider', 'value')]
)
def update_graph(selected_year):
    filtered_df = grouped_df[(grouped_df.year >= selected_year[0]) & (grouped_df.year <= selected_year[1])]
    fig = px.bar(filtered_df, x="product_category__name", y="total_price", barmode="group", color="month")
    fig.update_layout(
        title='จำนวนสินค้าที่ขายได้ในแต่ละหมวดหมู่',
        xaxis_title='หมวดหมู่สินค้า',
        yaxis_title='จำนวนสินค้า',
        font=dict(family='Sarabun, sans-serif', size=11, color='black')
    )
    return fig
