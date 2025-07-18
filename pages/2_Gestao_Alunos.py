import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_handler import DataHandler
from datetime import datetime

st.set_page_config(page_title="Gestão de Alunos", page_icon="👥", layout="wide")

def main():
    st.title("👥 Gestão de Alunos")
    st.markdown("---")
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Lista de Alunos", "➕ Cadastrar Aluno", "📊 Estatísticas", "📤 Exportar"])
    
    with tab1:
        st.subheader("📋 Lista de Alunos Cadastrados")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            filtro_curso = st.selectbox(
                "Filtrar por Curso:",
                ["Todos", "Formação Analista Comportamental", "Outros"]
            )
        
        with col2:
            filtro_estado = st.selectbox(
                "Filtrar por Estado:",
                ["Todos", "BA", "SP", "PA", "RS", "PE", "GO", "MG", "SC"]
            )
        
        with col3:
            busca_nome = st.text_input("🔍 Buscar por nome:")
        
        try:
            # Dados dos alunos baseados no PDF de inscrições
            alunos_dados = [
                {
                    'Nome': 'Fernanda Passos Silva dos Santos',
                    'Email': 'gs2fernanda@gmail.com',
                    'CPF': '05595210575',
                    'Telefone': '71992509996',
                    'Cidade': 'Camaçari',
                    'Estado': 'BA',
                    'Curso': 'Formação Analista Comportamental',
                    'Data_Inscricao': '15/04/2024',
                    'Profissao': 'Analista de RH'
                },
                {
                    'Nome': 'Nathalia da Silva Bezerra',
                    'Email': 'nathalia.s.beze@gmail.com',
                    'CPF': '38157732883',
                    'Telefone': '11989359930',
                    'Cidade': 'Osasco',
                    'Estado': 'SP',
                    'Curso': 'Formação Analista Comportamental',
                    'Data_Inscricao': '23/04/2024',
                    'Profissao': 'Coordenadora de Recursos Humanos'
                },
                {
                    'Nome': 'Áurea Cristina de Oliveira Aguiar',
                    'Email': 'aureaaguiar30@gmail.com',
                    'CPF': '403.323.222.20',
                    'Telefone': '91981129597',
                    'Cidade': 'Ananindeua',
                    'Estado': 'PA',
                    'Curso': 'Formação Analista Comportamental',
                    'Data_Inscricao': '27/04/2024',
                    'Profissao': 'Professora de Gestão'
                },
                {
                    'Nome': 'Diane Machado',
                    'Email': 'dihmachado81@gmail.com',
                    'CPF': '02375186001',
                    'Telefone': '55981524180',
                    'Cidade': 'Eugênio De Castro',
                    'Estado': 'RS',
                    'Curso': 'Formação Analista Comportamental',
                    'Data_Inscricao': '06/05/2024',
                    'Profissao': 'Terapeuta'
                },
                {
                    'Nome': 'Kathleen Julianna M Sampaio Interaminsense',
                    'Email': 'kathleensampa@hotmail.com',
                    'CPF': '08264603483',
                    'Telefone': '81996793483',
                    'Cidade': 'Recife',
                    'Estado': 'PE',
                    'Curso': 'Formação Analista Comportamental',
                    'Data_Inscricao': '15/05/2024',
                    'Profissao': 'Gestora de RH'
                },
                {
                    'Nome': 'Ruan Macedo Santana',
                    'Email': 'ruan.macedo48@gmail.com',
                    'CPF': '01755332106',
                    'Telefone': '61993279632',
                    'Cidade': 'Goianésia',
                    'Estado': 'GO',
                    'Curso': 'Formação Analista Comportamental',
                    'Data_Inscricao': '20/05/2024',
                    'Profissao': 'Gerente'
                },
                {
                    'Nome': 'Paula Nunes Vieira Silva',
                    'Email': 'paulanunes.adm22@gmail.com',
                    'CPF': '105.162.366-95',
                    'Telefone': '(38)99944-7822',
                    'Cidade': 'Paracatu',
                    'Estado': 'MG',
                    'Curso': 'Formação Analista Comportamental',
                    'Data_Inscricao': '20/05/2024',
                    'Profissao': 'Assistente de Recursos Humanos I'
                },
                {
                    'Nome': 'Lilian Jane de Menezes Farias',
                    'Email': 'lilianjane1980@gmail.com',
                    'CPF': '00542224518',
                    'Telefone': '73988443997',
                    'Cidade': 'Tijucas',
                    'Estado': 'SC',
                    'Curso': 'Formação Analista Comportamental',
                    'Data_Inscricao': '20/05/2024',
                    'Profissao': 'Analista de RH'
                }
            ]
            
            df_alunos = pd.DataFrame(alunos_dados)
            
            # Aplicar filtros
            df_filtrado = df_alunos.copy()
            
            if filtro_curso != "Todos":
                df_filtrado = df_filtrado[df_filtrado['Curso'] == filtro_curso]
            
            if filtro_estado != "Todos":
                df_filtrado = df_filtrado[df_filtrado['Estado'] == filtro_estado]
            
            if busca_nome:
                df_filtrado = df_filtrado[df_filtrado['Nome'].str.contains(busca_nome, case=False, na=False)]
            
            # Exibir métricas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 Total de Alunos", len(df_filtrado))
            
            with col2:
                if not df_filtrado.empty:
                    estados_unicos = df_filtrado['Estado'].nunique()
                    st.metric("🌍 Estados Representados", estados_unicos)
                else:
                    st.metric("🌍 Estados Representados", 0)
            
            with col3:
                if not df_filtrado.empty:
                    cursos_unicos = df_filtrado['Curso'].nunique()
                    st.metric("📚 Cursos Ativos", cursos_unicos)
                else:
                    st.metric("📚 Cursos Ativos", 0)
            
            st.markdown("---")
            
            # Tabela de alunos
            if not df_filtrado.empty:
                # Configurar colunas para exibição
                colunas_exibir = ['Nome', 'Email', 'Telefone', 'Cidade', 'Estado', 'Curso', 'Data_Inscricao']
                
                st.dataframe(
                    df_filtrado[colunas_exibir],
                    use_container_width=True,
                    hide_index=True
                )
                
                # Botão para ver detalhes
                if st.button("👁️ Ver Detalhes Completos"):
                    st.subheader("📄 Dados Completos")
                    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)
            else:
                st.info("Nenhum aluno encontrado com os filtros aplicados.")
                
        except Exception as e:
            st.error(f"Erro ao carregar dados dos alunos: {str(e)}")
    
    with tab2:
        st.subheader("➕ Cadastrar Novo Aluno")
        
        with st.form("cadastro_aluno"):
            col1, col2 = st.columns(2)
            
            with col1:
                nome = st.text_input("Nome Completo *", placeholder="Digite o nome completo")
                email = st.text_input("E-mail *", placeholder="exemplo@email.com")
                cpf = st.text_input("CPF *", placeholder="000.000.000-00")
                telefone = st.text_input("Telefone/WhatsApp *", placeholder="(00) 00000-0000")
                profissao = st.text_input("Profissão", placeholder="Digite a profissão")
            
            with col2:
                curso = st.selectbox(
                    "Curso *",
                    ["Formação Analista Comportamental", "Outros"]
                )
                cidade = st.text_input("Cidade *", placeholder="Digite a cidade")
                estado = st.selectbox(
                    "Estado *",
                    ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
                )
                cep = st.text_input("CEP", placeholder="00000-000")
                endereco = st.text_input("Endereço", placeholder="Rua, número, complemento")
            
            st.markdown("**Campos marcados com * são obrigatórios")
            
            submitted = st.form_submit_button("✅ Cadastrar Aluno", use_container_width=True)
            
            if submitted:
                # Validação dos campos obrigatórios
                if not all([nome, email, cpf, telefone, curso, cidade, estado]):
                    st.error("❌ Por favor, preencha todos os campos obrigatórios.")
                else:
                    # Simular cadastro
                    st.success(f"✅ Aluno {nome} cadastrado com sucesso!")
                    st.info("💡 Em um sistema real, estes dados seriam salvos em banco de dados.")
                    
                    # Mostrar resumo dos dados cadastrados
                    with st.expander("📋 Resumo dos Dados Cadastrados"):
                        st.write(f"**Nome:** {nome}")
                        st.write(f"**E-mail:** {email}")
                        st.write(f"**CPF:** {cpf}")
                        st.write(f"**Telefone:** {telefone}")
                        st.write(f"**Curso:** {curso}")
                        st.write(f"**Cidade:** {cidade}")
                        st.write(f"**Estado:** {estado}")
                        if profissao:
                            st.write(f"**Profissão:** {profissao}")
                        if cep:
                            st.write(f"**CEP:** {cep}")
                        if endereco:
                            st.write(f"**Endereço:** {endereco}")
    
    with tab3:
        st.subheader("📊 Estatísticas dos Alunos")
        
        try:
            # Usando os mesmos dados da tab1
            alunos_dados = [
                {
                    'Nome': 'Fernanda Passos Silva dos Santos',
                    'Estado': 'BA',
                    'Curso': 'Formação Analista Comportamental',
                    'Profissao': 'Analista de RH'
                },
                {
                    'Nome': 'Nathalia da Silva Bezerra',
                    'Estado': 'SP',
                    'Curso': 'Formação Analista Comportamental',
                    'Profissao': 'Coordenadora de Recursos Humanos'
                },
                {
                    'Nome': 'Áurea Cristina de Oliveira Aguiar',
                    'Estado': 'PA',
                    'Curso': 'Formação Analista Comportamental',
                    'Profissao': 'Professora de Gestão'
                },
                {
                    'Nome': 'Diane Machado',
                    'Estado': 'RS',
                    'Curso': 'Formação Analista Comportamental',
                    'Profissao': 'Terapeuta'
                },
                {
                    'Nome': 'Kathleen Julianna M Sampaio Interaminsense',
                    'Estado': 'PE',
                    'Curso': 'Formação Analista Comportamental',
                    'Profissao': 'Gestora de RH'
                },
                {
                    'Nome': 'Ruan Macedo Santana',
                    'Estado': 'GO',
                    'Curso': 'Formação Analista Comportamental',
                    'Profissao': 'Gerente'
                },
                {
                    'Nome': 'Paula Nunes Vieira Silva',
                    'Estado': 'MG',
                    'Curso': 'Formação Analista Comportamental',
                    'Profissao': 'Assistente de Recursos Humanos I'
                },
                {
                    'Nome': 'Lilian Jane de Menezes Farias',
                    'Estado': 'SC',
                    'Curso': 'Formação Analista Comportamental',
                    'Profissao': 'Analista de RH'
                }
            ]
            
            df_stats = pd.DataFrame(alunos_dados)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🌍 Distribuição por Estado")
                estados_count = df_stats['Estado'].value_counts()
                fig_estados = px.pie(
                    values=estados_count.values,
                    names=estados_count.index,
                    title="Alunos por Estado"
                )
                st.plotly_chart(fig_estados, use_container_width=True)
            
            with col2:
                st.subheader("💼 Distribuição por Profissão")
                profissoes_count = df_stats['Profissao'].value_counts()
                fig_profissoes = px.bar(
                    x=profissoes_count.values,
                    y=profissoes_count.index,
                    orientation='h',
                    title="Alunos por Profissão"
                )
                fig_profissoes.update_layout(height=400)
                st.plotly_chart(fig_profissoes, use_container_width=True)
            
            # Tabela de estatísticas
            st.subheader("📈 Resumo Estatístico")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("👥 Total de Alunos", len(df_stats))
                st.metric("🌍 Estados", df_stats['Estado'].nunique())
            
            with col2:
                st.metric("📚 Cursos", df_stats['Curso'].nunique())
                st.metric("💼 Profissões", df_stats['Profissao'].nunique())
            
            with col3:
                # Calcular estado com mais alunos
                estado_top = df_stats['Estado'].value_counts().index[0]
                count_top = df_stats['Estado'].value_counts().iloc[0]
                st.metric("🏆 Estado com mais alunos", f"{estado_top} ({count_top})")
                
                # Profissão mais comum
                prof_top = df_stats['Profissao'].value_counts().index[0]
                st.metric("👔 Profissão mais comum", prof_top)
                
        except Exception as e:
            st.error(f"Erro ao gerar estatísticas: {str(e)}")
    
    with tab4:
        st.subheader("📤 Exportar Dados dos Alunos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 📋 Opções de Exportação
            
            Selecione o formato desejado para exportar os dados dos alunos:
            """)
            
            formato_export = st.radio(
                "Formato de exportação:",
                ["CSV", "Excel", "JSON"]
            )
            
            incluir_dados = st.multiselect(
                "Dados a incluir:",
                ["Dados Pessoais", "Contato", "Endereço", "Curso", "Profissão"],
                default=["Dados Pessoais", "Contato", "Curso"]
            )
        
        with col2:
            st.markdown("""
            ### ℹ️ Informações
            
            - **CSV**: Arquivo de texto separado por vírgulas, ideal para Excel
            - **Excel**: Planilha do Microsoft Excel com formatação
            - **JSON**: Formato estruturado para sistemas
            
            **Nota**: Esta é uma demonstração. Em um sistema real, os arquivos seriam gerados e baixados automaticamente.
            """)
        
        if st.button("📥 Gerar Arquivo de Exportação", use_container_width=True):
            if incluir_dados:
                st.success(f"✅ Arquivo {formato_export} gerado com sucesso!")
                st.info(f"📊 Dados incluídos: {', '.join(incluir_dados)}")
                st.warning("💡 Em um sistema real, o download iniciaria automaticamente.")
            else:
                st.error("❌ Selecione pelo menos um tipo de dado para exportar.")

if __name__ == "__main__":
    main()
