from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import base64
import time
import inspect
import requests
import json
from collections import deque
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
from google.protobuf.message import Message
from google.protobuf.json_format import MessageToDict, ParseDict

app = Flask(__name__)
CORS(app)

# ==========================================
# 🧠 1. ALL PROTOBUFS INJECTED DIRECTLY
# ==========================================
_sym_db = _symbol_database.Default()

try:
    # 1. account_show_pb2
    DESC1 = _descriptor_pool.Default().AddSerializedFile(b'\n\x19\x41\x63\x63ountPersonalShow.proto\x12\x08\x66reefire\"\xbc\x01\n\x0e\x41\x63\x63ountPrefers\x12\x15\n\rhide_my_lobby\x18\x01 \x01(\x08\x12\x1c\n\x14pregame_show_choices\x18\x02 \x03(\r\x12\x1f\n\x17\x62r_pregame_show_choices\x18\x03 \x03(\r\x12\x1a\n\x12hide_personal_info\x18\x04 \x01(\x08\x12\x1f\n\x17\x64isable_friend_spectate\x18\x05 \x01(\x08\x12\x17\n\x0fhide_occupation\x18\x06 \x01(\x08\"\x8a\x01\n\x10\x45xternalIconInfo\x12\x15\n\rexternal_icon\x18\x01 \x01(\t\x12,\n\x06status\x18\x02 \x01(\x0e\x32\x1c.freefire.ExternalIconStatus\x12\x31\n\tshow_type\x18\x03 \x01(\x0e\x32\x1e.freefire.ExternalIconShowType\"\\\n\x0fSocialHighLight\x12\'\n\nhigh_light\x18\x01 \x01(\x0e\x32\x13.freefire.HighLight\x12\x11\n\texpire_at\x18\x02 \x01(\x03\x12\r\n\x05value\x18\x03 \x01(\r\"\xfc\x01\n\x14WeaponPowerTitleInfo\x12\x0e\n\x06region\x18\x01 \x01(\t\x12\x14\n\x0ctitle_cfg_id\x18\x02 \x01(\r\x12\x16\n\x0eleaderboard_id\x18\x03 \x01(\x04\x12\x11\n\tweapon_id\x18\x04 \x01(\r\x12\x0c\n\x04rank\x18\x05 \x01(\r\x12\x13\n\x0b\x65xpire_time\x18\x06 \x01(\x03\x12\x13\n\x0breward_time\x18\x07 \x01(\x03\x12\x12\n\nRegionName\x18\x08 \x01(\t\x12\x39\n\nRegionType\x18\t \x01(\x0e\x32%.freefire.ELeaderBoardTitleRegionType\x12\x0c\n\x04IsBr\x18\n \x01(\x08\"\xad\x01\n\x11GuildWarTitleInfo\x12\x0e\n\x06region\x18\x01 \x01(\t\x12\x0f\n\x07\x63lan_id\x18\x02 \x01(\x04\x12\x14\n\x0ctitle_cfg_id\x18\x03 \x01(\r\x12\x16\n\x0eleaderboard_id\x18\x04 \x01(\x04\x12\x0c\n\x04rank\x18\x05 \x01(\r\x12\x13\n\x0b\x65xpire_time\x18\x06 \x01(\x03\x12\x13\n\x0breward_time\x18\x07 \x01(\x03\x12\x11\n\tclan_name\x18\x08 \x01(\t\"\x92\x01\n\x14LeaderboardTitleInfo\x12?\n\x17weapon_power_title_info\x18\x01 \x03(\x0b\x32\x1e.freefire.WeaponPowerTitleInfo\x12\x39\n\x14guild_war_title_info\x18\x02 \x03(\x0b\x32\x1b.freefire.GuildWarTitleInfo\"\xfb\x03\n\x0fSocialBasicInfo\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12 \n\x06gender\x18\x02 \x01(\x0e\x32\x10.freefire.Gender\x12$\n\x08language\x18\x03 \x01(\x0e\x32\x12.freefire.Language\x12)\n\x0btime_online\x18\x04 \x01(\x0e\x32\x14.freefire.TimeOnline\x12)\n\x0btime_active\x18\x05 \x01(\x0e\x32\x14.freefire.TimeActive\x12/\n\nbattle_tag\x18\x06 \x03(\x0e\x32\x1b.freefire.PlayerBattleTagID\x12\'\n\nsocial_tag\x18\x07 \x03(\x0e\x32\x13.freefire.SocialTag\x12)\n\x0bmode_prefer\x18\x08 \x01(\x0e\x32\x14.freefire.ModePrefer\x12\x11\n\tsignature\x18\t \x01(\t\x12%\n\trank_show\x18\n \x01(\x0e\x32\x12.freefire.RankShow\x12\x18\n\x10\x62\x61ttle_tag_count\x18\x0b \x03(\r\x12!\n\x19signature_ban_expire_time\x18\x0c \x01(\x03\x12:\n\x12leaderboard_titles\x18\r \x01(\x0b\x32\x1e.freefire.LeaderboardTitleInfo\"\x92\x01\n#SocialHighLightsWithSocialBasicInfo\x12\x35\n\x12social_high_lights\x18\x01 \x03(\x0b\x32\x19.freefire.SocialHighLight\x12\x34\n\x11social_basic_info\x18\x02 \x01(\x0b\x32\x19.freefire.SocialBasicInfo\"c\n\x0eOccupationInfo\x12\x15\n\roccupation_id\x18\x01 \x01(\r\x12\x0e\n\x06scores\x18\x02 \x01(\x04\x12\x13\n\x0bproficients\x18\x03 \x01(\x04\x12\x15\n\rproficient_lv\x18\x04 \x01(\r\"d\n\x14OccupationSeasonInfo\x12\x11\n\tseason_id\x18\x01 \x01(\r\x12\x11\n\tgame_mode\x18\x02 \x01(\r\x12&\n\x04info\x18\x03 \x01(\x0b\x32\x18.freefire.OccupationInfo\"\xcb\x0c\n\x10\x41\x63\x63ountInfoBasic\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x14\n\x0c\x61\x63\x63ount_type\x18\x02 \x01(\r\x12\x10\n\x08nickname\x18\x03 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x04 \x01(\t\x12\x0e\n\x06region\x18\x05 \x01(\t\x12\r\n\x05level\x18\x06 \x01(\r\x12\x0b\n\x03\x65xp\x18\x07 \x01(\r\x12\x15\n\rexternal_type\x18\x08 \x01(\r\x12\x15\n\rexternal_name\x18\t \x01(\t\x12\x15\n\rexternal_icon\x18\n \x01(\t\x12\x11\n\tbanner_id\x18\x0b \x01(\r\x12\x10\n\x08head_pic\x18\x0c \x01(\r\x12\x11\n\tclan_name\x18\r \x01(\t\x12\x0c\n\x04rank\x18\x0e \x01(\r\x12\x16\n\x0eranking_points\x18\x0f \x01(\r\x12\x0c\n\x04role\x18\x10 \x01(\r\x12\x16\n\x0ehas_elite_pass\x18\x11 \x01(\x08\x12\x11\n\tbadge_cnt\x18\x12 \x01(\r\x12\x10\n\x08\x62\x61\x64ge_id\x18\x13 \x01(\r\x12\x11\n\tseason_id\x18\x14 \x01(\r\x12\r\n\x05liked\x18\x15 \x01(\r\x12\x12\n\nis_deleted\x18\x16 \x01(\x08\x12\x11\n\tshow_rank\x18\x17 \x01(\x08\x12\x15\n\rlast_login_at\x18\x18 \x01(\x03\x12\x14\n\x0c\x65xternal_uid\x18\x19 \x01(\x04\x12\x11\n\treturn_at\x18\x1a \x01(\x03\x12\x1e\n\x16\x63hampionship_team_name\x18\x1b \x01(\t\x12$\n\x1c\x63hampionship_team_member_num\x18\x1c \x01(\r\x12\x1c\n\x14\x63hampionship_team_id\x18\x1d \x01(\x04\x12\x0f\n\x07\x63s_rank\x18\x1e \x01(\r\x12\x19\n\x11\x63s_ranking_points\x18\x1f \x01(\r\x12\x19\n\x11weapon_skin_shows\x18  \x03(\r\x12\x0e\n\x06pin_id\x18! \x01(\r\x12\x19\n\x11is_cs_ranking_ban\x18\" \x01(\x08\x12\x10\n\x08max_rank\x18# \x01(\r\x12\x13\n\x0b\x63s_max_rank\x18$ \x01(\r\x12\x1a\n\x12max_ranking_points\x18% \x01(\r\x12\x15\n\rgame_bag_show\x18& \x01(\r\x12\x15\n\rpeak_rank_pos\x18\' \x01(\r\x12\x18\n\x10\x63s_peak_rank_pos\x18( \x01(\r\x12\x31\n\x0f\x61\x63\x63ount_prefers\x18) \x01(\x0b\x32\x18.freefire.AccountPrefers\x12\x1f\n\x17periodic_ranking_points\x18* \x01(\r\x12\x15\n\rperiodic_rank\x18+ \x01(\r\x12\x11\n\tcreate_at\x18, \x01(\x03\x12:\n\x16veteran_leave_days_tag\x18- \x01(\x0e\x32\x1a.freefire.VeteranLeaveDays\x12\x1b\n\x13selected_item_slots\x18. \x03(\r\x12\x38\n\x10pre_veteran_type\x18/ \x01(\x0e\x32\x1e.freefire.PreVeteranActionType\x12\r\n\x05title\x18\x30 \x01(\r\x12\x36\n\x12\x65xternal_icon_info\x18\x31 \x01(\x0b\x32\x1a.freefire.ExternalIconInfo\x12\x17\n\x0frelease_version\x18\x32 \x01(\t\x12\x1b\n\x13veteran_expire_time\x18\x33 \x01(\x04\x12\x14\n\x0cshow_br_rank\x18\x34 \x01(\x08\x12\x14\n\x0cshow_cs_rank\x18\x35 \x01(\x08\x12\x0f\n\x07\x63lan_id\x18\x36 \x01(\x04\x12\x15\n\rclan_badge_id\x18\x37 \x01(\r\x12\x19\n\x11\x63ustom_clan_badge\x18\x38 \x01(\t\x12\x1d\n\x15use_custom_clan_badge\x18\x39 \x01(\x08\x12\x15\n\rclan_frame_id\x18: \x01(\r\x12\x18\n\x10membership_state\x18; \x01(\x08\x12:\n\x12select_occupations\x18< \x03(\x0b\x32\x1e.freefire.OccupationSeasonInfo\x12Y\n\"social_high_lights_with_basic_info\x18= \x01(\x0b\x32-.freefire.SocialHighLightsWithSocialBasicInfo\"\x9a\x01\n\x0f\x41vatarSkillSlot\x12\x14\n\x07slot_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x15\n\x08skill_id\x18\x02 \x01(\x04H\x01\x88\x01\x01\x12\x30\n\x0c\x65quip_source\x18\x03 \x01(\x0e\x32\x15.freefire.EquipSourceH\x02\x88\x01\x01\x42\n\n\x08_slot_idB\x0b\n\t_skill_idB\x0f\n\r_equip_source\"\xfe\x03\n\rAvatarProfile\x12\x16\n\tavatar_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nskin_color\x18\x02 \x01(\rH\x01\x88\x01\x01\x12\x0f\n\x07\x63lothes\x18\x03 \x03(\r\x12\x16\n\x0e\x65quiped_skills\x18\x04 \x03(\r\x12\x18\n\x0bis_selected\x18\x05 \x01(\x08H\x02\x88\x01\x01\x12\x1f\n\x12pve_primary_weapon\x18\x06 \x01(\rH\x03\x88\x01\x01\x12\x1f\n\x12is_selected_awaken\x18\x07 \x01(\x08H\x04\x88\x01\x01\x12\x15\n\x08\x65nd_time\x18\x08 \x01(\rH\x05\x88\x01\x01\x12.\n\x0bunlock_type\x18\t \x01(\x0e\x32\x14.freefire.UnlockTypeH\x06\x88\x01\x01\x12\x18\n\x0bunlock_time\x18\n \x01(\rH\x07\x88\x01\x01\x12\x1b\n\x0eis_marked_star\x18\x0b \x01(\x08H\x08\x88\x01\x01\x12\x1e\n\x16\x63lothes_tailor_effects\x18\x0c \x03(\rB\x0c\n\n_avatar_idB\r\n\x0b_skin_colorB\x0e\n\x0c_is_selectedB\x15\n\x13_pve_primary_weaponB\x15\n\x13_is_selected_awakenB\x0b\n\t_end_timeB\x0e\n\x0c_unlock_typeB\x0e\n\x0c_unlock_timeB\x11\n\x0f_is_marked_star\"\xd8\x02\n\x12\x41\x63\x63ountNewsContent\x12\x10\n\x08item_ids\x18\x01 \x03(\r\x12\x11\n\x04rank\x18\x02 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nmatch_mode\x18\x03 \x01(\rH\x01\x88\x01\x01\x12\x13\n\x06map_id\x18\x04 \x01(\rH\x02\x88\x01\x01\x12\x16\n\tgame_mode\x18\x05 \x01(\rH\x03\x88\x01\x01\x12\x17\n\ngroup_mode\x18\x06 \x01(\rH\x04\x88\x01\x01\x12\x1b\n\x0etreasurebox_id\x18\x07 \x01(\rH\x05\x88\x01\x01\x12\x19\n\x0c\x63ommodity_id\x18\x08 \x01(\rH\x06\x88\x01\x01\x12\x15\n\x08store_id\x18\t \x01(\rH\x07\x88\x01\x01\x42\x07\n\x05_rankB\r\n\x0b_match_modeB\t\n\x07_map_idB\x0c\n\n_game_modeB\r\n\x0b_group_modeB\x11\n\x0f_treasurebox_idB\x0f\n\r_commodity_idB\x0b\n\t_store_id\"\xa7\x01\n\x0b\x41\x63\x63ountNews\x12%\n\x04type\x18\x01 \x01(\x0e\x32\x12.freefire.NewsTypeH\x00\x88\x01\x01\x12\x32\n\x07\x63ontent\x18\x02 \x01(\x0b\x32\x1c.freefire.AccountNewsContentH\x01\x88\x01\x01\x12\x18\n\x0bupdate_time\x18\x03 \x01(\x03H\x02\x88\x01\x01\x42\x07\n\x05_typeB\n\n\x08_contentB\x0e\n\x0c_update_time\"\x99\x02\n\x0b\x42\x61sicEPInfo\x12\x18\n\x0b\x65p_event_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x17\n\nowned_pass\x18\x02 \x01(\x08H\x01\x88\x01\x01\x12\x15\n\x08\x65p_badge\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x16\n\tbadge_cnt\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x14\n\x07\x62p_icon\x18\x05 \x01(\tH\x04\x88\x01\x01\x12\x16\n\tmax_level\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x17\n\nevent_name\x18\x07 \x01(\tH\x06\x88\x01\x01\x42\x0e\n\x0c_ep_event_idB\r\n\x0b_owned_passB\x0b\n\t_ep_badgeB\x0c\n\n_badge_cntB\n\n\x08_bp_iconB\x0c\n\n_max_levelB\r\n\x0b_event_name\"\x9d\x02\n\rClanInfoBasic\x12\x14\n\x07\x63lan_id\x18\x01 \x01(\x04H\x00\x88\x01\x01\x12\x16\n\tclan_name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x17\n\ncaptain_id\x18\x03 \x01(\x04H\x02\x88\x01\x01\x12\x17\n\nclan_level\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x15\n\x08\x63\x61pacity\x18\x05 \x01(\rH\x04\x88\x01\x01\x12\x17\n\nmember_num\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x18\n\x0bhonor_point\x18\x07 \x01(\rH\x06\x88\x01\x01\x42\n\n\x08_clan_idB\x0c\n\n_clan_nameB\r\n\x0b_captain_idB\r\n\x0b_clan_levelB\x0b\n\t_capacityB\r\n\x0b_member_numB\x0e\n\x0c_honor_point\"|\n\x0cPetSkillInfo\x12\x13\n\x06pet_id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x15\n\x08skill_id\x18\x02 \x01(\rH\x01\x88\x01\x01\x12\x18\n\x0bskill_level\x18\x03 \x01(\rH\x02\x88\x01\x01\x42\t\n\x07_pet_idB\x0b\n\t_skill_idB\x0e\n\x0c_skill_level\"\x84\x03\n\x07PetInfo\x12\x0f\n\x02id\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x11\n\x04name\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05level\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x10\n\x03\x65xp\x18\x04 \x01(\rH\x03\x88\x01\x01\x12\x18\n\x0bis_selected\x18\x05 \x01(\x08H\x04\x88\x01\x01\x12\x14\n\x07skin_id\x18\x06 \x01(\rH\x05\x88\x01\x01\x12\x0f\n\x07\x61\x63tions\x18\x07 \x03(\r\x12&\n\x06skills\x18\x08 \x03(\x0b\x32\x16.freefire.PetSkillInfo\x12\x1e\n\x11selected_skill_id\x18\t \x01(\rH\x06\x88\x01\x01\x12\x1b\n\x0eis_marked_star\x18\n \x01(\x08H\x07\x88\x01\x01\x12\x15\n\x08\x65nd_time\x18\x0b \x01(\rH\x08\x88\x01\x01\x42\x05\n\x03_idB\x07\n\x05_nameB\x08\n\x06_levelB\x06\n\x04_expB\x0e\n\x0c_is_selectedB\n\n\x08_skin_idB\x14\n\x12_selected_skill_idB\x11\n\x0f_is_marked_starB\x0b\n\t_end_time\"<\n\x0e\x44iamondCostRes\x12\x19\n\x0c\x64iamond_cost\x18\x01 \x01(\rH\x00\x88\x01\x01\x42\x0f\n\r_diamond_cost\"\xfd\x03\n\x14\x43reditScoreInfoBasic\x12\x19\n\x0c\x63redit_score\x18\x01 \x01(\rH\x00\x88\x01\x01\x12\x14\n\x07is_init\x18\x02 \x01(\x08H\x01\x88\x01\x01\x12\x30\n\x0creward_state\x18\x03 \x01(\x0e\x32\x15.freefire.RewardStateH\x02\x88\x01\x01\x12&\n\x19periodic_summary_like_cnt\x18\x04 \x01(\rH\x03\x88\x01\x01\x12)\n\x1cperiodic_summary_illegal_cnt\x18\x05 \x01(\rH\x04\x88\x01\x01\x12\x1d\n\x10weekly_match_cnt\x18\x06 \x01(\rH\x05\x88\x01\x01\x12(\n\x1bperiodic_summary_start_time\x18\x07 \x01(\x03H\x06\x88\x01\x01\x12&\n\x19periodic_summary_end_time\x18\x08 \x01(\x03H\x07\x88\x01\x01\x42\x0f\n\r_credit_scoreB\n\n\x08_is_initB\x0f\n\r_reward_stateB\x1c\n\x1a_periodic_summary_like_cntB\x1f\n\x1d_periodic_summary_illegal_cntB\x13\n\x11_weekly_match_cntB\x1e\n\x1c_periodic_summary_start_timeB\x1c\n\x1a_periodic_summary_end_time\"-\n\x0c\x45quipAchInfo\x12\x0e\n\x06\x61\x63h_id\x18\x01 \x01(\r\x12\r\n\x05level\x18\x02 \x01(\r\"\xfa\x06\n\x17\x41\x63\x63ountPersonalShowInfo\x12\x33\n\nbasic_info\x18\x01 \x01(\x0b\x32\x1a.freefire.AccountInfoBasicH\x00\x88\x01\x01\x12\x32\n\x0cprofile_info\x18\x02 \x01(\x0b\x32\x17.freefire.AvatarProfileH\x01\x88\x01\x01\x12$\n\x17ranking_leaderboard_pos\x18\x03 \x01(\x05H\x02\x88\x01\x01\x12#\n\x04news\x18\x04 \x03(\x0b\x32\x15.freefire.AccountNews\x12.\n\x0fhistory_ep_info\x18\x05 \x03(\x0b\x32\x15.freefire.BasicEPInfo\x12\x35\n\x0f\x63lan_basic_info\x18\x06 \x01(\x0b\x32\x17.freefire.ClanInfoBasicH\x03\x88\x01\x01\x12;\n\x12\x63\x61ptain_basic_info\x18\x07 \x01(\x0b\x32\x1a.freefire.AccountInfoBasicH\x04\x88\x01\x01\x12(\n\x08pet_info\x18\x08 \x01(\x0b\x32\x11.freefire.PetInfoH\x05\x88\x01\x01\x12\x33\n\x0bsocial_info\x18\t \x01(\x0b\x32\x19.freefire.SocialBasicInfoH\x06\x88\x01\x01\x12\x37\n\x10\x64iamond_cost_res\x18\n \x01(\x0b\x32\x18.freefire.DiamondCostResH\x07\x88\x01\x01\x12>\n\x11\x63redit_score_info\x18\x0b \x01(\x0b\x32\x1e.freefire.CreditScoreInfoBasicH\x08\x88\x01\x01\x12=\n\x10pre_veteran_type\x18\x0c \x01(\x0e\x32\x1e.freefire.PreVeteranActionTypeH\t\x88\x01\x01\x12,\n\x0c\x65quipped_ach\x18\r \x03(\x0b\x32\x16.freefire.EquipAchInfoB\r\n\x0b_basic_infoB\x0f\n\r_profile_infoB\x1a\n\x18_ranking_leaderboard_posB\x12\n\x10_clan_basic_infoB\x15\n\x13_captain_basic_infoB\x0b\n\t_pet_infoB\x0e\n\x0c_social_infoB\x13\n\x11_diamond_cost_resB\x14\n\x12_credit_score_infoB\x13\n\x11_pre_veteran_type*\xa0\x01\n\x10VeteranLeaveDays\x12\x19\n\x15VeteranLeaveDays_NONE\x10\x00\x12\x1a\n\x16VeteranLeaveDays_SHORT\x10\x01\x12\x1b\n\x17VeteranLeaveDays_NORMAL\x10\x02\x12\x19\n\x15VeteranLeaveDays_LONG\x10\x03\x12\x1d\n\x19VeteranLeaveDays_VERYLONG\x10\x04*w\n\x14PreVeteranActionType\x12\x1d\n\x19PreVeteranActionType_NONE\x10\x00\x12!\n\x1dPreVeteranActionType_ACTIVITY\x10\x01\x12\x1d\n\x19PreVeteranActionType_BUFF\x10\x02*s\n\x12\x45xternalIconStatus\x12\x1b\n\x17\x45xternalIconStatus_NONE\x10\x00\x12!\n\x1d\x45xternalIconStatus_NOT_IN_USE\x10\x01\x12\x1d\n\x19\x45xternalIconStatus_IN_USE\x10\x02*t\n\x14\x45xternalIconShowType\x12\x1d\n\x19\x45xternalIconShowType_NONE\x10\x00\x12\x1f\n\x1b\x45xternalIconShowType_FRIEND\x10\x01\x12\x1c\n\x18\x45xternalIconShowType_ALL\x10\x02*\xf0\x02\n\tHighLight\x12\x12\n\x0eHighLight_NONE\x10\x00\x12\x14\n\x10HighLight_BR_WIN\x10\x01\x12\x14\n\x10HighLight_CS_MVP\x10\x02\x12\x1b\n\x17HighLight_BR_STREAK_WIN\x10\x03\x12\x1b\n\x17HighLight_CS_STREAK_WIN\x10\x04\x12#\n\x1fHighLight_CS_RANK_GROUP_UPGRADE\x10\x05\x12\x16\n\x12HighLight_TEAM_ACE\x10\x06\x12 \n\x1cHighLight_WEAPON_POWER_TITLE\x10\x07\x12#\n\x1fHighLight_BR_RANK_GROUP_UPGRADE\x10\t\x12&\n\"HighLight_BR_STREAK_WIN_EXECELLENT\x10\n\x12&\n\"HighLight_CS_STREAK_WIN_EXECELLENT\x10\x0b\x12\x15\n\x11HighLight_VETERAN\x10\x0c*T\n\x06Gender\x12\x0f\n\x0bGender_NONE\x10\x00\x12\x0f\n\x0bGender_MALE\x10\x01\x12\x11\n\rGender_FEMALE\x10\x02\x12\x15\n\x10Gender_UNLIMITED\x10\xe7\x07*\xf5\x03\n\x08Language\x12\x11\n\rLanguage_NONE\x10\x00\x12\x0f\n\x0bLanguage_EN\x10\x01\x12\x1a\n\x16Language_CN_SIMPLIFIED\x10\x02\x12\x1b\n\x17Language_CN_TRADITIONAL\x10\x03\x12\x11\n\rLanguage_Thai\x10\x04\x12\x17\n\x13Language_VIETNAMESE\x10\x05\x12\x17\n\x13Language_INDONESIAN\x10\x06\x12\x17\n\x13Language_PORTUGUESE\x10\x07\x12\x14\n\x10Language_SPANISH\x10\x08\x12\x14\n\x10Language_RUSSIAN\x10\t\x12\x13\n\x0fLanguage_KOREAN\x10\n\x12\x13\n\x0fLanguage_FRENCH\x10\x0b\x12\x13\n\x0fLanguage_GERMAN\x10\x0c\x12\x14\n\x10Language_TURKISH\x10\r\x12\x12\n\x0eLanguage_HINDI\x10\x0e\x12\x15\n\x11Language_JAPANESE\x10\x0f\x12\x15\n\x11Language_ROMANIAN\x10\x10\x12\x13\n\x0fLanguage_ARABIC\x10\x11\x12\x14\n\x10Language_BURMESE\x10\x12\x12\x11\n\rLanguage_URDU\x10\x13\x12\x14\n\x10Language_BENGALI\x10\x14\x12\x17\n\x12Language_UNLIMITED\x10\xe7\x07*l\n\nTimeOnline\x12\x13\n\x0fTimeOnline_NONE\x10\x00\x12\x16\n\x12TimeOnline_WORKDAY\x10\x01\x12\x16\n\x12TimeOnline_WEEKEND\x10\x02\x12\x19\n\x14TimeOnline_UNLIMITED\x10\xe7\x07*\x84\x01\n\nTimeActive\x12\x13\n\x0fTimeActive_NONE\x10\x00\x12\x16\n\x12TimeActive_MORNING\x10\x01\x12\x18\n\x14TimeActive_AFTERNOON\x10\x02\x12\x14\n\x10TimeActive_NIGHT\x10\x03\x12\x19\n\x14TimeActive_UNLIMITED\x10\xe7\x07*\xf6\x02\n\x11PlayerBattleTagID\x12\x1a\n\x16PlayerBattleTagID_NONE\x10\x00\x12!\n\x1cPlayerBattleTagID_DOMINATION\x10\xcd\x08\x12\x1e\n\x19PlayerBattleTagID_UNCROWN\x10\xce\x08\x12\"\n\x1dPlayerBattleTagID_BESTPARTNER\x10\xcf\x08\x12\x1d\n\x18PlayerBattleTagID_SNIPER\x10\xd0\x08\x12\x1c\n\x17PlayerBattleTagID_MELEE\x10\xd1\x08\x12!\n\x1cPlayerBattleTagID_PEACEMAKER\x10\xd2\x08\x12\x1d\n\x18PlayerBattleTagID_AMBUSH\x10\xd3\x08\x12 \n\x1bPlayerBattleTagID_SHORTSTOP\x10\xd4\x08\x12\x1e\n\x19PlayerBattleTagID_RAMPAGE\x10\xd5\x08\x12\x1d\n\x18PlayerBattleTagID_LEADER\x10\xd6\x08*\xe4\x01\n\tSocialTag\x12\x12\n\x0eSocialTag_NONE\x10\x00\x12\x16\n\x11SocialTag_FASHION\x10\xb5\x10\x12\x15\n\x10SocialTag_SOCIAL\x10\xb6\x10\x12\x16\n\x11SocialTag_VETERAN\x10\xb7\x10\x12\x15\n\x10SocialTag_NEWBIE\x10\xb8\x10\x12\x19\n\x14SocialTag_PLAYFORWIN\x10\xb9\x10\x12\x19\n\x14SocialTag_PLAYFORFUN\x10\xba\x10\x12\x16\n\x11SocialTag_VOICEON\x10\xbb\x10\x12\x17\n\x12SocialTag_VOICEOFF\x10\xbc\x10*\x80\x01\n\nModePrefer\x12\x13\n\x0fModePrefer_NONE\x10\x00\x12\x11\n\rModePrefer_BR\x10\x01\x12\x11\n\rModePrefer_CS\x10\x02\x12\x1c\n\x18ModePrefer_ENTERTAINMENT\x10\x03\x12\x19\n\x14ModePrefer_UNLIMITED\x10\xe7\x07*X\n\x08RankShow\x12\x11\n\rRankShow_NONE\x10\x00\x12\x0f\n\x0bRankShow_BR\x10\x01\x12\x0f\n\x0bRankShow_CS\x10\x02\x12\x17\n\x12RankShow_UNLIMITED\x10\xe7\x07*L\n\x1b\x45LeaderBoardTitleRegionType\x12\x08\n\x04None\x10\x00\x12\x0b\n\x07\x43ountry\x10\x01\x12\x0c\n\x08Province\x10\x02\x12\x08\n\x04\x43ity\x10\x03*6\n\nUnlockType\x12\x13\n\x0fUnlockType_NONE\x10\x00\x12\x13\n\x0fUnlockType_LINK\x10\x01*E\n\x0b\x45quipSource\x12\x14\n\x10\x45quipSource_SELF\x10\x00\x12 \n\x1c\x45quipSource_CONFIDANT_FRIEND\x10\x01*\xfa\x01\n\x08NewsType\x12\x11\n\rNewsType_NONE\x10\x00\x12\x11\n\rNewsType_RANK\x10\x01\x12\x14\n\x10NewsType_LOTTERY\x10\x02\x12\x15\n\x11NewsType_PURCHASE\x10\x03\x12\x18\n\x14NewsType_TREASUREBOX\x10\x04\x12\x16\n\x12NewsType_ELITEPASS\x10\x05\x12\x1a\n\x16NewsType_EXCHANGESTORE\x10\x06\x12\x13\n\x0fNewsType_BUNDLE\x10\x07\x12#\n\x1fNewsType_LOTTERYSPECIALEXCHANGE\x10\x08\x12\x13\n\x0fNewsType_OTHERS\x10\t*]\n\x0bRewardState\x12\x18\n\x14REWARD_STATE_INVALID\x10\x00\x12\x1a\n\x16REWARD_STATE_UNCLAIMED\x10\x01\x12\x18\n\x14REWARD_STATE_CLAIMED\x10\x02\x62\x06proto3')
    _builder.BuildMessageAndEnumDescriptors(DESC1, globals())
    _builder.BuildTopDescriptorsAndMessages(DESC1, 'account_show_pb2', globals())

    # 2. freefire_pb2 (LoginReq, LoginRes)
    DESC2 = _descriptor_pool.Default().AddSerializedFile(b'\n\x0e\x46reeFire.proto\"c\n\x08LoginReq\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0blogin_token\x18\x1d \x01(\t\x12\x1b\n\x13orign_platform_type\x18\x63 \x01(\t\"]\n\x10\x42lacklistInfoRes\x12\x1e\n\nban_reason\x18\x01 \x01(\x0e\x32\n.BanReason\x12\x17\n\x0f\x65xpire_duration\x18\x02 \x01(\r\x12\x10\n\x08\x62\x61n_time\x18\x03 \x01(\r\"f\n\x0eLoginQueueInfo\x12\r\n\x05\x61llow\x18\x01 \x01(\x08\x12\x16\n\x0equeue_position\x18\x02 \x01(\r\x12\x16\n\x0eneed_wait_secs\x18\x03 \x01(\r\x12\x15\n\rqueue_is_full\x18\x04 \x01(\x08\"\xa0\x03\n\x08LoginRes\x12\x12\n\naccount_id\x18\x01 \x01(\x04\x12\x13\n\x0block_region\x18\x02 \x01(\t\x12\x13\n\x0bnoti_region\x18\x03 \x01(\t\x12\x11\n\tip_region\x18\x04 \x01(\t\x12\x19\n\x11\x61gora_environment\x18\x05 \x01(\t\x12\x19\n\x11new_active_region\x18\x06 \x01(\t\x12\x19\n\x11recommend_regions\x18\x07 \x03(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03ttl\x18\t \x01(\r\x12\x12\n\nserver_url\x18\n \x01(\t\x12\x16\n\x0e\x65mulator_score\x18\x0b \x01(\r\x12$\n\tblacklist\x18\x0c \x01(\x0b\x32\x11.BlacklistInfoRes\x12#\n\nqueue_info\x18\r \x01(\x0b\x32\x0f.LoginQueueInfo\x12\x0e\n\x06tp_url\x18\x0e \x01(\t\x12\x15\n\rapp_server_id\x18\x0f \x01(\r\x12\x0f\n\x07\x61no_url\x18\x10 \x01(\t\x12\x0f\n\x07ip_city\x18\x11 \x01(\t\x12\x16\n\x0eip_subdivision\x18\x12 \x01(\t*\xa8\x01\n\tBanReason\x12\x16\n\x12\x42\x41N_REASON_UNKNOWN\x10\x00\x12\x1b\n\x17\x42\x41N_REASON_IN_GAME_AUTO\x10\x01\x12\x15\n\x11\x42\x41N_REASON_REFUND\x10\x02\x12\x15\n\x11\x42\x41N_REASON_OTHERS\x10\x03\x12\x16\n\x12\x42\x41N_REASON_SKINMOD\x10\x04\x12 \n\x1b\x42\x41N_REASON_IN_GAME_AUTO_NEW\x10\xf6\x07\x62\x06proto3')
    _builder.BuildMessageAndEnumDescriptors(DESC2, globals())
    _builder.BuildTopDescriptorsAndMessages(DESC2, 'freefire_pb2', globals())

    # 3. register_req_pb2
    DESC3 = _descriptor_pool.Default().AddSerializedFile(b'\n\x19PlatformRegisterReq.proto\x12\x05proto\"\xa3\x02\n\x13PlatformRegisterReq\x12\x10\n\x08nickname\x18\x01 \x01(\t\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x02 \x01(\t\x12\x0f\n\x07open_id\x18\x03 \x01(\t\x12\x11\n\tavatar_id\x18\x05 \x01(\r\x12\x15\n\rplatform_type\x18\x06 \x01(\r\x12\x17\n\x0fplatform_sdk_id\x18\x07 \x01(\r\x12\x36\n\rusing_version\x18\r \x01(\x0e\x32\x1f.proto.EAuth_ClientUsingVersion\x12\x1e\n\x16platform_register_info\x18\x0e \x01(\x0c\x12\x10\n\x08language\x18\x0f \x01(\t\x12\x12\n\nunknown_16\x18\x10 \x01(\r\x12\x12\n\nunknown_17\x18\x11 \x01(\r*\xae\x01\n\x18\x45\x41uth_ClientUsingVersion\x12\x1b\n\x17\x43lientUsingVersion_NONE\x10\x00\x12\x1d\n\x19\x43lientUsingVersion_NORMAL\x10\x01\x12\x1a\n\x16\x43lientUsingVersion_MAX\x10\x02\x12\x1a\n\x16\x43lientUsingVersion_FFI\x10\x03\x12\x1e\n\x1a\x43lientUsingVersion_MAX_HPE\x10\x04\x62\x06proto3')
    _builder.BuildMessageAndEnumDescriptors(DESC3, globals())
    _builder.BuildTopDescriptorsAndMessages(DESC3, 'register_req_pb2', globals())

    print("✅ All Protos Injected Successfully!")
except Exception as e:
    print("❌ Proto Injection Error:", str(e))

# ==========================================
# 🔍 2. DYNAMICALLY EXTRACT LOADED MESSAGES
# ==========================================
PROTO_MAP = {}
for name, obj in list(globals().items()):
    if inspect.isclass(obj) and issubclass(obj, Message) and name != 'Message':
        PROTO_MAP[name] = obj

print(f"🚀 Loaded {len(PROTO_MAP)} Proto Classes into Memory!")

# ==========================================
# 🔐 3. AES CRYPTO HELPERS
# ==========================================
from Crypto.Cipher import AES
import hashlib

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

def encrypt_aes(data: bytes) -> bytes:
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    pad_len = 16 - (len(data) % 16)
    padded_data = data + bytes([pad_len] * pad_len)
    return cipher.encrypt(padded_data)

def decrypt_aes(data: bytes) -> bytes:
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES.IV)
    decrypted = cipher.decrypt(data)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len]

# ==========================================
# 📋 4. LOGGING SYSTEM
# ==========================================
api_logs = deque(maxlen=200)

def add_log(action, msg_name, status, payload, response=""):
    log_entry = {
        "id": str(int(time.time() * 1000)),
        "time": time.strftime('%H:%M:%S'),
        "action": action,
        "msg_name": msg_name,
        "status": status,
        "payload": payload,
        "response": response
    }
    api_logs.appendleft(log_entry)

# ==========================================
# 🚀 5. API ENDPOINTS
# ==========================================

# Decode endpoint (existing)
@app.route('/api/decode', methods=['POST'])
def decode_proto():
    try:
        data = request.json
        msg_name = data.get('msg_name') 
        b64_data = data.get('data')     

        if not msg_name or msg_name not in PROTO_MAP:
            add_log("DECODE_FAIL", msg_name or "UNKNOWN", 404, b64_data[:50] if b64_data else "None", "Proto message class not found.")
            return jsonify({"error": f"Proto message '{msg_name}' not found."}), 404

        raw_bytes = base64.b64decode(b64_data)
        
        proto_obj = PROTO_MAP[msg_name]()
        proto_obj.ParseFromString(raw_bytes)
        
        result_dict = MessageToDict(proto_obj, preserving_proto_field_name=True)
        
        add_log("DECODE_SUCCESS", msg_name, 200, f"Size: {len(raw_bytes)} bytes", result_dict)
        return jsonify({"success": True, "data": result_dict})

    except Exception as e:
        add_log("DECODE_ERROR", msg_name, 500, b64_data[:50] if b64_data else "", str(e))
        return jsonify({"error": str(e)}), 500

# 🆕 JWT GENERATE ENDPOINT
@app.route('/api/generate-jwt', methods=['POST'])
def generate_jwt():
    try:
        data = request.json
        print(f"[JWT] Received: {data}")
        
        # Extract UID and password
        guest_info = data.get('guest_account_info', {})
        uid = guest_info.get('com.garena.msdk.guest_uid', '')
        password = guest_info.get('com.garena.msdk.guest_password', '')
        
        if not uid or not password:
            return jsonify({"error": "Missing UID or password"}), 400
        
        # Clean password
        password = password.replace(' ', '').replace('\n', '').replace('\r', '')
        
        print(f"[JWT] Generating for UID: {uid}")
        
        # Create LoginReq protobuf
        login_req = PROTO_MAP['LoginReq']()
        login_req.open_id = password
        login_req.open_id_type = "5"  # Guest type
        login_req.login_token = password
        login_req.orign_platform_type = "1"  # Android
        
        # Serialize and encrypt
        serialized = login_req.SerializeToString()
        encrypted = encrypt_aes(serialized)
        
        # Send to Garena server
        headers = {
            'Host': 'loginbp.ggpolarbear.com',
            'Content-Type': 'application/octet-stream',
            'User-Agent': 'FreeFire/2.95.0 Android'
        }
        
        response = requests.post(
            'https://loginbp.ggpolarbear.com/MajorLogin',
            data=encrypted,
            headers=headers,
            timeout=15
        )
        
        if response.status_code != 200:
            add_log("JWT_FAIL", "MajorLogin", response.status_code, f"UID: {uid}", response.text[:200])
            return jsonify({"error": f"Garena server error: {response.status_code}"}), 500
        
        # Decrypt response
        encrypted_resp = response.content
        decrypted = decrypt_aes(encrypted_resp)
        
        # Parse LoginRes
        login_res = PROTO_MAP['LoginRes']()
        login_res.ParseFromString(decrypted)
        
        result = MessageToDict(login_res, preserving_proto_field_name=True)
        
        if result.get('token'):
            add_log("JWT_SUCCESS", "MajorLogin", 200, f"UID: {uid}", "Token generated")
            return jsonify({
                "success": True,
                "token": result['token'],
                "uid": uid,
                "server_url": result.get('server_url', ''),
                "lock_region": result.get('lock_region', 'Global')
            })
        else:
            add_log("JWT_FAIL", "MajorLogin", 500, f"UID: {uid}", "No token in response")
            return jsonify({"error": "No token in response", "response": result}), 500
            
    except Exception as e:
        print(f"[JWT Error] {e}")
        add_log("JWT_ERROR", "MajorLogin", 500, "", str(e))
        return jsonify({"error": str(e)}), 500

# Encode endpoint (for Node.js proxy)
@app.route('/api/encode', methods=['POST'])
def encode_proto():
    try:
        data = request.json
        msg_name = data.get('msg_name')
        json_data = data.get('data')
        
        if not msg_name or msg_name not in PROTO_MAP:
            return jsonify({"error": f"Proto message '{msg_name}' not found."}), 404
        
        proto_obj = PROTO_MAP[msg_name]()
        ParseDict(json_data, proto_obj)
        
        serialized = proto_obj.SerializeToString()
        b64_result = base64.b64encode(serialized).decode('ascii')
        
        add_log("ENCODE_SUCCESS", msg_name, 200, json_data, f"Size: {len(serialized)} bytes")
        return jsonify({"success": True, "data": b64_result})
        
    except Exception as e:
        add_log("ENCODE_ERROR", msg_name, 500, "", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api/logs/sync', methods=['GET'])
def get_logs():
    return jsonify(list(api_logs))

# ==========================================
# 👑 6. PYTHON API DASHBOARD
# ==========================================
@app.route('/', methods=['GET'])
def dashboard():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>👑 KING NEXUS | Python Core</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            * { font-family: 'Inter', sans-serif; }
            body { background: linear-gradient(135deg, #0a0a2e 0%, #1a0a3e 50%, #0a0a2e 100%); min-height: 100vh; }
            .glass-panel { background: rgba(15, 15, 35, 0.7); backdrop-filter: blur(12px); border: 1px solid rgba(139, 92, 246, 0.3); transition: all 0.3s; }
            .glass-panel:hover { border-color: rgba(139, 92, 246, 0.7); box-shadow: 0 0 25px rgba(139, 92, 246, 0.2); }
            .glow-text { text-shadow: 0 0 20px rgba(139, 92, 246, 0.5); }
            .btn-primary { background: linear-gradient(135deg, #a855f7, #7c3aed); transition: all 0.2s; }
            .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.4); }
            ::-webkit-scrollbar { width: 4px; }
            ::-webkit-scrollbar-track { background: #0a0a0f; }
            ::-webkit-scrollbar-thumb { background: #8b5cf6; border-radius: 10px; }
            pre { white-space: pre-wrap; word-wrap: break-word; font-size: 10px; }
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="max-w-7xl mx-auto">
            <div class="glass-panel rounded-2xl p-6 mb-6">
                <div class="flex flex-col md:flex-row justify-between items-center gap-4">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                            <i class="fab fa-python text-white text-2xl"></i>
                        </div>
                        <div>
                            <h1 class="text-3xl md:text-4xl font-black glow-text" style="background: linear-gradient(135deg, #a855f7, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                                KING NEXUS | PYTHON CORE
                            </h1>
                            <p class="text-xs text-purple-300/80">Protobuf Decode/Encode Engine + JWT Generator</p>
                        </div>
                    </div>
                    <div class="text-xs bg-purple-900/30 border border-purple-500/50 px-4 py-2 rounded-full text-purple-300">
                        <i class="fas fa-database mr-1"></i> PROTO LOADED: """ + str(len(PROTO_MAP)) + """
                    </div>
                </div>
            </div>
            
            <div id="logs-container" class="space-y-3"></div>
        </div>

        <script>
            async function fetchLogs() {
                try {
                    const res = await fetch('/api/logs/sync');
                    const logs = await res.json();
                    const container = document.getElementById('logs-container');
                    if (logs.length === 0) {
                        container.innerHTML = '<div class="text-center text-purple-400/50 py-12"><i class="fas fa-inbox text-3xl mb-2"></i><p>No logs yet. Use /api/decode or /api/generate-jwt</p></div>';
                        return;
                    }
                    container.innerHTML = logs.map(l => {
                        let isError = l.status >= 400;
                        let statusColor = isError ? 'text-red-400 bg-red-900/30' : 'text-green-400 bg-green-900/30';
                        let statusIcon = isError ? 'fa-times-circle' : 'fa-check-circle';
                        return `
                        <div class="glass-panel rounded-xl p-4">
                            <div class="flex flex-wrap justify-between items-center mb-3 pb-2 border-b border-purple-500/20 gap-2">
                                <div class="flex items-center gap-2 flex-wrap">
                                    <span class="bg-purple-900/40 text-purple-300 px-2 py-1 rounded text-xs font-bold">${l.action}</span>
                                    <span class="text-white text-xs font-mono">${l.msg_name}</span>
                                    <span class="text-gray-500 text-xs">${l.time}</span>
                                </div>
                                <span class="${statusColor} px-2 py-1 rounded text-xs font-bold flex items-center gap-1">
                                    <i class="fas ${statusIcon}"></i> ${l.status}
                                </span>
                            </div>
                            <div class="grid grid-cols-1 lg:grid-cols-2 gap-3">
                                <div>
                                    <div class="text-purple-400/70 text-xs mb-1">📤 REQUEST</div>
                                    <pre class="bg-black/50 rounded-lg p-2 text-purple-300/80 overflow-x-auto max-h-32">${typeof l.payload === 'object' ? JSON.stringify(l.payload, null, 2) : l.payload || '{}'}</pre>
                                </div>
                                <div>
                                    <div class="text-purple-400/70 text-xs mb-1">📥 RESPONSE</div>
                                    <pre class="bg-black/50 rounded-lg p-2 ${isError ? 'text-red-300/80' : 'text-green-300/80'} overflow-x-auto max-h-32">${typeof l.response === 'object' ? JSON.stringify(l.response, null, 2) : l.response || '{}'}</pre>
                                </div>
                            </div>
                        </div>`;
                    }).join('');
                } catch(e) { console.error(e); }
            }
            setInterval(fetchLogs, 1500);
            fetchLogs();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    print("🌸 KING NEXUS Python Core Running on http://localhost:5000")
    print("📡 Endpoints: /api/decode, /api/encode, /api/generate-jwt")
    app.run(debug=True, host='0.0.0.0', port=5000)