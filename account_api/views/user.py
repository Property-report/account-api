from flask import request, Blueprint, Response, jsonify, current_app
from account_api.exceptions import ApplicationError

from account_api.models import Report
from account_api.sqs import EmailSqsSender

user = Blueprint('user', __name__)


@user.route("/report", methods=['POST'])
def new_report():
    json_data = request.json
    try:
        result = Report.create_report(json_data)
        return jsonify(result.to_dict())
    except Exception as e:
        print(e)
    raise ApplicationError('something has gone wrong creating a new report', 'UAclient-a001')


@user.route("/report/<report_id>", methods=['PUT'])
def update_report(report_id):
    json_data = request.json
    try:
        report = Report.get_report_by_id(report_id)
        if report:
            report.update(json_data)
            if json_data.get("creation_status", None) == "complete":
                report_details = report.to_dict()
                formatted_address = "{} {} {}".format(
                    report_details.get('house_number', ''),
                    report_details.get('street', ''),
                    report_details.get('postcode', '')
                )
                EmailSqsSender().send_message({
                    "type": "send report",
                    "report_id": report_id,
                    "email": report.email,
                    "formatted address": formatted_address
                })

            return jsonify(report.to_dict())
        else:
            raise ApplicationError('report not found', 'UAclient-a002')
    except Exception as e:
        print(e)
    raise ApplicationError('something has gone wrong updating the report', 'UAclient-a003')


@user.route("/report/<report_id>/report_data", methods=['GET'])
def get_report_data(report_id):
    try:
        report = Report.get_report_by_id(report_id)
        if report:
            return jsonify(report.get_report_data())
        else:
            raise ApplicationError('report not found', 'UAclient-a002')
    except Exception as e:
        print(e)
    raise ApplicationError('something has gone wrong updating the report', 'UAclient-a003')


@user.route("/report/<report_id>", methods=['GET'])
def get_report(report_id):
    try:
        report = Report.get_report_by_id(report_id)
        if report:
            return jsonify(report.to_dict())
        else:
            raise ApplicationError('report not found', 'UAclient-a002')
    except Exception as e:
        print(e)
    raise ApplicationError('something has gone wrong updating the report', 'UAclient-a003')


# @user.route("/get_client_purchase_ref", methods=['GET'])
# def get_client_by_purchase_ref():
#     json_data = request.json

#     users_check = Sql.get_users(json_data)
#     output = []
#     for user in users_check:
#         output.append(user.to_dict())

#     return jsonify(output)


# @user.route("/verify_login", methods=['POST'])
# def verify_login():
#     json_data = request.json

#     if 'email' in json_data.keys() and 'password' in json_data.keys():
#         user = {}
#         user["email"] = json_data["email"]
#         hashed_password = hashlib.sha256(json_data['password'].encode('utf-8')).hexdigest()
#         user["password"] = hashed_password

#         # check if user exists
#         users_check = Sql.get_user(user)
#         if len(users_check) == 1:
#             return jsonify(users_check[0].to_dict())
#         else:
#             raise ApplicationError('no user has been found with this email and password combination', 'u001')
#     else:
#         raise ApplicationError('email or password missing', 'unspecified')


# @user.route("/verify_second_auth", methods=['POST'])
# def verify_second_auth():
#     json_data = request.json

#     if 'email' in json_data.keys() and 'second_code' in json_data.keys() and 'ip_addresses' in json_data.keys():
#         userget = {}
#         userget["second_code"] = json_data["second_code"]
#         userget["email"] = json_data["email"]

#         users_check = Sql.get_user(userget)
#         if len(users_check) != 1:
#             raise ApplicationError('no user has been found with this email and code combination', 'u001')

#         user = users_check[0].to_dict()

#         timestamp = datetime.datetime.now()

#         if timestamp < user['second_code_timestamp'] + timedelta(minutes=10):

#             if user['ip_addresses'] == None or user['ip_addresses'] == []:
#                 userdict = {}
#                 userdict["second_code"] = " "
#                 userdict["ip_addresses"] = [json_data["ip_addresses"]]
#                 update_user = Sql.update_user(user['id'], userdict)

#             else:

#                 new_list = user['ip_addresses']
#                 new_list.append(json_data["ip_addresses"])

#                 userdictlist = {}
#                 userdictlist["second_code"] = " "
#                 userdictlist["ip_addresses"] = ""
#                 update_user = Sql.update_user(user['id'], userdictlist)

#                 userdictlist = {}
#                 userdictlist["second_code"] = " "
#                 userdictlist["ip_addresses"] = new_list

#                 Sql.update_user(user['id'], userdictlist)

#             return jsonify(users_check[0].to_dict())
#         else:
#             raise ApplicationError('Code expired', 'u004')
#     else:
#         raise ApplicationError('email or password missing', 'unspecified')


# @user.route("/second_auth", methods=['POST'])
# def second_auth():
#     json_data = request.json

#     if 'email' in json_data.keys():
#         user = {}
#         user["email"] = json_data["email"]

#         # check if user exists
#         users_check = Sql.get_user(user)
#         if len(users_check) == 1:
#             rand_code = random_with_N_digits(6)

#             second_code_timestamp = datetime.datetime.now()
#             user = users_check[0].to_dict()
#             update_userdict = {}
#             update_userdict['second_code'] = rand_code
#             update_userdict['second_code_timestamp'] = second_code_timestamp

#             update_user = Sql.update_user(user['id'], update_userdict)
#             get_company = get_company_account(user['comp_id'])
#             get_client = get_client_account(user['id'])

#             client = get_client[0]
#             check_dict = {}
#             check_dict['second_name'] = ""
#             if 'second_forename' in client:
#                 check_dict['second_name'] = client["second_forename"]
#             check_dict['name'] = client["forname"]
#             check_dict['email'] = client["email"]
#             check_dict['number'] = client.get("mobile", "")
#             check_dict['second_code'] = rand_code
#             check_dict['company_id'] = client['company_id']
#             check_dict['company'] = get_company[0]["name"]
#             check_dict['contact_name'] = get_company[0]["contact_name"]
#             check_dict['contact_num'] = get_company[0]["contact_num"]
#             check_dict['seen_bool'] = 'unseen'
#             check_dict['director_name'] = get_company[0]["contact_name"]
#             check_dict['colour_hex'] = get_company[0]["colour_hex"]
#             check_dict['owner_name'] = get_company[0]["owner_name"]
#             check_dict['owner_status'] = get_company[0]["owner_status"]
#             names = client["forname"]
#             if client['user_count'] == 'two':
#                 names = "{} and {}".format(client["forname"], client["second_forname"])
#             check_dict['names'] = names
#             check_dict['url'] = get_company[0]['url']
#             print("sending")
#             send_second_auth(check_dict)

#             return jsonify(users_check[0].to_dict())
#         else:
#             raise ApplicationError('no user has been found with this email and password combination', 'u001')
#     else:
#         raise ApplicationError('email or password missing', 'unspecified')


# @user.route("/reset_pass", methods=['POST'])
# def reset_pass():
#     json_data = request.json
#     print(json_data)
#     if 'email' in json_data.keys():
#         user = {}
#         user["email"] = json_data["email"]

#         # check if user exists
#         users_check = Sql.get_user(user)
#         print(users_check)
#         if len(users_check) == 1:
#             random = token_urlsafe(16)
#             timestamp = datetime.datetime.now()
#             user = users_check[0].to_dict()
#             hashed_password = hashlib.sha256(random.encode('utf-8')).hexdigest()
#             user["password"] = hashed_password
#             user["code"] = random
#             user["timestamp"] = timestamp
#             update_user = Sql.update_user(user['id'], user)
#             get_company = get_company_account(user['comp_id'])
#             get_client = get_client_account(user['id'])
#             print(get_client)
#             client = get_client[0]
#             check_dict = {}
#             check_dict['second_name'] = ""
#             if 'second_forename' in client:
#                 check_dict['second_name'] = client["second_forename"]
#             check_dict['name'] = client["forname"]
#             check_dict['email'] = client["email"]
#             check_dict['number'] = client.get("mobile", "")
#             check_dict['random'] = random
#             check_dict['company_id'] = client['company_id']
#             check_dict['company'] = get_company[0]["name"]
#             check_dict['contact_name'] = get_company[0]["contact_name"]
#             check_dict['contact_num'] = get_company[0]["contact_num"]
#             check_dict['seen_bool'] = 'unseen'
#             check_dict['director_name'] = get_company[0]["contact_name"]
#             check_dict['colour_hex'] = get_company[0]["colour_hex"]
#             check_dict['owner_name'] = get_company[0]["owner_name"]
#             check_dict['owner_status'] = get_company[0]["owner_status"]
#             names = client["forname"]
#             if client['user_count'] == 'two':
#                 names = "{} and {}".format(client["forname"], client["second_forname"])
#             check_dict['names'] = names
#             check_dict['url'] = get_company[0]['url']
#             print("sending")
#             send_reset_password(check_dict)

#             return jsonify(users_check[0].to_dict())
#         else:
#             raise ApplicationError('no user has been found with this email and password combination', 'u001')
#     else:
#         raise ApplicationError('email or password missing', 'unspecified')


# @user.route("/new_client_with_pass", methods=['POST'])
# def new_client_pass():
#     json_data = request.json
#     timestamp = datetime.datetime.now()
#     print("hi")
#     if 'email' in json_data.keys():
#         user = {}
#         user["email"] = json_data["email"]
#         # check if user exists
#         users_check = Sql.get_user(user)
#         if len(users_check) == 0:
#             random = token_urlsafe(16)
#             get_company = get_company_account(json_data['comp_id'])
#             hashed_password = hashlib.sha256(random.encode('utf-8')).hexdigest()
#             user["password"] = hashed_password
#             user["code"] = random
#             user["timestamp"] = timestamp
#             user["comp_id"] = json_data['comp_id']
#             new_user = Sql.new_user(user)
#             jsonify_user = new_user[0].to_dict()
#             print(jsonify_user['id'])
#             check_dict = {}
#             if 'second_forename' in json_data:
#                 check_dict['second_name'] = json_data["second_forename"]
#             check_dict['name'] = json_data["forname"]
#             check_dict['email'] = json_data["email"]
#             check_dict['number'] = json_data.get("number", "")
#             check_dict['random'] = random
#             check_dict['company_id'] = json_data['company_id']
#             check_dict['company'] = json_data["company"]
#             check_dict['contact_name'] = json_data["contact_name"]
#             check_dict['contact_num'] = json_data["contact_num"]
#             check_dict['seen_bool'] = 'unseen'
#             check_dict['director_name'] = json_data["director_name"]
#             check_dict['company_colour_hex'] = json_data["company_colour_hex"]
#             check_dict['names'] = json_data['names']
#             check_dict['url'] = get_company[0]['url']
#             print("sending")
#             send_client_notification(check_dict)
#             print("sent")
#             if len(new_user) == 1:
#                 return jsonify(new_user[0].to_dict())
#             else:
#                 raise ApplicationError('something has gone wrong creating a new user', 'unspecified')
#         else:
#             raise ApplicationError('a user with this email alredy exists', 'u002')
#     else:
#         raise ApplicationError('email or password missing', 'unspecified')


# def build_output(results):
#     result_dict = []
#     for key in results:
#         output = key.to_dict()
#         result_dict.append(output)
#     return jsonify(result_dict)
