import auxclasses

tx_manager = auxclasses.TransactionManager()
for method in ["wait-die", "wound-wait"]:
    auxclasses.METHOD = method
    print('\n----------- MÉTODO USADO -----------\n', method)
    arq_read = open("in3.txt")

    for linha in arq_read:
        op = linha

        match op[0]:
            case 'B':
                op_aux = linha.split('T(')
                transaction_id = int(op_aux[1].replace(')\n', '').replace(')', ''))

                tx_manager.startTransaction(transaction_id)
            case 'r':
                op_aux = linha.split('(')
                
                transaction_id = int(op_aux[0].replace('r',''))
                obj = op_aux[1].replace(')\n','').replace(')','')

                tx_manager.executeOperation("shared-lock", transaction_id, obj)
            case 'w':
                op_aux = linha.split('(')
                
                transaction_id = int(op_aux[0].replace('w',''))
                
                obj = op_aux[1].replace(')\n','').replace(')','')
                
                tx_manager.executeOperation("exclusive-lock", transaction_id, obj)
            case 'C':
                op_aux = linha.split('(')
                transaction_id = op_aux[1].replace(')\n','').replace(')','')

                tx_manager.executeOperation("commit-transaction",transaction_id, None )
            case _:
                print('ERRO - OPERAÇÃO NÃO ENCONTRADA\n')

    arq_read.close()