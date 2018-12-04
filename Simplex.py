import numpy as np


def simplex (c, A, b, verbose=False):
    '''
    @Autor : Tibor Boglár, 
    @Github: https://github.com/tiborzinho/
    
    Dado o problema de minimização, já incluindo as variáveis artificiais e de folga, resolve o problema.
    
    min c^Tx sujeito a Ax=b, x >= 0

    Att: Deve-se importar o numpy, caso não queira, basta implementar uma função que transpõe matrizes.
    
    
    Args:
        c (list): vetor de custos
        A (list): matriz de coeficients
        b (list): vetor de restrições
        verbose (boolean) : decide se quer printar as iterações ou não
        
    Returns:
        tuple: retorna uma tupla de 3 ordenadas (tableau final, dicionário de soluções, custo final)
               o dicionário resultante tem como chave a indíce da variável e o valor da chave é o próprio valor da variável.
    '''
    
    iteracoes = 0
    tableau = tableauInicial(c, A, b)

    while podeMelhorar(tableau) and iteracoes < 100:
        iteracoes+=1
        pivot = encontrarIndexPivot(tableau)
        if pivot[0] == float("-inf"):
            return '.Problema ilimitado.'
        if pivot[0] == 'sem_solucao':
            return '.Problema sem solução.'
        if pivot[0] == 'ilimitado':
            return '.Problema ilimitado'
        if verbose:
            print('Iteração {}:'.format(iteracoes))
            print(np.array(tableau))
            print('O pivô está na linha', pivot[0], 'e coluna', pivot[1], '\n')
        pivoteamento(tableau, pivot)
    
    return tableau, solucao(tableau), valorCusto(tableau)

def tableauInicial(c, A, b):
    '''
    Monta o tableau inicial no formato do Bertsimas.
    '''
    
    # Adiciono aqui o custo inicial 0 e a linha correspondente ao custo
    tableau = [[0] + c] 
    
    # Aqui eu itero sobre todas as linhas de A, adicionando x_b à esquerda
    for row in range (len(A)): 
        tableau.append([b[row]] + A[row])
    return tableau

def podeMelhorar(tableau):
    '''
    Verifica se existe algum custo negativo, se sim, então o algoritmo continua.
    
    retorna : boolean
    '''
    primeiraLinha = tableau[0]
    return any(x < 0 for x in primeiraLinha)

def encontrarIndexPivot(tableau):
    '''
    Dado o tableau, verifica os custos reduzidos, pegando seu primeiro valor negativo e usa a regra do quociente.
    Devolve a linha e a coluna do elemento pivot. 
    '''

    # pegar o primeiro valor negativo do vetor de custos reduzidos
    custos_reduzidos = [index_col for index_col, val in enumerate(tableau[0][1:]) if val < 0]
    if len(custos_reduzidos) == 0:
        return ['sem_solucao']
    pivot_col = [index_col for index_col, val in enumerate(tableau[0][1:]) if val < 0][0]
    quotients = []
    for index, row in enumerate(tableau):
        if row[pivot_col + 1] > 0:
            quotient = row[pivot_col] / row[pivot_col + 1]
            quotients.append((index, quotient))

    # pega o índice do menor quociente do teste da razão, se todos os valores são menores que zero então o problema é ilimitado
    k = len([idx for idx, val in quotients])
    if k == 0:
        return ['ilimitado']
    else:
        pivot_row = min([idx for idx, val in quotients])    
        if pivot_row < 0:
            pivot_row = float("-inf")

        return pivot_row, pivot_col+1

def solucao(tableau):
    '''
    Dado a última iteração do Simplex, pega o tableau final e verifiac quais as variáveis finais e seus valores.
    Retorna um dicionário contendo o índice da variável e seu valor.
    '''
    my_dict = {}
    for idx, row in enumerate(np.transpose(tableau)):
        if colunaPivot(row):
            for i in range(0, len(row)):
                if row[i] == 1:
                    my_dict['x'+ str(idx)] = np.transpose(tableau)[0][i]
    return my_dict

def colunaPivot(col):
    '''
    Verifica-se se a coluna é pivô, isto é, se seu custo reduzido é zero e se a soma de seus valores dá 1.
    '''
    return (len([c for c in col if c == 0]) == len(col) - 1) and sum(col) == 1

def valorCusto(tableau):
    '''
    Apenas retornando o primeiro valor do Simplex, correspondente ao custo do tableau
    ''' 
    return -tableau[0][0]

def pivoteamento(tableau, pivot):
    '''
    Regra do pivoteamento: 
    1. Sabendo-se qual o elemento pivot, iremos dividir a linha do elemento pivot por ela mesma.
    2. Iremos dividir as demais linhas pelos elemento que se encontra na mesma coluna pivot e subtrair a linha do elemento pivot.
    '''
    
    i,j = pivot

    pivotDenom = tableau[i][j]
    tableau[i] = [x / pivotDenom for x in tableau[i]]

    for k,row in enumerate(tableau):
        if k != i:
            pivotRow = [y * tableau[k][j] for y in tableau[i]]
            tableau[k] = [x - y for x,y in zip(tableau[k], pivotRow)]
            
def teste_1():
    '''
    Teste do algoritmo com um exemplo qualquer.
    '''
    c = [1,-5,-23,0,0]
    A = [[1,2,10,1,0],[1,-1,0,0,1]]
    b = [4,1]
    
    return simplex(c,A,b)

def teste_2():
    c = [1,-3,4,3,5,6,7,1,0,0]
    A = [[1,2,10,1,5,7,8,1,1,0],[1,-1,0,0,1,3,2,4,0,1]]
    b = [4,1]
    
    return simplex(c,A,b)

def teste_3():
    A = [[2,-5,1,1,0],[1,4,0,0,1]]
    b = [3,5]
    c = [-1,-3,-5,0,0]
    
    return simplex(c,A,b)

if __name__ == "__main__":
    tests = [teste_1(), teste_2(), teste_3()]
    
    for idx, test in enumerate(tests):
        print('Teste', idx+1)
        print(test[1:])
        print('passou no teste.')
        print()
