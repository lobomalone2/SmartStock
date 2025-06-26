import sqlite3




class DatabaseManager(): # Classe exclusiva para estabelecer a conexão com o banco de dados e salvar alterações! # Funcionando

    def __init__(self,db_nome='pythondb.db'):

        self.db_nome = db_nome
        self.conn = None
        self.cursor = None

    
    def  conectar(self):
        

        try: # Tratamento de erro caso algo de errado aconteça durante a conexão 

            self.conn = sqlite3.connect(self.db_nome)
            self.cursor = self.conn.cursor()

            mensagem = f'Conectando ao banco de dados: {self.db_nome}'

            return  mensagem

        except sqlite3.Error as e:

            mensagem = f'Erro ao conectar no banco de dados: {e}'

            return mensagem
    
    def commit(self): # Salva as alterações realizadas no DB

        if self.conn:

            self.conn.commit()

            mensagem = "Transação confirmada."

            return mensagem

        else:

            mensagem = "Erro: Conexão não estabelecida para commit."

            return mensagem



class Tabelas(): #Funcionando, função para criar as tabelas do DB
    
    def __init__(self, db_connect):

        self.db_connect = db_connect

    
    

    def criar_tabelas(self): # Criando tabelas para o banco de dados! #Funcionando
            
        if not self.db_connect.conn:

            mensagem = 'Erro: conexão com o banco de dados não estabelecida no DatabaseManager'

            return mensagem

        try: 

            self.db_connect.cursor.execute('''

                    CREATE TABLE produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    quantidade INTEGER,
                    preco FLOAT
            )
            ''')

            self.db_connect.commit()
            mensagem = "Tabela 'produtos' criada com sucesso ou já existente."

            return mensagem

        except sqlite3.Error as e:

            mensagem = f"Erro ao criar tabela 'produtos': {e}"

            return mensagem

            
    def vendas(self):



        try:
            self.db_connect.cursor.execute('''CREATE TABLE IF NOT EXISTS vendas(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            quantidade INTEGER,
                            data_venda DATE,
                            id_produto INTEGER,
                            FOREIGN KEY (id_produto) REFERENCES produtos(id) ) ''')

            self.db_connect.commit()

        except sqlite3.Error as e:

            mensagem = 'Erro ao criar tabela vendas!'

            self.db_connect.rollback()

            return mensagem

        


class Produto(): # Funcionando, contém funções para cadastro de produtos no DB

    def __init__(self,db_connect):

        self.db_connect = db_connect

    def cadastrar_produto(self,nome,descricao,quantidade,preco): #UPDATE
            
            if not self.db_connect.conn:

                mensagem = "Erro: Conexão com o banco de dados não estabelecida no DatabaseManager."

                return mensagem
            
            try:

                self.db_connect.cursor.execute('''INSERT  INTO produtos (nome,descricao,quantidade,preco) VALUES (?,?,?,?)''',(nome,descricao,quantidade,preco))

                self.db_connect.commit()

                mensagem = f"Produto '{nome}' inserido com sucesso."

                return mensagem

            except sqlite3.Error as e:

                mensagem = f"Erro ao inserir produto '{nome}': {e}"

                self.db_connect.rollback() # Desfaz as alterações feitas durante a compilação

                return mensagem


    def atualizar_quantidade(self,id,quantidade):
            
            if not self.db_connect.conn:

                mensagem = "Erro: Conexão com o banco de dados não estabelecida no DatabaseManager."
                
                return mensagem
            
            try:

                self.db_connect.cursor.execute('''UPDATE produtos SET quantidade = ? WHERE id = ?''',(quantidade,id))

                self.db_connect.commit()

                mensagem = f"quantidade do produto do id: '{id}' atualizado com sucesso."

            except sqlite3.Error as e:

                mensagem = f"Erro ao inserir produto '{id}': {e}"

                self.db_connect.rollback() # Desfaz as alterações feitas durante a compilação

                return mensagem




    def consultar_produto(self,id): #Parei aqui

        if not self.db_connect.conn:
            mensagem = "Não tem conexão"

            return mensagem
        
        try:
            self.db_connect.cursor.execute(''' SELECT id, nome, descricao, quantidade, preco FROM produtos WHERE id = ? ''',(id,))

            produto = self.db_connect.cursor.fetchone()

            if produto:

                mensagem = f'Produto encontrado {produto}'

                return mensagem,produto
            
            else:

                mensagem = f'Nenhum produto encontrado com o ID {id}'

                return mensagem
            
        except sqlite3.Error as e:

            mensagem = f'Erro ao consultar produto "{id}:{e}"'

            return mensagem

            

    
    def deletar_produto(self,id):

        produto = self.consultar_produto(id)

        if produto:

            self.db_connect.cursor.execute(''' DELETE FROM produtos WHERE id = ? ''',(id,))
            self.db_connect.conn.commit()
            mensagem = f'produto {produto} deletado'

            return mensagem
        
        else:
            mensagem = 'Produto não encontrado! '

            return mensagem


            
            
class Venda(): # Contém funções de cadastro de vendas  # Funcionando #UPDATE

    def __init__(self,db_connect):

        self.db_connect = db_connect
    
    def inserir_venda(self,id_produto,qtd_vendida,data_venda):

        self.db_connect.cursor.execute('''INSERT INTO vendas(id_produto,quantidade,data_venda) VALUES (?,?,?) ''',(id_produto,qtd_vendida,data_venda))
        self.db_connect.commit() # salva as alterações no Banco de Dados


estabelecerconn = DatabaseManager()

estabelecerconn.conectar()

GerenciarDB = Tabelas(estabelecerconn)

GerenciarVendas = Venda(estabelecerconn)

GerenciarProduto = Produto(estabelecerconn)



#TODAS AS FUNCIONALIDADES DO C-R-U-D ABAIXO:


# GerenciarDB.vendas() #CREATE CRIANDO TABELAS

# GerenciarProduto.cadastrar_produto('Bolo Cremoso','Bolo Cremoso com chocolate ao cacau puro, com pitadinhas de leite condensado',20,10.00) #CREATE

# GerenciarProduto.consultar_produto(6) #READ

# GerenciarProduto.atualizar_quantidade(1,5) #UPDATE

# GerenciarVendas.inserir_venda(1,30,"2025-06-16") #CREATE

# GerenciarProduto.deletar_produto(6) #DELETE





        

