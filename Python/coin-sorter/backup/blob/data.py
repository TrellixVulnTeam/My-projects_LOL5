import multiprocessing
import os
import signal

import coins_detect

def abort():
    f = open('RUNNING.txt', 'r')
    process = f.readline()
    process = filter(None, process.split(","))

    for p in process:
        os.kill(int(p), signal.SIGQUIT)

    f.close()
    os.remove('RUNNING.txt')
    print(abort)

def main():
    if not os.path.isfile("RUNNING.txt"):
        f = open('RUNNING.txt', 'w+')
        processes = []
        
        processes.append(multiprocessing.Process(target=coins_detect.main))
        processes[-1].start()

        for p in processes:
            f.write(str(p.pid))
            f.write(",")
        f.close()


    else:
        print ("Processes already operational.")
        # if form.getvalue('offline') == "True":
        abort()
main()