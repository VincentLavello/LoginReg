import re

class PWDChecker:
    def __init__(self):
        pass   
    def IsPasswordValid( pwd):
        while True:   
            if (len(pwd)<8): 
                flag = 0
                break
            elif not re.search("[a-z]", pwd): 
                flag = 0
                break
            elif not re.search("[A-Z]", pwd): 
                flag = 0
                break
            elif not re.search("[0-9]", pwd): 
                flag = 0
                break
            elif not re.search("[!_@$]", pwd): 
                flag = 0
                break
            # elif re.search("\s", pwd): 
            #     flag = 0
            #     break
            else: 
                flag = 1
                print("Valid pwd") 
                break
        return flag
    def isUserNameValid(strUserName):
        lower = any(lc.islower() for lc in strUserName)
        upper = any(uc.isupper() for uc in strUserName)
        digit = any(d.isdigit() for d in strUserName)
        length = len(strUserName)

        return  (bool) ((lower and upper and digit) and (length >= 6))
def Passwords():
    return PWDChecker
        
