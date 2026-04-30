import random


def generate_user_code() -> str:
    code = ''
 
    for number in range(6):
        random_number = random.randint(0, 9)
        code += str(random_number) 
        
    return code


    

