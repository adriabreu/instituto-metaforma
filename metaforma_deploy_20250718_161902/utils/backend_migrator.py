import sqlite3
import pandas as pd
import logging
from typing import Dict, List, Optional
from datetime import datetime
import json

class BackendMigrator:
    """
    Migrador completo do backend Node.js/Express para Streamlit.
    Integra dados do SQLite e estrutura do projeto React original.
    """
    
    def __init__(self, db_path: str):
        """
        Inicializa o migrador.
        
        Args:
            db_path: Caminho para o banco SQLite do backend
        """
        self.db_path = db_path
        self.logger = self._setup_logger()
        
        # Estruturas de dados migradas
        self.students_data = pd.DataFrame()
        self.users_data = pd.DataFrame()
        self.migration_report = {}
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o sistema de logging."""
        logger = logging.getLogger('BackendMigrator')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def migrate_all_data(self) -> Dict:
        """
        Executa migração completa dos dados do backend.
        
        Returns:
            Relatório da migração
        """
        try:
            self.logger.info("Iniciando migração completa do backend")
            
            # Conectar ao banco
            conn = sqlite3.connect(self.db_path)
            
            # Migrar tabelas
            self._migrate_students(conn)
            self._migrate_users(conn)
            
            # Gerar relatório
            self._generate_migration_report()
            
            conn.close()
            
            self.logger.info("Migração completa finalizada com sucesso")
            return self.migration_report
            
        except Exception as e:
            self.logger.error(f"Erro na migração: {str(e)}")
            return {'error': str(e)}
    
    def _migrate_students(self, conn: sqlite3.Connection):
        """Migra dados da tabela students."""
        try:
            # Ler dados dos alunos
            query = "SELECT * FROM students"
            self.students_data = pd.read_sql_query(query, conn)
            
            if self.students_data.empty:
                self.logger.warning("Tabela de alunos está vazia no backend")
                # Criar estrutura vazia baseada no schema
                self.students_data = pd.DataFrame(columns=[
                    'id', 'name', 'email', 'phone', 'birthDate', 'course'
                ])
            else:
                self.logger.info(f"Migrados {len(self.students_data)} alunos do backend")
            
            # Mapear campos para o formato Streamlit
            self._transform_students_data()
            
        except Exception as e:
            self.logger.error(f"Erro ao migrar alunos: {str(e)}")
            self.students_data = pd.DataFrame()
    
    def _migrate_users(self, conn: sqlite3.Connection):
        """Migra dados da tabela users."""
        try:
            # Ler dados dos usuários
            query = "SELECT id, username, role FROM users"  # Não migrar senhas por segurança
            self.users_data = pd.read_sql_query(query, conn)
            
            self.logger.info(f"Migrados {len(self.users_data)} usuários do backend")
            
        except Exception as e:
            self.logger.error(f"Erro ao migrar usuários: {str(e)}")
            self.users_data = pd.DataFrame()
    
    def _transform_students_data(self):
        """Transforma dados dos alunos para formato compatível com Streamlit."""
        if self.students_data.empty:
            return
        
        try:
            # Mapear campos do backend para formato Streamlit
            transformed_data = []
            
            for _, student in self.students_data.iterrows():
                transformed_student = {
                    'id': student.get('id', ''),
                    'fullName': student.get('name', ''),
                    'email': student.get('email', ''),
                    'cpfCnpj': '',  # Campo não existia no backend simples
                    'certificateName': student.get('name', ''),
                    'profession': '',  # Campo não existia no backend simples
                    'phone': student.get('phone', ''),
                    'whatsapp': student.get('phone', ''),  # Usar mesmo telefone
                    'cep': '',
                    'address': '',
                    'addressNumber': '',
                    'addressComplement': '',
                    'neighborhood': '',
                    'city': '',
                    'state': 'SP',  # Valor padrão
                    'chosenCourseName': student.get('course', ''),
                    'facCode': 'FAC_17',  # Valor padrão para alunos migrados
                    'paymentMethod': 'BOLETO',  # Valor padrão
                    'totalInstallments': 10,  # Valor padrão
                    'courseFee': 400.0,  # Valor padrão
                    'boletoDueDate': '10',  # Valor padrão
                    'howFound': 'Migração Backend',  # Identificar origem
                    'enrollmentStatus': 'Matriculado',  # Valor padrão
                    'birthDate': student.get('birthDate', ''),
                    'data_cadastro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'timestamp': datetime.now().isoformat(),
                    'migrated_from_backend': True  # Flag para identificar origem
                }
                
                transformed_data.append(transformed_student)
            
            # Substituir DataFrame original
            self.students_data = pd.DataFrame(transformed_data)
            
            self.logger.info(f"Dados de {len(transformed_data)} alunos transformados para formato Streamlit")
            
        except Exception as e:
            self.logger.error(f"Erro ao transformar dados: {str(e)}")
    
    def _generate_migration_report(self):
        """Gera relatório da migração."""
        self.migration_report = {
            'migration_date': datetime.now().isoformat(),
            'database_path': self.db_path,
            'students_migrated': len(self.students_data),
            'users_migrated': len(self.users_data),
            'students_details': {
                'total': len(self.students_data),
                'with_email': len(self.students_data[self.students_data['email'] != '']),
                'with_phone': len(self.students_data[self.students_data['phone'] != '']),
                'courses': self.students_data['chosenCourseName'].value_counts().to_dict() if not self.students_data.empty else {}
            },
            'users_details': {
                'total': len(self.users_data),
                'by_role': self.users_data['role'].value_counts().to_dict() if not self.users_data.empty else {}
            },
            'backend_structure': {
                'original_tables': ['students', 'users'],
                'api_endpoints': [
                    'POST /login',
                    'POST /register', 
                    'GET /students',
                    'POST /students',
                    'PUT /students/:id',
                    'DELETE /students/:id'
                ],
                'technologies': ['Node.js', 'Express', 'SQLite', 'CORS']
            }
        }
    
    def get_migrated_students(self) -> pd.DataFrame:
        """Retorna dados dos alunos migrados."""
        return self.students_data.copy()
    
    def get_migrated_users(self) -> pd.DataFrame:
        """Retorna dados dos usuários migrados."""
        return self.users_data.copy()
    
    def export_migration_report(self, file_path: str) -> bool:
        """
        Exporta relatório da migração para arquivo JSON.
        
        Args:
            file_path: Caminho do arquivo
            
        Returns:
            True se exportado com sucesso
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(self.migration_report, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Relatório de migração exportado para {file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar relatório: {str(e)}")
            return False
    
    def integrate_with_streamlit_data(self, existing_students: pd.DataFrame) -> pd.DataFrame:
        """
        Integra dados migrados com dados existentes do Streamlit.
        
        Args:
            existing_students: DataFrame com alunos existentes no Streamlit
            
        Returns:
            DataFrame combinado
        """
        try:
            if self.students_data.empty:
                return existing_students
            
            if existing_students.empty:
                return self.students_data
            
            # Evitar duplicatas por email
            migrated_emails = set(self.students_data['email'].dropna())
            existing_emails = set(existing_students['email'].dropna())
            
            # Filtrar alunos migrados que não existem no Streamlit
            new_students = self.students_data[
                ~self.students_data['email'].isin(existing_emails)
            ]
            
            # Combinar dados
            combined_data = pd.concat([existing_students, new_students], ignore_index=True)
            
            self.logger.info(f"Integrados {len(new_students)} novos alunos do backend")
            self.logger.info(f"Total após integração: {len(combined_data)} alunos")
            
            return combined_data
            
        except Exception as e:
            self.logger.error(f"Erro na integração: {str(e)}")
            return existing_students
    
    def validate_migration(self) -> Dict:
        """
        Valida a migração executada.
        
        Returns:
            Relatório de validação
        """
        validation_report = {
            'is_valid': True,
            'issues': [],
            'recommendations': []
        }
        
        try:
            # Validar estrutura dos dados
            if self.students_data.empty:
                validation_report['issues'].append("Nenhum aluno foi migrado")
                validation_report['recommendations'].append("Verificar se há dados na tabela students do backend")
            
            # Validar campos obrigatórios
            required_fields = ['fullName', 'email']
            for field in required_fields:
                if field in self.students_data.columns:
                    empty_count = self.students_data[field].isna().sum() + (self.students_data[field] == '').sum()
                    if empty_count > 0:
                        validation_report['issues'].append(f"{empty_count} alunos sem {field}")
                
            # Validar emails únicos
            if not self.students_data.empty and 'email' in self.students_data.columns:
                duplicate_emails = self.students_data['email'].duplicated().sum()
                if duplicate_emails > 0:
                    validation_report['issues'].append(f"{duplicate_emails} emails duplicados encontrados")
            
            # Determinar se migração é válida
            validation_report['is_valid'] = len(validation_report['issues']) == 0
            
            # Adicionar recomendações gerais
            if validation_report['is_valid']:
                validation_report['recommendations'].append("Migração executada com sucesso")
                validation_report['recommendations'].append("Considere complementar dados faltantes manualmente")
            
            return validation_report
            
        except Exception as e:
            validation_report['is_valid'] = False
            validation_report['issues'].append(f"Erro na validação: {str(e)}")
            return validation_report