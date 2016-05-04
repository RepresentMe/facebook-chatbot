import requests, json


def ask_question(user_id):
    quest = requests.get('https://represent.me/api/next_question/')
    ret_string = json.loads(quest.text)['results'][0]['question']

    question_req = {
        'recipient': {
            'id': user_id
        },
        'message': {
            'text': ret_string
        }
    }
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % \
          (
              'EAAVZCyjFh4eEBAF6ox3WSbpiTUI4ksXPCTFLXpK2ZAeT7i85SgWM9aekq1eu8ZBMSCetTqObtl8DYWHPzRMGnYPT2ugwpD394mAZBonciOefHVxtZCiMsOKgYr6o3N5yKCbvuqVCV0Of6wRuoaY4UBH5AzjDPwUwntasI3jqGMgZDZD',)
    response_msg = json.dumps(question_req)
    r = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(r.text)


def misunderstood(user_id):
    question_req = {
        'recipient': {
            'id': user_id
        },
        'message': {
            'text': 'Sorry, I didn\'t understand you :(. If you want me to ask question, type "Ask"'
        }
    }
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s' % \
          (
              'EAAVZCyjFh4eEBAF6ox3WSbpiTUI4ksXPCTFLXpK2ZAeT7i85SgWM9aekq1eu8ZBMSCetTqObtl8DYWHPzRMGnYPT2ugwpD394mAZBonciOefHVxtZCiMsOKgYr6o3N5yKCbvuqVCV0Of6wRuoaY4UBH5AzjDPwUwntasI3jqGMgZDZD',)
    response_msg = json.dumps(question_req)
    r = requests.post(url, headers={"Content-Type": "application/json"}, data=response_msg)
    print(r.text)
