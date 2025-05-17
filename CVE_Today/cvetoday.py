import requests
import pandas as pd
import altair as alt
import streamlit as st
import time
from streamlit_autorefresh import st_autorefresh
from datetime import date
from datetime import datetime

# config menu
alt.themes.enable('dark')
st.set_page_config(page_title="CVE Today", layout="wide", initial_sidebar_state="expanded")


col1, col2 = st.columns([2, 5])
with col1:
    with st.expander('Menu',expanded=True):
        st.title(":space_invader: CVE Today")
        # seleciona a data (padrão: hoje)
        selected_date = st.date_input("📅 Escolha a data da consulta", value=date.today(), max_value=date.today())
        # auto-refresh a cada 1 hora
        st_autorefresh(interval=3600000, key="refresh")
        st.link_button("Go to HACKING BR", "https://www.hackingbr.com.br/")
        if st.button("🔄 Atualizar agora"):
            st.rerun()


@st.cache_data(ttl=36000)
def source(query_date):
    pub_start = f"{query_date}T00:00:00.000"
    pub_end = f"{query_date}T23:59:59.000"
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0/?pubStartDate={pub_start}&pubEndDate={pub_end}"
    response = requests.get(url)
    data = response.json()
    vulnerabilities = data.get('vulnerabilities', [])
    severity_counts = {'CRITICAL': 0, 'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'NONE': 0, 'UNKNOWN': 0}
    filtered_data = []

    for vuln in vulnerabilities:
        cve = vuln['cve']
        english_desc = next((desc['value'] for desc in cve['descriptions'] if desc['lang'] == 'en'), None)
        metrics = cve.get('metrics', {})
        cvss_info = {}

        if 'cvssMetricV31' in metrics:
            cvss_info = metrics['cvssMetricV31'][0]['cvssData']
            severity = cvss_info.get('baseSeverity')
        elif 'cvssMetricV40' in metrics:
            cvss_info = metrics['cvssMetricV40'][0]
            severity = cvss_info.get('baseSeverity')
        else:
            severity = 'UNKNOWN'

        if severity in severity_counts:
            severity_counts[severity] += 1
        else:
            severity_counts['UNKNOWN'] += 1

        filtered_data.append({
            'ID': cve['id'],
            'Description': english_desc,
            'baseSeverity': severity,
            'vectorString': cvss_info.get('vectorString', ''),
            'baseScore': cvss_info.get('baseScore', 0),
            'url': f"https://nvd.nist.gov/vuln/detail/{cve['id']}",
            'References': "; ".join([ref['url'] for ref in cve.get('references', [])])
        })

    df_bruto = pd.DataFrame(filtered_data)
    df = df_bruto[~df_bruto['Description'].str.contains('^Rejected reason:*', na=False)]


    return {
        'total': data.get('totalResults', 0),
        'severity_counts': severity_counts,
        'cve_df': df,
	    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def severity_donut_chart(df, use_container_width: bool):
    severity_counts = df['baseSeverity'].value_counts().reset_index()
    severity_counts.columns = ['category', 'value']
    severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'NONE', 'UNKNOWN']
    severity_counts['category'] = pd.Categorical(
        severity_counts['category'],
        categories=severity_order,
        ordered=True
    )
    severity_counts = severity_counts.sort_values('category')

    color_scale = alt.Scale(
        domain=severity_order,
        range=['#ff0000', '#ff6e00', '#ffbf00', '#00ff2a', '#cccccc', '#999999']
    )

    chart = alt.Chart(severity_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="value", type="quantitative", title="Contagem"),
        color=alt.Color(
            field="category",
            type="nominal",
            title="Severidade",
            scale=color_scale,
            legend=alt.Legend(orient='bottom')
        ),
        tooltip=['category', 'value']
    ).properties(
        title="Vulnerabilidades por Severidade"
    )

    st.altair_chart(chart, theme=None, use_container_width=use_container_width)

    
# resultado 
with col2:
    dados = source(selected_date)

    st.caption(f"🕒 Última atualização: {dados['last_updated']}")
	
    st.metric(label=f"Total de CVEs publicados em {selected_date}", value=dados['total'])

    st.subheader("Vulnerabilidade x Severidade")
    severity_donut_chart(dados['cve_df'], use_container_width=True)
   
    st.subheader("Severidades")
    cols = st.columns(len(dados['severity_counts']))
    for i, (sev, count) in enumerate(dados['severity_counts'].items()):
        cols[i].metric(sev, count)
    

    # filtro de severidade para a tabela
    severidades_disponiveis = dados['cve_df']['baseSeverity'].unique().tolist()
    severidade_selecionada = st.multiselect(
    "Filtrar por severidade:",
    options=severidades_disponiveis,
    default=severidades_disponiveis,
)	
    # aplica o filtro ao dataFrame
    df_filtrado = dados['cve_df'][dados['cve_df']['baseSeverity'].isin(severidade_selecionada)]

    st.dataframe(df_filtrado, use_container_width=True)
