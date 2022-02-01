import json

def create_new_json(json_path: str):
    try:
        library = open(json_path, 'w+')
        return library
    except:
        ret = ReturnToPreventErrors(('FATAL ERROR CANNOT '
                                     'CREATE JSON DIR ' + json_path))
        logging(ret.text)
        return ret


class ReturnToPreventErrors:
    text = ''

    def __init__(self, txt):
        self.text = txt



def read_json(json_path: str, line_num=-1):
    library = None
    try:
        library = open(json_path, 'r')
    except:
        log = open('log', 'a')
        forret = ReturnToPreventErrors('ERROR CAN\'T FIND ' + json_path)
        logging(forret.text)
        return forret
    if line_num > -1:
        line = ''
        for cur_num in range(0, line_num):
            line = library.readline()
        return json.loads(line)
    if line_num == -1:
        while True:
            line = library.readline()
            if line=='':
                return json.loads(line)


def iterate_json(json_path:str):
    library=None
    try:
        library=open(json_path, 'r')
    except:
        error=ReturnToPreventErrors("CAN\' FIND JSON LIB WITH ID "+json_path)
        logging(error.text)
    while True:
        cur_json=json.loads(library.readline())
        if(cur_json==''):
            break
        else:
            yield cur_json


def find_by_name(json_path, username: str):
    current_json = ''
    with open(json_path, 'r') as library:
        current_json = json.loads(library.readline())
        if username in current_json['u1']:
            return [username, 'SENDER', current_json]
        elif username in current_json['u2']:
            return [username, 'RECEIVER', current_json]


def logging(logmsg):
    try:
        open('log', 'a').write(logmsg + "\n")
        return 1
    except:
        return 0


def json_write(u1, u2, json_path, time, message: str):
    library = create_new_json(json_path)
    if type(library) != ReturnToPreventErrors:
        json_2_write = {
            'u1': u1,
            'u2': u2,
            'message': message,
            'time': time
        }
        logging("SUCCESS WITH APPENDING MESSAGE")
        library.write(json_2_write)
        return 1
    else:
        return library

