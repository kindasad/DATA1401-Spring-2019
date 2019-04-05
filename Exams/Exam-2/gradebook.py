import numpy as np
import math

# Create some virtual classes
class base:
    __name=""
    
    def __init__(self,name):
        self.__name=name

    def name(self):
        return self.__name

class data(base):
    def __init__(self,name):
        base.__init__(self,name)
        
class alg(base):
    def __init__(self,name):
        base.__init__(self,name)

class grade(data):
    __value=0
    __numerical=True
    __gradebook_name=str()
    __letter_grades=["F-","F","F+","D-","D","D+","C-","C","C+","B-","B","B+","A-","A","A+"]
    
    def __init__(self,name,numerical=True,value=None):
        if value:
            if isinstance(value,(int,float)):
                self.__numerical=True
            elif isinstance(value,str):
                self.__numerical=False
            self.set(value)
        else:            
            self.__numerical=numerical
        self.__gradebook_name=name
        data.__init__(self,name+" Grade Algorithm")        

    def set(self,value):
        if isinstance(value,(int,float)) and self.__numerical:
            self.__value=value
        elif isinstance(value,str) and not self.__numerical:
            if value in self.__letter_grades:
                self.__value=value
        else:
            print self.name()+" Error: Bad Grade."
            raise Exception
    
    def value(self):
        return self.__value
    
    def numerical(self):
        return self.__numerical
    
    def gradebook_name(self):
        return self.__gradebook_name
    
    def __str__(self):
        return self.__gradebook_name+": "+str(self.__value)

class student(data):
    __id_number=0
    __grades=dict()
    
    def __init__(self,first_name, last_name,id_number):
        self.__id_number=id_number
        self.__grades=dict()
        data.__init__(self,first_name+" "+last_name+" Student Data")

    def add_grade(self,a_grade,overwrite=False,**kwargs):
        if overwrite or not a_grade.gradebook_name() in self.__grades:
            self.__grades[a_grade.gradebook_name()]=a_grade
        else:
            print self.name()+" Error Adding Grade "+a_grade.name()+". Grade already exists."
            raise Exception

    def id_number(self):
        return self.__id_number
    
    def __getitem__(self,key):
        return self.__grades[key]
    
    def print_grades(self):
        for grade in self.__grades:
            print self.__grades[grade]
    

class calculator(alg):    
    def __init__(self,name):
        alg.__init__(self,name)

    def apply(self,a_grade_book):
        raise NotImplementedError

class grade_book(data):
    # New member class to hold arbitrary data associated with the class

    __data=dict()
    __students=dict()
    
    def __init__(self,name):
        data.__init__(self,name+" Course Grade Book")
        self.__students=dict()
        self.__data=dict()
        
    # New method to access data
    def __getitem__(self,key):
        return self.__data[key]
            
    # New method to add data
    def __setitem__(self, key, value):
        self.__data[key] = value
        
    def add_student(self,a_student):
        self.__students[a_student.id_number()]=a_student

    # New method to allow iterating over students
    def get_students(self):
        return self.__students
    
    def assign_grade(self,key,a_grade):
        the_student=None
        try:
            the_student=self.__students[key]
        except:
            for id in self.__students:
                if key == self.__students[id].name():
                    the_student=self.__students[id]
                    break
        if the_student:
            the_student.add_grade(a_grade)
        else:
            print self.name()+" Error: Did not find student."
            
    def apply_calculator(self,a_calculator,**kwargs):
        a_calculator.apply(self,**kwargs)
        
    def print_data(self):
        for k,v in self.__data.iteritems():
            print k,":",v
            
    def get_data(self,key=None):
        a_data=dict()
        for k,v in self.__data.iteritems():
            if key:
                if key in k:
                    a_data[k]=v
            else:
                a_data[k]=v

        return a_data
            
    def print_grades(self,grade_name):
        if isinstance(grade_name,str):
            grade_names=list()
            grade_names.append(grade_name)
        else:
            grade_names=grade_name
                      
        for k,a_student in self.__students.iteritems():
            print a_student.name(),
            for a_grade_name in grade_names:
                print a_student[a_grade_name],
            print
        
        
    
class uncurved_letter_grade_percent(calculator):
    __grades_definition=[ (.97,"A+"),
                          (.93,"A"),
                          (.9,"A-"),
                          (.87,"B+"),
                          (.83,"B"),
                          (.8,"B-"),
                          (.77,"C+"),
                          (.73,"C"),
                          (.7,"C-"),
                          (.67,"C+"),
                          (.63,"C"),
                          (.6,"C-"),
                          (.57,"F+"),
                          (.53,"F"),
                          (0.,"F-")]
    __max_grade=100.
    __grade_name=str()
    
    def __init__(self,grade_name,max_grade=100.):
        self.__max_grade=max_grade
        self.__grade_name=grade_name
        calculator.__init__(self,
                                  "Uncurved Percent Based Grade Calculator "+self.__grade_name+" Max="+str(self.__max_grade))
        
    def apply(self,a_grade_book,grade_name=None,**kwargs):
        if grade_name:
            pass
        else:
            grade_name=self.__grade_name
              
        for k,a_student in a_grade_book.get_students().iteritems():
            a_grade=a_student[grade_name]

            if not a_grade.numerical():
                print self.name()+ " Error: Did not get a numerical grade as input."
                raise Exception
    
            percent=a_grade.value()/self.__max_grade
        
            for i,v in enumerate(self.__grades_definition):
                #print percent, i, v
                if percent>=v[0]:
                    break
                            
            a_student.add_grade(grade(grade_name+" Letter",value=self.__grades_definition[i][1]),**kwargs)
            
class mean_std_calculator(calculator):
    def __init__(self,grade_name,cut_off=None):
        self.__grade_name=grade_name
        self.__cut_off=cut_off
        calculator.__init__(self,"Mean and Standard Deviation Calculator")
        
    def apply(self,a_grade_book,grade_name=None,cut_off=None,**kwargs):
        if grade_name:
            pass
        else:
            grade_name=self.__grade_name
            
        if cut_off:
            pass
        else:
            cut_off=self.__cut_off
                    
        grades=list()
        for k,a_student in a_grade_book.get_students().iteritems():
            a_grade_val=a_student[grade_name].value()
            if cut_off:
                if a_grade_val>cut_off:
                    grades.append(a_student[grade_name].value())
            else:
                grades.append(a_student[grade_name].value())
        
        a_grade_book[grade_name+" Mean"] = np.mean(grades)
        a_grade_book[grade_name+" STD"] = math.sqrt(np.var(grades))
        a_grade_book[grade_name+" Max"] = max(grades)
        a_grade_book[grade_name+" Min"] = min(grades)

class grade_summer(calculator):
    def __init__(self,prefix,n=None):
        self.__prefix=prefix
        self.__n=n
        calculator.__init__(self,"Sum Grades")
        
    def apply(self,a_grade_book,**kwargs):
        first=True
        
        for k,a_student in a_grade_book.get_students().iteritems():
            if first:
                first=False                
                if self.__n:
                    labels=[self.__prefix+str(x) for x in range(1,self.__n)]
                else:
                    labels=list()
                    for i in range(1,1000):
                        label=self.__prefix+str(i)
                        try:
                            a_grade=a_student[label]
                            labels.append(label)
                        except:
                            break                

            grade_sum=0.
            for label in labels:
                grade_sum+=a_student[label].value()

            a_student.add_grade(grade(self.__prefix+"sum",value=grade_sum),**kwargs)

class curved_letter_grade(calculator):
    __grades_definition=[ (.97,"A+"),
                          (.93,"A"),
                          (.9,"A-"),
                          (.87,"B+"),
                          (.83,"B"),
                          (.8,"B-"),
                          (.77,"C+"),
                          (.73,"C"),
                          (.7,"C-"),
                          (.67,"C+"),
                          (.63,"C"),
                          (.6,"C-"),
                          (.57,"F+"),
                          (.53,"F"),
                          (0.,"F-")]
    __max_grade=100.
    __grade_name=str()
    
    def __init__(self,grade_name,mean,std,max_grade=100.):
        self.__max_grade=max_grade
        self.__mean=mean
        self.__std=std
        self.__grade_name=grade_name
        calculator.__init__(self,
                              "Curved Percent Based Grade Calculator "+self.__grade_name+ \
                              " Mean="+str(self.__mean)+\
                              " STD="+str(self.__std)+\
                              " Max="+str(self.__max_grade))


    def apply(self,a_grade_book,grade_name=None,**kwargs):
        if grade_name:
            pass
        else:
            grade_name=self.__grade_name

        for k,a_student in a_grade_book.get_students().iteritems():
            a_grade=a_student[grade_name]

            if not a_grade.numerical():
                print self.name()+ " Error: Did not get a numerical grade as input."
                raise Exception

            # Rescale the grade
            percent=a_grade.value()/self.__max_grade
            shift_to_zero=percent-(self.__mean/self.__max_grade)
            scale_std=0.1*shift_to_zero/(self.__std/self.__max_grade)
            scaled_percent=scale_std+0.8

            for i,v in enumerate(self.__grades_definition):
                #print percent, i, v
                if scaled_percent>=v[0]:
                    break
                            
            a_student.add_grade(grade(grade_name+" Letter",value=self.__grades_definition[i][1]),**kwargs)
            
