# Defining the needed classes for this to work




class Professor():
    def __init__(self,
        name:str,
        availability_dict:dict,
        ):

        self.name = name
        self.availability_dict = availability_dict # This corresponds with the ids of the TimeBlocks

    def available(self,tb:str):
        tb = str(tb)

        return self.availability_dict[tb]

    @property
    def availability_metric(self):
        '''
        Use their current available timeslots as an availbility metric
        NOTE: May be a better version in the future?
        '''
        count = 0
        for key,val in self.availability_dict.items():
            if val:
                count += 1
        
        return count
                                                                                                                                               
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Student():
    def __init__(self,
        name:str,
        professor_list:list[str]):
        self.name = name
        self._professor_list = professor_list
        self.professor_dict = {str(professor):False for professor in professor_list} # False: Not met, needs to. TimeBlock: Has met Professor

    def needs_to_meet_professor(self,professor:str):
        '''
        Check if the Student needs to meet iwth the professor or doesn't have them listed
        '''
        if str(professor) in self.professor_dict:
            return not self.professor_dict[str(professor)]
        
        return False
    
    def summary(self):
        '''
        Quick string summary per student
        '''
        thresh = len(self.professor_dict)
        count = 0
        failed_prof = ""
        for key,val in self.professor_dict.items():
            if val:
                count += 1
            else:
                failed_prof += key+","
        
        return f"{self.name} met with {count}/{thresh} (Didn't Meet: {failed_prof})({self.professor_dict.items()})"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class TimeBlock():
    '''
    Class holds information for which Professors are available AND which students are available
    '''
    def __init__(self,
        id,
        professor_list:list[Professor],
        student_list:list[Student]
        ):
        self.id = id
        self.professor_dict = {str(professor):professor.available(id) for professor in professor_list}
        self.student_dict = {str(student):False for student in student_list}

    def get_professor_student_count(self,professor):
        count = 0
        for key,item in professor_dict.items():
            if item == professor:
                count += 1
        
        return count

    def set_professor_student_match(self,professor,student_list:list[Student]):
        '''
        Set students to chosen Professor
        '''
        for student in student_list:
            student = str(student)
            self.student_dict[student] = professor

    def __str__(self):
        return self.id

