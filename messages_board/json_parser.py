import json
import os
BASE_JSONS='jsons/'

def create_new_json(json_path: str):
    json_path=BASE_JSONS+json_path
    try:
        if not os.path.exists(BASE_JSONS):
            os.mkdir(BASE_JSONS)
        library = open(json_path, 'a+')
        logging('CREATED NEW JSON LIB AT '+json_path)
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
    json_path=BASE_JSONS+json_path
    try:
        library = open(json_path, 'r')
    except:
        log = open(BASE_JSONS+'log', 'a')
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
    json_path = BASE_JSONS + json_path
    try:
        library=open(json_path, 'r+')
    except:
        error=ReturnToPreventErrors("CAN\' FIND JSON LIB WITH ID "+json_path)
        logging(error.text)
        print(error.text)
        return error
    while True:
        try:
            cur_json=json.loads(library.readline())
            if (cur_json == ''):
                break
            else:
                yield cur_json
        except:
            error=ReturnToPreventErrors("JSON {} LIB IS EMPTY".format(json_path))
            logging(error.text)
            return error



def find_by_name(json_path, username: str):
    current_json = ''
    json_path = BASE_JSONS + json_path
    with open(json_path, 'r') as library:
        current_json = json.loads(library.readline())
        if username in current_json['u1']:
            return [username, 'SENDER', current_json]
        elif username in current_json['u2']:
            return [username, 'RECEIVER', current_json]


def logging(logmsg):
    try:
        open(BASE_JSONS+'log', 'a').write(logmsg + "\n")
        return 1
    except:
        return 0


def json_write(u1, u2, json_path, time, message: str):
    json_path = BASE_JSONS + json_path
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

