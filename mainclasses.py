

class Transaction_Manager:
    def __init__(self):
        pass
    

    def LS(transaction, item):
#         Insere um bloqueio no modo compartilhado na Lock Table sobre o item D
#         para a transacao Tr se puder, caso contrario cria/atualiza a Wait Q de D com a
#         transacao Tr.
        pass

    def LX(transaction, item):
        # Insere um bloqueio no modo exclusivo na Lock Table sobre o item D para a
#transa ̧c ̃ao Tr se puder, caso contr ́ario cria/atualiza a Wait Q de D com a transa ̧c ̃ao
#Tr.
        pass

    def U(transaction, item):
        #Apaga o bloqueio da transa ̧c ̃ao Tr sobre o item D na Lock Table.
        pass

##################

class Transaction:
    def __init__(self, number):
        self.timestamp
        self.state  #active|commited|aborted
        self.wait_list

##################

class Lock_Manager:
    def __init__(self):
        self.lock_table
        self.wait_q
