from flask import request, Blueprint, Response, jsonify, current_app
from account_api.exceptions import ApplicationError

from account_api.models import Payment
from account_api.sqs import SqsSender

payment = Blueprint('payment', __name__)

# NOTE this route is being used to create new payment records and update existing ones as its possible for stripe to send a webhook before the payment is created


@payment.route("/payment/<intent_id>", methods=['PUT'])
def new_payment(intent_id):
    json_data = request.json
    json_data['id'] = intent_id

    payment = Payment.get_payment_by_id(intent_id)
    new_payment = False
    if not payment:
        payment = Payment.create_payment(json_data)
        new_payment = True

    if not new_payment and json_data["status"] == "in_progress":
        del json_data['status']

    payment.update(json_data)

    if payment.status == 'success' and payment.report_id != None:
        # add a message to the queue to generate the report
        SqsSender().send_message({
            "report_id": payment.report_id
        })

    return jsonify(payment.to_dict())
# @user.route("/report", methods=['POST'])
# def new_report():
#     json_data = request.json
#     try:
#         result = Report.create_report(json_data)
#         return jsonify(result.to_dict())
#     except Exception as e:
#         print(e)
#     raise ApplicationError('something has gone wrong creating a new report', 'UAclient-a001')


# @user.route("/report/<report_id>", methods=['PUT'])
# def update_report(report_id):
#     json_data = request.json
#     try:
#         report = Report.get_report_by_id(report_id)
#         if report:
#             report.update(json_data)
#             return jsonify(report.to_dict())
#         else:
#             raise ApplicationError('report not found', 'UAclient-a002')
#     except Exception as e:
#         print(e)
#     raise ApplicationError('something has gone wrong updating the report', 'UAclient-a003')
