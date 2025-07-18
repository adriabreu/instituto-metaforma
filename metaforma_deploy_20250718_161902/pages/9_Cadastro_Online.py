import streamlit as st
import pandas as pd
import re
from datetime import datetime
import logging
from utils.advanced_data_handler import AdvancedDataHandler
import uuid

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_cpf(cpf):
    """Valida CPF brasileiro"""
    cpf = re.sub(r'[^\d]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    
    # Validar primeiro dígito
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto
    
    if int(cpf[9]) != digito1:
        return False
    
    # Validar segundo dígito
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto
    
    return int(cpf[10]) == digito2

def validate_email(email):
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Valida telefone brasileiro"""
    phone = re.sub(r'[^\d]', '', phone)
    return len(phone) >= 10 and len(phone) <= 11

def format_cpf(cpf):
    """Formata CPF com máscara"""
    cpf = re.sub(r'[^\d]', '', cpf)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

def format_phone(phone):
    """Formata telefone com máscara"""
    phone = re.sub(r'[^\d]', '', phone)
    if len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    elif len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    return phone

def main():
    st.set_page_config(
        page_title="Cadastro Online - Instituto Metaforma",
        page_icon="📝",
        layout="wide"
    )
    
    # CSS customizado para formulário
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    .info-box {
        background: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Cabeçalho
    st.markdown("""
    <div class="main-header">
        <h1>📝 Cadastro Online - Instituto Metaforma</h1>
        <p>Preencha todos os campos obrigatórios para completar sua inscrição</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Verificar se é admin ou formulário público
    if 'admin_mode' not in st.session_state:
        st.session_state.admin_mode = False
    
    # Sidebar para administrador
    with st.sidebar:
        st.header("🔧 Administração")
        
        admin_password = st.text_input("Senha Admin:", type="password")
        if admin_password == "admin123":
            st.session_state.admin_mode = True
            st.success("Modo administrador ativado")
        
        if st.session_state.admin_mode:
            st.markdown("---")
            st.subheader("📊 Estatísticas")
            
            # Carregar dados
            data_handler = AdvancedDataHandler()
            students = data_handler.get_all_students()
            
            st.metric("Total de Alunos", len(students))
            if not students.empty:
                st.metric("Receita Total", f"R$ {students['courseFee'].sum():,.2f}")
                st.metric("Valor Médio", f"R$ {students['courseFee'].mean():,.2f}")
            
            # Botão para ver cadastros
            if st.button("📋 Ver Todos os Cadastros"):
                st.session_state.show_all_students = True
    
    # Mostrar lista de alunos se admin
    if st.session_state.admin_mode and st.session_state.get('show_all_students', False):
        st.subheader("📋 Alunos Cadastrados")
        
        data_handler = AdvancedDataHandler()
        students = data_handler.get_all_students()
        
        if not students.empty:
            # Exibir tabela
            display_df = students[['fullName', 'email', 'phone', 'courseFee', 'installments']].copy()
            display_df.columns = ['Nome', 'Email', 'Telefone', 'Valor do Curso', 'Parcelas']
            st.dataframe(display_df, use_container_width=True)
            
            # Botão para exportar
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Baixar Cadastros (CSV)",
                data=csv,
                file_name=f"cadastros_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Nenhum aluno cadastrado ainda.")
        
        if st.button("🔙 Voltar"):
            st.session_state.show_all_students = False
            st.rerun()
    
    # Formulário principal
    if not st.session_state.get('show_all_students', False):
        st.markdown("""
        <div class="info-box">
            <h3>ℹ️ Informações Importantes</h3>
            <ul>
                <li>Todos os campos marcados com (*) são obrigatórios</li>
                <li>Mantenha seus dados atualizados para receber informações do curso</li>
                <li>Em caso de dúvidas, entre em contato conosco</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Container do formulário
        with st.container():
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            
            # Formulário de cadastro
            with st.form("student_registration", clear_on_submit=True):
                st.subheader("👤 Dados Pessoais")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    full_name = st.text_input("Nome Completo *", placeholder="Digite seu nome completo")
                    email = st.text_input("Email *", placeholder="seu.email@exemplo.com")
                    phone = st.text_input("Telefone *", placeholder="(11) 99999-9999")
                
                with col2:
                    cpf = st.text_input("CPF *", placeholder="000.000.000-00")
                    birth_date = st.date_input("Data de Nascimento *")
                    gender = st.selectbox("Gênero *", ["", "Masculino", "Feminino", "Outro", "Prefiro não informar"])
                
                st.markdown("---")
                st.subheader("📍 Endereço")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    address = st.text_input("Endereço Completo *", placeholder="Rua, número, bairro")
                    city = st.text_input("Cidade *", placeholder="Sua cidade")
                
                with col2:
                    state = st.selectbox("Estado *", [
                        "", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", 
                        "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", 
                        "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
                    ])
                    zip_code = st.text_input("CEP *", placeholder="00000-000")
                
                st.markdown("---")
                st.subheader("🎓 Informações do Curso")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    course_name = st.selectbox("Curso *", [
                        "", "Desenvolvimento Web", "Data Science", "Marketing Digital",
                        "Design Gráfico", "Gestão de Projetos", "Outro"
                    ])
                    course_fee = st.number_input("Valor do Curso (R$) *", min_value=0.0, step=0.01)
                
                with col2:
                    installments = st.number_input("Número de Parcelas *", min_value=1, max_value=24, value=1)
                    start_date = st.date_input("Data de Início Pretendida *")
                
                st.markdown("---")
                st.subheader("💰 Informações Financeiras")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    income = st.selectbox("Renda Mensal *", [
                        "", "Até R$ 1.000", "R$ 1.001 - R$ 2.000", "R$ 2.001 - R$ 3.000",
                        "R$ 3.001 - R$ 5.000", "R$ 5.001 - R$ 10.000", "Acima de R$ 10.000"
                    ])
                
                with col2:
                    payment_method = st.selectbox("Forma de Pagamento Preferida *", [
                        "", "Cartão de Crédito", "Boleto Bancário", "Pix", "Transferência Bancária"
                    ])
                
                st.markdown("---")
                st.subheader("📝 Informações Adicionais")
                
                how_found = st.selectbox("Como nos conheceu? *", [
                    "", "Google", "Redes Sociais", "Indicação", "Publicidade", "Outro"
                ])
                
                observations = st.text_area("Observações", placeholder="Alguma informação adicional que gostaria de compartilhar?")
                
                # Termos e condições
                st.markdown("---")
                terms_agreed = st.checkbox("Li e aceito os termos e condições *")
                privacy_agreed = st.checkbox("Concordo com a política de privacidade *")
                
                # Botão de submissão
                submit_button = st.form_submit_button("📤 Enviar", use_container_width=True)
                
                if submit_button:
                    # Validações
                    errors = []
                    
                    if not full_name:
                        errors.append("Nome completo é obrigatório")
                    
                    if not email:
                        errors.append("Email é obrigatório")
                    elif not validate_email(email):
                        errors.append("Email inválido")
                    
                    if not phone:
                        errors.append("Telefone é obrigatório")
                    elif not validate_phone(phone):
                        errors.append("Telefone inválido")
                    
                    if not cpf:
                        errors.append("CPF é obrigatório")
                    elif not validate_cpf(cpf):
                        errors.append("CPF inválido")
                    
                    if not birth_date:
                        errors.append("Data de nascimento é obrigatória")
                    
                    if not gender:
                        errors.append("Gênero é obrigatório")
                    
                    if not address:
                        errors.append("Endereço é obrigatório")
                    
                    if not city:
                        errors.append("Cidade é obrigatória")
                    
                    if not state:
                        errors.append("Estado é obrigatório")
                    
                    if not zip_code:
                        errors.append("CEP é obrigatório")
                    
                    if not course_name:
                        errors.append("Curso é obrigatório")
                    
                    if course_fee <= 0:
                        errors.append("Valor do curso deve ser maior que zero")
                    
                    if not start_date:
                        errors.append("Data de início é obrigatória")
                    
                    if not income:
                        errors.append("Renda mensal é obrigatória")
                    
                    if not payment_method:
                        errors.append("Forma de pagamento é obrigatória")
                    
                    if not how_found:
                        errors.append("Como nos conheceu é obrigatório")
                    
                    if not terms_agreed:
                        errors.append("Você deve aceitar os termos e condições")
                    
                    if not privacy_agreed:
                        errors.append("Você deve concordar com a política de privacidade")
                    
                    if errors:
                        st.markdown('<div class="error-message">', unsafe_allow_html=True)
                        st.error("❌ Corrija os seguintes erros:")
                        for error in errors:
                            st.write(f"• {error}")
                        st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        # Cadastrar aluno
                        try:
                            data_handler = AdvancedDataHandler()
                            
                            # Preparar dados do aluno
                            student_data = {
                                'id': str(uuid.uuid4()),
                                'fullName': full_name,
                                'email': email,
                                'phone': format_phone(phone),
                                'cpf': format_cpf(cpf),
                                'birthDate': birth_date.strftime('%Y-%m-%d'),
                                'gender': gender,
                                'address': address,
                                'city': city,
                                'state': state,
                                'zipCode': zip_code,
                                'courseName': course_name,
                                'courseFee': course_fee,
                                'installments': installments,
                                'startDate': start_date.strftime('%Y-%m-%d'),
                                'income': income,
                                'paymentMethod': payment_method,
                                'howFound': how_found,
                                'observations': observations,
                                'registrationDate': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                'status': 'active'
                            }
                            
                            # Salvar aluno
                            success = data_handler.create_student(student_data)
                            
                            if success:
                                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                                st.success("✅ Cadastro realizado com sucesso!")
                                st.write(f"**Nome:** {full_name}")
                                st.write(f"**Email:** {email}")
                                st.write(f"**Curso:** {course_name}")
                                st.write(f"**Valor:** R$ {course_fee:,.2f}")
                                st.write(f"**Parcelas:** {installments}x")
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                # Informações importantes
                                st.info("📧 Você receberá um email com mais informações sobre o curso e formas de pagamento.")
                                
                                logger.info(f"Novo aluno cadastrado: {full_name} - {email}")
                            else:
                                st.error("❌ Erro ao cadastrar aluno. Tente novamente.")
                                
                        except Exception as e:
                            st.error(f"❌ Erro inesperado: {str(e)}")
                            logger.error(f"Erro ao cadastrar aluno: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>© 2025 Instituto Metaforma - Todos os direitos reservados</p>
        <p>Em caso de dúvidas, entre em contato: <a href="mailto:contato@metaforma.com">contato@metaforma.com</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()