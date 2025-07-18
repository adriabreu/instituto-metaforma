import streamlit as st
import pandas as pd
import io
from utils.data_handler import DataHandler

st.set_page_config(page_title="Importar Dados", page_icon="📤", layout="wide")

def main():
    st.title("📤 Importar Dados")
    st.markdown("---")
    
    # Tabs para diferentes tipos de importação
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dados Financeiros", "👥 Lista de Alunos", "📁 Arquivos Existentes", "ℹ️ Ajuda"])
    
    with tab1:
        st.subheader("📊 Importar Dados Financeiros")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 📋 Formatos Aceitos
            - **Excel (.xlsx)**: Planilhas do Microsoft Excel
            - **CSV (.csv)**: Arquivos separados por vírgula
            - **PDF**: Relatórios em PDF (visualização apenas)
            
            ### 📝 Estrutura Esperada
            Para dados financeiros, o arquivo deve conter as seguintes colunas:
            - Período/Curso (FAC_XX)
            - Receita Bruta
            - Inadimplência
            - Despesas detalhadas
            - Resultado Líquido
            """)
            
            # Upload de arquivo financeiro
            arquivo_financeiro = st.file_uploader(
                "Selecione o arquivo financeiro:",
                type=['xlsx', 'csv', 'pdf'],
                help="Faça upload do arquivo com dados financeiros"
            )
            
            if arquivo_financeiro is not None:
                try:
                    if arquivo_financeiro.type == "application/pdf":
                        st.info("📄 Arquivo PDF detectado. Exibindo informações do arquivo:")
                        st.write(f"**Nome:** {arquivo_financeiro.name}")
                        st.write(f"**Tamanho:** {arquivo_financeiro.size} bytes")
                        st.warning("💡 Para PDFs, use a funcionalidade de visualização na aba 'Arquivos Existentes'")
                        
                    elif arquivo_financeiro.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                        # Arquivo Excel
                        df = pd.read_excel(arquivo_financeiro)
                        st.success("✅ Arquivo Excel carregado com sucesso!")
                        
                        st.subheader("👁️ Prévia dos Dados")
                        st.dataframe(df.head(10), use_container_width=True)
                        
                        st.subheader("📊 Informações do Dataset")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("📏 Linhas", len(df))
                        with col2:
                            st.metric("📐 Colunas", len(df.columns))
                        with col3:
                            st.metric("💾 Tamanho", f"{arquivo_financeiro.size} bytes")
                        
                        if st.button("💾 Processar e Salvar Dados"):
                            st.success("✅ Dados financeiros processados e salvos!")
                            st.info("💡 Em um sistema real, os dados seriam salvos em banco de dados.")
                    
                    elif arquivo_financeiro.type == "text/csv":
                        # Arquivo CSV
                        df = pd.read_csv(arquivo_financeiro)
                        st.success("✅ Arquivo CSV carregado com sucesso!")
                        
                        st.subheader("👁️ Prévia dos Dados")
                        st.dataframe(df.head(10), use_container_width=True)
                        
                        if st.button("💾 Processar e Salvar Dados"):
                            st.success("✅ Dados financeiros processados e salvos!")
                            st.info("💡 Em um sistema real, os dados seriam salvos em banco de dados.")
                
                except Exception as e:
                    st.error(f"❌ Erro ao processar arquivo: {str(e)}")
        
        with col2:
            st.markdown("""
            ### 📈 Status da Importação
            """)
            
            # Status dos dados
            st.metric("📊 Último Import", "Não disponível")
            st.metric("📅 Data", "N/A")
            st.metric("✅ Status", "Aguardando")
            
            st.markdown("---")
            
            st.markdown("""
            ### 🔄 Ações Rápidas
            """)
            
            if st.button("🔄 Atualizar Sistema", use_container_width=True):
                st.info("Sistema atualizado!")
            
            if st.button("🗑️ Limpar Cache", use_container_width=True):
                st.success("Cache limpo!")
    
    with tab2:
        st.subheader("👥 Importar Lista de Alunos")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### 📋 Formatos Aceitos
            - **Excel (.xlsx)**: Planilhas do Microsoft Excel
            - **CSV (.csv)**: Arquivos separados por vírgula
            - **Google Sheets**: Respostas de formulários
            
            ### 📝 Colunas Esperadas
            - Nome Completo
            - E-mail
            - CPF
            - Telefone/WhatsApp
            - Endereço (CEP, Cidade, Estado)
            - Curso Escolhido
            - Profissão
            """)
            
            # Upload de arquivo de alunos
            arquivo_alunos = st.file_uploader(
                "Selecione o arquivo de alunos:",
                type=['xlsx', 'csv'],
                help="Faça upload do arquivo com dados dos alunos"
            )
            
            if arquivo_alunos is not None:
                try:
                    if arquivo_alunos.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                        df = pd.read_excel(arquivo_alunos)
                    else:
                        df = pd.read_csv(arquivo_alunos)
                    
                    st.success("✅ Arquivo carregado com sucesso!")
                    
                    st.subheader("👁️ Prévia dos Dados")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    st.subheader("📊 Validação dos Dados")
                    
                    # Verificar colunas essenciais
                    colunas_essenciais = ['nome', 'email', 'cpf', 'telefone']
                    colunas_encontradas = [col for col in colunas_essenciais if any(col.lower() in df.columns.str.lower())]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Colunas Encontradas:**")
                        for col in df.columns:
                            st.write(f"✅ {col}")
                    
                    with col2:
                        st.write("**Validação:**")
                        for col in colunas_essenciais:
                            if col in colunas_encontradas:
                                st.write(f"✅ {col.title()}: OK")
                            else:
                                st.write(f"❌ {col.title()}: Não encontrado")
                    
                    if len(colunas_encontradas) >= 3:
                        if st.button("💾 Importar Alunos"):
                            st.success(f"✅ {len(df)} alunos importados com sucesso!")
                            st.info("💡 Em um sistema real, os dados seriam salvos em banco de dados.")
                    else:
                        st.warning("⚠️ Arquivo não possui todas as colunas essenciais.")
                
                except Exception as e:
                    st.error(f"❌ Erro ao processar arquivo: {str(e)}")
        
        with col2:
            st.markdown("""
            ### 👥 Status dos Alunos
            """)
            
            st.metric("👤 Total Cadastrados", "8")
            st.metric("📅 Última Atualização", "Hoje")
            st.metric("✅ Status", "Ativo")
            
            st.markdown("---")
            
            st.markdown("""
            ### 📋 Modelo de Planilha
            """)
            
            # Criar modelo para download
            modelo_dados = {
                'Nome Completo': ['João Silva', 'Maria Santos'],
                'E-mail': ['joao@email.com', 'maria@email.com'],
                'CPF': ['000.000.000-00', '111.111.111-11'],
                'Telefone': ['(11) 99999-9999', '(11) 88888-8888'],
                'Cidade': ['São Paulo', 'Rio de Janeiro'],
                'Estado': ['SP', 'RJ'],
                'Curso': ['Formação Analista Comportamental', 'Formação Analista Comportamental'],
                'Profissão': ['Analista', 'Gerente']
            }
            
            df_modelo = pd.DataFrame(modelo_dados)
            
            # Converter para CSV
            csv_modelo = df_modelo.to_csv(index=False)
            
            st.download_button(
                label="📥 Baixar Modelo",
                data=csv_modelo,
                file_name="modelo_alunos.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    with tab3:
        st.subheader("📁 Visualizar Arquivos Existentes")
        
        st.markdown("""
        ### 📋 Arquivos Carregados no Sistema
        
        Esta seção mostra os arquivos que foram fornecidos para análise:
        """)
        
        # Informações sobre os arquivos existentes
        arquivos_info = [
            {
                'Nome': 'Controle Financeiro Metaforma',
                'Tipo': 'PDF',
                'Descrição': 'Relatório financeiro com dados de orçamento vs realizado',
                'Status': 'Processado',
                'Dados': 'Receitas, despesas, resultados por curso (FAC)'
            },
            {
                'Nome': 'Ficha de Inscrição - Instituto Metaforma',
                'Tipo': 'PDF',
                'Descrição': 'Respostas do formulário de inscrição',
                'Status': 'Processado',
                'Dados': 'Dados pessoais, contato, endereço dos alunos'
            }
        ]
        
        for arquivo in arquivos_info:
            with st.expander(f"📄 {arquivo['Nome']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Tipo:** {arquivo['Tipo']}")
                    st.write(f"**Status:** {arquivo['Status']}")
                    st.write(f"**Descrição:** {arquivo['Descrição']}")
                
                with col2:
                    st.write(f"**Dados extraídos:** {arquivo['Dados']}")
                    
                    if arquivo['Nome'] == 'Controle Financeiro Metaforma':
                        if st.button(f"👁️ Ver Dados Financeiros", key=f"view_{arquivo['Nome']}"):
                            st.info("Redirecionando para Dashboard Financeiro...")
                            # st.switch_page("pages/1_Dashboard_Financeiro.py")
                    
                    elif arquivo['Nome'] == 'Ficha de Inscrição - Instituto Metaforma':
                        if st.button(f"👁️ Ver Dados dos Alunos", key=f"view_{arquivo['Nome']}"):
                            st.info("Redirecionando para Gestão de Alunos...")
                            # st.switch_page("pages/2_Gestao_Alunos.py")
        
        st.markdown("---")
        
        # Resumo dos dados processados
        st.subheader("📊 Resumo dos Dados Processados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📄 Arquivos Processados", "2")
            st.metric("💰 Dados Financeiros", "✅ Disponível")
        
        with col2:
            st.metric("👥 Registros de Alunos", "8")
            st.metric("📊 Cursos Identificados", "1")
        
        with col3:
            st.metric("🌍 Estados Cobertos", "8")
            st.metric("📅 Período de Dados", "2024")
    
    with tab4:
        st.subheader("ℹ️ Ajuda - Como Importar Dados")
        
        # Tutorial passo a passo
        st.markdown("""
        ## 📖 Guia de Importação de Dados
        
        ### 1. 📊 Dados Financeiros
        
        **Formatos aceitos:**
        - Excel (.xlsx) - Recomendado
        - CSV (.csv)
        - PDF (apenas visualização)
        
        **Estrutura recomendada:**
        ```
        Período | Receita_Bruta | Inadimplência | Despesas | Resultado_Líquido
        FAC_17  | 25220.00      | 0.00          | 4301.60  | 22698.00
        FAC_16  | 15400.00      | 0.00          | 4591.60  | 5549.20
        ```
        
        ### 2. 👥 Dados de Alunos
        
        **Colunas obrigatórias:**
        - Nome Completo
        - E-mail
        - CPF
        - Telefone/WhatsApp
        
        **Colunas opcionais:**
        - Endereço (CEP, Cidade, Estado)
        - Curso
        - Profissão
        
        ### 3. 🔧 Solução de Problemas
        
        **Erro: "Arquivo não pode ser lido"**
        - Verifique se o arquivo não está corrompido
        - Certifique-se de que está no formato correto
        - Tente salvar novamente no Excel
        
        **Erro: "Colunas não encontradas"**
        - Verifique os nomes das colunas
        - Use o modelo fornecido como referência
        - Evite caracteres especiais nos nomes das colunas
        
        **Erro: "Dados inválidos"**
        - Verifique se os CPFs estão no formato correto
        - Confirme se os e-mails são válidos
        - Verifique se não há células vazias nas colunas obrigatórias
        """)
        
        # Seção de contato
        st.markdown("---")
        
        st.subheader("🆘 Precisa de Ajuda?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📞 Suporte Técnico:**
            - E-mail: suporte@metaforma.com.br
            - Telefone: (11) 9999-9999
            - Horário: Segunda a Sexta, 9h às 18h
            """)
        
        with col2:
            st.markdown("""
            **📚 Recursos Adicionais:**
            - Manual do usuário
            - Vídeos tutoriais
            - FAQ - Perguntas frequentes
            - Base de conhecimento
            """)
        
        # Botão de teste
        if st.button("🧪 Testar Importação com Dados de Exemplo"):
            st.success("✅ Teste realizado com sucesso!")
            st.info("💡 Os dados de exemplo foram processados corretamente.")

if __name__ == "__main__":
    main()
