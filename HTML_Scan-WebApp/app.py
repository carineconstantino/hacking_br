# app.py

import streamlit as st
from scanner.core import extract_data

st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
) 
st.markdown("""
<style>
    /* Remove padding padrão do Streamlit */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    /* Ajusta o header */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
        height: 50px;
    }
    
    /* Ajusta o espaço acima do título */
    h1 {
        margin-top: 0.5rem;
    }
    
    /* Opcional: remove o padding extra em dispositivos móveis */
    @media screen and (max-width: 768px) {
        .block-container {
            padding-top: 0.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)


# Interface do Streamlit
def main():
    st.sidebar.title(":space_invader: HTML Scan")
    
    # Input da URL
    url = st.sidebar.text_input("Digite a URL para análise: [https://exemplo.com]")
    
    # Opções de extração
    st.sidebar.subheader("Selecione o que deseja extrair:")
    links = st.sidebar.checkbox("Links")
    images = st.sidebar.checkbox("Imagens")
    cookies = st.sidebar.checkbox("Cookies")
    forms = st.sidebar.checkbox("Formulários")
    js_urls = st.sidebar.checkbox("URLs JavaScript")
    domains = st.sidebar.checkbox("Domínios/Subdomínios")
    ips = st.sidebar.checkbox("Endereços IP")
    leaked_creds = st.sidebar.checkbox("Credenciais vazadas")
    cookies_js = st.sidebar.checkbox("Cookies em JavaScript")
    local_storage = st.sidebar.checkbox("Local Storage")
    
    extract_options = {
        'links': links,
        'images': images,
        'cookies': cookies,
        'forms': forms,
        'js_urls': js_urls,
        'domains': domains,
        'ips': ips,
        'leaked_creds': leaked_creds,
        'cookies_js': cookies_js,
        'local_storage': local_storage,
    }
    
    if st.sidebar.button("Executar Análise"):
        with st.spinner("Analisando a URL..."):
            extracted_data = extract_data(url, extract_options)
            
            if extracted_data:
                st.success("Análise concluída!")
                st.subheader("Resultados da Análise")
                
                # Exibe os resultados em abas
                tabs = st.tabs([key.capitalize() for key in extracted_data.keys()])
                
                for tab, (key, value) in zip(tabs, extracted_data.items()):
                    with tab:
                        if not value:
                            st.write("Nenhum resultado encontrado.")
                        else:
                            if key == 'links':
                                for link in value:
                                    st.markdown(f"- [{link}]({link})")
                            elif key == 'forms':
                                for form in value:
                                    st.subheader("Formulário")
                                    st.write(f"Ação: {form['action']}")
                                    st.write(f"Método: {form['method']}")
                                    st.write("Campos:")
                                    for input_field in form['inputs']:
                                        st.write(f"- Nome: {input_field['name']}, Tipo: {input_field['type']}, Valor: {input_field['value']}")
                            else:
                                for item in value:
                                    st.write(f"- {item}")
                
                # Botão para gerar relatório HTML
                #if st.button("Gerar Relatório HTML"):
                #    d = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #    str_current_datetime = str(d)
                #    
                #    html_lines = [
                #        '<html>',
                #        '<head><meta charset="UTF-8"><title>Resultado</title>',
                #        '</head>',
                #        '<body>',
                #        '<h1>Resultado</h1>']
                #    
                #    for key, value in extracted_data.items():
                #        html_lines.append(f'<h2>{key.capitalize()}</h2>')
                #        html_lines.append('<ul>')
                #        for item in value:
                #            if key == 'links':
                #                html_lines.append(f'<li><a href="{item}" target="_blank">{item}</a></li>')
                #            elif key == 'forms':
                #                html_lines.append('<li>Formulário:')
                #                html_lines.append(f'<ul><li>Ação: {item["action"]}</li>')
                #                html_lines.append(f'<li>Método: {item["method"]}</li>')
                #                html_lines.append('<li>Campos:')
                #                html_lines.append('<ul>')
                #                for input_field in item['inputs']:
                #                    html_lines.append(f'<li>Nome: {input_field["name"]}, Tipo: {input_field["type"]}, Valor: {input_field["value"]}</li>')
                #                html_lines.append('</ul></li></ul></li>')
                #            else:
                #                html_lines.append(f'<li>{item}</li>')
                #        html_lines.append('</ul>')
                #    
                #    html_lines.append('</body></html>')
                #    
                #    html_content = '\n'.join(html_lines)
                #    
                #    st.download_button(
                #        label="Baixar Relatório HTML",
                #        data=html_content,
                #        file_name=f'{str_current_datetime}_relatorio_do_scan.html',
                #        mime='text/html'
                #    )

if __name__ == "__main__":
    main()
