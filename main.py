from classes import *
import json
import pandas as pd


def create_professor_list(path_to_csv):
    '''
    Abstracted away, likely loading a Json, csv, or something
    '''
    df = pd.read_csv(path_to_csv)

    professor_list = []
    for ii,row in df.iterrows():
        
        prof = Professor(row["Professor"],row.drop("Professor").to_dict())
        professor_list.append(prof)
    return professor_list

def create_student_list(path_to_csv):
    '''
    Abstracted away, likely loading a Json, csv, or something
    '''
    df = pd.read_csv(path_to_csv)

    student_list = []
    for ii,row in df.iterrows():
        row = row.replace('','NaN')
        row = row.dropna()
        student = Student(row["Student"],list(row.drop("Student").to_dict().values()))
        student_list.append(student)

    return student_list

professor_sort_key = lambda x: x.availability_metric


# RunTime Parameters
num_tb = 5 
k_max = 52 # Group Size

if __name__ == "__main__":
    # Create Data
    professor_list = create_professor_list("week2_professors.csv")
    student_list = create_student_list("week2_students.csv")
    tb_list = [TimeBlock(f"Meeting {id+1}",professor_list,student_list) for id in range(5)]

    # Main run

    professor_list = list(sorted(professor_list,key=professor_sort_key)) # Priortize professors with lower availability (NOTE: May need to add a weighting of overlapped timeslots, too)

    for professor in professor_list:
        for tb in tb_list:
            subset_students = [student for student in student_list if 
                student.needs_to_meet_professor(professor) and not tb.student_dict[str(student)]] 

            if not professor.available(tb):
                continue
            
            grabbed_students = subset_students[0:k_max]
            tb.set_professor_student_match(professor,grabbed_students)
            for student in grabbed_students:
                student.professor_dict[str(professor)] = tb.id # Can use this to check that students have met every professor at end
            
    for student in student_list:
        print(student.summary())
    
    # Make final csv
    df_arr = []
    for tb in tb_list:
        df_arr.append(pd.DataFrame(tb.student_dict,index=[tb.id]))
    
    df_final = pd.concat(df_arr)
    df_final = df_final.T 
    df_final.replace(False,"Available",inplace=True)
    df_final.to_csv(f"Week2_{k_max}_groups.csv")
