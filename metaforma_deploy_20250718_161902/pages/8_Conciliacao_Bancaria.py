import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from utils.bank_reconciliation import BankReconciliation
from utils.advanced_data_handler import AdvancedDataHandler

def main():
    """Página principal de conciliação bancária."""
    
    st.set_page_config(
        page_title="Conciliação Bancária - Instituto Metaforma",
        page_icon="🏦",
        layout="wide"
    )
    
    st.title("🏦 Conciliação Bancária e Adimplência")
    st.markdown("### Sistema de validação de pagamentos e análise de inadimplência")
    
    # Inicializar handlers
    if 'bank_reconciliation' not in st.session_state:
        st.session_state.bank_reconciliation = BankReconciliation()
    
    if 'advanced_data_handler' not in st.session_state:
        st.session_state.advanced_data_handler = AdvancedDataHandler()
    
    reconciler = st.session_state.bank_reconciliation
    data_handler = st.session_state.advanced_data_handler
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard Adimplência", 
        "🏦 Conciliação Extrato", 
        "📋 Relatórios Detalhados", 
        "⚙️ Configurações"
    ])
    
    with tab1:
        show_adimplencia_dashboard(reconciler, data_handler)
    
    with tab2:
        show_bank_reconciliation(reconciler, data_handler)
    
    with tab3:
        show_detailed_reports(reconciler, data_handler)
    
    with tab4:
        show_reconciliation_settings(reconciler)

def show_adimplencia_dashboard(reconciler, data_handler):
    """Mostra dashboard de adimplência."""
    
    st.subheader("📊 Dashboard de Adimplência")
    
    # Obter dados dos alunos
    students_data = data_handler.get_all_students()
    
    if students_data.empty:
        st.warning("⚠️ Nenhum aluno cadastrado. Acesse 'Gestão Avançada de Alunos' para adicionar dados.")
        return
    
    # Gerar pagamentos esperados
    expected_payments = reconciler.generate_expected_payments(students_data)
    
    if not expected_payments:
        st.error("❌ Erro ao gerar pagamentos esperados")
        return
    
    # Simular conciliação com dados bancários de exemplo
    bank_transactions = reconciler.load_bank_extract()
    reconciliation_result = reconciler.reconcile_payments(bank_transactions, expected_payments)
    
    if not reconciliation_result:
        st.error("❌ Erro na conciliação bancária")
        return
    
    # Obter métricas para dashboard
    dashboard_metrics = reconciler.generate_dashboard_metrics(reconciliation_result)
    
    # Métricas principais
    st.subheader("📈 Métricas Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        adimplencia_rate = dashboard_metrics['adimplencia']['rate']
        st.metric(
            "📈 Taxa de Adimplência",
            f"{adimplencia_rate:.1f}%",
            delta=f"+{adimplencia_rate - 75:.1f}% vs meta (75%)"
        )
    
    with col2:
        inadimplencia_rate = dashboard_metrics['inadimplencia']['rate']
        st.metric(
            "📉 Taxa de Inadimplência",
            f"{inadimplencia_rate:.1f}%",
            delta=f"{inadimplencia_rate - 25:.1f}% vs meta (25%)"
        )
    
    with col3:
        eficiencia = dashboard_metrics['financeiro']['eficiencia_cobranca']
        st.metric(
            "💰 Eficiência Cobrança",
            f"{eficiencia:.1f}%",
            delta=f"+{eficiencia - 85:.1f}% vs meta (85%)"
        )
    
    with col4:
        taxa_identificacao = dashboard_metrics['conciliacao']['taxa_identificacao']
        st.metric(
            "🔍 Taxa Identificação",
            f"{taxa_identificacao:.1f}%",
            delta=f"+{taxa_identificacao - 90:.1f}% vs meta (90%)"
        )
    
    # Gráficos de análise
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribuição de Pagamentos")
        
        # Dados para gráfico de pizza
        paid_count = dashboard_metrics['adimplencia']['count']
        overdue_count = dashboard_metrics['inadimplencia']['count']
        pending_count = len(expected_payments) - paid_count - overdue_count
        
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=['Pagos', 'Em Atraso', 'Pendentes'],
                values=[paid_count, overdue_count, pending_count],
                hole=0.4,
                marker_colors=['#2E8B57', '#DC143C', '#FFD700']
            )
        ])
        
        fig_pie.update_layout(
            title='Status dos Pagamentos',
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("💵 Valores por Status")
        
        # Gráfico de barras com valores
        categories = ['Recebido', 'Em Atraso', 'Pendente']
        values = [
            dashboard_metrics['adimplencia']['amount'],
            dashboard_metrics['inadimplencia']['amount'],
            dashboard_metrics['financeiro']['total_esperado'] - 
            dashboard_metrics['adimplencia']['amount'] - 
            dashboard_metrics['inadimplencia']['amount']
        ]
        
        fig_bar = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=['#2E8B57', '#DC143C', '#FFD700'],
                text=[f'R$ {v:,.2f}' for v in values],
                textposition='auto'
            )
        ])
        
        fig_bar.update_layout(
            title='Valores por Status (R$)',
            yaxis_title='Valor (R$)',
            height=400
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Análise temporal
    st.subheader("📅 Análise Temporal de Pagamentos")
    
    # Criar dados para gráfico temporal
    date_analysis = {}
    for payment in expected_payments:
        month_key = payment.due_date.strftime('%Y-%m')
        if month_key not in date_analysis:
            date_analysis[month_key] = {'expected': 0, 'paid': 0, 'overdue': 0}
        
        date_analysis[month_key]['expected'] += payment.amount
        if payment.status == 'paid':
            date_analysis[month_key]['paid'] += payment.amount
        elif payment.status == 'overdue':
            date_analysis[month_key]['overdue'] += payment.amount
    
    dates = sorted(date_analysis.keys())
    expected_values = [date_analysis[date]['expected'] for date in dates]
    paid_values = [date_analysis[date]['paid'] for date in dates]
    overdue_values = [date_analysis[date]['overdue'] for date in dates]
    
    fig_timeline = go.Figure()
    
    fig_timeline.add_trace(go.Scatter(
        x=dates,
        y=expected_values,
        mode='lines+markers',
        name='Esperado',
        line=dict(color='blue', width=2)
    ))
    
    fig_timeline.add_trace(go.Scatter(
        x=dates,
        y=paid_values,
        mode='lines+markers',
        name='Recebido',
        fill='tonexty',
        line=dict(color='green', width=2)
    ))
    
    fig_timeline.add_trace(go.Scatter(
        x=dates,
        y=overdue_values,
        mode='lines+markers',
        name='Em Atraso',
        line=dict(color='red', width=2)
    ))
    
    fig_timeline.update_layout(
        title='Evolução de Pagamentos por Mês',
        xaxis_title='Mês',
        yaxis_title='Valor (R$)',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Alertas e ações recomendadas
    st.subheader("🚨 Alertas e Ações Recomendadas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Alunos com mais atraso
        overdue_students = {}
        for payment in expected_payments:
            if payment.status == 'overdue':
                if payment.student_name not in overdue_students:
                    overdue_students[payment.student_name] = {
                        'count': 0,
                        'amount': 0,
                        'days_overdue': 0
                    }
                overdue_students[payment.student_name]['count'] += 1
                overdue_students[payment.student_name]['amount'] += payment.amount
                days_overdue = (datetime.now() - payment.due_date).days
                overdue_students[payment.student_name]['days_overdue'] = max(
                    overdue_students[payment.student_name]['days_overdue'],
                    days_overdue
                )
        
        if overdue_students:
            st.write("**🔴 Alunos com Maior Inadimplência:**")
            
            # Ordenar por valor em atraso
            sorted_students = sorted(
                overdue_students.items(),
                key=lambda x: x[1]['amount'],
                reverse=True
            )[:5]
            
            for student_name, info in sorted_students:
                st.write(f"• **{student_name}**: R$ {info['amount']:.2f} ({info['count']} parcelas, {info['days_overdue']} dias)")
        else:
            st.success("✅ Nenhum aluno em situação crítica")
    
    with col2:
        st.write("**💡 Ações Recomendadas:**")
        
        if inadimplencia_rate > 25:
            st.warning("📞 Intensificar cobrança - inadimplência acima da meta")
        
        if dashboard_metrics['conciliacao']['transacoes_nao_identificadas'] > 0:
            st.info(f"🔍 Investigar {dashboard_metrics['conciliacao']['transacoes_nao_identificadas']} transações não identificadas")
        
        if eficiencia < 85:
            st.warning("📈 Revisar processo de cobrança")
        
        st.write("🎯 **Próximas ações:**")
        st.write("1. Entrar em contato com inadimplentes")
        st.write("2. Revisar condições de pagamento")
        st.write("3. Atualizar dados bancários")
        st.write("4. Enviar lembretes automáticos")

def show_bank_reconciliation(reconciler, data_handler):
    """Mostra interface de conciliação bancária."""
    
    st.subheader("🏦 Conciliação de Extrato Bancário")
    
    st.markdown("""
    ### 📋 Como Funciona
    
    1. **Carregue seu extrato bancário** (CSV ou Excel)
    2. **Configure os parâmetros** de conciliação
    3. **Execute a conciliação** automática
    4. **Analise os resultados** e faça ajustes manuais
    """)
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📁 Carregar Extrato Bancário",
        type=['csv', 'xlsx', 'xls'],
        help="Arquivo deve conter colunas: Data, Valor, Descrição"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("⚙️ Parâmetros de Conciliação")
        
        tolerance_amount = st.number_input(
            "💰 Tolerância de Valor (R$)",
            min_value=0.0,
            max_value=50.0,
            value=5.0,
            step=1.0,
            help="Diferença máxima aceita entre valor esperado e recebido"
        )
        
        tolerance_days = st.number_input(
            "📅 Tolerância de Data (dias)",
            min_value=0,
            max_value=30,
            value=3,
            step=1,
            help="Diferença máxima aceita entre data de vencimento e pagamento"
        )
        
        # Atualizar tolerâncias no reconciler
        reconciler.tolerance_amount = tolerance_amount
        reconciler.tolerance_days = tolerance_days
    
    with col2:
        st.subheader("📊 Dados dos Alunos")
        
        students_data = data_handler.get_all_students()
        
        if not students_data.empty:
            st.success(f"✅ {len(students_data)} alunos carregados")
            st.write(f"💰 Total esperado: R$ {students_data['courseFee'].sum():,.2f}")
        else:
            st.warning("⚠️ Nenhum aluno cadastrado")
            return
    
    # Executar conciliação
    if st.button("🚀 Executar Conciliação", use_container_width=True):
        with st.spinner("Executando conciliação bancária..."):
            
            # Carregar extrato
            if uploaded_file:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        bank_data = pd.read_csv(uploaded_file)
                    else:
                        bank_data = pd.read_excel(uploaded_file)
                    
                    bank_transactions = reconciler.load_bank_extract(data=bank_data)
                    st.success(f"✅ Extrato carregado: {len(bank_transactions)} transações")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao carregar extrato: {str(e)}")
                    return
            else:
                # Usar dados de exemplo
                st.info("💡 Usando dados bancários de exemplo para demonstração")
                bank_transactions = reconciler.load_bank_extract()
            
            # Gerar pagamentos esperados
            expected_payments = reconciler.generate_expected_payments(students_data)
            
            # Executar conciliação
            reconciliation_result = reconciler.reconcile_payments(bank_transactions, expected_payments)
            
            if reconciliation_result:
                st.session_state['reconciliation_result'] = reconciliation_result
                st.session_state['reconciliation_timestamp'] = datetime.now()
                
                # Mostrar resultados resumidos
                metrics = reconciliation_result['metrics']
                
                st.subheader("📊 Resultados da Conciliação")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("✅ Pagamentos Identificados", metrics['total_paid'])
                
                with col2:
                    st.metric("❌ Pagamentos em Atraso", metrics['total_overdue'])
                
                with col3:
                    st.metric("⚠️ Transações Não Identificadas", len(reconciliation_result['unmatched_transactions']))
                
                with col4:
                    st.metric("📈 Taxa de Adimplência", f"{metrics['adimplencia_rate']:.1f}%")
                
                # Prévia do relatório
                st.subheader("👁️ Prévia dos Resultados")
                
                # Pagamentos identificados
                if reconciliation_result['matched_payments']:
                    st.write("**✅ Pagamentos Identificados:**")
                    matched_df = pd.DataFrame([
                        {
                            'Aluno': match['payment'].student_name,
                            'Valor': f"R$ {match['transaction'].amount:.2f}",
                            'Data': match['transaction'].date.strftime('%d/%m/%Y'),
                            'Score': f"{match['match_score']:.1%}"
                        }
                        for match in reconciliation_result['matched_payments'][:5]
                    ])
                    st.dataframe(matched_df, use_container_width=True)
                
                # Transações não identificadas
                if reconciliation_result['unmatched_transactions']:
                    st.write("**⚠️ Transações Não Identificadas:**")
                    unmatched_df = pd.DataFrame([
                        {
                            'Data': tx.date.strftime('%d/%m/%Y'),
                            'Valor': f"R$ {tx.amount:.2f}",
                            'Descrição': tx.description[:50]
                        }
                        for tx in reconciliation_result['unmatched_transactions'][:5]
                    ])
                    st.dataframe(unmatched_df, use_container_width=True)
                
                st.success("✅ Conciliação executada com sucesso! Acesse a aba 'Relatórios Detalhados' para ver o resultado completo.")
            
            else:
                st.error("❌ Erro na conciliação bancária")

def show_detailed_reports(reconciler, data_handler):
    """Mostra relatórios detalhados da conciliação."""
    
    st.subheader("📋 Relatórios Detalhados")
    
    if 'reconciliation_result' not in st.session_state:
        st.info("💡 Execute uma conciliação na aba 'Conciliação Extrato' primeiro")
        return
    
    reconciliation_result = st.session_state['reconciliation_result']
    timestamp = st.session_state.get('reconciliation_timestamp', datetime.now())
    
    st.write(f"**📅 Última conciliação:** {timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Gerar relatório completo
    report_df = reconciler.generate_reconciliation_report(reconciliation_result)
    
    if report_df.empty:
        st.error("❌ Erro ao gerar relatório")
        return
    
    # Filtros para o relatório
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tipo_filter = st.selectbox(
            "🔍 Filtrar por Tipo",
            ['Todos'] + list(report_df['Tipo'].unique())
        )
    
    with col2:
        status_filter = st.selectbox(
            "📊 Filtrar por Status",
            ['Todos'] + list(report_df['Status'].unique())
        )
    
    with col3:
        min_valor = st.number_input(
            "💰 Valor Mínimo (R$)",
            min_value=0.0,
            value=0.0
        )
    
    # Aplicar filtros
    filtered_df = report_df.copy()
    
    if tipo_filter != 'Todos':
        filtered_df = filtered_df[filtered_df['Tipo'] == tipo_filter]
    
    if status_filter != 'Todos':
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    
    if min_valor > 0:
        filtered_df = filtered_df[filtered_df['Valor_Esperado'] >= min_valor]
    
    # Mostrar relatório filtrado
    st.subheader(f"📊 Relatório Filtrado ({len(filtered_df)} registros)")
    
    # Formatação condicional
    def format_status(val):
        if '✅' in str(val):
            return 'background-color: #d4edda'
        elif '❌' in str(val):
            return 'background-color: #f8d7da'
        elif '⚠️' in str(val):
            return 'background-color: #fff3cd'
        return ''
    
    def format_diferenca(val):
        try:
            if float(val) > 0:
                return 'color: green'
            elif float(val) < 0:
                return 'color: red'
        except:
            pass
        return ''
    
    styled_df = filtered_df.style.applymap(format_status, subset=['Status']).applymap(format_diferenca, subset=['Diferenca'])
    
    st.dataframe(styled_df, use_container_width=True)
    
    # Estatísticas do relatório filtrado
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_records = len(filtered_df)
        st.metric("📊 Total de Registros", total_records)
    
    with col2:
        pagos = len(filtered_df[filtered_df['Status'].str.contains('✅', na=False)])
        st.metric("✅ Pagamentos Identificados", pagos)
    
    with col3:
        atrasados = len(filtered_df[filtered_df['Status'].str.contains('❌', na=False)])
        st.metric("❌ Pagamentos em Atraso", atrasados)
    
    with col4:
        nao_identificados = len(filtered_df[filtered_df['Status'].str.contains('⚠️', na=False)])
        st.metric("⚠️ Não Identificados", nao_identificados)
    
    # Opções de exportação
    st.markdown("---")
    st.subheader("📤 Exportar Relatório")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Exportar Excel", use_container_width=True):
            excel_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="⬇️ Baixar Excel",
                data=excel_data,
                file_name=f"conciliacao_bancaria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📄 Exportar JSON", use_container_width=True):
            json_data = {
                'relatorio': filtered_df.to_dict('records'),
                'resumo': reconciliation_result['metrics'],
                'timestamp': timestamp.isoformat()
            }
            
            json_str = json.dumps(json_data, indent=2, ensure_ascii=False, default=str)
            
            st.download_button(
                label="⬇️ Baixar JSON",
                data=json_str,
                file_name=f"conciliacao_relatorio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
    
    with col3:
        if st.button("📧 Gerar Email Resumo", use_container_width=True):
            email_content = f"""
Relatório de Conciliação Bancária - Instituto Metaforma
Data: {timestamp.strftime('%d/%m/%Y %H:%M:%S')}

RESUMO:
- Total de registros analisados: {len(filtered_df)}
- Pagamentos identificados: {pagos}
- Pagamentos em atraso: {atrasados}
- Transações não identificadas: {nao_identificados}

Taxa de adimplência: {reconciliation_result['metrics']['adimplencia_rate']:.1f}%
Taxa de inadimplência: {reconciliation_result['metrics']['inadimplencia_rate']:.1f}%

Para detalhes completos, consulte o sistema de gestão.
            """
            
            st.text_area("📧 Conteúdo do Email", email_content, height=200)
            st.info("💡 Copie o conteúdo acima para enviar por email")

def show_reconciliation_settings(reconciler):
    """Mostra configurações da conciliação."""
    
    st.subheader("⚙️ Configurações de Conciliação")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Parâmetros de Correspondência")
        
        # Configurações de tolerância
        tolerance_amount = st.slider(
            "💰 Tolerância de Valor (R$)",
            min_value=0.0,
            max_value=50.0,
            value=reconciler.tolerance_amount,
            step=1.0,
            help="Diferença máxima aceita entre valor esperado e recebido"
        )
        
        tolerance_days = st.slider(
            "📅 Tolerância de Data (dias)",
            min_value=0,
            max_value=30,
            value=reconciler.tolerance_days,
            step=1,
            help="Diferença máxima aceita entre data de vencimento e pagamento"
        )
        
        # Threshold de correspondência
        match_threshold = st.slider(
            "🎯 Threshold de Correspondência (%)",
            min_value=50,
            max_value=100,
            value=60,
            step=5,
            help="Score mínimo para considerar uma correspondência válida"
        )
        
        if st.button("💾 Salvar Configurações", use_container_width=True):
            reconciler.tolerance_amount = tolerance_amount
            reconciler.tolerance_days = tolerance_days
            st.success("✅ Configurações salvas com sucesso!")
    
    with col2:
        st.subheader("🔍 Padrões de Identificação")
        
        st.write("**Padrões atuais para identificar pagamentos:**")
        
        for i, pattern in enumerate(reconciler.payment_patterns):
            st.code(pattern, language="regex")
        
        st.info("💡 Estes padrões são usados para identificar automaticamente os pagamentos nas descrições bancárias")
        
        # Teste de padrões
        st.subheader("🧪 Testar Padrões")
        
        test_description = st.text_input(
            "Descrição de teste",
            value="PIX RECEBIDO - FERNANDA SILVA 123.456.789-00",
            help="Digite uma descrição bancária para testar os padrões"
        )
        
        if test_description:
            matches_found = []
            for pattern in reconciler.payment_patterns:
                import re
                match = re.search(pattern, test_description.upper())
                if match:
                    matches_found.append(f"✅ Padrão '{pattern}' encontrou: {match.group()}")
            
            if matches_found:
                st.success("🎯 Correspondências encontradas:")
                for match in matches_found:
                    st.write(match)
            else:
                st.warning("⚠️ Nenhuma correspondência encontrada")
    
    # Informações do sistema
    st.markdown("---")
    st.subheader("ℹ️ Informações do Sistema")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**🔧 Versão do Sistema**")
        st.code("v1.0.0 - Conciliação Bancária")
    
    with col2:
        st.write("**📊 Estatísticas de Uso**")
        reconciliation_count = st.session_state.get('reconciliation_count', 0)
        st.write(f"Conciliações executadas: {reconciliation_count}")
    
    with col3:
        st.write("**💡 Suporte**")
        st.write("Para dúvidas sobre conciliação bancária, consulte a documentação do sistema.")

if __name__ == "__main__":
    main()