METHOD = ""

class LockManager:
    def __init__(self):
        self.lock_table = []
        self.wait_queue = {}

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

    def insertWaitQueue(self, transaction, item, lock):
        #inserir transacao e sua lista de espera no dicionario do Lock Manager
        self.wait_queue[ str(item) ] = [ [transaction,lock] ]
        

###################

lock_manager = LockManager()

class TransactionManager:
    def __init__(self):
        self.graph_wait_die = []
        self.graph_wound_wait = []
        self.timestamp = 0
        self.transaction_list = {}
        self.deadlock = Deadlock()

    def startTransaction(self, transaction_number):
        self.timestamp += 1
        new_transaction = Transaction(transaction_number)
        new_transaction.timestamp = self.timestamp

        self.transaction_list[str(transaction_number)] = new_transaction
        print('\nTransacao [', transaction_number,'] iniciada')
        print(METHOD)

    def sharedLock(self, transaction, item):
        print('\nBloqueio compartilhado no item [', item, '], na transacao [', transaction, ']')

    def exclusiveLock(self, transaction, item):
        print('\nBloqueio exclusivo no item [', item, '], na transacao [', transaction, ']')

    def commitTransaction(self, transaction):
        print('\nTransacao [', transaction, '] foi validada e seus bloqueios foram liberados')

    def __freeLock(self, transaction):
        pass

    def executeOperation(self, operation, transaction_id, item_id):
        transaction = self.transaction_list[str(transaction_id)]

        # caso a transação não esteja esperando outra para prosseguir, continua
        if (transaction.state == "active"):
            if(item_id == None):
                #makeCommit()
                return
            # verificar a situação do item na lock table
            #lock = lock_manager.checkLock(item_id)[0] (o tipo do bloqueio que atualmente bloqueia o item)
            lock = ""

            # caso o item esteja livre de bloqueios ou em bloqueio compartilhado inserimos o lock da operação na lock table
            if(lock == "S" or lock == ""):
                #lock_manager.insertLock(item_id, operation, transaction_id)
                return
            else:
                #locker_transaction = lock_manager.checkLock(item_id)[1] (id da transação que atualmente bloqueia o item)
                locker_transaction = 3
                if(METHOD == "wait-die"):
                    self.deadlock.waitDie(transaction, locker_transaction, item_id, operation)
                else:
                    self.deadlock.woundWait(transaction, locker_transaction, item_id, operation)
                return
        else:
            # caso a transacao esteja em "waiting", a operacao vai para a fila de operacoes da transação
            transaction.operations_queue.append([operation, transaction_id, item_id])
    
    def insertGraph(self, transaction, item):
        pass

##################

class Transaction:
    def __init__(self, number):
        self.id = number
        self.timestamp = 0#timestamp
        self.state = "active" #active|commited|waiting
        self.operations_queue = []

##################

class Deadlock:
    def __init__(self):
        pass
    
    def woundWait(self):
        pass

    def waitDie(self, transaction_x, transaction_y, item, lock):
        # Tx deseja um dado bloqueado por Ty
        if (transaction_x.timestamp < transaction_y.timestamp):
            transaction_x.state = "waiting"
            lock_manager.insertWaitQ(transaction_x, item, lock)
        else:
            print("--- Transação %d sofreu rollback ---", transaction_x.id)
        return