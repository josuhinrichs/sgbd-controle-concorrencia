METHOD = ""
LOCK_TABLE_PATH = 'lock_table.txt'

class LockManager:
    def __init__(self):
        self.lock_table = LOCK_TABLE_PATH
        self.wait_queue = {}

    def LS(self, transaction, item):
#         Insere um bloqueio no modo compartilhado na Lock Table sobre o item D
#         para a transacao Tr
        lock_table_file = open(self.lock_table, 'a')
        lock_table_file.write(str(item) + ';' + str(transaction) + ';' + 'S' + '\n')
        lock_table_file.close

    def LX(self, transaction, item):
        # Insere um bloqueio no modo exclusivo na Lock Table sobre o item D para a
        #transaco Tr
        lock_table_file = open(self.lock_table, 'a')
        lock_table_file.write(str(item) + ';' + str(transaction) + ';' + 'X' + '\n')
        lock_table_file.close

    def U(self, transaction, item):
        #Apaga o bloqueio da transacao Tr sobre o item D na Lock Table.
        pass

    def insertWaitQueue(self, transaction, item, lock):
        #inserir transacao e sua lista de espera no dicionario do Lock Manager
        transaction.status = "waiting"
        self.wait_queue[ str(item) ] = [ [transaction,lock] ]

    # Funcao chamdada pelo TrManeger para inserir um bloqueio
    def insertLock(self, item_id, operation, transaction_id):
        if operation == 'shared-lock':
            self.LS(transaction_id, item_id)
        elif operation == 'exclusive-lock':
            self.LX(transaction_id, item_id)
        else:
            return 'Indefined Operation'
    
    # Remove todos os bloqueios de uma transacao
    def deleteTransactionLocks(self, transaction_id):
        print(transaction_id)
        lock_table_file = open(self.lock_table)
        new_lock_table = []

        for line in lock_table_file:
            list_line_lock_table = line.split(';')
            if list_line_lock_table[1] != transaction_id:
                new_lock_table.append(line)
        lock_table_file.close

        lock_table_file = open(self.lock_table, 'w')
        for line in new_lock_table:
            lock_table_file.write(line)
        lock_table_file.close

    #recebe o id do item e retorna uma lista onde o primeiro elemento eh
    # o tipo do bloqueio e o segundo eh uma lista com as transacoes q tem
    # o bloqueio
    def checkLock(self, item_id):
        lock_table_file = open(self.lock_table)
        lock = ''
        transactions = []
        for line in lock_table_file:
            list_line_lock_table = line.split(';')
            if list_line_lock_table[0] == item_id:
                if list_line_lock_table[2] == 'X':
                    return [list_line_lock_table[2], [list_line_lock_table[1]]]
                else:
                    lock = list_line_lock_table[2]
                    transactions.append(list_line_lock_table[1])
        lock_table_file.close()
        lock = lock.replace('\n', '')
        return [lock, transactions]

    def saveLockTable(self):
        pass
        

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
    
    def getTransaction(self, transaction_id):
        return self.transaction_list[str(transaction_id)]

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
            checked_lock = lock_manager.checkLock(item_id) #(o tipo do bloqueio que atualmente bloqueia o item)

            # caso o item esteja livre de bloqueios ou em bloqueio compartilhado inserimos o lock da operação na lock table
            if(checked_lock[0] == ""):
                lock_manager.insertLock(item_id, operation, transaction_id)
                return
            elif(checked_lock[0] == "S"):
                res = True
                for locker_transaction_id in checked_lock[1]:
                    locker_transaction = self.getTransaction(locker_transaction_id)

                    if(METHOD == "wait-die"):
                        res = self.deadlock.waitDie(transaction, locker_transaction, item_id, operation)
                    else:
                        res = self.deadlock.woundWait(transaction, locker_transaction, item_id, operation)
                    if not res:
                        break
                if res:
                    lock_manager.insertLock(item_id, operation, transaction_id)
                return
            else:
                if(METHOD == "wait-die"):
                    self.deadlock.waitDie(transaction, self.getTransaction(checked_lock[1]), item_id, operation)
                else:
                    self.deadlock.woundWait(transaction, self.getTransaction(checked_lock[1]), item_id, operation)
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
    
    def woundWait(self, transaction_x, transaction_y, item, lock):
        if (transaction_x.timestamp < transaction_y.timestamp):
            print("--- Transação %d sofreu rollback ---", transaction_y.id)
            #freeAllLocks()
            #deve apresentar a lista de espera do item de dado que gerar
            #Rollback.]
            return True
        else:
            lock_manager.insertWaitQ(transaction_x, item, lock)
            #insereGrafo(transaction_x, transaction_y)
            return False

    def waitDie(self, transaction_x, transaction_y, item, lock):
        # Tx deseja um dado bloqueado por Ty
        if (transaction_x.timestamp < transaction_y.timestamp):
            lock_manager.insertWaitQ(transaction_x, item, lock)
            #insereGrafo(transaction_x, transaction_y)
            return False
        else:
            print("--- Transação %d sofreu rollback ---", transaction_x.id)
            #freeAllLocks()
            #deve apresentar a lista de espera do item de dado que gerar
            #Rollback.
            return True