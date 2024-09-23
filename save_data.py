from datetime import datetime

def store_data(id, name):
    current_time = datetime.now()
    time = current_time.time()

    print(id)
    print(name)
    print(time)
    print(current_time.date())
    print(current_time)



def extract_id_and_name(data):
    data = data.split(',')
    return data[0], data[1], data[2]#id, name, graduated (1) or not (0)