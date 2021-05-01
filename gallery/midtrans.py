import requests
from requests.auth import HTTPBasicAuth
import json

MIDTRANS_API_SERVER_KEY = "VT-server-ftq_xybTgql3yHJJ0Kb3qav4"
MIDTRANS_API_CLIENT_KEY = "VT-client-XcDBcTnX5yTeBgxT"

MIDTRANS_API_BASEURL = "https://app.midtrans.com/snap/v1/{0}"
MIDTRANS_API_SANDBOXURL = "https://app.sandbox.midtrans.com/snap/v1/{0}"

def call_midtrans_api(method, endpoint, data, sandbox=True):
    if sandbox:
        API_BASEURL = MIDTRANS_API_SANDBOXURL
    else:
        API_BASEURL = MIDTRANS_API_BASEURL
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json',
    }
    if method == "POST":
        result = requests.post(API_BASEURL.format(endpoint), data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(MIDTRANS_API_SERVER_KEY, ''))
    else:
        result = requests.get(API_BASEURL.format(endpoint), headers=headers)
    return result

def get_SNAP_token(request, current_user, order_id, gross_amount):
  SNAP_token = call_midtrans_api("POST", "transactions", {
    "transaction_details": {
      "order_id": order_id,
      "gross_amount": gross_amount,
    },
    "customer_details": {
      "first_name": current_user.first_name,
      "last_name": current_user.last_name,
      "email": current_user.email,
      "phone": current_user.profile.phone,
      "billing_address": {
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "phone": current_user.profile.phone,
        "address": current_user.profile.address,
        "city": current_user.profile.city,
        "postal_code": current_user.profile.postal_code,
        "country_code": current_user.profile.country_code
      }
    }
  })
  return SNAP_token