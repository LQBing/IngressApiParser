# IngressApiParser

## usage

1. use [ingrex lib](https://github.com/blackgear/ingrex_lib) api to get response json

    import intel
    ingress_json_parser
    
    cookies = ""
    field = ""
    intel = intel.Intel(cookies, field)
    result = intel.fetch_msg()

2. put response json into parser and get data from parser just with par name, without complex data structures.

    for message in result:
        message_parser = ingress_json_parser.MessageParser(message)
        print(message_parser.agent)
        print(message_parser.plext)
        print(message_parser.team)


## parsers lib for ingress json.:

### class MessageParser 
A small amount of data is not parsed.

### class PortalListParser
wait

### class GameScoreParser wait

### class RegionScoreDetailsParser 
wait

### class ArtifactPortalsParser
 wait

### class SendMessageParser 
wait

### SendInviteEmailParser 
wait

### class RedeemRewardParser 
wait


# quote
[https://github.com/blackgear/ingrex_lib](https://github.com/blackgear/ingrex_lib)
