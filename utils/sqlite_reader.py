import sqlite3
import pandas as pd
import logging
from typing import Dict, List, Optional, Tuple

class SQLiteReader:
    """
    Classe para ler dados do banco SQLite existente do projeto anterior.
    """
    
    def __init__(self, db_path: str):
        """
        Inicializa o leitor SQLite.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados
        """
        self.db_path = db_path
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """Configura o sistema de logging."""
        logger = logging.getLogger('SQLiteReader')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def get_tables(self) -> List[str]:
        """
        Obtém lista de tabelas no banco.
        
        Returns:
            Lista com nomes das tabelas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            conn.close()
            return tables
            
        except Exception as e:
            self.logger.error(f"Erro ao obter tabelas: {str(e)}")
            return []
    
    def get_table_schema(self, table_name: str) -> List[Tuple]:
        """
        Obtém esquema de uma tabela.
        
        Args:
            table_name: Nome da tabela
            
        Returns:
            Lista com informações das colunas
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            schema = cursor.fetchall()
            
            conn.close()
            return schema
            
        except Exception as e:
            self.logger.error(f"Erro ao obter esquema da tabela {table_name}: {str(e)}")
            return []
    
    def read_table(self, table_name: str) -> pd.DataFrame:
        """
        Lê dados de uma tabela.
        
        Args:
            table_name: Nome da tabela
            
        Returns:
            DataFrame com dados da tabela
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, conn)
            
            conn.close()
            
            self.logger.info(f"Tabela {table_name} lida com sucesso: {len(df)} registros")
            return df
            
        except Exception as e:
            self.logger.error(f"Erro ao ler tabela {table_name}: {str(e)}")
            return pd.DataFrame()
    
    def get_database_summary(self) -> Dict:
        """
        Obtém resumo completo do banco de dados.
        
        Returns:
            Dicionário com informações do banco
        """
        try:
            tables = self.get_tables()
            summary = {
                'total_tables': len(tables),
                'tables': {}
            }
            
            for table in tables:
                df = self.read_table(table)
                schema = self.get_table_schema(table)
                
                summary['tables'][table] = {
                    'rows': len(df),
                    'columns': len(df.columns) if not df.empty else 0,
                    'schema': schema,
                    'column_names': df.columns.tolist() if not df.empty else []
                }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar resumo do banco: {str(e)}")
            return {'error': str(e)}
    
    def migrate_students_data(self) -> pd.DataFrame:
        """
        Migra dados de alunos do banco SQLite.
        
        Returns:
            DataFrame com dados dos alunos migrados
        """
        try:
            # Tentar diferentes nomes de tabela possíveis
            possible_tables = ['students', 'alunos', 'student', 'aluno']
            
            for table_name in possible_tables:
                if table_name in self.get_tables():
                    df = self.read_table(table_name)
                    if not df.empty:
                        self.logger.info(f"Dados de alunos encontrados na tabela: {table_name}")
                        return df
            
            self.logger.warning("Nenhuma tabela de alunos encontrada")
            return pd.DataFrame()
            
        except Exception as e:
            self.logger.error(f"Erro ao migrar dados de alunos: {str(e)}")
            return pd.DataFrame()
    
    def migrate_financial_data(self) -> pd.DataFrame:
        """
        Migra dados financeiros do banco SQLite.
        
        Returns:
            DataFrame com dados financeiros migrados
        """
        try:
            # Tentar diferentes nomes de tabela possíveis
            possible_tables = ['payments', 'pagamentos', 'financial', 'financeiro', 'expenses', 'despesas']
            
            migrated_data = []
            
            for table_name in possible_tables:
                if table_name in self.get_tables():
                    df = self.read_table(table_name)
                    if not df.empty:
                        df['source_table'] = table_name
                        migrated_data.append(df)
                        self.logger.info(f"Dados financeiros encontrados na tabela: {table_name}")
            
            if migrated_data:
                # Combinar todos os dados financeiros encontrados
                combined_df = pd.concat(migrated_data, ignore_index=True)
                return combined_df
            else:
                self.logger.warning("Nenhuma tabela financeira encontrada")
                return pd.DataFrame()
            
        except Exception as e:
            self.logger.error(f"Erro ao migrar dados financeiros: {str(e)}")
            return pd.DataFrame()
    
    def export_all_data(self) -> Dict[str, pd.DataFrame]:
        """
        Exporta todos os dados do banco.
        
        Returns:
            Dicionário com DataFrames de todas as tabelas
        """
        try:
            tables = self.get_tables()
            all_data = {}
            
            for table in tables:
                df = self.read_table(table)
                if not df.empty:
                    all_data[table] = df
            
            return all_data
            
        except Exception as e:
            self.logger.error(f"Erro ao exportar todos os dados: {str(e)}")
            return {}