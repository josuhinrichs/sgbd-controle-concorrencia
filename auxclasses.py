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
        #transaco Tr se puder, caso contrario cria/atualiza a Wait Q de D com a transacao
        #Tr
        pass

    def U(self, transaction, item):
        #Apaga o bloqueio da transacao Tr sobre o item D na Lock Table.
        pass

    def insertWaitQ(self, transaction, item, lock):
        #inserir transacao e sua lista de espera no dicionario do Lock Manager
        self.wait_q[ str(item) ] = [ [transaction,lock] ]
        

###################

lock_manager = LockManager()

class TransactionManager:
    def __init__(self):
        self.graph_wait_die = []
        self.graph_wound_wait = []
        self.time_stamp = 0
        self.transaction_queue
        self.transactions

    def startTransaction(self, transaction):
        
        print('\nTransacao [', transaction,'] iniciada')

    def sharedLock(self, transaction_id, item):
        if( self.transactions[str(transaction_id)].state == "active" ):
            if( not lock_manager.wait_q[str[item]] ):
                pass
        else:
            

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
        self.timestamp #timestamp
        self.state = "active" #active|commited|waiting
        self.wait_list

##################

class DeadLock:
    def __init__(self):
        pass

    def verifyDeadlock(self, transaction_x, item):
        if(not lock_manager.wait_q[str[item]]):
            
        pass
    
    def woundWait(self):
        pass

    def waitDie(self, transaction_x, transaction_y, item):
        #Tx deseja um dado bloqueado por Ty
        if (True):
            lock_manager.insertWaitQ(transaction_x, item, )
        else:
            
            print("--- Transação %d sofreu rollback ---", transaction_x.id)
            lock_manager.insertWaitQ(transaction_x, item)
            pass
        pass