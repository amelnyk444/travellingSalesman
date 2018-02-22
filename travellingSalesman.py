infinity = float('inf')
bestResult = infinity
bestpath = []
vertices = {}#in this code i use matrix, so when i print that, full names of cities are too long to print them with matrix, so i made dict with cities
#and their numbers.When the program finds an edge, matrix records it as a "city-> city", but only numbers are displayed in the matrix
matrix = []


def FormMatrix(m):
    for i in range(len(m)):
        for j in range(len(m)):
            if 0==i:
                m[i][j] = j
            elif 0==j:
                m[i][j] = i
            elif i==j:
                m[i][j] = infinity#in order to avoid the path between the same city
    m[0][0] = " "


def Subtract(m):
    rowMin = [infinity for i in range(len(m)-1)]
    colMin = [infinity for i in range(len(m)-1)]
    #here program finds minimal values in rows and subtracts the minimal value from each element of the row
    for i in range(1,len(m)):
        rowMin[i-1] = min(m[i][1:])
    for i in range(1,len(m)):
        for j in range(1,len(m)):
            m[i][j] -=rowMin[i-1]
    #here program makes the same with columns
    for i in range(1,len(m)):
        for j in range(1,len(m)):
            if colMin[i-1]>m[j][i]:
                colMin[i-1] = m[j][i]
    for i in range(1,len(m)):
        for j in range(1,len(m)):
            m[j][i] -= colMin[i-1]
    #function returns sum of minimal elements from all rows and columns
    return sum(rowMin)+sum(colMin)


def CreateSlicedMatrix(m):#this function creates a matrix without row and column, which have already been included in path 
    slicedRow,slicedCol = GetMaxFineCoord(m)
    print("Edge: "+vertices[m[slicedRow][0]].__str__()+"->"+vertices[m[0][slicedCol]].__str__())#dict in use
    matrix = [m[i][:] for i in range(len(m))]
    del matrix[slicedRow]
    for i in range(len(matrix)):
        del matrix[i][slicedCol]
    DelReverse(matrix, m[slicedRow][0],m[0][slicedCol])
    return matrix,[ vertices[m[slicedRow][0]],vertices[m[0][slicedCol]]]
    

def GetFineForNull(m,row,col):
    rowMin = infinity
    colMin = infinity
    for i in range(1,len(m)):
        for j in range(1,len(m)):
            if row==i and col!=j:
                if m[i][j]<rowMin:
                    rowMin = m[i][j]
            elif row!=i and col == j:
                if m[i][j]<colMin:
                    colMin = m[i][j]
    return rowMin+colMin


def GetMaxFineCoord(m):#This function returns coordinates of element with max fine
    maxFine = 0
    mf_row = 0
    mf_column = 0
    for i in range(1,len(m)):
        for j in range(1,len(m)):
            if 0==m[i][j]:
                f = GetFineForNull(m,i,j)
                if maxFine<f:
                    maxFine = f
                    mf_row = i
                    mf_column = j
    return mf_row,mf_column


def CreateNewBranch(m,lim,path):#recursive function, which realizes the main part of algorithm
    global bestResult
    Print(m)
    temp = Subtract(m)
    print("Subtraction: ")
    Print(m)
    if lim+temp>bestResult:
        print("Result: "+(lim+temp).__str__()+", Best result: "+bestResult.__str__())
        print("Branch was rejected")
        return
    elif 2==len(m):
        Print(m)
        for i in range(1,len(m)):
            for j in range(1,len(m)):
                if m[i][j] != infinity:
                    path += [[vertices[m[i][0]],vertices[m[0][j]]]]

        print("Result: "+(lim+temp).__str__()+", Best result: "+bestResult.__str__())
        print("New best result")
        print("Path: "+path.__str__())
        bestResult = lim+temp
        return
    else:
         matrix,edge = CreateSlicedMatrix(m)
         CreateNewBranch(matrix,lim+temp,path+[edge])
         row,col = GetMaxFineCoord(m)
         m[row][col] = infinity
         CreateNewBranch(m,lim+temp,path)


def Print(m):
     for i in range(len(m)):
        for j in range(len(m)):
            if infinity == m[i][j]:
                print("M", end=' ')
            else:
                print(m[i][j], end=' ')
        print()


def DelReverse(m,row,col):#Reverse edges deleting
    possibleCol = m[0][1:] 
    possibleRows = [];
    for i in range(1,len(m)):
        possibleRows.append(m[i][0])
    if col in possibleRows and row in possibleCol:
         i = possibleRows.index(col)+1
         j = possibleCol.index(row)+1
         m[i][j] = infinity
        

def LoadToFile(m,v,f_name):
    f = open(f_name+'.pkl', 'wb')
    from pickle import dump
    from os import getcwd
    pickle.dump(m,f)
    f.close()
    f = open(os.getcwd()+'\\VerticesNames\\'+f_name+'_names.pkl','wb')
    pickle.dump(v,f)
    f.close()


def LoadFromFile(f_name):
    f = open(f_name+'.pkl', 'rb')
    from pickle import load
    from os import getcwd
    m = pickle.load(f)
    f.close()
    Print(m)
    f = open(getcwd()+'\\VerticesNames\\'+f_name+'_names.pkl','rb')
    v = pickle.load(f)
    f.close()
    return m,v


def InputVertices():    
    counter = 0
    while key!= b'\x1b':
        vertices[counter] = input()
        key = PressButton()
        counter+=1


def PressButton():
    from msvcrt import getch
    key = msvcrt.getch()
    return key


def InitVertices(v_count):
    for i in range(v_count):
        vertices[i+1] = i+1


def InputMatrix():
    m = [[0 for i in range(len(vertices)+1)] for i in range(len(vertices)+1)]
    for i in range(1,len(m)):
        for j in range(1,len(m)):
            print("Element ("+i+', '+j+'): ', end=' ')
            m[i][j] = ValueInput()
            print()
    FormMatrix(m)
    return m


def InputRoute():
    print('Write the route name')
    inp = input()
    from os import listdir , getcwd
    routes = filter(lambda x: x.endswith('.pkl'), os.listdir(os.getcwd()))
    if inp+'.pkl' in routes:
        print('Let`s go')
        return inp
    else:
        print('Incorrect input, try again')
        return InputRoute()


def InputChoice():
    pr = PressButton()
    if b'K' == pr:
         return False
    elif b'M' == pr:
         return True
    else:
         return InputChoice()


def ShowRoutes():
    from os import listdir , getcwd 
    routes = list(filter(lambda x: x.endswith('.pkl'), os.listdir(os.getcwd())))
    for route in routes:
        print(route[:-4])


def ValueInput():
    try:
       inp = float(input())
    except ValueError:
         print("Incorrect input, try again: ")
         return ValueInput()
    else:
         return inp


def Menu():
    global matrix
    print('You can choose one of the existing routes or create your own (Press left arrow to choose existing route or right arrow to create your own)')
    choice  = InputChoice()
    if False == choice:
        ShowRoutes()        
        matrix,vertices = LoadFromFile(InputRoute())
        for key in vertices:
            print(key+' : '+vertices[key])
        CreateNewBranch(matrix,0,bestpath)
    elif True == choice:
        print('Do you want to name vertices?(Right Arrow - Yes\Left Arrow - No)')
        choice = InputChoice()
        if True == choice:
            InputVertices()
        elif False == choice:
            print('Input amount of the vertices')
            InitVertices(ValueInput())
        print('Input matrix')
        matrix = InputMatrix()
        print('Do you want to save this route?(Right Arrow - Yes\Left Arrow - No)')
        choice = InputChoice()
        if True == choice:
            print('Name of the route: ',end = ' ')
            LoadToFile(matrix,vertices,input())
        CreateNewBranch(matrix,0,bestpath)