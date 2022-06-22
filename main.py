import auxclasses

arq_read = open("in.txt")

tx_manager = auxclasses.TransactionManager()
for method in ["wait-die"]:
    auxclasses.METHOD = method
    print('###### MÉTODO USADO #####:', method)
    for linha in arq_read:
        op = linha
        tx_manager.printGraph() # TESTE ---------------------------------------------------------------------------------------------------
        match op[0]:
            case 'B':
                op_aux = linha.split('T(')
                transaction_id = int(op_aux[1].replace(')\n', '').replace(')', ''))
                #print("id:", obj)
                tx_manager.startTransaction(transaction_id)
            case 'r':
                op_aux = linha.split('(')
                
                transaction_id = int(op_aux[0].replace('r',''))
                obj = op_aux[1].replace(')\n','').replace(')','')
                
                # print("obj:", obj)
                # print("id:", id)

                #tx_manager.sharedLock(obj, id)
                tx_manager.executeOperation("shared-lock", transaction_id, obj)
            case 'w':
                op_aux = linha.split('(')
                
                transaction_id = int(op_aux[0].replace('w',''))
                
                obj = op_aux[1].replace(')\n','').replace(')','')
                
                # print("obj:", obj)
                # print("id:", id)

                #tx_manager.exclusiveLock(obj, id)
                tx_manager.executeOperation("exclusive-lock", transaction_id, obj)
            case 'C':
                op_aux = linha.split('(')
                transaction_id = op_aux[1].replace(')\n','').replace(')','')
                # print("id:", id)
                
                tx_manager.executeOperation("commit-transaction",transaction_id, None )
            case _:
                print('ERRO - OPERAÇÃO NÃO ENCONTRADA\n')