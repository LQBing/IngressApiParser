import json
from data_sample import *
from ingress_json_parser import PortalDetailParser, MessageParser

portal_json_list = list()

# white portal

portal_json_list.append(json.loads(white_portal))

portal_json_list.append(json.loads(res_portal))

portal_json_list.append(json.loads(enl_portal))

message_json_list = list()
message_json_list.append(json.loads(faction_first_field))
message_json_list.append(json.loads(faction_message))
message_json_list.append(json.loads(faction_at_message))
message_json_list.append(json.loads(faction_complete_training))
message_json_list.append(json.loads(faction_first_portal))
message_json_list.append(json.loads(faction_first_link))
message_json_list.append(json.loads(common_deploy_resonator))
message_json_list.append(json.loads(common_link))
message_json_list.append(json.loads(common_create_control_field))
message_json_list.append(json.loads(common_capture))
message_json_list.append(json.loads(common_destroy_resonator))
message_json_list.append(json.loads(common_destroy_link))
message_json_list.append(json.loads(common_at_message))
message_json_list.append(json.loads(common_message))
message_json_list.append(json.loads(alert_under_attack))
message_json_list.append(json.loads(alert_neutralize))


def test_parser(parser_json):
    result = MessageParser(parser_json['result']).message_type
    if parser_json['type'] != result:
        raise ValueError("true value is %s , not %s" % (parser_json['type'], result))


for item in message_json_list:
    test_parser(item)
print("test complete.")
