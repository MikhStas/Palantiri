import socket
import threading
import os
import json


def metrics_handler(conn, addr):
    ip_str = addr[0].replace('.','_')
    work_dir = '/dev/shm/' + ip_str

    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
        print("Directory", work_dir, "created")

    with conn:
        while True:
            data = conn.recv(1024)

            if not data:
                break

            print("Data received")
            print(data.decode('utf-8'))
            metrics = json.loads(data.decode('utf-8'))
            for name, value in metrics.items():
                if name == 'cores':
                    core_number = len(value)
                    for i in range(core_number):
                        basic_path = work_dir + '/' + 'core' + str(i)
                        freq_path = basic_path + 'freq'
                        util_path = basic_path + 'util'
                        temp_path = basic_path + 'temp'
                        
                        with open(freq_path, 'w') as ouf:
                            ouf.write(str(value[i]['freq']))

                        with open(util_path, 'w') as ouf:
                            ouf.write(str(value[i]['util']))

                        with open(temp_path, 'w') as ouf:
                            ouf.write(str(value[i]['temp']))
                elif name == 'proc_by_cpu':
                    i = 1
                    for process in value:
                        name_path = work_dir + '/proc' + str(i)
                        with open(name_path, 'w') as ouf:
                            ouf.write(process['name'])
                            
                        value_path = work_dir + '/util' + str(i)
                        with open(value_path, 'w') as ouf:
                            ouf.write(str(process['cpu_percent']))
                        i += 1     
                else:
                    path = work_dir + '/' + name
                    with open(path, 'w') as ouf:
                        ouf.write(str(value))                

with socket.socket() as sock:
    sock.bind(('', 10001))
    sock.listen()
    while True:
        conn, addr = sock.accept()
        th = threading.Thread(target=metrics_handler, args=(conn, addr))
        th.start()
