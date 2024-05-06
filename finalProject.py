import random as rd
from itertools import product
import random as rd

itercount = 0
def visualizer(curBoard):
    rowLen = 3*len(curBoard)+2
    semi = int(len(curBoard)**0.5)
    print("="*rowLen)
    for i in range(len(curBoard)):
        item = curBoard[i]
        print("|| ", end = "")
        for j in range(len(item)):
            if j % semi == semi - 1:
                print(item[j], end = " || ")
            else:
                print(item[j], end = " ")
        print()

        if i % semi == semi - 1:
            print("="*rowLen)


def sudokuSolverLite(n, grid):

    flag = False
    '''
    for i in range(r, 9):
        for j in range(c, 9):
            if(grid[i][j] != 0):
                n += 1
            else:
                flag = True
                break
        if flag == True:
            break
    '''
    if (n >= 81):
        return (True, grid)
    while(grid[n//9][n%9] != 0):
        n+=1
        if (n >= 81):
            return (True, grid)

    r = n//9
    c = n%9
    available = []
    for val in range(1,10):
        if (safe(r,c, val, grid) == True):
            available.append(val)

    for i in range(len(available)):
        val = available[rd.randrange(len(available))]
        grid[r][c] = val
        if (sudokuSolverLite(n+1, grid)[0] == True):
            return (True, grid)
        available.remove(val)
    
    grid[r][c] = 0
    return (False, grid)

def sudokuCreator():
    grid = []
    for i in range(9):
        grid.append([0]*9)
    return sudokuSolverLite(0, grid)[1]

def gridRemover(grid, dif):
    i = 0
    contained = []
    r_rand = 0
    c_rand = 0
    while 2*i < dif:
        while True:
            r_rand = rd.randrange(9)
            c_rand = rd.randrange(9)
            if (r_rand, c_rand) not in contained and (c_rand, r_rand) not in contained:
                break
        
        grid[r_rand][c_rand] = '.'
        grid[c_rand][r_rand] = '.'
        i+= 1
    return grid



def notInRow(row, col, val, grid):
    size = len(grid)
    for i in range(size):
        if grid[row][i] == val and i != col:
            return False
    return True

def notInCol(row, col, val, grid):
    size = len(grid)
    for i in range(size):
        if grid[i][col] == val and i != row:
            return False
    return True

def notInBox(row, col, val, grid):
    size = len(grid)
    semi = int(size**0.5)
    for i in range(semi):
        for j in range(semi):
            r = semi*(row//semi) + (i+row%semi)%semi
            c = semi*(col//semi) + (j+col%semi)%semi
            if grid[r][c] == val and r != row and c != col:
                return False
    return True

def safe(row, col, val, grid):
    return notInRow(row, col, val, grid) and \
            notInCol(row, col, val, grid) and \
            notInBox(row, col, val, grid)

def findNextFill(grid):
    size = len(grid)
    listEmpty = []
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '.':
                listEmpty.append((i,j))
    if len(listEmpty) == 0:
        return None
    return listEmpty[rd.randrange(0,len(listEmpty))]

def degreeCount(grid, row, col):
    size = len(grid)
    count = 0
    for i in range(size):
        if grid[row][i] == '.':
            count += 1
        if grid[i][col] == '.':
            count += 1
    semi = int(size**0.5)
    for i in range(semi):
        for j in range(semi):
            r = semi*(row//semi) + (i+row%semi)%semi
            c = semi*(col//semi) + (j+col%semi)%semi
            if grid[r][c] == '.':
                count += 1
    return count

def degreeHeuristic(grid):
    size = len(grid)
    maxVal = -1
    maxCell = None
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '.':
                count = degreeCount(grid, i, j)
                if count > maxVal:
                    maxVal = count
                    maxCell = (i,j)
    return maxCell

def remainingValues(grid):
    remVal = {}
    size = len(grid)
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '.':
                remVal[(i,j)] = set(range(1,size + 1))
                for k in range(1, size+1):
                    if not safe(i,j,k,grid):
                        remVal[(i,j)].remove(k)
    return remVal

def forwardChecking(grid, remVal):
    size = len(grid)
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '.':
                if len(remVal[(i,j)]) == 0:
                    return False
    return True

def MRV(grid):
    size = len(grid)
    minVal = size + 1
    minCell = None
    remVal = remainingValues(grid)
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '.':
                if len(remVal[(i,j)]) < minVal:
                    minVal = len(remVal[(i,j)])
                    minCell = (i,j)
    return minCell

def MRVdegreeHeuristic(grid):
    size = len(grid)
    minVal = size + 1
    minCell = None
    minList = []
    remVal = remainingValues(grid)
    for i in range(size):
        for j in range(size):
            if grid[i][j] == '.':
                if len(remVal[(i,j)]) < minVal:
                    minVal = len(remVal[(i,j)])
                    minCell = (i,j)
                    minList = [(i,j)]
                elif len(remVal[(i,j)]) == minVal:
                    minList.append((i,j))
    for cell in minList: 
        if minCell is None or degreeCount(grid, cell[0], cell[1]) > degreeCount(grid, minCell[0], minCell[1]):
            minCell = cell
    return minCell

# End of helper functions

def DFS(board):
    global itercount   
    itercount += 1
    size = len(board)
    next = findNextFill(board)
    if next is None:
        return board
    
    row, col = next
    for val in range(1,size + 1):
        board[row][col] = val
        if not safe(row, col, val, board):
            continue
        result = DFS(board)
        if result is not None:
            return result
    board[row][col] = '.'
# update the remaining values for each cell


def DFSWithForwardChecking(board):
    next = findNextFill(board)
    global itercount   
    itercount += 1
    if next is None:
        return board
    
    row, col = next
    remVal = remainingValues(board)
    for val in remVal[(row,col)]:
        if forwardChecking(board, remVal):
            board[row][col] = val
            result = DFSWithForwardChecking(board)
            if result is not None:
                return result
            else:
                board[row][col] = '.'

    return None

def DFSwithDegreeHeuristic(board):
    next = degreeHeuristic(board)
    global itercount   
    itercount += 1
    if next is None:
        return board
    row, col = next
    remVal = remainingValues(board)
    for val in remVal[(row,col)]:
        if forwardChecking(board, remVal):
            board[row][col] = val
            result = DFSwithDegreeHeuristic(board)
            if result is not None:
                return result
            else:
                board[row][col] = '.'

    return None
def DFSwithFCMRV(board):
    next = MRV(board)
    global itercount   
    itercount += 1
    if next is None:
        return board
    row, col = next
    remVal = remainingValues(board)
    for val in remVal[(row,col)]:
        if forwardChecking(board, remVal):
            board[row][col] = val
            result = DFSwithFCMRV(board)
            if result is not None:
                return result
            else:
                board[row][col] = '.'

    return None

def DFSwithFCMRVdegree(board):
    next = MRVdegreeHeuristic(board)
    global itercount   
    itercount += 1
    if next is None:
        return board
    row, col = next
    remVal = remainingValues(board)
    for val in remVal[(row,col)]:
        if forwardChecking(board, remVal):
            board[row][col] = val
            result = DFSwithFCMRVdegree(board)
            if result is not None:
                return result
            else:
                board[row][col] = '.'

    return None

def LCV(remVal, values):
    dic = {}
    for val in values:
        dic[val] = 0
    for item in list(remVal.values()):
        for val in item:
            if val in dic:
                dic[val] += 1
    
    minVal = len(remVal.values()) + 1
    for key in dic:
        if dic[key] < minVal:
            minVal = dic[key]
            minKey = key
    return minKey

def DFSwithFCLCV(board):
    next = findNextFill(board)
    global itercount   
    itercount += 1
    if next is None:
        return board
    row, col = next
    remVal = remainingValues(board)
    values = list(remVal[(row,col)]).copy()
    while len(values) > 0:
        val = LCV(remVal, values)
        values.remove(val)
        if forwardChecking(board, remVal):
            board[row][col] = val
            result = DFSwithFCLCV(board)
            if result is not None:
                return result
            else:
                board[row][col] = '.'

    return None

def DFSwithFCLCVMRV(board):
    next = MRV(board)
    global itercount   
    itercount += 1
    if next is None:
        return board
    row, col = next
    remVal = remainingValues(board)
    values = list(remVal[(row,col)]).copy()
    while len(values) > 0:
        val = LCV(remVal, values)
        values.remove(val)
        if forwardChecking(board, remVal):
            board[row][col] = val
            result = DFSwithFCLCVMRV(board)
            if result is not None:
                return result
            else:
                board[row][col] = '.'

    return None
def DFSwithFCLCVdegree(board):
    next = degreeHeuristic(board)
    global itercount   
    itercount += 1
    if next is None:
        return board
    row, col = next
    remVal = remainingValues(board)
    values = list(remVal[(row,col)]).copy()
    while len(values) > 0:
        val = LCV(remVal, values)
        values.remove(val)
        if forwardChecking(board, remVal):
            board[row][col] = val
            result = DFSwithFCLCVdegree(board)
            if result is not None:
                return result
            else:
                board[row][col] = '.'

    return None

def DFSwithFCLCVMRVdegree(board):
    next = MRVdegreeHeuristic(board)
    global itercount   
    itercount += 1
    if next is None:
        return board
    row, col = next
    remVal = remainingValues(board)
    values = list(remVal[(row,col)]).copy()
    while len(values) > 0:
        val = LCV(remVal, values)
        values.remove(val)
        if forwardChecking(board, remVal):
            board[row][col] = val
            result = DFSwithFCLCVMRVdegree(board)
            if result is not None:
                return result
            else:
                board[row][col] = '.'

    return None

def TabuSearch(board):
    size = len(board)
    tabu = []
    while True:
        next = findNextFill(board)
        if next is None:
            return board
        row, col = next
        best = 0
        bestVal = 0
        for val in range(1,size + 1):
            if not safe(row, col, val, board):
                continue
            board[row][col] = val
            if board not in tabu:
                tabu.append(board)
                best = board
                bestVal = val
        board = best
        board[row][col] = bestVal

# test
    
def checkValidSolution(grid):
    for i in range(9):
        for j in range(9):
            if (safe(i,j,grid[i][j],grid) == False):
                return False
    return True

from copy import deepcopy

def demo(testname, board):
    global itercount
    itercount = 0
    board2 = deepcopy(board)
    match testname:
        case "DFS":
            result = DFS(board2)

        case "DFSWithForwardChecking":
            result = DFSWithForwardChecking(board2)
        case "DFSwithFCMRV":
            result = DFSwithFCMRV(board2)
        case "DFSwithDegreeHeuristic":
            result = DFSwithDegreeHeuristic(board2)
        case "TabuSearch":
            result = TabuSearch(board2)
        case "DFSwithFCMRVdegree":
            result = DFSwithFCMRVdegree(board2)
        case "DFSwithFCLCV":
            result = DFSwithFCLCV(board2)
        case "DFSwithFCLCVMRV":
            result = DFSwithFCLCVMRV(board2)
        case "DFSwithFCLCVMRVdegree":
            result = DFSwithFCLCVMRVdegree(board2)
        case "DFSwithFCLCVdegree":
            result = DFSwithFCLCVdegree(board2)
        case _:
            print("Invalid test name")
    return itercount
def test(values):
    for i in values:
        DFS = []
        DFSWithForwardChecking = []
        DFSwithFCMRV = []
        DFSwithFCMRVdegree = []
        DFSwithFCLCV = []
        DFSwithFCLCVMRV = []
        DFSwithFCLCVMRVdegree = []
        for j in range(10):
            board = sudokuCreator()
            board2 = gridRemover(board, 60)

            demo("DFS", board2)
            DFS.append(itercount)
            demo("DFSWithForwardChecking", board2)
            DFSWithForwardChecking.append(itercount)
            demo("DFSwithFCMRV", board2)
            DFSwithFCMRV.append(itercount)
            demo("DFSwithFCMRVdegree", board2)
            DFSwithFCMRVdegree.append(itercount)
            demo("DFSwithFCLCV", board2)
            DFSwithFCLCV.append(itercount)
            demo("DFSwithFCLCVMRV", board2)
            DFSwithFCLCVMRV.append(itercount)
            demo("DFSwithFCLCVMRVdegree", board2)
            DFSwithFCLCVMRVdegree.append(itercount)
        
        print("DFS: ", DFS)

        print("DFSWithForwardChecking: ", DFSWithForwardChecking)
        
        print("DFSwithFCMRV: ", DFSwithFCMRV)
        
        print("DFSwithFCMRVdegree: ", DFSwithFCMRVdegree)
        
        print("DFSwithFCLCV: ", DFSwithFCLCV)
        
        print("DFSwithFCLCVMRV: ", DFSwithFCLCVMRV)
        
        print("DFSwithFCLCVMRVdegree: ", DFSwithFCLCVMRVdegree)

        print("DFSmean: ", sum(DFS)/len(DFS))
        print("DFSWithForwardCheckingmean: ", sum(DFSWithForwardChecking)/len(DFSWithForwardChecking))
        print("DFSwithFCMRVmean: ", sum(DFSwithFCMRV)/len(DFSwithFCMRV))
        print("DFSwithFCMRVdegreemean: ", sum(DFSwithFCMRVdegree)/len(DFSwithFCMRVdegree))
        print("DFSwithFCLCVmean: ", sum(DFSwithFCLCV)/len(DFSwithFCLCV))
        print("DFSwithFCLCVMRVmean: ", sum(DFSwithFCLCVMRV)/len(DFSwithFCLCVMRV))
        print("DFSwithFCLCVMRVdegreemean: ", sum(DFSwithFCLCVMRVdegree)/len(DFSwithFCLCVMRVdegree))
        print("////////////////////////////////////////")

def main():
    test([60,70,80,90,100,110,120,130,140])

if __name__ == "__main__":
    main()
        
