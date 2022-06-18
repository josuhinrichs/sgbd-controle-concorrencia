

class TransactionManager:
    def __init__(self):
        self.graph_wait_die = []
        self.graph_wound_wait = []
        self.time_stamp = 0

    def startTransaction(self, transaction):
        print('\nTransacao [', transaction,'] iniciada')

    def sharedLock(self, transaction, item):
        print('\nBloqueio compartilhado no item [', item, '], na transacao [', transaction, ']')

    def exclusiveLock(self, transaction, item):
        print('\nBloqueio exclusivo no item [', item, '], na transacao [', transaction, ']')

    def commitTransaction(self, transaction):
        print('\nTransacao [', transaction, '] foi validada e seus bloqueios foram liberados')

    def __freeLock(self, transaction):
        pass
    
    def insertGraph(self, transaction, item):
        pass

##################

class Transaction:
    def __init__(self, number):
        self.id = number
        self.ts #timestamp
        self.state  #active|commited|aborted
        self.wait_list

##################

class LockManager:
    def __init__(self):
        self.lock_table
        self.wait_q

    
    def LS(self, transaction, item):
#         Insere um bloqueio no modo compartilhado na Lock Table sobre o item D
#         para a transacao Tr se puder, caso contrario cria/atualiza a Wait Q de D com a
#         transacao Tr.
        pass

    def LX(self, transaction, item):
        # Insere um bloqueio no modo exclusivo na Lock Table sobre o item D para a
#transa ̧c ̃ao Tr se puder, caso contr ́ario cria/atualiza a Wait Q de D com a transa ̧c ̃ao
#Tr.
        pass

    def U(self, transaction, item):
        #Apaga o bloqueio da transa ̧c ̃ao Tr sobre o item D na Lock Table.
        pass

###################

class DeadLock:
    def __init__(self):
        pass
    
    def woundWait(self):
        pass

    def waitDie(self):
        pass