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


class MessageMarkupParser:
    def __init__(self, markup):
        self.secure = None
        self.sender = None
        self.text1 = None
        self.text2 = None
        self.at_player = None
        self.player = None
        self.portal = None
        self.portal_name = None
        self.portal_team = None
        self.portal_address = None
        self.portal_latE6 = None
        self.portal_lngE6 = None
        text_count = 0
        for markup_item in markup:
            if markup_item[0] == "SECURE":
                self.secure = markup_item[1]['plain']
            if markup_item[0] == "SENDER":
                self.sender = markup_item[1]['plain'][:-2]
            if markup_item[0] == "AT_PLAYER":
                self.at_player = markup_item[1]['plain']
            if markup_item[0] == "PLAYER":
                self.player = markup_item[1]['plain']

            if markup_item[0] == "PORTAL":
                self.portal = markup_item[1]['plain']
                self.portal_name = markup_item[1]['name']
                self.portal_team = markup_item[1]['team']
                self.portal_address = markup_item[1]['address']
                self.portal_latE6 = markup_item[1]['latE6']
                self.portal_lngE6 = markup_item[1]['lngE6']

            if markup_item[0] == "TEXT":
                if text_count == 0:
                    self.text1 = markup_item[1]['plain']
                    text_count += 1
                elif text_count == 1:
                    self.text2 = markup_item[1]['plain']
                    text_count += 1


# get by api getPlexts with par ascendingTimestampOrder,
#  maxLatE6, maxLngE6, minLatE6, minLngE6, maxTimestampMs, minTimestampMs, tab, v
class MessageParser:
    def __init__(self, result_json):
        self.agent = None
        self.message_type = None
        self.guid = result_json[0]
        self.time_stamp = result_json[1]
        plext = result_json[2]['plext']
        self.text = plext['text']
        self.plext_type = plext['plextType']
        self.team = plext['team']
        self.categories = plext['categories']
        self.markup = MessageMarkupParser(plext['markup'])
        self.deal_markup()

    def deal_markup(self):
        # alert message
        if self.categories == 4:
            # alert_under_attack
            if self.markup.text2 == " is under attack by ":
                self.message_type = "alert_under_attack"
                self.agent = self.markup.player
            # alert_neutralize
            elif self.markup.text2 == " neutralized by ":
                self.message_type = "alert_neutralize"
                self.agent = self.markup.player
            else:
                raise ValueError("unknown alert message")
        # faction message
        elif self.categories == 2:
            # faction player send messages
            if self.markup.sender:
                self.agent = self.markup.sender
                # faction_complete_training
                # weird, complete training message is 'sender', not player
                if (self.markup.text1 == "has completed training." or
                            self.markup.text2 == "has completed training."):
                    self.message_type = "faction_complete_training"
                # faction_at_message
                elif self.markup.at_player:
                    self.message_type = "faction_at_message"
                # faction_message
                else:
                    self.message_type = "faction_message"
            # player action alert messages
            elif self.markup.player:
                self.agent = self.markup.player
                # faction_first_portal
                if (self.markup.text1 == " captured their first Portal." or
                            self.markup.text2 == " captured their first Portal."):
                    self.message_type = "faction_first_portal"
                # faction_first_link
                elif (self.markup.text1 == " created their first Link." or
                              self.markup.text2 == " created their first Link."):
                    self.message_type = "faction_first_link"
                # faction_first_field
                elif (self.markup.text1 == " created their first Control Field" or
                              self.markup.text2 == " created their first Control Field"):
                    self.message_type = "faction_first_field"
                else:
                    raise ValueError("unknown player action alert message")
            else:
                raise ValueError("unknown faction message")
        # common messages
        elif self.categories == 1:
            # player send messages
            if self.markup.sender:
                self.agent = self.markup.sender
                # common_at_message
                if self.markup.at_player:
                    self.message_type = "common_at_message"
                else:
                    self.message_type = "common_message"
            # system common messages
            elif self.markup.player:
                self.agent = self.markup.player
                #
                if self.markup.text1 == " linked " and self.markup.text2 == " to ":
                    self.message_type = "common_link"
                elif self.markup.text1 == " destroyed a Resonator on ":
                    self.message_type = "common_destroy_resonator"
                elif self.markup.text1 == " deployed a Resonator on ":
                    self.message_type = "common_deploy_resonator"
                elif self.markup.text1 == " captured ":
                    self.message_type = "common_capture"
                else:
                    raise ValueError("unknown common system message")
            else:
                raise ValueError("unknown common message")


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
