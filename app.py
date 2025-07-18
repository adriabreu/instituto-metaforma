import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_handler import DataHandler
from utils.financial_calculator import FinancialCalculator
import os

# Configuração da página
st.set_page_config(
    page_title="Instituto Metaforma - Gestão Financeira",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar manipulador de dados
@st.cache_resource
def init_data_handler():
    return DataHandler()

def main():
    st.title("📊 Instituto Metaforma - Sistema de Gestão Financeira")
    st.markdown("---")
    
    # Sidebar com informações do sistema
    with st.sidebar:
        st.header("🏛️ Instituto Metaforma")
        st.markdown("**Sistema de Gestão Financeira e Cadastral**")
        st.markdown("---")
        
        # Status do sistema
        st.subheader("📈 Status do Sistema")
        data_handler = init_data_handler()
        
        try:
            # Verificar se há dados carregados
            if hasattr(data_handler, 'financial_data') and not data_handler.financial_data.empty:
                st.success("✅ Dados financeiros carregados")
            else:
                st.warning("⚠️ Nenhum dado financeiro encontrado")
                
            if hasattr(data_handler, 'student_data') and not data_handler.student_data.empty:
                st.success("✅ Dados de alunos carregados")
            else:
                st.warning("⚠️ Nenhum dado de aluno encontrado")
                
        except Exception as e:
            st.error(f"❌ Erro ao verificar dados: {str(e)}")
    
    # Página principal - Dashboard resumido
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        data_handler = init_data_handler()
        calculator = FinancialCalculator(data_handler)
        
        # Métricas principais
        with col1:
            st.metric(
                label="📈 Receita Total Realizada",
                value="R$ 24.348,00",
                delta="-53.932,00 vs Orçado"
            )
        
        with col2:
            st.metric(
                label="💰 Resultado Líquido",
                value="R$ -166,90",
                delta="-42.046,20 vs Orçado"
            )
        
        with col3:
            st.metric(
                label="👥 Total de Alunos",
                value="81",
                delta="Ativos no sistema"
            )
        
        with col4:
            st.metric(
                label="🎯 Ticket Médio",
                value="R$ 300,60",
                delta="Por aluno"
            )
    
    except Exception as e:
        st.error(f"Erro ao carregar métricas: {str(e)}")
        # Exibir métricas em branco em caso de erro
        with col1:
            st.metric("📈 Receita Total", "R$ 0,00")
        with col2:
            st.metric("💰 Resultado Líquido", "R$ 0,00")
        with col3:
            st.metric("👥 Total de Alunos", "0")
        with col4:
            st.metric("🎯 Ticket Médio", "R$ 0,00")
    
    st.markdown("---")
    
    # Seção de navegação rápida
    st.subheader("🚀 Navegação Rápida")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Dashboard Financeiro", use_container_width=True):
            st.switch_page("pages/1_Dashboard_Financeiro.py")
        if st.button("📋 Relatórios", use_container_width=True):
            st.switch_page("pages/4_Relatorios.py")
    
    with col2:
        if st.button("👥 Gestão de Alunos", use_container_width=True):
            st.switch_page("pages/2_Gestao_Alunos.py")
        if st.button("🔄 Migrar Dados", use_container_width=True):
            st.switch_page("pages/5_Migração_Dados.py")
    
    with col3:
        if st.button("📤 Importar Dados", use_container_width=True):
            st.switch_page("pages/3_Importar_Dados.py")
        if st.button("⭐ Melhorias Sistema", use_container_width=True):
            st.switch_page("pages/6_Melhorias_Sistema.py")
    
    # Nova seção para funcionalidades avançadas
    st.markdown("### 🚀 Funcionalidades Avançadas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👥 Gestão Avançada de Alunos", use_container_width=True):
            st.switch_page("pages/7_Gestao_Alunos_Avancada.py")
    
    with col2:
        if st.button("🏦 Conciliação Bancária", use_container_width=True):
            st.switch_page("pages/8_Conciliacao_Bancaria.py")
    
    # Seção de resumo gráfico
    st.markdown("---")
    st.subheader("📈 Resumo Financeiro por Curso (FAC)")
    
    try:
        # Dados dos cursos (baseado no PDF)
        cursos_data = {
            'Curso': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14'],
            'Orçado': [25220.0, 15400.0, 17290.0, 20370.0],
            'Realizado': [3589.0, 3760.0, 7105.0, 9894.0],
            'Resultado': [-2696.9, 48.6, 1380.7, 1100.9]
        }
        
        df_cursos = pd.DataFrame(cursos_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de receita orçada vs realizada
            fig_receita = go.Figure()
            fig_receita.add_trace(go.Bar(
                name='Orçado',
                x=df_cursos['Curso'],
                y=df_cursos['Orçado'],
                marker_color='lightblue'
            ))
            fig_receita.add_trace(go.Bar(
                name='Realizado',
                x=df_cursos['Curso'],
                y=df_cursos['Realizado'],
                marker_color='darkblue'
            ))
            fig_receita.update_layout(
                title='Receita: Orçado vs Realizado',
                xaxis_title='Curso',
                yaxis_title='Valor (R$)',
                barmode='group'
            )
            st.plotly_chart(fig_receita, use_container_width=True)
        
        with col2:
            # Gráfico de resultado por curso
            fig_resultado = px.bar(
                df_cursos,
                x='Curso',
                y='Resultado',
                title='Resultado Líquido por Curso',
                color='Resultado',
                color_continuous_scale=['red', 'yellow', 'green']
            )
            fig_resultado.update_layout(
                xaxis_title='Curso',
                yaxis_title='Resultado (R$)'
            )
            st.plotly_chart(fig_resultado, use_container_width=True)
    
    except Exception as e:
        st.error(f"Erro ao gerar gráficos: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666666;'>
        <p>Instituto Metaforma - Sistema de Gestão Financeira</p>
        <p>Para suporte técnico, entre em contato com a equipe de TI</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
