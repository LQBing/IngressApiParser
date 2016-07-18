class PortalMod:
    def __init__(self, info_dict):
        if info_dict:
            self.owner = info_dict[0]
            self.name = info_dict[1]
            self.rarity = info_dict[2]
            # info_dict[3]


class PortalResonator:
    def __init__(self, info_dict):
        self.owner = info_dict[0]
        self.level = info_dict[1]
        self.health_slot = info_dict[2]


# get by api getPortalDetails with par guid, v
class PortalDetailParser:
    def __init__(self, portal_details_result):
        self.result = portal_details_result
        # self.result[0]  # uncertain. all portal value is 'p', means 'portal'?
        if self.result[1] == 'N':
            self.team = None
        elif self.result[1] == 'R':
            self.team = 'RESISTANCE'
        elif self.result[1] == 'E':
            self.team = 'ENLIGHTENED'
        else:
            raise ValueError("unknown portal team data '%s'" % self.result[1])
        self.latE6 = self.result[2]
        self.lngE6 = self.result[3]
        self.level = self.result[4]
        self.health = self.result[5]
        self.resonators_count = self.result[6]
        self.pic = self.result[7]
        self.name = self.result[8]
        # self.result[9]
        # self.result[10]  # uncertain. mission start here , true; not mission start here , false
        # self.result[11]  # uncertain. mission start here , true; not mission start here , false
        # self.result[12]
        # self.result[13]
        self.mods = list()
        self.mods.append(PortalMod(self.result[14][0]))
        self.mods.append(PortalMod(self.result[14][1]))
        self.mods.append(PortalMod(self.result[14][2]))
        self.mods.append(PortalMod(self.result[14][3]))
        self.resonators = list()
        self.resonators.append(PortalMod(self.result[15][0]))
        self.resonators.append(PortalMod(self.result[15][1]))
        self.resonators.append(PortalMod(self.result[15][2]))
        self.resonators.append(PortalMod(self.result[15][3]))
        self.resonators.append(PortalMod(self.result[15][4]))
        self.resonators.append(PortalMod(self.result[15][5]))
        self.resonators.append(PortalMod(self.result[15][6]))
        self.resonators.append(PortalMod(self.result[15][7]))
        self.owner = self.result[16]
        # self.result[17]


# get by api getPlexts with par ascendingTimestampOrder,
#  maxLatE6, maxLngE6, minLatE6, minLngE6, maxTimestampMs, minTimestampMs, tab, v
class MessageParser:
    def __init__(self, result_json):
        self.agent = None
        self.guid = result_json[0]
        self.time_stamp = result_json[1]
        plext = result_json[2]['plext']
        self.text = plext['text']
        self.plext_type = plext['plextType']
        self.team = plext['team']
        self.categories = plext['categories']
        self.portal_name = None
        self.portal_address = None
        self.portal_lat = None
        self.portal_lng = None
        self.portal_plain = None
        self.markup = plext['markup']
        self.message_type = self.get_message_type()

    def get_message_type(self):
        if self.categories == 4:
            # alert message
            if len(self.markup) == 4 and self.markup[0][0] == "TEXT" and self.markup[1][0] == "PORTAL" and \
                            self.markup[2][0] == "TEXT" and self.markup[3][0] == "PLAYER":
                # attack alert
                if self.markup[2][1]['plain'] == " is under attack by ":
                    if self.markup[3][0] == "PLAYER":
                        self.agent = self.markup[3][1]['plain']
                        return "alert_under_attack"
                # neutralize alert
                elif self.markup[2][1]['plain'] == " neutralized by ":
                    if self.markup[3][0] == "PLAYER":
                        self.agent = self.markup[3][1]['plain']
                        return "alert_neutralize"
        elif self.categories == 2:
            # faction message
            if self.markup[2][0] == "TEXT":
                if self.markup[2][1]['plain'] == "has completed training.":
                    # !!! maybe send by agent, do not trust it as sent by system
                    #  for determine whether he(or she) is a new agent.
                    if self.markup[1][0] == "SENDER":
                        self.agent = self.markup[1][1]['plain'][:-2]
                        return "faction_complete_training"
                    else:
                        raise ValueError("unknown message type")
                elif len(self.markup) == 3 and self.markup[1][0] == "SENDER":
                    self.agent = self.markup[1][1]['plain'][:-2]
                    return "faction_message"
                elif self.markup[3][0] == "AT_PLAYER":
                    # at message
                    if self.markup[1][0] == "SENDER":
                        self.agent = self.markup[1][1]['plain'][:-2]
                        return "faction_at_message"
                    else:
                        raise ValueError("unknown message type")
                else:
                    raise ValueError("unknown message type")
            elif self.markup[3][0] == "TEXT":
                if self.markup[3][1]['plain'] == " captured their first Portal.":
                    if self.markup[2][0] == "PLAYER":
                        self.agent = self.markup[2][1]['plain']
                        return "faction_first_portal"
                    else:
                        raise ValueError("unknown message type")

                elif self.markup[3][1]['plain'] == " created their first Control Field":
                    if self.markup[2][0] == "PLAYER":
                        self.agent = self.markup[1][1]['plain']
                        return "faction_first_field"
                    else:
                        raise ValueError("unknown message type")
                elif self.markup[3][1]['plain'] == " created their first Link.":
                    if self.markup[2][0] == "PLAYER":
                        self.agent = self.markup[1][1]['plain']
                        return "faction_first_link"
                    else:
                        raise ValueError("unknown message type")
        elif self.categories == 1:
            # common messages
            if self.plext_type == "SYSTEM_BROADCAST":
                if self.markup[0][0] == "PLAYER":
                    self.agent = self.markup[0][1]['plain']
                    if self.markup[2][0] == "PORTAL":
                        self.portal_name = self.markup[2][1]['name']
                        self.portal_plain = self.markup[2][1]['plain']
                        self.portal_address = self.markup[2][1]['address']
                        self.portal_lat = self.markup[2][1]['latE6']
                        self.portal_lng = self.markup[2][1]['lngE6']
                        if self.markup[1][0] == "TEXT":
                            if self.markup[1][1]['plain'] == " captured ":
                                return 'common_capture'
                            elif self.markup[1][1]['plain'] == " deployed a Resonator on ":
                                return 'common_deploy_resonator'
                            elif self.markup[1][1]['plain'] == " destroyed a Resonator on ":
                                return 'common_destroy_resonator'
                            # TODO: deploy mod

                            # TODO: destroy mod

                            elif self.markup[1][1]['plain'] == " linked ":
                                return 'common_link'
            elif self.plext_type == "PLAYER_GENERATED":
                if self.markup[0][0] == 'SENDER' and self.markup[1][0] == 'TEXT':
                    if len(self.markup) == 2:
                        self.agent = self.markup[0][1]['plain'][:-2]
                        return 'common_message'
                    elif len(self.markup) == 4 and self.markup[2][0] == "AT_PLAYER" and self.markup[3][0] == "TEXT":
                        self.agent = self.markup[0][1]['plain'][:-2]
                        return 'common_at_message'
        return 'unknown_type'


# get by api getEntities with par tileKeys list, v
class PortalListParser:
    def __init__(self):
        pass
        # TODO : portal list parser


# get by api getGameScore with par v
class GameScoreParser:
    def __init__(self):
        pass
        # TODO : game source parser


# get by api getRegionScoreDetails with pars latE6, lngE6, v
class RegionScoreDetailsParser:
    def __init__(self):
        pass
        # TODO : region source detail parser


# get by api getArtifactPortals with par v
class ArtifactPortalsParser:
    def __init__(self):
        pass
        # TODO : artifact portals parser


# get by api sendPlext with par message, latE6, lngE6, tab ,v
class SendMessageParser:
    def __init__(self):
        pass
        # TODO : send  message parser


# get by api sendInviteEmail with par address
class SendInviteEmailParser:
    def __init__(self):
        pass
        # TODO : send  invite email parser


# get by api sendInviteEmail with par address
class RedeemRewardParser:
    def __init__(self):
        pass
        # TODO : redeem reward parser
