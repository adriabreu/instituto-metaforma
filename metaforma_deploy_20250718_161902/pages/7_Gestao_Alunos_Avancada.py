import streamlit as st
import pandas as pd
import plotly.express as px
from utils.advanced_data_handler import AdvancedDataHandler
from datetime import datetime
import re

st.set_page_config(page_title="Gestão Avançada de Alunos", page_icon="👥", layout="wide")

# Inicializar handler de dados
@st.cache_resource
def get_data_handler():
    return AdvancedDataHandler()

def validate_cpf(cpf: str) -> bool:
    """Valida formato básico de CPF."""
    # Remove caracteres não numéricos
    cpf_clean = re.sub(r'[^0-9]', '', cpf)
    return len(cpf_clean) == 11

def validate_email(email: str) -> bool:
    """Valida formato básico de email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone: str) -> bool:
    """Valida formato básico de telefone."""
    # Remove caracteres não numéricos
    phone_clean = re.sub(r'[^0-9]', '', phone)
    return len(phone_clean) >= 10

def render_student_form(data_handler, student_data=None, is_edit=False):
    """Renderiza formulário de aluno baseado no componente React."""
    
    st.subheader("📝 Formulário do Aluno")
    
    # Obter dados para select boxes
    courses = data_handler.get_courses()
    facs = data_handler.get_facs()
    
    with st.form("student_form", clear_on_submit=not is_edit):
        # Dados Pessoais
        st.markdown("### 👤 Dados Pessoais")
        
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(
                "Nome Completo *", 
                value=student_data.get('fullName', '') if student_data else '',
                help="Nome completo como aparecerá no certificado"
            )
            
            cpf_cnpj = st.text_input(
                "CPF/CNPJ", 
                value=student_data.get('cpfCnpj', '') if student_data else '',
                help="Formato: 000.000.000-00"
            )
            
            profession = st.text_input(
                "Profissão", 
                value=student_data.get('profession', '') if student_data else ''
            )
            
            whatsapp = st.text_input(
                "WhatsApp (com DDD)", 
                value=student_data.get('whatsapp', '') if student_data else '',
                help="Formato: (11) 99999-9999"
            )
        
        with col2:
            email = st.text_input(
                "Email *", 
                value=student_data.get('email', '') if student_data else ''
            )
            
            certificate_name = st.text_input(
                "Nome para Certificado", 
                value=student_data.get('certificateName', full_name) if student_data else full_name,
                help="Nome que aparecerá no certificado (se diferente do nome completo)"
            )
            
            phone = st.text_input(
                "Telefone Celular (com DDD) *", 
                value=student_data.get('phone', '') if student_data else '',
                help="Formato: (11) 99999-9999"
            )
            
            cep = st.text_input(
                "CEP", 
                value=student_data.get('cep', '') if student_data else '',
                help="Formato: 00000-000"
            )
        
        # Endereço
        st.markdown("### 🏠 Endereço")
        
        address = st.text_input(
            "Logradouro (Rua, Av.)", 
            value=student_data.get('address', '') if student_data else ''
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            address_number = st.text_input(
                "Número", 
                value=student_data.get('addressNumber', '') if student_data else ''
            )
            
            neighborhood = st.text_input(
                "Bairro", 
                value=student_data.get('neighborhood', '') if student_data else ''
            )
        
        with col2:
            address_complement = st.text_input(
                "Complemento", 
                value=student_data.get('addressComplement', '') if student_data else ''
            )
            
            city = st.text_input(
                "Cidade", 
                value=student_data.get('city', '') if student_data else ''
            )
        
        state = st.selectbox(
            "Estado", 
            options=data_handler.STATES_BR,
            index=data_handler.STATES_BR.index(student_data.get('state', 'SP')) if student_data else data_handler.STATES_BR.index('SP')
        )
        
        # Dados da Matrícula
        st.markdown("### 📚 Detalhes da Matrícula")
        
        col1, col2 = st.columns(2)
        
        with col1:
            chosen_course = st.selectbox(
                "Curso Escolhido *",
                options=courses['name'].tolist(),
                index=courses['name'].tolist().index(student_data.get('chosenCourseName', '')) if student_data and student_data.get('chosenCourseName') in courses['name'].tolist() else 0
            )
            
            payment_method = st.selectbox(
                "Forma de Pagamento *",
                options=data_handler.PAYMENT_METHOD_OPTIONS,
                index=data_handler.PAYMENT_METHOD_OPTIONS.index(student_data.get('paymentMethod', 'BOLETO')) if student_data else 0
            )
        
        with col2:
            fac_code = st.selectbox(
                "Turma (FAC) *",
                options=facs['code'].tolist(),
                index=facs['code'].tolist().index(student_data.get('facCode', '')) if student_data and student_data.get('facCode') in facs['code'].tolist() else 0
            )
            
            enrollment_status = st.selectbox(
                "Status da Matrícula",
                options=data_handler.ENROLLMENT_STATUS_OPTIONS,
                index=data_handler.ENROLLMENT_STATUS_OPTIONS.index(student_data.get('enrollmentStatus', 'Matriculado')) if student_data else 0
            )
        
        # Dados Financeiros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Valor padrão baseado no curso selecionado
            selected_course_data = courses[courses['name'] == chosen_course].iloc[0] if not courses.empty else None
            default_fee = selected_course_data['defaultFee'] if selected_course_data is not None else 400.0
            
            course_fee = st.number_input(
                "Taxa do Curso (R$) *",
                min_value=0.0,
                value=float(student_data.get('courseFee', default_fee)) if student_data else default_fee,
                step=10.0
            )
        
        with col2:
            default_installments = selected_course_data['defaultInstallments'] if selected_course_data is not None else 10
            
            total_installments = st.number_input(
                "Total de Parcelas *",
                min_value=1,
                max_value=24,
                value=int(student_data.get('totalInstallments', default_installments)) if student_data else default_installments
            )
        
        with col3:
            if payment_method == 'BOLETO':
                boleto_due_date = st.selectbox(
                    "Melhor dia Venc. Boleto",
                    options=data_handler.BOLETO_DUE_DATE_OPTIONS,
                    index=data_handler.BOLETO_DUE_DATE_OPTIONS.index(student_data.get('boletoDueDate', '10')) if student_data else 1
                )
            else:
                boleto_due_date = '10'  # Valor padrão
        
        # Informações Adicionais
        col1, col2 = st.columns(2)
        
        with col1:
            how_found = st.selectbox(
                "Como nos encontrou?",
                options=data_handler.HOW_FOUND_OPTIONS,
                index=data_handler.HOW_FOUND_OPTIONS.index(student_data.get('howFound', 'Facebook')) if student_data else 0
            )
        
        with col2:
            # Campo vazio para simetria
            st.empty()
        
        # Botões de ação
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            submit_button = st.form_submit_button(
                "💾 Salvar Alterações" if is_edit else "➕ Adicionar Aluno",
                use_container_width=True
            )
        
        with col2:
            if is_edit:
                cancel_button = st.form_submit_button(
                    "❌ Cancelar",
                    use_container_width=True
                )
                if cancel_button:
                    st.session_state.editing_student = None
                    st.rerun()
        
        # Validação e submissão
        if submit_button:
            errors = []
            
            # Validações obrigatórias
            if not full_name.strip():
                errors.append("Nome completo é obrigatório")
            
            if not email.strip():
                errors.append("Email é obrigatório")
            elif not validate_email(email):
                errors.append("Email deve ter formato válido")
            
            if not phone.strip():
                errors.append("Telefone é obrigatório")
            elif not validate_phone(phone):
                errors.append("Telefone deve ter pelo menos 10 dígitos")
            
            if cpf_cnpj and not validate_cpf(cpf_cnpj):
                errors.append("CPF deve ter 11 dígitos")
            
            if not chosen_course:
                errors.append("Curso é obrigatório")
            
            if not fac_code:
                errors.append("Turma (FAC) é obrigatória")
            
            if course_fee <= 0:
                errors.append("Taxa do curso deve ser maior que zero")
            
            # Mostrar erros ou salvar
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Preparar dados do aluno
                student_form_data = {
                    'fullName': full_name.strip(),
                    'email': email.strip().lower(),
                    'cpfCnpj': cpf_cnpj.strip(),
                    'certificateName': certificate_name.strip() or full_name.strip(),
                    'profession': profession.strip(),
                    'phone': phone.strip(),
                    'whatsapp': whatsapp.strip() or phone.strip(),
                    'cep': cep.strip(),
                    'address': address.strip(),
                    'addressNumber': address_number.strip(),
                    'addressComplement': address_complement.strip(),
                    'neighborhood': neighborhood.strip(),
                    'city': city.strip(),
                    'state': state,
                    'chosenCourseName': chosen_course,
                    'facCode': fac_code,
                    'paymentMethod': payment_method,
                    'totalInstallments': total_installments,
                    'courseFee': course_fee,
                    'boletoDueDate': boleto_due_date,
                    'howFound': how_found,
                    'enrollmentStatus': enrollment_status
                }
                
                # Salvar aluno
                if is_edit and student_data:
                    success = data_handler.update_student(student_data['id'], student_form_data)
                    if success:
                        st.success("✅ Aluno atualizado com sucesso!")
                        st.session_state.editing_student = None
                        st.rerun()
                    else:
                        st.error("❌ Erro ao atualizar aluno")
                else:
                    success = data_handler.add_student(student_form_data)
                    if success:
                        st.success("✅ Aluno adicionado com sucesso!")
                        st.rerun()
                    else:
                        st.error("❌ Erro ao adicionar aluno")

def render_students_table(data_handler):
    """Renderiza tabela de alunos baseada no componente React."""
    
    students_df = data_handler.get_all_students()
    
    if students_df.empty:
        st.info("📝 Nenhum aluno cadastrado ainda.")
        return
    
    st.subheader("👥 Lista de Alunos")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Buscar por nome ou email")
    
    with col2:
        facs = data_handler.get_facs()
        fac_filter = st.selectbox("🎓 Filtrar por turma", ["Todas"] + facs['code'].tolist())
    
    with col3:
        status_filter = st.selectbox("📊 Filtrar por status", ["Todos"] + data_handler.ENROLLMENT_STATUS_OPTIONS)
    
    # Aplicar filtros
    filtered_df = students_df.copy()
    
    if search_term:
        mask = (
            filtered_df['fullName'].str.contains(search_term, case=False, na=False) |
            filtered_df['email'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if fac_filter != "Todas":
        filtered_df = filtered_df[filtered_df['facCode'] == fac_filter]
    
    if status_filter != "Todos":
        filtered_df = filtered_df[filtered_df['enrollmentStatus'] == status_filter]
    
    # Mostrar estatísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("👥 Total de Alunos", len(students_df))
    
    with col2:
        matriculados = len(students_df[students_df['enrollmentStatus'] == 'Matriculado'])
        st.metric("✅ Matriculados", matriculados)
    
    with col3:
        receita_total = students_df['courseFee'].sum()
        st.metric("💰 Receita Total", f"R$ {receita_total:,.2f}")
    
    with col4:
        ticket_medio = students_df['courseFee'].mean() if not students_df.empty else 0
        st.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}")
    
    # Tabela de alunos
    if not filtered_df.empty:
        st.markdown(f"**Mostrando {len(filtered_df)} aluno(s):**")
        
        # Configurar colunas para exibição
        display_columns = ['fullName', 'email', 'facCode', 'phone', 'enrollmentStatus', 'courseFee']
        display_df = filtered_df[display_columns].copy()
        
        # Renomear colunas para exibição
        display_df.columns = ['Nome Completo', 'Email', 'Turma', 'Telefone', 'Status', 'Valor Curso']
        
        # Formatação
        display_df['Valor Curso'] = display_df['Valor Curso'].apply(lambda x: f"R$ {x:,.2f}")
        
        # Adicionar colunas de ação
        for idx, row in display_df.iterrows():
            original_idx = filtered_df.index[display_df.index.get_loc(idx)]
            student_id = filtered_df.loc[original_idx, 'id']
            
            col1, col2, col3 = st.columns([6, 1, 1])
            
            with col1:
                # Exibir dados do aluno
                st.write(f"**{row['Nome Completo']}** | {row['Email']} | {row['Turma']} | {row['Status']} | {row['Valor Curso']}")
            
            with col2:
                if st.button("✏️", key=f"edit_{student_id}", help="Editar aluno"):
                    st.session_state.editing_student = student_id
                    st.rerun()
            
            with col3:
                if st.button("🗑️", key=f"delete_{student_id}", help="Excluir aluno"):
                    if st.session_state.get(f"confirm_delete_{student_id}", False):
                        success = data_handler.delete_student(student_id)
                        if success:
                            st.success("✅ Aluno excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error("❌ Erro ao excluir aluno")
                    else:
                        st.session_state[f"confirm_delete_{student_id}"] = True
                        st.warning("⚠️ Clique novamente para confirmar exclusão")
    else:
        st.info("📝 Nenhum aluno encontrado com os filtros aplicados.")

def main():
    st.title("👥 Gestão Avançada de Alunos")
    st.markdown("---")
    
    # Inicializar handler de dados
    data_handler = get_data_handler()
    
    # Verificar se está editando um aluno
    editing_student_id = st.session_state.get('editing_student', None)
    
    if editing_student_id:
        # Modo de edição
        student_data = data_handler.get_student_by_id(editing_student_id)
        
        if student_data:
            st.info(f"✏️ Editando aluno: **{student_data['fullName']}**")
            render_student_form(data_handler, student_data, is_edit=True)
        else:
            st.error("❌ Aluno não encontrado")
            st.session_state.editing_student = None
    else:
        # Tabs para organizar funcionalidades
        tab1, tab2, tab3, tab4 = st.tabs(["➕ Adicionar Aluno", "👥 Lista de Alunos", "💰 Gestão Financeira", "📊 Relatórios"])
        
        with tab1:
            render_student_form(data_handler)
        
        with tab2:
            render_students_table(data_handler)
        
        with tab3:
            st.subheader("💰 Gestão Financeira dos Alunos")
            
            # Resumo financeiro
            financial_summary = data_handler.get_financial_summary()
            
            if financial_summary:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("💰 Receita Total", f"R$ {financial_summary.get('total_revenue', 0):,.2f}")
                
                with col2:
                    st.metric("✅ Total Pago", f"R$ {financial_summary.get('total_paid', 0):,.2f}")
                
                with col3:
                    st.metric("⏳ Total Pendente", f"R$ {financial_summary.get('total_pending', 0):,.2f}")
                
                with col4:
                    st.metric("⚠️ Em Atraso", f"R$ {financial_summary.get('total_overdue', 0):,.2f}")
                
                # Gráficos financeiros
                col1, col2 = st.columns(2)
                
                with col1:
                    # Gráfico de pizza - Status dos pagamentos
                    payments_data = {
                        'Status': ['Pago', 'Pendente', 'Em Atraso'],
                        'Valor': [
                            financial_summary.get('total_paid', 0),
                            financial_summary.get('total_pending', 0) - financial_summary.get('total_overdue', 0),
                            financial_summary.get('total_overdue', 0)
                        ]
                    }
                    
                    fig_payments = px.pie(
                        values=payments_data['Valor'],
                        names=payments_data['Status'],
                        title="Distribuição dos Pagamentos"
                    )
                    st.plotly_chart(fig_payments, use_container_width=True)
                
                with col2:
                    # Receita por turma
                    students_df = data_handler.get_all_students()
                    if not students_df.empty:
                        revenue_by_fac = students_df.groupby('facCode')['courseFee'].sum().reset_index()
                        
                        fig_revenue = px.bar(
                            revenue_by_fac,
                            x='facCode',
                            y='courseFee',
                            title="Receita por Turma",
                            labels={'courseFee': 'Receita (R$)', 'facCode': 'Turma'}
                        )
                        st.plotly_chart(fig_revenue, use_container_width=True)
        
        with tab4:
            st.subheader("📊 Relatórios e Análises")
            
            students_df = data_handler.get_all_students()
            
            if not students_df.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Distribuição por estado
                    state_dist = students_df['state'].value_counts().reset_index()
                    state_dist.columns = ['Estado', 'Quantidade']
                    
                    fig_states = px.bar(
                        state_dist.head(10),
                        x='Estado',
                        y='Quantidade',
                        title="Top 10 Estados dos Alunos"
                    )
                    st.plotly_chart(fig_states, use_container_width=True)
                
                with col2:
                    # Como encontraram o curso
                    how_found_dist = students_df['howFound'].value_counts().reset_index()
                    how_found_dist.columns = ['Canal', 'Quantidade']
                    
                    fig_channels = px.pie(
                        how_found_dist,
                        values='Quantidade',
                        names='Canal',
                        title="Como os Alunos nos Encontraram"
                    )
                    st.plotly_chart(fig_channels, use_container_width=True)
                
                # Exportar dados
                st.markdown("---")
                st.subheader("📤 Exportar Dados")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📊 Exportar para Excel", use_container_width=True):
                        file_path = "relatorio_alunos.xlsx"
                        success = data_handler.export_students_to_excel(file_path)
                        if success:
                            st.success("✅ Dados exportados com sucesso!")
                            
                            # Disponibilizar download
                            with open(file_path, "rb") as file:
                                st.download_button(
                                    label="⬇️ Baixar Arquivo Excel",
                                    data=file.read(),
                                    file_name=f"relatorio_alunos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        else:
                            st.error("❌ Erro ao exportar dados")
                
                with col2:
                    if st.button("📋 Gerar Relatório CSV", use_container_width=True):
                        csv_data = students_df.to_csv(index=False)
                        st.download_button(
                            label="⬇️ Baixar CSV",
                            data=csv_data,
                            file_name=f"alunos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
            else:
                st.info("📝 Adicione alguns alunos para visualizar relatórios.")

if __name__ == "__main__":
    main()