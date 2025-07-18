import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

st.set_page_config(page_title="Relatórios", page_icon="📋", layout="wide")

def main():
    st.title("📋 Relatórios")
    st.markdown("---")
    
    # Tabs para diferentes tipos de relatórios
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Relatório Financeiro", "📊 Performance", "👥 Inadimplência", "📈 Dashboard Executivo"])
    
    with tab1:
        st.subheader("💰 Relatório Financeiro Detalhado")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            periodo_relatorio = st.selectbox(
                "Período:",
                ["Todos os Períodos", "FAC_17", "FAC_16", "FAC_15", "FAC_14"]
            )
        
        with col2:
            tipo_relatorio = st.selectbox(
                "Tipo de Relatório:",
                ["Completo", "Apenas Receitas", "Apenas Despesas", "Apenas Resultados"]
            )
        
        with col3:
            formato_valores = st.selectbox(
                "Formato dos Valores:",
                ["Reais (R$)", "Percentual (%)", "Ambos"]
            )
        
        # Dados financeiros consolidados
        dados_financeiros = {
            'Período': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14', 'TOTAL'],
            'Receita_Orçada': [25220.0, 15400.0, 17290.0, 20370.0, 78280.0],
            'Receita_Realizada': [3589.0, 3760.0, 7105.0, 9894.0, 24348.0],
            'Variação_Receita': [-21631.0, -11640.0, -10185.0, -10476.0, -53932.0],
            'Despesas_Orçadas': [0.0, 4301.6, 4591.6, 5804.2, 14697.4],
            'Despesas_Realizadas': [6072.9, 3662.9, 4052.7, 5364.3, 19152.7],
            'Variação_Despesas': [6072.9, -638.7, -538.9, -439.9, 4455.3],
            'Resultado_Orçado': [22698.0, 5549.2, 6349.2, 7282.9, 41879.3],
            'Resultado_Realizado': [-2696.9, 48.6, 1380.7, 1100.9, -166.9],
            'Variação_Resultado': [-25394.9, -5500.6, -4968.5, -6182.0, -42046.2]
        }
        
        df_financeiro = pd.DataFrame(dados_financeiros)
        
        # Aplicar filtro se necessário
        if periodo_relatorio != "Todos os Períodos":
            df_filtrado = df_financeiro[df_financeiro['Período'] == periodo_relatorio]
        else:
            df_filtrado = df_financeiro
        
        # Exibir métricas principais
        st.subheader("📊 Métricas Principais")
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_receita_orc = df_financeiro[df_financeiro['Período'] == 'TOTAL']['Receita_Orçada'].iloc[0]
        total_receita_real = df_financeiro[df_financeiro['Período'] == 'TOTAL']['Receita_Realizada'].iloc[0]
        total_resultado_orc = df_financeiro[df_financeiro['Período'] == 'TOTAL']['Resultado_Orçado'].iloc[0]
        total_resultado_real = df_financeiro[df_financeiro['Período'] == 'TOTAL']['Resultado_Realizado'].iloc[0]
        
        with col1:
            st.metric(
                "💰 Receita Total Orçada",
                f"R$ {total_receita_orc:,.2f}",
                help="Valor total planejado de receitas"
            )
        
        with col2:
            st.metric(
                "💵 Receita Total Realizada",
                f"R$ {total_receita_real:,.2f}",
                delta=f"{((total_receita_real - total_receita_orc) / total_receita_orc * 100):.1f}%"
            )
        
        with col3:
            st.metric(
                "📊 Resultado Orçado",
                f"R$ {total_resultado_orc:,.2f}",
                help="Lucro planejado"
            )
        
        with col4:
            st.metric(
                "📈 Resultado Realizado",
                f"R$ {total_resultado_real:,.2f}",
                delta=f"{((total_resultado_real - total_resultado_orc) / abs(total_resultado_orc) * 100):+.1f}%"
            )
        
        st.markdown("---")
        
        # Gráficos do relatório financeiro
        if tipo_relatorio in ["Completo", "Apenas Receitas"]:
            st.subheader("💰 Análise de Receitas")
            
            fig_receitas = go.Figure()
            
            periodos = df_filtrado[df_filtrado['Período'] != 'TOTAL']['Período']
            receitas_orc = df_filtrado[df_filtrado['Período'] != 'TOTAL']['Receita_Orçada']
            receitas_real = df_filtrado[df_filtrado['Período'] != 'TOTAL']['Receita_Realizada']
            
            fig_receitas.add_trace(go.Bar(
                name='Orçado',
                x=periodos,
                y=receitas_orc,
                marker_color='lightblue'
            ))
            
            fig_receitas.add_trace(go.Bar(
                name='Realizado',
                x=periodos,
                y=receitas_real,
                marker_color='darkblue'
            ))
            
            fig_receitas.update_layout(
                title='Receitas: Orçado vs Realizado',
                xaxis_title='Período',
                yaxis_title='Valor (R$)',
                barmode='group'
            )
            
            st.plotly_chart(fig_receitas, use_container_width=True)
        
        if tipo_relatorio in ["Completo", "Apenas Despesas"]:
            st.subheader("💸 Análise de Despesas")
            
            # Dados detalhados de despesas
            despesas_detalhadas = {
                'Categoria': ['Facebook (Anúncios)', 'Créditos Plataforma', 'Boletos', 'Gestor de Tráfego'],
                'FAC_17': [3000.0, 1305.2, 1167.7, 600.0],
                'FAC_16': [2100.0, 803.2, 159.7, 600.0],
                'FAC_15': [2100.0, 903.6, 449.1, 600.0],
                'FAC_14': [3000.0, 1104.4, 659.9, 600.0]
            }
            
            df_despesas = pd.DataFrame(despesas_detalhadas)
            
            # Gráfico de despesas por categoria
            fig_despesas = px.bar(
                df_despesas.melt(id_vars=['Categoria'], var_name='Período', value_name='Valor'),
                x='Categoria',
                y='Valor',
                color='Período',
                title='Despesas por Categoria e Período',
                barmode='group'
            )
            
            st.plotly_chart(fig_despesas, use_container_width=True)
        
        if tipo_relatorio in ["Completo", "Apenas Resultados"]:
            st.subheader("📈 Análise de Resultados")
            
            fig_resultados = go.Figure()
            
            resultados_orc = df_filtrado[df_filtrado['Período'] != 'TOTAL']['Resultado_Orçado']
            resultados_real = df_filtrado[df_filtrado['Período'] != 'TOTAL']['Resultado_Realizado']
            
            fig_resultados.add_trace(go.Scatter(
                x=periodos,
                y=resultados_orc,
                mode='lines+markers',
                name='Resultado Orçado',
                line=dict(color='green')
            ))
            
            fig_resultados.add_trace(go.Scatter(
                x=periodos,
                y=resultados_real,
                mode='lines+markers',
                name='Resultado Realizado',
                line=dict(color='red')
            ))
            
            fig_resultados.update_layout(
                title='Evolução dos Resultados',
                xaxis_title='Período',
                yaxis_title='Valor (R$)'
            )
            
            st.plotly_chart(fig_resultados, use_container_width=True)
        
        # Tabela detalhada
        st.subheader("📋 Dados Detalhados")
        
        colunas_exibir = ['Período']
        
        if tipo_relatorio in ["Completo", "Apenas Receitas"]:
            colunas_exibir.extend(['Receita_Orçada', 'Receita_Realizada', 'Variação_Receita'])
        
        if tipo_relatorio in ["Completo", "Apenas Despesas"]:
            colunas_exibir.extend(['Despesas_Orçadas', 'Despesas_Realizadas', 'Variação_Despesas'])
        
        if tipo_relatorio in ["Completo", "Apenas Resultados"]:
            colunas_exibir.extend(['Resultado_Orçado', 'Resultado_Realizado', 'Variação_Resultado'])
        
        df_exibicao = df_filtrado[colunas_exibir].copy()
        
        # Formatação condicional para valores
        if formato_valores in ["Reais (R$)", "Ambos"]:
            for col in df_exibicao.columns:
                if col != 'Período':
                    df_exibicao[col] = df_exibicao[col].apply(lambda x: f"R$ {x:,.2f}")
        
        st.dataframe(df_exibicao, use_container_width=True, hide_index=True)
        
        # Botões de exportação
        st.subheader("📤 Exportar Relatório")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Exportar Excel", use_container_width=True):
                st.success("✅ Relatório Excel gerado!")
                st.info("💡 Em produção, o download iniciaria automaticamente.")
        
        with col2:
            if st.button("📄 Exportar PDF", use_container_width=True):
                st.success("✅ Relatório PDF gerado!")
                st.info("💡 Em produção, o download iniciaria automaticamente.")
        
        with col3:
            if st.button("📋 Copiar para Clipboard", use_container_width=True):
                st.success("✅ Dados copiados!")
                st.info("💡 Em produção, os dados seriam copiados para a área de transferência.")
    
    with tab2:
        st.subheader("📊 Relatório de Performance")
        
        # KPIs de Performance
        st.subheader("🎯 Indicadores de Performance")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 Taxa de Conversão",
                "31.1%",
                delta="2.1%",
                help="Receita realizada / Receita orçada"
            )
        
        with col2:
            st.metric(
                "💰 Ticket Médio",
                "R$ 300,60",
                delta="-R$ 50,40",
                help="Receita total / Número de alunos"
            )
        
        with col3:
            st.metric(
                "📈 ROI",
                "-0.87%",
                delta="-100.87%",
                help="(Resultado - Investimento) / Investimento"
            )
        
        with col4:
            st.metric(
                "⚡ Eficiência Operacional",
                "78.7%",
                delta="-21.3%",
                help="1 - (Despesas realizadas / Receita realizada)"
            )
        
        st.markdown("---")
        
        # Gráficos de performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Performance por Período")
            
            periodos_perf = ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14']
            taxa_conversao = [14.2, 24.4, 41.1, 48.6]  # % receita realizada vs orçada
            
            fig_perf = px.line(
                x=periodos_perf,
                y=taxa_conversao,
                title='Taxa de Conversão por Período (%)',
                markers=True
            )
            fig_perf.update_traces(line_color='blue', marker_color='red')
            fig_perf.update_layout(
                xaxis_title='Período',
                yaxis_title='Taxa de Conversão (%)'
            )
            
            st.plotly_chart(fig_perf, use_container_width=True)
        
        with col2:
            st.subheader("💸 Eficiência de Custos")
            
            # Dados de eficiência (Despesas vs Receita)
            eficiencia_dados = {
                'Período': periodos_perf,
                'Receita': [3589.0, 3760.0, 7105.0, 9894.0],
                'Despesas': [6072.9, 3662.9, 4052.7, 5364.3]
            }
            
            df_eficiencia = pd.DataFrame(eficiencia_dados)
            df_eficiencia['Eficiência'] = (1 - df_eficiencia['Despesas'] / df_eficiencia['Receita']) * 100
            
            fig_efic = px.bar(
                df_eficiencia,
                x='Período',
                y='Eficiência',
                title='Eficiência Operacional (%)',
                color='Eficiência',
                color_continuous_scale=['red', 'yellow', 'green']
            )
            
            st.plotly_chart(fig_efic, use_container_width=True)
        
        # Análise de tendências
        st.subheader("📊 Análise de Tendências")
        
        tendencias_dados = {
            'Métrica': ['Receita', 'Despesas', 'Resultado', 'Inadimplência'],
            'Tendência': ['📉 Declinante', '📈 Crescente', '📉 Negativa', '📈 Alta'],
            'Variação_Mensal': ['-15.2%', '+8.5%', '-85.3%', '+22.7%'],
            'Status': ['⚠️ Atenção', '⚠️ Atenção', '🚨 Crítico', '🚨 Crítico'],
            'Ação_Recomendada': ['Revisar estratégia de vendas', 'Otimizar custos operacionais', 'Reestruturar modelo financeiro', 'Implementar política de cobrança']
        }
        
        df_tendencias = pd.DataFrame(tendencias_dados)
        
        st.dataframe(
            df_tendencias,
            use_container_width=True,
            hide_index=True
        )
    
    with tab3:
        st.subheader("👥 Relatório de Inadimplência")
        
        # Dados de inadimplência por período
        inadimplencia_dados = {
            'Período': ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14', 'TOTAL'],
            'Receita_Bruta': [3589.0, 3760.0, 7105.0, 9894.0, 24348.0],
            'Inadimplência': [2910.0, 0.0, 291.0, 2328.0, 5529.0],
            'Taxa_Inadimplência': [81.1, 0.0, 4.1, 23.5, 22.7],
            'Receita_Líquida': [679.0, 3760.0, 6814.0, 7566.0, 18819.0]
        }
        
        df_inadim = pd.DataFrame(inadimplencia_dados)
        
        # Métricas de inadimplência
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_inadim = df_inadim[df_inadim['Período'] == 'TOTAL']['Inadimplência'].iloc[0]
            st.metric(
                "💸 Total Inadimplência",
                f"R$ {total_inadim:,.2f}",
                help="Valor total não recebido"
            )
        
        with col2:
            taxa_media = df_inadim[df_inadim['Período'] == 'TOTAL']['Taxa_Inadimplência'].iloc[0]
            st.metric(
                "📊 Taxa Média",
                f"{taxa_media:.1f}%",
                delta="+22.7%",
                help="Percentual de inadimplência sobre receita bruta"
            )
        
        with col3:
            # Período com maior inadimplência
            periodo_max = df_inadim[df_inadim['Período'] != 'TOTAL'].loc[df_inadim['Taxa_Inadimplência'].idxmax(), 'Período']
            taxa_max = df_inadim[df_inadim['Período'] != 'TOTAL']['Taxa_Inadimplência'].max()
            st.metric(
                "🚨 Maior Taxa",
                f"{periodo_max}: {taxa_max:.1f}%",
                help="Período com maior taxa de inadimplência"
            )
        
        with col4:
            # Impacto financeiro
            impacto = (total_inadim / df_inadim[df_inadim['Período'] == 'TOTAL']['Receita_Bruta'].iloc[0]) * 100
            st.metric(
                "📉 Impacto na Receita",
                f"{impacto:.1f}%",
                help="Redução da receita devido à inadimplência"
            )
        
        st.markdown("---")
        
        # Gráficos de inadimplência
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Taxa de Inadimplência por Período")
            
            periodos_inadim = df_inadim[df_inadim['Período'] != 'TOTAL']['Período']
            taxas_inadim = df_inadim[df_inadim['Período'] != 'TOTAL']['Taxa_Inadimplência']
            
            fig_inadim = px.bar(
                x=periodos_inadim,
                y=taxas_inadim,
                title='Taxa de Inadimplência (%)',
                color=taxas_inadim,
                color_continuous_scale=['green', 'yellow', 'red']
            )
            fig_inadim.update_layout(
                xaxis_title='Período',
                yaxis_title='Taxa (%)'
            )
            
            st.plotly_chart(fig_inadim, use_container_width=True)
        
        with col2:
            st.subheader("💰 Impacto Financeiro")
            
            # Gráfico de receita bruta vs líquida
            fig_impacto = go.Figure()
            
            fig_impacto.add_trace(go.Bar(
                name='Receita Bruta',
                x=periodos_inadim,
                y=df_inadim[df_inadim['Período'] != 'TOTAL']['Receita_Bruta'],
                marker_color='lightblue'
            ))
            
            fig_impacto.add_trace(go.Bar(
                name='Receita Líquida',
                x=periodos_inadim,
                y=df_inadim[df_inadim['Período'] != 'TOTAL']['Receita_Líquida'],
                marker_color='darkblue'
            ))
            
            fig_impacto.update_layout(
                title='Receita Bruta vs Líquida',
                xaxis_title='Período',
                yaxis_title='Valor (R$)',
                barmode='group'
            )
            
            st.plotly_chart(fig_impacto, use_container_width=True)
        
        # Análise detalhada
        st.subheader("🔍 Análise Detalhada de Inadimplência")
        
        # Tabela com dados de inadimplência
        df_inadim_display = df_inadim[df_inadim['Período'] != 'TOTAL'].copy()
        df_inadim_display['Receita_Bruta'] = df_inadim_display['Receita_Bruta'].apply(lambda x: f"R$ {x:,.2f}")
        df_inadim_display['Inadimplência'] = df_inadim_display['Inadimplência'].apply(lambda x: f"R$ {x:,.2f}")
        df_inadim_display['Receita_Líquida'] = df_inadim_display['Receita_Líquida'].apply(lambda x: f"R$ {x:,.2f}")
        df_inadim_display['Taxa_Inadimplência'] = df_inadim_display['Taxa_Inadimplência'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(df_inadim_display, use_container_width=True, hide_index=True)
        
        # Recomendações
        st.subheader("💡 Recomendações")
        
        st.warning("""
        **🚨 Ações Urgentes Recomendadas:**
        
        1. **FAC_17**: Taxa crítica de 81.1% - Implementar cobrança imediata
        2. **FAC_14**: Taxa alta de 23.5% - Revisar política de crédito
        3. **Implementar**: Sistema de cobrança automatizada
        4. **Monitorar**: Indicadores de risco de inadimplência
        5. **Revisar**: Processo de aprovação de crédito
        """)
    
    with tab4:
        st.subheader("📈 Dashboard Executivo")
        
        # Resumo executivo
        st.markdown("""
        ## 📊 Resumo Executivo - Instituto Metaforma
        
        **Período de Análise:** 2024 (FAC_14 a FAC_17)
        """)
        
        # Indicadores principais em cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            ### 💰 Situação Financeira
            - **Receita Orçada:** R$ 78.280,00
            - **Receita Realizada:** R$ 24.348,00
            - **Atingimento:** 31.1% do orçado
            - **Status:** 🚨 Crítico
            """)
        
        with col2:
            st.markdown("""
            ### 📊 Operacional
            - **Total de Alunos:** 81
            - **Ticket Médio:** R$ 300,60
            - **Cursos Ativos:** 4 (FAC_14-17)
            - **Estados Atendidos:** 8
            """)
        
        with col3:
            st.markdown("""
            ### ⚠️ Principais Riscos
            - **Inadimplência:** 22.7%
            - **Resultado Negativo:** -R$ 166,90
            - **ROI:** -0.87%
            - **Despesas Acima:** +30.3%
            """)
        
        st.markdown("---")
        
        # Gráfico executivo principal
        st.subheader("📊 Visão Consolidada")
        
        # Criar gráfico combinado
        fig_executivo = go.Figure()
        
        periodos = ['FAC_17', 'FAC_16', 'FAC_15', 'FAC_14']
        receita_orc = [25220.0, 15400.0, 17290.0, 20370.0]
        receita_real = [3589.0, 3760.0, 7105.0, 9894.0]
        resultado = [-2696.9, 48.6, 1380.7, 1100.9]
        
        # Barras de receita
        fig_executivo.add_trace(go.Bar(
            name='Receita Orçada',
            x=periodos,
            y=receita_orc,
            yaxis='y',
            marker_color='lightblue',
            opacity=0.7
        ))
        
        fig_executivo.add_trace(go.Bar(
            name='Receita Realizada',
            x=periodos,
            y=receita_real,
            yaxis='y',
            marker_color='darkblue'
        ))
        
        # Linha de resultado
        fig_executivo.add_trace(go.Scatter(
            name='Resultado Líquido',
            x=periodos,
            y=resultado,
            yaxis='y2',
            mode='lines+markers',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        fig_executivo.update_layout(
            title='Visão Executiva: Receitas e Resultado por Período',
            xaxis_title='Período',
            yaxis=dict(
                title='Receita (R$)',
                side='left'
            ),
            yaxis2=dict(
                title='Resultado Líquido (R$)',
                side='right',
                overlaying='y'
            ),
            barmode='group',
            height=500
        )
        
        st.plotly_chart(fig_executivo, use_container_width=True)
        
        # Análise SWOT simplificada
        st.subheader("🎯 Análise Estratégica")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### ✅ Pontos Fortes
            - Diversificação geográfica (8 estados)
            - Curso especializado com demanda
            - Base de dados de alunos estabelecida
            - Sistema de gestão implementado
            """)
            
            st.markdown("""
            ### 🚫 Pontos Fracos
            - Alta taxa de inadimplência
            - Baixo atingimento do orçamento
            - Resultado financeiro negativo
            - Despesas operacionais elevadas
            """)
        
        with col2:
            st.markdown("""
            ### 🔮 Oportunidades
            - Melhorar processo de cobrança
            - Otimizar investimento em marketing
            - Expandir para novos cursos
            - Implementar parcerias estratégicas
            """)
            
            st.markdown("""
            ### ⚠️ Ameaças
            - Concorrência no mercado educacional
            - Impacto econômico na inadimplência
            - Dependência de marketing digital
            - Sazonalidade na demanda
            """)
        
        # Recomendações estratégicas
        st.subheader("🎯 Recomendações Estratégicas")
        
        st.info("""
        **🔄 Ações Imediatas (30 dias):**
        1. Implementar sistema de cobrança automatizada
        2. Revisar estratégia de marketing digital
        3. Análise detalhada da inadimplência por período
        4. Renegociação de contratos de fornecedores
        
        **📈 Ações de Médio Prazo (90 dias):**
        1. Reestruturação do modelo de precificação
        2. Diversificação da matriz de cursos
        3. Implementação de programa de fidelização
        4. Otimização dos canais de aquisição
        
        **🚀 Ações de Longo Prazo (180+ dias):**
        1. Expansão para novos mercados
        2. Parcerias estratégicas com empresas
        3. Desenvolvimento de plataforma própria
        4. Criação de programa de certificação
        """)

if __name__ == "__main__":
    main()
