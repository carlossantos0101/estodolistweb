import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexao = mysql.connector.connect(
        host="localhost",   #Endereço
        user="root",    #Usuario
        password="senai",   #Senha
        database="estodolist"   #DataBase criado
        )
        cursor =  conexao.cursor(dictionary=True)
        # retorna duas informações: Conexão e cursor
        return conexao, cursor
    
    except Error as erro:
        print(f"ERRO! Falha ao se conectar com o banco de dados: {erro}")
        return None, None 


def inserir_tarefa(nome_tarefa,descricao,categoria,data_prazo,prioridade):
    conexao, cursor = conectar() # Se conectar com BD

    # Verifica se a conexão funcionou
    if conexao is None:
        return False

    try:
        # %s SQL Parametrizado para evitar SQL Injection
        # INSERT = COMANDO SQL QUE INSERE (CRIA) UMA NOVA TAREFA NO BANCO
        sql = "INSERT INTO tarefa (nomeTarefa,descricao,categoria,dataPrazo,prioridade) VALUES (%s, %s, %s, %s, %s)"
        # Executa o SQL Parametrizado e passa os parâmetros da função via TUPLA
        cursor.execute(sql,(nome_tarefa,descricao,categoria,data_prazo,prioridade))
        # Confirma as alterações
        conexao.commit()
        # Retornar TRUE para função principal
        return True

    except Error as erro:
        print(f"ERRO! Falha ao inserir a tarefa: {erro}")
        return False
    finally:
        cursor.close()
        conexao.close()
        

def consultar_tarefas():
    #Chamar função conectar
    conexao, cursor = conectar()
    
    #Verificar se a conexão falhou
    if conexao is None:
        return [] #Lista vazia
    
    try: #Tente executar o comando SQL.
        #selecione todas as colunas da tabela tarefa;
        sql = """
            SELECT 
            idTarefa AS idtarefa,
            dataPrazo AS data_prazo,
            nomeTarefa AS nome_tarefa,
            status,
            descricao,
            categoria,
            prioridade
            FROM tarefa
            """
        #Executa o comando da variável SQL
        cursor.execute(sql)
        
        #Buscar todas as linhasda consuta execultada
        tarefas = cursor.fetchall()
        
        #Retorna para a programação principal as tarefas
        return tarefas
    
    
    except Error as erro: #Se der erro
        print(f"ERRO! Falha ao editar tarefa: {erro}")
        return [] #Retorna lista vazia em caso de erro
        
    finally: #Finalize sempre
        cursor.close() #Encerrar o cursor
        conexao.close() #Encerrar a conexão
        
        
# ---------------------------------------------------------------------------------------------------------------------

# Essa função marca como Concluída a tarefa indicada
def concluir_tarefa(idtarefa):
    conexao, cursor = conectar()

    if conexao is None:
        return False

    try:
        sql = "UPDATE tarefa SET status = 'Concluída' WHERE idTarefa = %s"
        cursor.execute(sql, (idtarefa,))
        conexao.commit() # Confirma a alteração nos dados
        return True
    except Error as erro:
        print(f"ERRO! Falha ao concluir a tarefa: {erro}")
        return False # Retorna Falso em caso de erro
    finally:
        cursor.close()
        conexao.close()
        
# -------------------------------------------------------------------------------------------------------------------

# Apagar tarefa

def apagar_tarefa(idtarefa):
    
    conexao, cursor = conectar()

    if conexao is None:
        return False

    try:
        sql = """
        DELETE FROM tarefa 
        WHERE idTarefa = %s
        """
        cursor.execute(sql, (idtarefa,))
        conexao.commit() # Confirma a alteração nos dados
        return True
    except Error as erro:
        print(f"ERRO! Falha ao excluir a tarefa: {erro}")
        return False # Retorna Falso em caso de erro
    finally:
        cursor.close()
        conexao.close()
        
#------------------------------------------------------------------------------------------------------------------

# Essa função irá editar as informações da tarefa

def alterar_tarefa(idtarefa, nome_tarefa,descricao,categoria,data_prazo,prioridade):
    
    conexao, cursor = conectar()

    if conexao is None:
        return False

    try:
        sql = """
        UPDATE tarefa 
        SET
        nomeTarefa = %s,
        descricao = %s,
        categoria = %s,
        dataPrazo = %s,
        prioridade = %s
        WHERE idTarefa = %s
        """
        cursor.execute(sql, (nome_tarefa, descricao, categoria, data_prazo, prioridade, idtarefa))
        conexao.commit() # Confirma a alteração nos dados
        return True
    except Error as erro:
        print(f"ERRO! Falha ao alterar a tarefa: {erro}")
        return False # Retorna Falso em caso de erro
    finally:
        cursor.close()
        conexao.close()
        
        
        
def buscar_tarefa(idtarefa):
    conexao, cursor = conectar()

    if conexao is None:
        return None

    try:
        sql = """
            SELECT
            idTarefa AS idtarefa,
            dataPrazo AS data_prazo,
            nomeTarefa AS nome_tarefa,
            status,
            descricao,
            categoria,
            prioridade
            FROM tarefa WHERE idTarefa = %s
            """
        cursor.execute(sql, (idtarefa,))
        return cursor.fetchone() # Um dicionário, ou None se não existir  
    except Error as erro:
        print(f"ERRO! Falha ao buscar a tarefa: {erro}")
        return None
    finally:
        cursor.close()
        conexao.close()
                    