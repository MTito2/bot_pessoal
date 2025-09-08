import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_FINANCES_MODULE_PATH
from general_functions import actually_date, read_json

IMG_BARS_PATH = FILES_FINANCES_MODULE_PATH / "expenses_graph_bar.png"
IMG_PIE_PATH = FILES_FINANCES_MODULE_PATH / "expenses_graph_pie.png"

def generate_chart_pie(year_month: str):
    """Gera e salva um gráfico de pizza com a proporção de gastos por categoria.

    Recebe o período informado, filtra as despesas correspondentes, 
    calcula os valores por categoria e salva a imagem do gráfico.

    Args:
        year_month (str): Período no formato 'mm/yyyy' usado para filtrar despesas.
    """

    expenses = read_json(FILES_FINANCES_MODULE_PATH, "expenses.json")
    date = actually_date()

    df_filtered = pd.DataFrame(expenses)
    df_filtered['date_time'] = pd.to_datetime(df_filtered['date_time'], dayfirst=True, errors='coerce')
    df_filtered = df_filtered[df_filtered['date_time'].dt.to_period('M') == year_month]

    df_filtered['value'] = pd.to_numeric(df_filtered['value'], errors='coerce')
    category_sum = df_filtered.groupby('category')['value'].sum()

    def func(pct, allvals):
        absolute = pct/100.*sum(allvals)
        return f"{pct:.1f}%\nR$ {absolute:.2f}"

    colors = sns.color_palette("muted")[0:len(category_sum)]
    sns.set_style("dark") 
    sns.set_context("paper") 

    plt.figure(figsize=(14, 7))
    plt.pie(category_sum,
            labels=category_sum.index,
            autopct=lambda pct: func(pct, category_sum),
            colors=colors,
            startangle=90)
    
    plt.title("Proporção de gastos por categoria")
    plt.figtext(0.5, 0.01, f"Período: {year_month}", ha='center', fontsize=10)
    plt.figtext(0.9, 0.01, f"Emitido em: {date}", ha='center', fontsize=10)

    plt.tight_layout()
    plt.savefig(IMG_PIE_PATH, dpi=300)
    plt.close()

def generate_chart_daily_bars(year_month: str):
    """Gera e salva um gráfico de barras mostrando gastos diários no período informado.

    Recebe o período informado, filtra as despesas correspondentes, 
    agrupa os valores por dia e salva a imagem do gráfico com os totais em cada barra.

    Args:
        year_month (str): Período no formato 'mm/yyyy' usado para filtrar despesas.
    """

    expenses = read_json(FILES_FINANCES_MODULE_PATH, "expenses.json")
    date = actually_date()

    df_filtered = pd.DataFrame(expenses)
    df_filtered['date_time'] = pd.to_datetime(df_filtered['date_time'], dayfirst=True, errors='coerce')
    df_filtered = df_filtered[df_filtered['date_time'].dt.to_period('M') == year_month]

    df_filtered['value'] = pd.to_numeric(df_filtered['value'], errors='coerce')
    df_filtered['date'] = df_filtered['date_time'].dt.date

    daily_sum = df_filtered.groupby('date')['value'].sum().reset_index()

    plt.figure(figsize=(14,7))
    bars = sns.barplot(data=daily_sum, x='date', y='value', color="#0D1B2A")

    for bar in bars.patches:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 2, f"R$ {height:.2f}", ha='center', va='bottom')

    plt.title("Gastos por dia")
    plt.ylabel("Valor gasto (R$)")
    plt.xlabel("")
    plt.xticks(rotation=25)

    plt.figtext(0.5, 0.01, f"Período: {year_month}", ha='center', fontsize=10)
    plt.figtext(0.93, 0.01, f"Emitido em: {date}", ha='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(IMG_BARS_PATH, dpi=300)
    plt.close()