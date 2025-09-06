import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import FILES_STUDY_MODULE_PATH
from modules.study_module.functions_study import read_json, actually_date

registers_path = FILES_STUDY_MODULE_PATH / "registers.json"
IMG_BARS_PATH = FILES_STUDY_MODULE_PATH / "time_study_graph_bar.png"
IMG_BUBBLE_PATH = FILES_STUDY_MODULE_PATH / "time_study_graph_bubble.png"

def generate_chart_bars(year_month: str):
    """Gera e salva gráfico de barras do tempo total de estudo por dia.

    Args:
        year_month (str): Período no formato 'mm/yyyy'.
    """

    registers = read_json(registers_path)
    date = actually_date()

    df_filtered = pd.DataFrame(registers)
    df_filtered['date_time'] = pd.to_datetime(df_filtered['date_time'], dayfirst=True, errors='coerce')
    df_filtered = df_filtered[df_filtered['date_time'].dt.to_period('M') == year_month]

    df_filtered['date'] = df_filtered['date_time'].dt.date
    daily_duration = df_filtered.groupby('date')['duration'].sum().reset_index()

    colors = ['#FF4C4C' if dur < 60 else '#4CAF50' for dur in daily_duration['duration']]

    sns.set_style("ticks")
    plt.figure(figsize=(14, 7))
    bars = sns.barplot(data=daily_duration, x='date', y='duration', palette=colors, hue='date', legend=False)
    plt.title("Tempo total de estudo por dia")
    plt.figtext(0.1, 0.98, f"Período: {year_month}", ha='center', fontsize=10)
    plt.figtext(0.25, 0.98, f"Emitido em: {date}", ha='center', fontsize=10)
    plt.xlabel("")
    plt.ylabel("Duração (minutos)")
    plt.xticks(rotation=45)

    for bar in bars.patches:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig(IMG_BARS_PATH, dpi=300)
    plt.close()

def generate_chart_bubble(year_month: str):
    """Gera e salva gráfico de bolhas de estudo por dia e horário.

    Args:
        year_month (str): Período no formato 'mm/yyyy'.
    """
  
    registers = read_json(registers_path)
    date = actually_date()

    df_filtered = pd.DataFrame(registers)
    df_filtered['date_time'] = pd.to_datetime(df_filtered['date_time'], dayfirst=True, errors='coerce')
    df_filtered = df_filtered[df_filtered['date_time'].dt.to_period('M') == year_month]
    df_filtered['date'] = df_filtered['date_time'].dt.date
    df_filtered['hour'] = df_filtered['date_time'].dt.hour
    df_filtered['day_week'] = df_filtered['date_time'].dt.strftime('%d/%m (%a)') 

    plt.figure(figsize=(15, 8))

    sns.scatterplot(
        data=df_filtered,
        x='hour',
        y='day_week',
        size='duration',        
        sizes=(100, 1000),          
        hue='duration',              
        palette=sns.light_palette("navy", as_cmap=True),
        legend='brief',
        alpha=0.8
    )

    plt.grid(axis='y', linestyle='--', alpha=0.3)

    for _, row in df_filtered.iterrows():
        plt.text(row['hour'], row['day_week'], str(row['duration']),
                horizontalalignment='center', verticalalignment='center', color='white', fontsize=9, weight='bold')

    plt.title("Estudo por dia e horário", fontsize=16)
    plt.figtext(0.1, 0.98, f"Período: {year_month}", ha='center', fontsize=10)
    plt.figtext(0.25, 0.98, f"Emitido em: {date}", ha='center', fontsize=10)
    plt.xlabel("")
    plt.ylabel("Dia / Semana")
    plt.legend(title="Duração (minutos)", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(IMG_BUBBLE_PATH, dpi=300)
    plt.close()