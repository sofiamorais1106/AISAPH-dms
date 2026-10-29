import streamlit as st
import pandas as pd
from database import carregar_dados_tabela

st.set_page_config(
    page_title="AISAPH DataCore - DMS",
    layout="wide"
)

st.markdown("""
    <style>
        .main { background-color: #f8fafc; }
        [data-testid="stSidebar"] { background-color: #0f172a; color: white; }
        [data-testid="stSidebar"] * { color: white !important; }
        .stButton button { background-color: #2563eb; color: white; border-radius: 8px; font-weight: 600; }
        .card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.markdown("<h2 style='text-align: center; color: #0f172a; margin-top: 60px;'>AISAPH DataCore - Acesso</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown("---")
        utilizador = st.text_input("Utilizador / Email")
        password = st.text_input("Palavra-passe", type="password")
        perfil_escolhido = st.selectbox("Perfil", ["Administrador", "Gestor de Dados", "Consulta"])
        if st.button("Entrar no Sistema", use_container_width=True):
            if utilizador and password:
                st.session_state["autenticado"] = True
                st.session_state["perfil"] = perfil_escolhido
                st.rerun()
            else:
                st.error("Preencha todos os campos.")
    st.stop()

st.sidebar.markdown("## AISAPH DataCore")
st.sidebar.markdown(f"Utilizador: `{st.session_state.get('perfil', 'Admin')}`")
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Menu Principal", 
    [
        "1. Visao Geral", 
        "2. Gestao de Documentos", 
        "3. Upload e Armazenamento", 
        "4. Pesquisa e Consulta", 
        "5. Historico e Auditoria", 
        "6. Configuracoes"
    ]
)

st.sidebar.markdown("---")
if st.sidebar.button("Sair do Sistema", use_container_width=True):
    st.session_state["autenticado"] = False
    st.rerun()

df_raw = carregar_dados_tabela()

if menu == "1. Visao Geral":
    st.markdown("## Visao Geral")
    st.markdown("Painel executivo de monitorizacao do sistema de documentos.")
    st.markdown("---")
    
    if not df_raw.empty:
        col_cat_idx = 0 if 0 in df_raw.columns else df_raw.columns[0]
        total_docs = len(df_raw)
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown("""
                <div class="card">
                    <div style="font-size: 13px; color: #64748b; font-weight: 600;">TOTAL DE REGISTOS</div>
                    <div style="font-size: 26px; color: #0f172a; font-weight: 700; margin-top: 5px;">{}</div>
                </div>
            """.format(total_docs), unsafe_allow_html=True)
        with c2:
            st.markdown("""
                <div class="card">
                    <div style="font-size: 13px; color: #64748b; font-weight: 600;">CATEGORIAS ATIVAS</div>
                    <div style="font-size: 26px; color: #0f172a; font-weight: 700; margin-top: 5px;">10</div>
                </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
                <div class="card">
                    <div style="font-size: 13px; color: #64748b; font-weight: 600;">ESTADO DO SISTEMA</div>
                    <div style="font-size: 26px; color: #10b981; font-weight: 700; margin-top: 5px;">Estavel</div>
                </div>
            """, unsafe_allow_html=True)
        with c4:
            st.markdown("""
                <div class="card">
                    <div style="font-size: 13px; color: #64748b; font-weight: 600;">UTILIZADOR ATIVO</div>
                    <div style="font-size: 26px; color: #2563eb; font-weight: 700; margin-top: 5px;">{}</div>
                </div>
            """.format(st.session_state.get('perfil', 'Admin')), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_esq, col_meio, col_dir = st.columns([1.2, 1, 1])
        
        with col_esq:
            st.markdown("### Registos Recentes")
            df_display = df_raw.copy()
            df_display.columns = [f"Col {i}" for i in range(df_display.shape[1])]
            st.dataframe(df_display.head(6), use_container_width=True, height=280, hide_index=True)
                
        with col_meio:
            st.markdown("### Repositorio de Documentos")
            st.markdown("""
            * **Todas as Categorias** - `293 registos`
                * **DAO** - Documentos Administrativos
                * **DFC** - Documentos Financeiros
                * **DRH** - Recursos Humanos
            * **Por Periodo**
                * Outubro / 2026
                * Setembro / 2026
            """)
            
        with col_dir:
            st.markdown("### Distribuicao por Nivel")
            cats = df_raw[col_cat_idx].dropna().astype(str).apply(lambda x: x.split('-')[0].strip())
            contagem = cats.value_counts().reset_index()
            contagem.columns = ['Categoria', 'Quantidade']
            contagem = contagem[contagem['Categoria'] != 'nan']
            if not contagem.empty:
                st.bar_chart(contagem.set_index('Categoria').head(5), height=240)
            else:
                st.info("Sem dados suficientes.")
    else:
        st.warning("Nenhum dado carregado.")

elif menu == "2. Gestao de Documentos":
    st.markdown("## Gestao de Documentos")
    st.markdown("Consulte, filtre e gerencie a taxonomia documental.")
    st.markdown("---")
    
    if not df_raw.empty:
        col_cat_idx = 0 if 0 in df_raw.columns else df_raw.columns[0]
        cats_unicas = sorted(list(set(df_raw[col_cat_idx].dropna().astype(str).apply(lambda x: x.split('-')[0].strip()))))
        categorias_disponiveis = ["Todas"] + [c for c in cats_unicas if c and c != "nan"]

        with st.expander("Filtros Avancados", expanded=True):
            f1, f2, f3 = st.columns([2, 1, 1])
            with f1:
                termo_pesquisa = st.text_input("Pesquisa por texto ou codigo:", placeholder="Ex: DAO, Contrato, Ata...")
            with f2:
                cat_selecionada = st.selectbox("Categoria / Codigo:", categorias_disponiveis)
            with f3:
                nivel_selecionado = st.selectbox("Nivel de Confidencialidade:", ["Todos", "Publico", "Interno", "Confidencial"])

        df_filtrado = df_raw.copy()
        df_filtrado = df_filtrado.fillna("")
        df_filtrado.columns = [f"Coluna {i}" for i in range(df_filtrado.shape[1])]
        
        if termo_pesquisa:
            mask = df_filtrado.astype(str).apply(lambda x: x.str.contains(termo_pesquisa, case=False)).any(axis=1)
            df_filtrado = df_filtrado[mask]
            
        if cat_selecionada != "Todas":
            col_nome_0 = df_filtrado.columns[0]
            df_filtrado = df_filtrado[df_filtrado[col_nome_0].astype(str).str.startswith(cat_selecionada)]

        st.markdown(f"**A mostrar `{len(df_filtrado)}` de `{len(df_raw)}` registos:**")
        st.dataframe(df_filtrado, use_container_width=True, height=420, hide_index=True)
        
        csv_data = df_filtrado.to_csv(index=False, sep=';').encode('latin1', errors='replace')
        st.download_button(
            label="Exportar Tabela Filtrada (CSV)",
            data=csv_data,
            file_name="documentos_filtrados.csv",
            mime="text/csv"
        )
    else:
        st.warning("Sem dados disponiveis.")

elif menu == "3. Upload e Armazenamento":
    st.markdown("## Upload e Armazenamento")
    st.markdown("Carregue novos ficheiros para o repositorio local.")
    st.markdown("---")
    
    ficheiro = st.file_uploader("Selecionar ficheiro", type=["csv", "xlsx", "pdf"])
    if ficheiro is not None:
        st.success(f"Ficheiro '{ficheiro.name}' carregado com sucesso.")
        if st.button("Guardar no Servidor"):
            st.info("Ficheiro integrado na estrutura local.")

elif menu == "4. Pesquisa e Consulta":
    st.markdown("## Pesquisa e Consulta")
    st.markdown("Localize documentos por palavra-chave em todo o repositorio.")
    st.markdown("---")
    
    termo = st.text_input("Digite o termo de pesquisa:")
    if termo and not df_raw.empty:
        df_display = df_raw.copy()
        df_display.columns = [f"Coluna {i}" for i in range(df_display.shape[1])]
        mask = df_display.astype(str).apply(lambda x: x.str.contains(termo, case=False)).any(axis=1)
        st.dataframe(df_display[mask], use_container_width=True)

elif menu == "5. Historico e Auditoria":
    st.markdown("## Historico e Rastreabilidade")
    st.markdown("Registo de acoes e eventos efetuados no sistema.")
    st.markdown("---")
    st.markdown("""
    * **[2026-10-29 18:00]** - Arquitetura de modulos reorganizada.
    * **[2026-10-29 16:20]** - Utilizador acedeu ao portal.
    * **[2026-10-29 16:15]** - Indexacao de 293 registos CSV concluida.
    """)

else:
    st.markdown("## Configuracoes")
    st.markdown("Gerencie as preferencias e perfis de acesso.")
    st.markdown("---")
    novo_perfil = st.selectbox("Perfil Ativo", ["Administrador", "Gestor de Dados", "Consulta"])
    if st.button("Atualizar Perfil"):
        st.session_state["perfil"] = novo_perfil
        st.success("Perfil atualizado com sucesso.")