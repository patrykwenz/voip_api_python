# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


import os


def create_user(name):
    user_string = f"[{name}] \n" \
                  f"\ttype=friend \n" \
                  f"\tcontext=phones \n" \
                  f"\tallow=ulaw, alaw\n" \
                  f"\tsecret=12345678abcd \n" \
                  f"\thost=dynamic \n"

    return user_string




SIP_CONF_FILE = os.path.abspath("/etc/asterisk/sip.conf")


class api_logic:
    @staticmethod
    def create_user(name):
        user_string = f"[{name}] \n" \
                      f"\ttype=friend \n" \
                      f"\tcontext=phones \n" \
                      f"\tallow=ulaw, alaw\n" \
                      f"\tsecret=12345678abcd \n" \
                      f"\thost=dynamic \n"

        return user_string

    @staticmethod
    def append_to_file(data, filename=SIP_CONF_FILE):
        with open(filename, 'a') as f:
            f.write(data)

    @staticmethod
    def read_conf_file(file=SIP_CONF_FILE):
        with open(file) as f:
            data = f.read()
        return data

    @staticmethod
    def load_file(file=SIP_CONF_FILE):
        with open(file) as f:
            data = f.readlines()
        return data

    @staticmethod
    def delete_user(name, file=SIP_CONF_FILE):
        with open(file) as f:
            data = f.readlines()

        new_data = None
        for index, line in enumerate(data):
            if line.startswith(f"[{name}]"):
                new_data = data[:index] + data[int(index + 6):]
                break
        new_data = "".join(new_data)

        with open(file, 'w') as f:
            f.write(new_data)

        return new_data


USERS = [
    {"user_name": "tom",
     "status": 0},
    {"user_name": "ziom",
     "status": 1},
    {"user_name": "don",
     "status": 1},
    {"user_name": "lon",
     "status": 1}

]


def set_user_flag(user_name, flag):
    for user in USERS:
        if user["user_name"] == user_name:
            user["status"] = flag
            break


def pair_users_to_chat():
    def _get_users_with_flag(flag):
        users_to_return = []
        for user in USERS:
            if user["status"] == flag:
                users_to_return.append(user["user_name"])
        return users_to_return

    rdy_users = _get_users_with_flag(1)

    pairs = dict()
    check_list = []
    while len(rdy_users) > 1:
        r1 = random.randrange(0, len(rdy_users))
        caller = rdy_users.pop(r1)
        set_user_flag(caller, 2)
        check_list.append(caller)

        r2 = random.randrange(0, len(rdy_users))
        receiver = rdy_users.pop(r2)
        set_user_flag(receiver, 2)
        check_list.append(receiver)

        pairs[caller] = receiver
    return pairs, check_list


import random


def create_exten(number, user):
    exten_string = f"\nexten => {number}, 1, NoOp(calling {user})\n" \
                   f"exten => {number}, 2, Dial(sip/{user})\n" \
                   f"exten => {number}. 3. HangUp\n"
    return exten_string


SIP_EXTEN_FILE = os.path.abspath("/etc/asterisk/extensions.conf")


def append_to_file(data, filename=SIP_CONF_FILE):
    with open(filename, 'a') as f:
        f.write(data)


def add_user_to_exten_conf(user_name):
    number = "111" + f"{1:03}"
    exten_string_to_append = create_exten(str(user_name), number)
    append_to_file(exten_string_to_append, filename=SIP_EXTEN_FILE)
    return exten_string_to_append


# Press the green button in the gutter to r
# un the script.
if __name__ == '__main__':
    # file = os.path.abspath("/etc/asterisk/sip.conf")
    #
    # with open(file) as f:
    #     data = f.readlines()
    #
    # for line in data:
    #     print(line)
    #
    # t_s = create_user("testowy")
    # append_to_file(file, t_s)
    #
    #
    # with open(file) as f:
    #     data = f.readlines()
    #
    # for line in data:
    #     print(line)

    # print(len(api_logic.load_file()))
    # l = api_logic.load_file()
    # for line in l:
    #     print(line)

    # print(api_logic.delete_user("kat"))

    # os.system()

    # set_user_flag("tom", 0)
    # set_user_flag("don", 0)

    user_name = "don"
    pairs, check = pair_users_to_chat()
    print(pairs)
    # if user_name not in check:
    #     print("Wait some more")
    # if user_name in pairs.keys():
    #     print({"call": pairs[str(user_name)]})
    # if user_name in pairs.values():
    #     print({"receive call"})

    l = {"a": 323, "B": 123213}

    d = [
        {"user_name": "a",
         "exten": "666666"},

        {"user_name": "b",
         "exten": "7777"},

        {"user_name": "c",
         "exten": "8888"},

    ]
    # file = os.path.abspath("/etc/asterisk/extensions.conf")
    # name = "tom"
    # with open(file) as f:
    #     data = f.readlines()
    #
    # print(data)
    # new_data = None
    # for index, line in enumerate(data):
    #     if f"sip/{name}" in line:
    #         new_data = data[:index - 1] + data[int(index + 2):]
    #         break
    #
    # print(new_data)
    # # new_data = "".join(new_data)
    #
    # with open(file, 'w') as f:
    #     f.write(new_data)
    #
    # print(new_data)

    add_user_to_exten_conf("tom")
# sudo asterisk -rx "reload"
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
