import uuid 
import threading


'''
function to create a unique 12 character code
'''
def generate_ref_code():
    code = str(uuid.uuid4()).replace("-", "")[:12]
    return code


'''
class to create a new thread to send an email while 
while the server is responding to other requests
'''
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)