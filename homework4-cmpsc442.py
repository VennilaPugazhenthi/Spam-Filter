############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Vennila Pugazhenthi"

############################################################
# Imports
from email.message import EmailMessage
import email
import math
import glob
import operator
############################################################

# Include your imports here, if any are used.

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    with open(email_path) as ep:
        try:
            message= email.message_from_file(ep)
        except:
            return []
        #print(email_path)
        message_body= email.iterators.body_line_iterator(message)
        new_list=[]
        while True:
            try:
                line=next(message_body)
                token=str(line).split()
                new_list.extend(token)
            except StopIteration:
                break
        return new_list

        #message_body=message.get_body()
        #print(message_body)
def log_probs(email_paths, smoothing):
    thisdict={}
    result={}
    total=0
    for x in email_paths:
        email_list=load_tokens(x)
        for y in email_list:
            if y in thisdict:
                thisdict[y]+=1
                total+=1
            else:
                thisdict[y]=1
                total+=1
    v = len(thisdict)
    den = total + smoothing * (v + 1)
    thisdict["<UNK>"]=smoothing/den

    for w,count in thisdict.items():
        num=count+smoothing
        frc=num/den
        result[w]=math.log(frc)

    return result
    #print(thisdict)





class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        self.spam_dir=spam_dir
        self.ham_dir=ham_dir
        self.smoothing=smoothing

        spam_files= glob.glob(spam_dir+"/*")
        spam_dict=log_probs(spam_files,smoothing)
        #self.spam_dir=spam_dir

        ham_files=glob.glob(ham_dir+"/*")
        ham_dict= log_probs(ham_files,smoothing)
        self.spam_dict=spam_dict
        self.ham_dict=ham_dict

        spam_files_len= len(spam_files)
        ham_files_len= len(ham_files)
        p_spam= spam_files_len/(ham_files_len+spam_files_len)
        p_not_spam= 1-p_spam
        self.p_spam=p_spam
        self.p_not_spam=p_not_spam
    
    def is_spam(self, email_path):
        pi= 0
        file_tokens=load_tokens(email_path)
        for x in file_tokens:
            if x not in self.spam_dict:
                x="<UNK>"
            pi+=self.spam_dict[x]
        pi2=0
        for y in file_tokens:
            if y not in self.ham_dict:
                y="<UNK>"
            pi2+=self.ham_dict[y]

        spam= self.p_spam * pi
        not_spam = self.p_not_spam * pi2
        if(spam>not_spam):
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        dict={}
        for w,spam in self.spam_dict.items():
            if w in self.ham_dict:
                not_spam=self.ham_dict[w]
                anti_not_spam= math.exp(not_spam)
                anti_spam=math.exp(spam)
                p_w= (anti_spam*self.p_spam)+(anti_not_spam*self.p_not_spam)
                indictive_value= math.log(anti_spam/p_w)
                dict[w]=indictive_value

        sorted_d= sorted(dict.items(),key=operator.itemgetter(1),reverse=True)
        #print(sorted_d)
        result=[]
        for x in range(n):
            result.append(sorted_d[x][0])
        return result



    def most_indicative_ham(self, n):
        dict={}
        for w,spam in self.spam_dict.items():
            if w in self.ham_dict:
                not_spam=self.ham_dict[w]
                anti_not_spam= math.exp(not_spam)
                anti_spam=math.exp(spam)
                p_w= (anti_spam*self.p_spam)+(anti_not_spam*self.p_not_spam)
                indictive_value= math.log(anti_not_spam/p_w)
                dict[w]=indictive_value

        sorted_d= sorted(dict.items(),key=operator.itemgetter(1),reverse=True)
        #print(sorted_d)
        result=[]
        for x in range(n):
            result.append(sorted_d[x][0])
        return result





#ham_dir="homework4_data/train/ham/"
#spam_dir="homework4_data/train/spam/"
#print(load_tokens(ham_dir+"ham1")[200:204])
#print(load_tokens(ham_dir+"ham2")[110:114])
#print(load_tokens(spam_dir+"spam1")[1:5])
#print(load_tokens(spam_dir+"spam2")[:4])
#print(sol.n)
#path=["homework4_data/train/ham/ham%d" % i for i in range(1,11)]
#p=log_probs(path,1e-5)
#print(p["the"])
#print(p["line"])
#path2=["homework4_data/train/spam/spam%d" % i for i in range(1,11)]
#p2=log_probs(path2,1e-5)
#print(p2["Credit"])

sf=SpamFilter("homework4_data/train/spam","homework4_data/train/ham",1e-5)
#print(sf.most_indicative_ham(5))

print(sf.is_spam("homework4_data/dev/ham/dev2"))
############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
I spent 5 hrs in this homework.
"""

feedback_question_2 = """
I stumbled in the last part where finding p(w) was challenging.
"""

feedback_question_3 = """
I would like the questions to be more detailed and clear cause I struggled understanding the question most 
of the time
"""
