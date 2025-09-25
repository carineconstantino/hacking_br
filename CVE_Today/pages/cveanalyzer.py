import streamlit as st
import requests
import re

# URL do webhook n8n
N8N_WEBHOOK = "http://62.171.180.64:5678/webhook/2547be73-bbe9-46bd-95bf-4b7a9afb67b6/analisar-cve"

st.set_page_config(page_title="CVE Analyzer", page_icon="🔎", layout="centered")

st.title("🔎 CVE Analyzer - Bug Bounty Focus")

# Input do usuário
cve_id = st.text_input("Informe a CVE ID (ex: CVE-2024-12345):")

if st.button("Analisar"):
    if cve_id.strip():
        try:
            # Faz request ao webhook
            url = f"{N8N_WEBHOOK}/{cve_id.strip()}"
            response = requests.get(url, timeout=30)

            if response.status_code == 200:
                raw_result = response.text.strip()

                st.subheader("📋 Resultado da Análise")

                # Regex para extrair blocos (ajustado ao formato do Agent)
                cve_match = re.search(r"\*CVE:\* (.+)", raw_result)
                sev_match = re.search(r"\| \*Severity:\* (.+)", raw_result)
                rel_match = re.search(r"🎯 \*Bug Bounty Relevance:\* (.+)", raw_result)
                strat_match = re.search(r"\*Strategy:\* (.+)", raw_result, re.DOTALL)

                # Exibe formatado
                if cve_match:
                    st.markdown(f"**🆔 CVE:** {cve_match.group(1)}")
                if sev_match:
                    st.markdown(f"**⚠ Severidade:** {sev_match.group(1)}")
                if rel_match:
                    st.markdown(f"**🎯 Relevância Bug Bounty:** {rel_match.group(1)}")
                if strat_match:
                    st.markdown("**🛠  Estratégia:**")
                    st.info(strat_match.group(1).strip())
