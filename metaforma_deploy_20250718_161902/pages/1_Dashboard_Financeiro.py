import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_handler import DataHandler
from utils.financial_calculator import FinancialCalculator

st.set_page_config(page_title="Dashboard Financeiro", page_icon="📊", layout="wide")

def main():
    st.title("📊 Dashboard Financeiro")
    st.markdown("---")
    
    # Sidebar com filtros
    with st.sidebar:
        st.header("🔍 Filtros")
        
        # Seleção de período
        periodo_opcoes = ["Todos", "FAC_17", "FAC_16", "FAC_15", "FAC_14"]
        periodo_selecionado = st.selectbox("Selecionar Período/Curso:", periodo_opcoes)
        
        # Tipo de visualização
        tipo_visualizacao = st.radio(
            "Tipo de Dados:",
            ["Orçamento vs Realizado", "Apenas Orçamento", "Apenas Realizado"]
        )
        
        st.markdown("---")
        st.subheader("📋 Legenda")
        st.markdown("""
        - **FAC**: Código do curso/turma
        - **Receita Bruta**: Valor total das vendas
        - **Inadimplência**: Valores não pagos
        - **Receita Líquida**: Receita após inadimplência
        - **Resultado Líquido**: Lucro final após todas as deduções
        """)
    
    try:
        # Dados financeiros baseados no PDF
        dados_orcamento = {
            'Periodo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14', 'TOTAL'],
            'Receita_Bruta': [25220.0, 15400.0, 17290.0, 20370.0, 78280.0],
            'Inadimplencia': [0.0, 0.0, 0.0, 0.0, 0.0],
            'Receita_Liquida': [25220.0, 15400.0, 17290.0, 20370.0, 78280.0],
            'Despesas': [0.0, 4301.6, 4591.6, 5804.2, 14697.4],
            'Facebook_Anuncios': [0.0, 2100.0, 2100.0, 3000.0, 7200.0],
            'Creditos_Plataforma': [0.0, 803.2, 903.6, 1104.4, 2811.2],
            'Boletos': [0.0, 798.4, 988.0, 1099.8, 2886.2],
            'Gestor_Trafego': [0.0, 600.0, 600.0, 600.0, 1800.0],
            'Resultado_Bruto': [25220.0, 11098.4, 12698.4, 14565.8, 63582.6],
            'Comissao': [2522.0, 5549.2, 6349.2, 7282.9, 21703.3],
            'Resultado_Liquido': [22698.0, 5549.2, 6349.2, 7282.9, 41879.3]
        }
        
        dados_realizado = {
            'Periodo': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14', 'TOTAL'],
            'Receita_Bruta': [3589.0, 3760.0, 7105.0, 9894.0, 24348.0],
            'Inadimplencia': [2910.0, 0.0, 291.0, 2328.0, 5529.0],
            'Receita_Liquida': [679.0, 3760.0, 6814.0, 7566.0, 18819.0],
            'Despesas': [6072.9, 3662.9, 4052.7, 5364.3, 19152.7],
            'Facebook_Anuncios': [3000.0, 2100.0, 2100.0, 3000.0, 10200.0],
            'Creditos_Plataforma': [1305.2, 803.2, 903.6, 1104.4, 4116.4],
            'Boletos': [1167.7, 159.7, 449.1, 659.9, 2436.3],
            'Gestor_Trafego': [600.0, 600.0, 600.0, 600.0, 2400.0],
            'Resultado_Bruto': [-5393.9, 97.1, 2761.3, 2201.7, -333.7],
            'Comissao': [-2696.9, 48.6, 1380.7, 1100.9, -166.9],
            'Resultado_Liquido': [-2696.9, 48.6, 1380.7, 1100.9, -166.9]
        }
        
        df_orcamento = pd.DataFrame(dados_orcamento)
        df_realizado = pd.DataFrame(dados_realizado)
        
        # Aplicar filtro de período
        if periodo_selecionado != "Todos":
            df_orcamento_filtrado = df_orcamento[df_orcamento['Periodo'] == periodo_selecionado]
            df_realizado_filtrado = df_realizado[df_realizado['Periodo'] == periodo_selecionado]
        else:
            df_orcamento_filtrado = df_orcamento[df_orcamento['Periodo'] != 'TOTAL']
            df_realizado_filtrado = df_realizado[df_realizado['Periodo'] != 'TOTAL']
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        if periodo_selecionado == "Todos":
            receita_orc = df_orcamento[df_orcamento['Periodo'] == 'TOTAL']['Receita_Bruta'].iloc[0]
            receita_real = df_realizado[df_realizado['Periodo'] == 'TOTAL']['Receita_Bruta'].iloc[0]
            resultado_orc = df_orcamento[df_orcamento['Periodo'] == 'TOTAL']['Resultado_Liquido'].iloc[0]
            resultado_real = df_realizado[df_realizado['Periodo'] == 'TOTAL']['Resultado_Liquido'].iloc[0]
        else:
            receita_orc = df_orcamento_filtrado['Receita_Bruta'].iloc[0] if not df_orcamento_filtrado.empty else 0
            receita_real = df_realizado_filtrado['Receita_Bruta'].iloc[0] if not df_realizado_filtrado.empty else 0
            resultado_orc = df_orcamento_filtrado['Resultado_Liquido'].iloc[0] if not df_orcamento_filtrado.empty else 0
            resultado_real = df_realizado_filtrado['Resultado_Liquido'].iloc[0] if not df_realizado_filtrado.empty else 0
        
        with col1:
            st.metric(
                "💰 Receita Orçada",
                f"R$ {receita_orc:,.2f}",
                delta=None
            )
        
        with col2:
            st.metric(
                "💵 Receita Realizada",
                f"R$ {receita_real:,.2f}",
                delta=f"{((receita_real - receita_orc) / receita_orc * 100):+.1f}%" if receita_orc != 0 else "N/A"
            )
        
        with col3:
            st.metric(
                "📊 Resultado Orçado",
                f"R$ {resultado_orc:,.2f}",
                delta=None
            )
        
        with col4:
            st.metric(
                "📈 Resultado Realizado",
                f"R$ {resultado_real:,.2f}",
                delta=f"{((resultado_real - resultado_orc) / abs(resultado_orc) * 100):+.1f}%" if resultado_orc != 0 else "N/A"
            )
        
        st.markdown("---")
        
        # Gráficos principais
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Receita: Orçado vs Realizado")
            
            if tipo_visualizacao in ["Orçamento vs Realizado", "Apenas Orçamento"]:
                periodos = df_orcamento_filtrado['Periodo'].tolist()
                receita_orc_valores = df_orcamento_filtrado['Receita_Bruta'].tolist()
            else:
                periodos = []
                receita_orc_valores = []
                
            if tipo_visualizacao in ["Orçamento vs Realizado", "Apenas Realizado"]:
                periodos_real = df_realizado_filtrado['Periodo'].tolist()
                receita_real_valores = df_realizado_filtrado['Receita_Bruta'].tolist()
            else:
                periodos_real = []
                receita_real_valores = []
            
            fig_receita = go.Figure()
            
            if receita_orc_valores:
                fig_receita.add_trace(go.Bar(
                    name='Orçado',
                    x=periodos,
                    y=receita_orc_valores,
                    marker_color='lightblue'
                ))
            
            if receita_real_valores:
                fig_receita.add_trace(go.Bar(
                    name='Realizado',
                    x=periodos_real,
                    y=receita_real_valores,
                    marker_color='darkblue'
                ))
            
            fig_receita.update_layout(
                xaxis_title='Período',
                yaxis_title='Valor (R$)',
                barmode='group',
                height=400
            )
            st.plotly_chart(fig_receita, use_container_width=True)
        
        with col2:
            st.subheader("💹 Resultado Líquido")
            
            if tipo_visualizacao in ["Orçamento vs Realizado", "Apenas Orçamento"]:
                resultado_orc_valores = df_orcamento_filtrado['Resultado_Liquido'].tolist()
            else:
                resultado_orc_valores = []
                
            if tipo_visualizacao in ["Orçamento vs Realizado", "Apenas Realizado"]:
                resultado_real_valores = df_realizado_filtrado['Resultado_Liquido'].tolist()
            else:
                resultado_real_valores = []
            
            fig_resultado = go.Figure()
            
            if resultado_orc_valores:
                fig_resultado.add_trace(go.Bar(
                    name='Orçado',
                    x=periodos,
                    y=resultado_orc_valores,
                    marker_color='lightgreen'
                ))
            
            if resultado_real_valores:
                fig_resultado.add_trace(go.Bar(
                    name='Realizado',
                    x=periodos_real,
                    y=resultado_real_valores,
                    marker_color='green'
                ))
            
            fig_resultado.update_layout(
                xaxis_title='Período',
                yaxis_title='Valor (R$)',
                barmode='group',
                height=400
            )
            st.plotly_chart(fig_resultado, use_container_width=True)
        
        # Tabela detalhada
        st.markdown("---")
        st.subheader("📋 Detalhamento Financeiro")
        
        # Abas para diferentes visualizações
        tab1, tab2, tab3 = st.tabs(["💰 Orçamento", "📊 Realizado", "🔍 Comparativo"])
        
        with tab1:
            st.dataframe(
                df_orcamento_filtrado.round(2),
                use_container_width=True,
                hide_index=True
            )
        
        with tab2:
            st.dataframe(
                df_realizado_filtrado.round(2),
                use_container_width=True,
                hide_index=True
            )
        
        with tab3:
            # Criar tabela comparativa
            if not df_orcamento_filtrado.empty and not df_realizado_filtrado.empty:
                df_comparativo = pd.DataFrame({
                    'Período': df_orcamento_filtrado['Periodo'],
                    'Receita_Orçada': df_orcamento_filtrado['Receita_Bruta'],
                    'Receita_Realizada': df_realizado_filtrado['Receita_Bruta'],
                    'Diferença_Receita': df_realizado_filtrado['Receita_Bruta'] - df_orcamento_filtrado['Receita_Bruta'],
                    'Resultado_Orçado': df_orcamento_filtrado['Resultado_Liquido'],
                    'Resultado_Realizado': df_realizado_filtrado['Resultado_Liquido'],
                    'Diferença_Resultado': df_realizado_filtrado['Resultado_Liquido'] - df_orcamento_filtrado['Resultado_Liquido']
                })
                
                st.dataframe(
                    df_comparativo.round(2),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.warning("Selecione um período específico para ver o comparativo.")
        
        # Análise de despesas
        st.markdown("---")
        st.subheader("💸 Análise de Despesas")
        
        if periodo_selecionado != "Todos":
            periodo_dados = df_realizado_filtrado.iloc[0] if not df_realizado_filtrado.empty else None
            
            if periodo_dados is not None:
                despesas_detalhes = {
                    'Facebook (Anúncios)': periodo_dados['Facebook_Anuncios'],
                    'Créditos Plataforma': periodo_dados['Creditos_Plataforma'],
                    'Boletos': periodo_dados['Boletos'],
                    'Gestor de Tráfego': periodo_dados['Gestor_Trafego']
                }
                
                fig_despesas = px.pie(
                    values=list(despesas_detalhes.values()),
                    names=list(despesas_detalhes.keys()),
                    title=f"Distribuição de Despesas - {periodo_selecionado}"
                )
                st.plotly_chart(fig_despesas, use_container_width=True)
        
    except Exception as e:
        st.error(f"Erro ao carregar dados financeiros: {str(e)}")
        st.info("Verifique se os dados foram importados corretamente na seção 'Importar Dados'.")

if __name__ == "__main__":
    main()
