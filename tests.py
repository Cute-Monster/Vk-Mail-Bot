from datetime import datetime
import os
if __name__ == '__main__':

    # test = {'test':1,
    #         'B':2}
    # test.update([('A', 3)])
    # test.update([('A', 4)])
    # print(datetime.now().minute)
    # print(datetime.now().minute*60)
    # print(datetime.now().second)
    # print(3600-(datetime.now().minute*60))

    # send_to_dev_only = bool(int(input("Send to dev:\n"
    #                                   "\t1 -> Yes\n"
    #                                   "\t0 -> No\n"
    #                                   "\t---> ")))
    file = open("Logs/test.txt", "a")
    priority = 3
    if file.closed:
        print("closed")
    else:
        print("Opened")
    file.close()
    if file.closed:
        print("closed")
    else:
        print("Opened")

    print(os.path.getsize("venv.tar.xz")/float(1 << 20))
    # testing = []
    # testing.append((1, 3))
    # testing.append((5, 7))
    if priority is 4 or 3:
        print(priority)
    # print(testing)
    # for first, last in enumerate(testing):
    #     print(f" : first -> {first} : last -> {last}")
    # print(send_to_dev_only)
    # for value in test:
    #     print(test.get(value))
    # print("Hi", test.__len__())
