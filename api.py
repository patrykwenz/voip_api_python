from flask import Flask, jsonify
import os
import random

app = Flask(__name__)

SIP_CONF_FILE = os.path.abspath("/etc/asterisk/sip.conf")
SIP_EXTEN_FILE = os.path.abspath("/etc/asterisk/extensions.conf")
RELOAD_CONF_COMMAND = "sudo asterisk -rx \"reload\""


def run_command(com=RELOAD_CONF_COMMAND):
    os.system(com)


"""
{user_name : <name>,
    status: <status>}
"""
USERS = []
DIAL_NUMBERS = []
PAIRS = {}


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
    def delete_user_from_sip_conf(name, file=SIP_CONF_FILE):
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
        run_command()
        return new_data

    @staticmethod
    def delete_user_from_exten_conf(name, file=SIP_EXTEN_FILE):
        with open(file) as f:
            data = f.readlines()

        new_data = None
        for index, line in enumerate(data):
            if f"sip/{name}" in line:
                new_data = data[:index - 1] + data[int(index + 2):]
                break
        new_data = "".join(new_data)

        with open(file, 'w') as f:
            f.write(new_data)
        run_command()
        return new_data

    @staticmethod
    def create_exten(number, user):
        exten_string = f"\nexten => {number}, 1, NoOp(calling {user})\n" \
                       f"exten => {number}, 2, Dial(sip/{user})\n" \
                       f"exten => {number}. 3. HangUp\n"
        return exten_string

    @staticmethod
    def add_user_to_exten_conf(user_name):
        n = len(DIAL_NUMBERS)
        number = "111" + f"{n:03}"
        exten_string_to_append = api_logic.create_exten(str(user_name), number)
        api_logic.append_to_file(exten_string_to_append, filename=SIP_EXTEN_FILE)
        api_logic.add_dial_number(user_name, number)
        run_command()
        return exten_string_to_append

    @staticmethod
    def add_dial_number(user_name, number):
        DIAL_NUMBERS.append({"user_name": user_name,
                             "exten": str(number)})

    @staticmethod
    def add_user_to_sip_conf(user_name):
        sip_string_to_append = api_logic.create_user(str(user_name))
        api_logic.append_to_file(sip_string_to_append)
        api_logic.add_user(user_name)
        run_command()
        return sip_string_to_append

    @staticmethod
    def set_user_flag(user_name, flag):
        for user in USERS:
            if user["user_name"] == user_name:
                user["status"] = flag
                break

    @staticmethod
    def add_user(user_name):
        USERS.append({"user_name": str(user_name), "status": 0})

    @staticmethod
    def pair_users_to_chat():
        global PAIRS

        def _get_users_with_flag(flag):
            users_to_return = []
            for user in USERS:
                if user["status"] == flag:
                    users_to_return.append(user["user_name"])
            return users_to_return

        rdy_users = _get_users_with_flag(1)

        pairs = dict()

        while len(rdy_users) > 1:
            r1 = random.randrange(0, len(rdy_users))
            caller = rdy_users.pop(r1)
            api_logic.set_user_flag(caller, 2)

            r2 = random.randrange(0, len(rdy_users))
            receiver = rdy_users.pop(r2)
            api_logic.set_user_flag(receiver, 2)

            pairs[caller] = receiver
        PAIRS = pairs
        return pairs

    @staticmethod
    def get_dial_number(user_name):
        for data in DIAL_NUMBERS:
            if data["user_name"] == user_name:
                return data["exten"]

    @staticmethod
    def delete_from_list_dict(structure, user_name):
        for i, data in enumerate(structure):
            if data["user_name"] == str(user_name):
                del structure[i]


@app.route('/')
def hello():
    return "VOIP Rest Service"


@app.route('/add-user-to-sip-exten-conf/<string:user_name>', methods=['POST'])
def add_user_to_sip_conf(user_name):
    sip_string_to_append = api_logic.add_user_to_sip_conf(user_name)
    exten_string_to_append = api_logic.add_user_to_exten_conf(user_name)
    return jsonify({"User added": "Exten Created"}), 200


@app.route('/sip-file-lookup', methods=['GET'])
def sip_file_lookup():
    data = api_logic.read_conf_file()
    return data, 200


@app.route('/user-status', methods=['GET'])
def status():
    return jsonify(USERS), 200


@app.route('/pair-status', methods=['GET'])
def status2():
    return jsonify(PAIRS), 200


@app.route('/update-status-rdy/<string:user_name>', methods=['PUT'])
def update_user_status_rdy(user_name):
    api_logic.set_user_flag(str(user_name), 1)
    return jsonify({"Status changed": "READY"}), 200


@app.route('/update-status-busy/<string:user_name>', methods=['PUT'])
def update_user_status_busy(user_name):
    api_logic.set_user_flag(str(user_name), 0)
    return jsonify({"Status changed": "BUSY"}), 200


@app.route('/get-peer/<string:user_name>', methods=['GET'])
def get_peer(user_name):
    c_flag = list(PAIRS.keys()) + list(PAIRS.values())

    def _get_users_with_flag(flag):
        users_to_return = []
        for user in USERS:
            if user["status"] == flag:
                users_to_return.append(user["user_name"])
        return len(users_to_return)

    rdy_user_number = _get_users_with_flag(1)

    if user_name in c_flag:
        number = str(api_logic.get_dial_number(PAIRS[str(user_name)]))
        return {"call": str(PAIRS[str(user_name)]),
                "exten": number}, 200
    if rdy_user_number < 2:
        return jsonify({"Wait some more 1": "soon someone will call"}), 200

    if user_name not in c_flag:
        pairs = api_logic.pair_users_to_chat()
        check = list(pairs.keys()) + list(pairs.values())
        if user_name not in check:
            return jsonify({"Wait some more 2": "soon someone will call"}), 200
        if user_name in pairs.keys():
            number = api_logic.get_dial_number(pairs[str(user_name)])
            return jsonify({"call": pairs[str(user_name)],
                            "exten": str(number)}), 200
        if user_name in pairs.values():
            return jsonify({"receive call": "soon your friend will call"}), 200


@app.route('/delete-user/<string:user_name>', methods=['DELETE'])
def delete_user(user_name):
    # Delete dial
    # delete conf
    # delete from user status
    api_logic.delete_user_from_exten_conf(user_name)
    api_logic.delete_user_from_sip_conf(user_name)
    api_logic.delete_from_list_dict(USERS, user_name)

    c1 = list(PAIRS.keys()) + list(PAIRS.values())
    if user_name in c1:
        api_logic.delete_from_list_dict(PAIRS, user_name)

    return jsonify({"Deleted": user_name}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')
