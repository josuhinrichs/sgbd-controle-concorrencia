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
        lock_table_file.close()
        print('\n##### Bloqueio compartilhado no item [', item, '], na transacao [', transaction, '] #####')

    def LX(self, transaction, item):
        # Insere um bloqueio no modo exclusivo na Lock Table sobre o item D para a
        #transaco Tr
        lock_table_file = open(self.lock_table, 'a')
        lock_table_file.write(str(item) + ';' + str(transaction) + ';' + 'X' + '\n')
        lock_table_file.close()
        print('\n##### Bloqueio exclusivo no item [', item, '], na transacao [', transaction, '] #####')

    def U(self, transaction, item):
        #Apaga o bloqueio da transacao Tr sobre o item D na Lock Table.
        lock_table_file = open(self.lock_table)
        new_lock_table = []
        
        for line in lock_table_file:
            list_lock_table = line.split(';')
            if list_lock_table[0] != item or list_lock_table[1] != transaction:
                new_lock_table.append(line)
        lock_table_file.close()

        lock_table_file = open(self.lock_table, 'w')
        for line in new_lock_table:
            lock_table_file.write(line)
        lock_table_file.close()

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
            return 'Undefined Operation'
    
    # Remove todos os bloqueios de uma transacao
    def deleteTransactionLocks(self, transaction_id):
        lock_table_file = open(self.lock_table)
        new_lock_table = []

        for line in lock_table_file:
            list_line_lock_table = line.split(';')
            if list_line_lock_table[1] != transaction_id:
                new_lock_table.append(line)
        lock_table_file.close()

        lock_table_file = open(self.lock_table, 'w')
        for line in new_lock_table:
            lock_table_file.write(line)
        lock_table_file.close()

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

    # recebe id da transacao e retorna uma lista do itens bloqueados pela transacao
    def checkLockTransaction(self, transaction_id):
        lock_table_file = open(self.lock_table)
        itens = []
        for line in lock_table_file:
            list_line_lock_table = line.split(';')
            if list_line_lock_table[1] == transaction_id: 
                itens.append(list_line_lock_table[0])
        lock_table_file.close()
        return itens

    def printWaitQueue(self, item_id):
        wait_list = self.wait_queue[ str(item_id) ]
        
        for tuple in wait_list:
            print(" - Transação ", tuple[0].id)
        pass

    def saveLockTable(self):
        pass
        

###################

lock_manager = LockManager()

class TransactionManager:
    def __init__(self):
        self.graph_wait_die = {}
        self.graph_wound_wait = {}
        self.timestamp = 0
        self.transaction_list = {}

    def startTransaction(self, transaction_number):
        self.timestamp += 1
        new_transaction = Transaction(transaction_number)
        new_transaction.timestamp = self.timestamp

        self.transaction_list[str(transaction_number)] = new_transaction
        print('\n##### Transacao [', transaction_number,'] iniciada #####')
    
    def getTransaction(self, transaction_id):
        return self.transaction_list[str(transaction_id)]

    def commitTransaction(self, transaction_id):
        item_lists = lock_manager.checkLockTransaction(transaction_id)
        lock_manager.deleteTransactionLocks(transaction_id)
        print('\n##### Transacao [', transaction_id, '] foi validada e seus bloqueios foram liberados#####')
        
        self.manageQueue(transaction_id, item_lists)

    def manageQueue(self, transaction, item_lists):
        if(not item_lists or not lock_manager.wait_queue[str(item_lists[0])]):
            return

        item = item_lists[0]
            
        lock_list = lock_manager.wait_queue[str(item)]
        next_op = lock_list[0]
        tupla = lock_manager.wait_queue[str(item)].pop(0)
        self.removeGraph(tupla[0])

        next_op[0].status = "active"
        self.executeOperation(next_op[1], next_op[0].id, item)
        
        transaction = self.getTransaction(transaction)

        for op in transaction.operations_queue:
            if (not self.executeOperation(op[0], op[1], op[2])):
                transaction.operations_queue.pop()
                break
            transaction.operations_queue.pop(0)
                    

    def executeOperation(self, operation, transaction_id, item_id):
        transaction = self.getTransaction(transaction_id)

        # caso a transação não esteja esperando outra para prosseguir, continua
        if (transaction.status == "active"):
            if(item_id == None):
                self.commitTransaction(transaction_id)
                return True
            # verificar a situação do item na lock table
            checked_lock = lock_manager.checkLock(item_id) #(o tipo do bloqueio que atualmente bloqueia o item)

            # caso o item esteja livre de bloqueios ou em bloqueio compartilhado inserimos o lock da operação na lock table
            if(checked_lock[0] == ""):
                lock_manager.insertLock(item_id, operation, transaction_id)
                return True
            elif(checked_lock[0] == "S" and operation == "exclusive-lock"):
                res = True
                for locker_transaction_id in checked_lock[1]:
                    locker_transaction = self.getTransaction(locker_transaction_id)

                    if(METHOD == "wait-die"):
                        res = self.waitDie(transaction, locker_transaction, item_id, operation)
                    else:
                        res = self.woundWait(transaction, locker_transaction, item_id, operation)
                    if not res:
                        break
                if res:
                    lock_manager.insertLock(item_id, operation, transaction_id)
                return True
            elif(checked_lock[0] == "S" and operation == "shared-lock"):
                lock_manager.insertLock(item_id, operation, transaction_id)
                return True
            else:
                if(METHOD == "wait-die"):
                    self.waitDie(transaction, self.getTransaction(checked_lock[1][0]), item_id, operation)
                else:
                    self.woundWait(transaction, self.getTransaction(checked_lock[1][0]), item_id, operation)
                return True
        else:
            # caso a transacao esteja em "waiting", a operacao vai para a fila de operacoes da transação
            transaction.operations_queue.append([operation, transaction_id, item_id])
            print("##### Transação em espera - Operação colocada na fila #####")
            return False
    
    # x espera pelo y
    def insertGraph(self, transaction_x, transaction_y, waitDie):
        x_id = transaction_x.id
        y_id = transaction_y.id

        x_exists = False
        y_exists = False
        
        if waitDie:
            for key in list(self.graph_wait_die.keys()):
                if key == str(x_id):
                    self.graph_wait_die[str(x_id)].append(str(y_id))
                    x_exists = True
                if key == str(y_id):
                    y_exists = True
            if not x_exists:
                self.graph_wait_die[str(x_id)] = []
                self.graph_wait_die[str(x_id)].append(str(y_id))
            if not y_exists:
                self.graph_wait_die[str(y_id)] = []
        else:
            for key in list(self.graph_wound_wait.keys()):
                if key == str(x_id):
                    self.graph_wound_wait[str(x_id)].append(str(y_id))
                    x_exists = True
                if key == str(y_id):
                    y_exists = True
            if not x_exists:
                self.graph_wound_wait[str(x_id)] = []
                self.graph_wound_wait[str(x_id)].append(str(y_id))
            if not y_exists:
                self.graph_wound_wait[str(y_id)] = []

    def removeGraph(self, transaction):
        trans_id = transaction.id

    def woundWait(self, transaction_x, transaction_y, item, lock):
        if (transaction_x.timestamp < transaction_y.timestamp):
            print("\n##### Transação %d sofreu rollback #####", transaction_y.id)
            lock_manager.deleteTransactionLocks(transaction_y.id)
            
            #deve apresentar a lista de espera do item de dado que gerar
            #Rollback.]
            print("\n##### FILA DE ESPERA DO ITEM #####")
            lock_manager.printWaitQueue(item)
            
            return True
        elif (transaction_x.timestamp == transaction_y.timestamp):
            lock_manager.U(transaction_x.id, item)
            return True
        else:
            lock_manager.insertWaitQueue(transaction_x, item, lock)
            print("\n##### Transação %d foi postergada #####", transaction_x.id)
            self.insertGraph(transaction_x, transaction_y, True)
            return False

    def waitDie(self, transaction_x, transaction_y, item, lock):
        # Tx deseja um dado bloqueado por Ty
        if (transaction_x.timestamp < transaction_y.timestamp ):
            print("\n##### Transação %d foi postergada #####" % transaction_x.id)
            lock_manager.insertWaitQueue(transaction_x, item, lock)
            self.insertGraph(transaction_x, transaction_y, True)
            return False
        elif (transaction_x.timestamp == transaction_y.timestamp):
            lock_manager.U(transaction_x.id, item)
            return False
        else:
            print("\n##### Transação %d sofreu rollback #####" % transaction_x.id)
            lock_manager.deleteTransactionLocks(transaction_x.id)
            lock_manager.insertWaitQueue(transaction_x, item, lock)
            print(transaction_x.status)
            
            #deve apresentar a lista de espera do item de dado que gerar
            #Rollback.
            print("\n##### FILA DE ESPERA DO ITEM #####")
            lock_manager.printWaitQueue(item)
            return False
            

##################

class Transaction:
    def __init__(self, number):
        self.id = number
        self.timestamp = 0#timestamp
        self.status = "active" #active|commited|waiting
        self.operations_queue = []

##################