from pyfcm import FCMNotification

api_key = 'AAAAtcSdXik:APA91bF8XdpJSWYEQfernh4qNaoeCS1KuXhvanEefSrwRZ5wgM1toXez-ZwwicSDr1WjldV7NJELFa_yMAjbiavIn4ZIApH5WS7SINrp7eapORfsbGJkRZCsIsyMSaOJ3pWCupy_dZxZlHw4cyrdBjhMe5KKuIBlnA'
push_service = FCMNotification(api_key=api_key)


def send_message_to_groups(topic, msg):
    topic_name = '/topics/' + str(topic)
    # topic_name = '/topics/cats'
    print topic_name,msg
    result = push_service.notify_topic_subscribers(topic_name=topic_name, data_message=msg)
    print result
    return


def send_group_subscription_message(to, topic):
    data_message = {'type': 0, 'group_id': topic}
    result = push_service.notify_single_device(to, data_message=data_message)
    print result
    return
