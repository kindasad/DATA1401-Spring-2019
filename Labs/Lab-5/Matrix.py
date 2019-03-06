class Matrix:
    
    def __init__(self,M):
            
            
        self.M = M
        
    def constant(self,c):
        self.M= [[float(c)for i in range(self.m)]  for i in range(self.n)]
        return self.M
    
    def zeros(self):
        return [[0.0 for i in range(self.m)]  for i in range(self.n)]
    
    def ones(self):
        return [[1.0 for i in range(self.m)] for i in range(self.n)]
    
    def eye(self):
        Identity=[[0.0 for i in range(self.n)] for i in range(self.n)]
        for i in range(0,self.n):
                Identity[i][i]=1.0
        return Identity
    
     
    def Shape(self,N=list()):
        FindingRow=True
        FindingColumn=True
        shape=0
        n=0
        m=0
        ######## iterating n and m till i find number of rows and colums. I know it will go out of index so i add a try and except###
        if N ==[]:
            try:
                while FindingRow==True:
                    try:
                        while FindingColumn==True:
                            self.M[0][m]
                            m+=1
                    except IndexError:
                        FindingColumn=False
                    self.M[n][0]
                    n+=1
            except IndexError:
                FindingRow=False
            size=(n,)+(m,)  
        else:
            try:
                while FindingRow==True:
                    try:
                        while FindingColumn==True:
                            N[0][m]
                            m+=1
                    except IndexError:
                        FindingColumn=False
                    N[n][0]
                    n+=1
            except IndexError:
                FindingRow=False
            size=(n,)+(m,)
            return size
        ######### Now testing that the matrix was made correctly ########
        
        for i in range(0,n):
            if len(self.M[i]) !=m:
                return False
        return size

    def row(self,n):
        return self.M[n]
    
    def column(self,n):
        self.Shape(self.M)
        hold=[]
        for i in range(0,self.Shape(self.M)):
            hold.append(self.M[i][n])
        return hold
    
    def block(self,n_0,n_1,m_0,m_1):
        hold=[[0 for i in range (n_1-n_0+1)]  for j in range(m_1-m_0+1)]
        x=0
        y=0
        try:
            for m in range(m_0,m_1+1):
                for n in range(n_0,n_1+1):
                    hold[x][y]=self.M[m][n]
                    y+=1
                y=0
                x+=1
        except IndexError:
            return "failed"
        return hold
    
    
    
    
    def transpose(self):
        Size=self.Shape(self.M)
        
        if Size==False:
            return "fail"
        hold=[[0] * Size[0] for i in range(Size[1])]
        for i in range(Size[0]):
            for j in range(Size[1]):
                hold[j][i]=self.M[i][j]
        
        return hold
    
    
    def __mul__(self,c):
        Size=self.Shape(self.M)
        P=[[0 for i in range (Size[0])] for j in range(Size[1])]
        if Size==False:
            return "failed"
        for i in range(Size[0]):
            for j in range(Size[1]):
                P[i][j]=self.M[i][j]*c
        return P
    
    def __add__(self,N):
        if len(self.M)!=len(N) or len(self.M[0])!=len(N[0]):
            return False
        n=len(self.M)
        hold=[[0 for i in range(n)] for j in range(n)]

        for i in range (0,len(self.M)):
            for j in range(0,len(self.M)):
                hold[i][j]=self.M[i][j]+N[i][j]
        return hold

    def __sub__(self,N):
        N=self.__mul__(-1)
        P=self.__add__(N)        
        return P
    
    def elementmult(self,N):
        n=len(self.M)
        m=len(self.M[0])
        out=[[0 for i in range(n)] for j in range(n)]

        for i in range (0,n):
            for j in range(0,m):
                out[i][j]=M[i][j]*N[i][j]
        return out



    def __matmult__(self,N):
        Size_M=self.Shape(self.M)
        Size_N=self.Shape(N)
        K=[[0] * Size_N[1] for i in range(Size_M[0])]
        x=0
        Sum=0
        if Size_M[1]!=Size_N[0]:
               return "failed"
        P=list(self.transpose())
        for k in range(Size_M[0]):
                for j in range(Size_N[1]):
                    for i in range(Size_N[0]):
                        sum1=P[i][k]*N[i][j]
                        Sum= Sum+sum1 
                    K[k][j]= Sum
                    Sum=0
        
        return K
    
    
    
    
    def rand(self,n,m):
        import random
        K=[[0.0 for i in range(m)]   for j in range(n)]
        for i in range (n):
            for j in range (m):
                K[i][j]=random.random()
   
        return K

        
    def compare(M):
        a=len(M)
        for i in range(0,a):
             if abs(M[i][i]-1)>0.1:
                    return False
        return True
    def copy(M):
        n=len(M)
        out=[[0 for i in range(n)] for j in range(n)]
        for i in range (0,n):
            for j in range (0,n):
                out[i][j]=M[i][j]
        return out
    def inv(self):
     
        A=self.copy(M)
     
     
     
     
        p=0
        d=1
        while True: 
                if p>=len(M):
                    break
                if M[p][p]==0:
                    break
                d=d*M[p][p]
             
                    
                for i in range (0,len(M)):
                    if i!=p:
                        M[i][p]=-M[i][p]/M[p][p]
                   
                for i in range (0,len(M)):
                    for j in range (0,len(M)):
                        if i!=p and j!=p:
                            M[i][j]=M[i][j]+M[p][j]*M[i][p]
                for j in range (0,len(M)):
                    if j!=p:
                        M[p][j]=M[p][j]/M[p][p]            
                M[p][p]=1.0/M[p][p]
            
                p=p+1
                if self.compare(matmult(M,A)):   
                    print 'yes'
                    return M
     
    
        print "nope"
        return False



class Vector(Matrix):
    def __init__(self,A=list(),B=list()):
        self.A=A
        self.B=B
        
    def dot(self):
        Size_A=len(self.A)
        Size_B=len(self.B)
         
        if Size_A!=Size_B:
            "failed"
        return sum(map(lambda x,y:x*y, self.A,self.B))
        
    def outer(self):
        Size_A=len(self.A)
        Size_B=len(self.B)
        hold=[[0] * len(self.A) for i in range(len(self.A))]
        if Size_A!=Size_B:
            return "fail"
        for i in range(Size_A):
                for j in range(Size_A):
                    hold[i][j]=self.A[i]*self.B[j]
        return hold
     

        
    
    def norm(self,A,i):
        import math
        hold=0
         
        for j in range(0,len(A)):
            A[j]=abs(A[j])
        if i==0:
            for j in range(0,len(A)):
                if [j]>hold:
                    hold=A[j]
            return hold


        else:
            for j in range(0,len(A)):
                z=A[j]**i
                hold=hold+z
            hold=float(hold)**(1.0/i)
            return hold