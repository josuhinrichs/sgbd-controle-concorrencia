import auxclasses

arq_read = open("in.txt")

tx_manager = auxclasses.TransactionManager()

for linha in arq_read:
    op = linha
    # print(op[0])

    match op[0]:
        case 'B':
            op_aux = linha.split('T(')
            id = int(op_aux[1].replace(')\n', '').replace(')', ''))
            #print("id:", obj)
            tx_manager.startTransaction(id)
        case 'r':
            op_aux = linha.split('(')
            
            id = int(op_aux[0].replace('r',''))
            obj = op_aux[1].replace(')\n','').replace(')','')
            
            # print("obj:", obj)
            # print("id:", id)

            tx_manager.sharedLock(obj, id)
        case 'w':
            op_aux = linha.split('(')
            
            id = int(op_aux[0].replace('w',''))
            
            obj = op_aux[1].replace(')\n','').replace(')','')
            
            # print("obj:", obj)
            # print("id:", id)

            tx_manager.exclusiveLock(obj, id)
        case 'C':
            op_aux = linha.split('(')
            id= op_aux[1].replace(')\n','').replace(')','')
            # print("id:", id)
            
            tx_manager.commitTransaction(id)
        case _:
            print('ERRO - OPERAÇÃO NÃO ENCONTRADA\n')