# -*- coding: utf-8 -*-
import unittest
import logging
import pymongo

from apps.oclib.client import Mongo
from nose.tools import *

DBNAME = 'test_maxstrike'

CONFIG_FILE = {
##############################提示语配置#############################################
#最外层key为相应的功能，里面的key为相对应的提示场合
#####################################################################################
    #//常用
    "config_id": 123456,
    "stone": unicode('宝石','utf-8'),
    "invCode_error": unicode('邀请码错误','utf-8'),
    "invCode_error_dlg": unicode('邀请码输入错误，是否重新输入邀请码？','utf-8'),
    "gameEnd": unicode('战斗结束','utf-8'),
    "publishWeiboTip": unicode('分享有礼哦~','utf-8'),
    "publishTip": unicode('发布','utf-8'),
    "backTip": unicode('返回','utf-8'),
    "exit": unicode('退出','utf-8'),
    "sureTip": unicode('确定','utf-8'),
    "cancelTip": unicode('取消','utf-8'),
    "acceptTip": unicode('接受','utf-8'),
    "refuseTip": unicode('拒绝','utf-8'),
    "deleteTip": unicode('删除','utf-8'),
    "alert": unicode('警告','utf-8'),
    "nothing": unicode('无','utf-8'),
    "max": unicode('最大','utf-8'),
    "round": unicode('回合','utf-8'),
    "lv": unicode('Lv','utf-8'),
    "skill_lv": unicode('技能Lv','utf-8'),
    "hp": unicode('HP','utf-8'),
    "attack": unicode('攻击','utf-8'),
    "recover": unicode('回复','utf-8'),
    "cost": unicode('统御力','utf-8'),
    "coin": unicode('铜钱','utf-8'),
    "coin_need": unicode('需要铜钱','utf-8'),
    "food": unicode('素材','utf-8'),
    "select": unicode('选择','utf-8'),
    "card_info": unicode('武将情报','utf-8'),
    "back": unicode('返回','utf-8'),
    "left": unicode('剩余','utf-8'),
    "left_day": unicode('天','utf-8'),
    "left_hour": unicode('小时','utf-8'),
    "left_minute": unicode('分钟','utf-8'),
    "strength": unicode('体力值','utf-8'),
    "bureau": unicode('局数','utf-8'),
    "army_friend": unicode('友军','utf-8'),
    "army_just": unicode('义军','utf-8'),
    "level": unicode('等级','utf-8'),
    "help_point": unicode('援军点','utf-8'),
    "price": unicode('价格','utf-8'),
    "exp_need": unicode('下次升级经验','utf-8'),
    "expansion": unicode('扩充','utf-8'),
    "sale": unicode('卖出','utf-8'),
    "loading_title": unicode('通信中...','utf-8'),
    "loading_prompt": unicode('*電波通信中，您的網路可能有點障礙，請耐心等待或者換個良好的網路環境。','utf-8'),
    "net_error": unicode('通信错误','utf-8'),
    "net_again": unicode('点击确定重试','utf-8'),
    "propTip": unicode('属性','utf-8'),
    "attackTip": unicode('攻击力','utf-8'),
    "skillTip": unicode('技能','utf-8'),
    "noTip": unicode('无','utf-8'),
    "exit_prompt": unicode('退出战斗，您之前战斗获得的铜钱、经验、令牌都将无法获得，确定要退出么？','utf-8'),
    "crashTitle": unicode('意外报错','utf-8'),
    "crashInfo": unicode('程序发生异常，将会退出游戏。为了让您更好的体验游戏乐趣，建议运行游戏时关闭其他的应用程序。希望您可以将错误报告发送邮件给到我们，我们会不断改进我们的产品，给您更好的游戏体验！','utf-8'),
    #/#/菜单
    "tab1": unicode('战场','utf-8'),
    "tab2": unicode('武将','utf-8'),
    "tab3": unicode('求将','utf-8'),
    "tab4": unicode('商店','utf-8'),
    "tab5": unicode('好友','utf-8'),
    "tab6": unicode('攻略','utf-8'),

    #/#/微博分享
    "weibo_shareInviteCode_success": unicode('分享成功','utf-8'),
    "weibo_shareInviteCode_sina_1": unicode('邀请码已经成功分享到了','utf-8'),
    "weibo_shareInviteCode_sina_2": unicode('的微博','utf-8'),
    "weibo_shareInviteCode_qq_1": unicode('邀请码已经成功分享到了','utf-8'),
    "weibo_shareInviteCode_qq_2": unicode('的腾讯微博','utf-8'),
    "weibo_authened": unicode('账号绑定','utf-8'),
    "weibo_authened_info": unicode('尚未绑定账号,请到攻略界面绑定,即可分享，分享得大礼','utf-8'),
    "weibo_inviteCode_1": unicode('我迷上了《逆转三国》，真的很上瘾呢，赶快来和我一起玩吧！我的邀请码是','utf-8'),
    "weibo_inviteCode_2": unicode('，通过邀请码进入游戏，就可获得很多奖励哦！http://itunes.apple.com/cn/app/ni-zhuan-san-guo/id533744303?mt=8','utf-8'),

    #/#/导航滚动文字
    "naviText_arena_1": unicode('点击战场就可以开始冒险啦！','utf-8'),
    "naviText_arena_2": unicode('在战场里战斗胜利可能会获得更多武将!','utf-8'),
    "naviText_floor_1": unicode('请选择要进入的战场。','utf-8'),
    "naviText_floor_2": unicode('每场战斗都有很多局，同时也会消耗一定的体力值。','utf-8'),
    "naviText_room_1": unicode('请选择需要的援军主将，点击援军主将——查看武将详情可查看详细资料。','utf-8'),
    "naviText_room_2": unicode('长按武将头像图标，可以查看武将详情。','utf-8'),
    "naviText_room_3": unicode('只有友军的主将技能会被发动，赶紧添加更多好友吧。','utf-8'),
    "naviText_specialArena": unicode('请注意特殊战场关卡的持续时间！','utf-8'),
    "naviText_general_1": unicode('包括武将的编队，以及强化、转生、出售等操作。','utf-8'),
    "naviText_general_2": unicode('强化、转生你的武将，都可以使他们变得更强。','utf-8'),
    "naviText_teamInfo_1": unicode('编队里至少要有一名主将。队伍的统御力会随玩家的升级而扩大。','utf-8'),
    "naviText_teamInfo_2": unicode('编队里所带的武将统御力总和不能超过玩家的队伍统御力。','utf-8'),
    "naviText_teamInfo_3": unicode('点击重置编队按钮可以移除所有的副将。点击队伍位置可以选取、替换武将，更改队伍阵容。','utf-8'),
    "naviText_selectCard_1": unicode('请选择武将加入队伍。统御力足够、可以选取的武将会显亮。','utf-8'),
    "naviText_selectCard_2": unicode('点击右上角排序，可以将所有武将按照一定的顺序排列。','utf-8'),
    "naviText_selectCard_3": unicode('长按武将头像图标，可以查看武将详情。','utf-8'),
    "naviText_pwUpSel_1": unicode('请选择需要被强化的武将，强化后该武将实力会大幅提升哦。','utf-8'),
    "naviText_pwUpSel_2": unicode('长按武将头像图标，可以查看武将详情。','utf-8'),
    "naviText_pwUpBase_1": unicode('长按武将头像图标，可以查看武将详情。','utf-8'),
    "naviText_pwUpBase_2": unicode('请选择强化素材，强化会消耗一定的铜钱，基础武将的性能会得到加强，同时素材武将会消失。','utf-8'),
    "naviText_pwUpBase_3": unicode('点击追加按钮选择强化素材，最少1只，最多选取5只。','utf-8'),
    "naviText_pwUpFood_1": unicode('素材武将会增强基础武将的实力，强化后素材武将会消失。','utf-8'),
    "naviText_pwUpFood_2": unicode('建议不要轻易将3星以及以上的武将选做素材消耗掉，他们都非常珍稀哦。','utf-8'),
    "naviText_pwUpFood_3": unicode('长按武将头像图标，可以查看武将详情。','utf-8'),
    "naviText_evoSel_1": unicode('武将可以转生为更强力的武将。','utf-8'),
    "naviText_evoSel_2": unicode('长按武将头像图标，可以查看武将详情。','utf-8'),
    "naviText_evoSel_3": unicode('点击右上角排序，可以将所有武将按照一定的顺序排列。','utf-8'),
    "naviText_evo_1": unicode('军营中已有的转生道具会高亮，未获得的则是灰暗的。','utf-8'),
    "naviText_evo_2": unicode('只有所有的转生道具都齐全且基础武将达到当前最大等级时，才可转生。','utf-8'),
    "naviText_evo_3": unicode('转生后，所有的转生道具都会消失。','utf-8'),
    "naviText_sell_1": unicode('最多5只武将可以一起被同时出售。','utf-8'),
    "naviText_sell_2": unicode('出售会获得一定数量的铜钱。','utf-8'),
    "naviText_sell_3": unicode('建议不要轻易出售3星及以上的武将，他们都非常珍稀哦。','utf-8'),
    "naviText_package_1": unicode('点击右上角排序，可以将所有武将按照一定的顺序排列。','utf-8'),
    "naviText_package_2": unicode('点击武将头像，可以直接查看到武将的详细信息。','utf-8'),
    "naviText_package_3": unicode('如需扩充军营，可以进入商店去扩充。','utf-8'),
    "naviText_shop": unicode('在这里你可以进行元宝的购买、体力恢复、军营扩充的操作。','utf-8'),
    "naviText_coin_1": unicode('在这里能够通过app store购买元宝','utf-8'),
    "naviText_coin_2": unicode('元宝可以用来战斗失败的复活、体力值的恢复以及军营的扩充等操作。','utf-8'),
    "naviText_coin_3": unicode('购买的元宝越多，价钱越优惠哦。','utf-8'),
    "naviText_staminaRecover": unicode('使用6个元宝就无需等待，可以恢复全部的体力值啦。','utf-8'),
    "naviText_boxEnlarge_1": unicode('使用6个元宝就可以扩充军营5个位置。','utf-8'),
    "naviText_boxEnlarge_2": unicode('军营位置越多，就可以留下越多的武将哦。','utf-8'),
    "naviText_gacha_1": unicode('请选择需要进行的求将类型。求将里无需战斗就可以获得一些武将啦！','utf-8'),
    "naviText_gacha_2": unicode('求神将可以获得3星以及以上的珍稀武将哦！','utf-8'),
    "naviText_friend": unicode('在这里可以进行查看好友、搜索好友、查看好友申请和邀请好友等操作。','utf-8'),
    "naviText_friendList_1": unicode('点击删除，可以删除好友。','utf-8'),
    "naviText_friendList_2": unicode('好友越多，可以借得好友主将越多，游戏也会更容易轻松！','utf-8'),
    "naviText_friendSearch_1": unicode('可以查看自己的游戏ID，将自己的ID分享给好友一起游戏吧。','utf-8'),

    "naviText_friendSearch_2": unicode('可以通过搜索已知的ID搜索到好友，一起在游戏中并肩作战啦。','utf-8'),
    "naviText_friendInfo": unicode('请求通过后，该用户会被直接添加进好友列表。','utf-8'),
    "naviText_friendInvitate": unicode('发送邀请码给好友共同游戏，双方都会获得额外奖励哦。','utf-8'),
    "naviText_other": unicode('可以查看武将图鉴、更改游戏设定等功能。','utf-8'),
    "naviText_collection_1": unicode('这里可以查看已经遇到过的武将。','utf-8'),
    "naviText_collection_2": unicode('曾经获得过的武将会高亮显示。','utf-8'),
    "naviText_collection_3": unicode('未曾获得过得武将不会被显示。','utf-8'),
    "naviText_setting": unicode('可以进行音乐、音效的设置等操作。','utf-8'),
    "naviText_raider": unicode('这里有游戏的攻略文档，会帮你更好更顺利的进行游戏。','utf-8'),
    "naviText_about": unicode('相关制作人员。','utf-8'),
    "naviText_weibo_1": unicode('将账号绑定，会帮你备份游戏数据，避免误删丢失。','utf-8'),
    "naviText_weibo_2": unicode('绑定账号后，游戏里的昵称会与绑定账号的用户名同步。','utf-8'),
    "naviText_teamConfirm":unicode('没问题的话，马上开始挑战吧！','utf-8'),
    "naviText_gacha_liang":unicode('千金易得，良将难求，试试手气吧。','utf-8'),
    "naviText_gacha_shen":unicode('逆转战局，稀有神将，你值得拥有！','utf-8'),
    "naviText_friendEnlarge":unicode('可以扩大好友上限了呦。','utf-8'),


    #/#/战场中的文字
    "arenaTip1": unicode('体力不足','utf-8'),
    "arenaTip2": unicode('要用元宝回复体力吗？','utf-8'),
    "arenaTip3": unicode('试炼城门','utf-8'),
    "arenaTip4": unicode('您现有元宝','utf-8'),
    "arenaTip5": unicode('个','utf-8'),
    "arenaTip6": unicode('恢复体力需消耗元宝','utf-8'),
    "arenaTip7": unicode('请先去商店购买元宝','utf-8'),
    "arenaTip8": unicode('元宝不足','utf-8'),
    "arenaTip9": unicode('特殊战场','utf-8'),
    "arenaTip10": unicode('体力上限不足','utf-8'),
    "arenaTip11": unicode('通过提升等级,增加体力值上限！','utf-8'),
    "arena_othercant": unicode('义军无法发动主将技','utf-8'),
    "org_othercant": unicode('同盟战没有义军','utf-8'),
    "arena_fightcfm":unicode('确认挑战','utf-8'),
    "arena_teamcfm":unicode('队伍确认','utf-8'),
    "org_teamcfm":unicode('确认编队','utf-8'),

    #/*cashInLayer*#/
    "cashInLayerTip1": unicode('获得武将','utf-8'),
    "cashInLayerTip2": unicode('您的统御力增加了 ','utf-8'),
    "cashInLayerTip3": unicode(' 上升到了 ','utf-8'),
    "cashInLayerTip4": unicode('体力值完全回复','utf-8'),
    "cashInLayerTip5": unicode('体力上限增加了 ','utf-8'),
    "cashInLayerTip6": unicode('您获得了系统奖励:元宝','utf-8'),
    "cashInLayerTip7": unicode('系统赠送:','utf-8'),
    "cashInLayerTip8": unicode('个元宝','utf-8'),
    "cashInLayerTip9": unicode('获得奖励','utf-8'),
    "cashInLayerTip10": unicode('获得金钱:','utf-8'),
    "cashInLayerTip11": unicode('下次升级:','utf-8'),
    #/*AddFriend*#/

    "addFriendTip1": unicode('获得','utf-8'),
    "addFriendTip2": unicode('点援军点数','utf-8'),
    "addFriendTip3": unicode('援军点数现在值','utf-8'),
    "addFriendTip4": unicode('援军点数结算','utf-8'),
    "addFriendTip5": unicode('要加为好友吗？','utf-8'),


    #/#/军营中的文字
    "general_teamInf": unicode('编队','utf-8'),
    "general_pwUp": unicode('强化','utf-8'),
    "general_evolution": unicode('转生','utf-8'),
    "general_sell": unicode('出售','utf-8'),
    "general_package": unicode('军营','utf-8'),

    "teamInf_title": unicode('编队','utf-8'),
    "teamInf_reset": unicode('编队\n重置','utf-8'),
    "teamInf_prompt1": unicode('试着将指定的暗属性的武将加入到队伍里吧','utf-8'),
    "teamInf_prompt2": unicode('好了，现在您的队伍已经具备5个属性的武将了，这样消除任意颜色的宝石都会有相应的武将发动攻击了。','utf-8'),
    "teamInf_prompt3": unicode('困难的关卡难以通过？说明您的队伍实力不够强，这时候需要提高您队伍的实力，最简单的方法之一就是强化您队伍里的武将了。','utf-8'),
    "teamInf_reset_alert": unicode('所有副将都会被移除，确定要重置吗？','utf-8'),

    "pwUp_title": unicode('强化','utf-8'),
    "pwUp_exp_current": unicode('现在的经验值','utf-8'),
    "pwUp_exp_need": unicode('下次升级还需经验','utf-8'),
    "pwUp_exp_get": unicode('获得经验','utf-8'),
    "pwUp_exp_will_get": unicode('将获得经验','utf-8'),
    "pwUp_success_normal": unicode('成功','utf-8'),
    "pwUp_success_big": unicode('大成功经验值1.5倍','utf-8'),
    "pwUp_success_super": unicode('超成功经验值2.0倍','utf-8'),
    "pwUp_lv_max": unicode('到最大等级啦!!!','utf-8'),
    "pwUp_button_add": unicode('追加','utf-8'),
    "pwUp_button_pwUp": unicode('开始强化','utf-8'),

    "evolution_title": unicode('转生','utf-8'),
    "evolution_lock_alert": unicode('转生素材中有素材被加锁，无法转生。','utf-8'),

    "sell_title": unicode('武将出售','utf-8'),
    "sell_alert_1": unicode('把选择的武将一起卖掉。卖价','utf-8'),
    "sell_alert_2": unicode('。是否确定卖出？','utf-8'),
    "sell_alert_stars": unicode('有3星或以上的稀有武将被选中确定要出售吗？','utf-8'),
    "sell_all_price": unicode('总计卖价','utf-8'),
    "sell_select_num": unicode('选择个数','utf-8'),

    "package_title": unicode('军营','utf-8'),
    "package_base_title": unicode('基础武将选择','utf-8'),
    "package_food_title": unicode('素材选择','utf-8'),
    "package_remove": unicode('移除','utf-8'),
    "package_using": unicode('使用中','utf-8'),
    "package_contain_num": unicode('容纳数','utf-8'),

    "range_title": unicode('排序\n更改','utf-8'),
    "range_attack": unicode('顺序\n攻击','utf-8'),
    "range_get": unicode('顺序\n入手','utf-8'),
    "range_hp": unicode('顺序\n血量','utf-8'),
    "range_property": unicode('顺序\n属性','utf-8'),
    "range_recover": unicode('顺序\n回复','utf-8'),
    "range_lock": unicode('顺序\n加锁','utf-8'),
    "range_plus": unicode('顺序\n武将+','utf-8'),
    "range_cost": unicode('顺序\n统御力','utf-8'),
    "range_lt":unicode('顺序\n登陆','utf-8'),

    "sortbtn_prop":unicode('属性','utf-8'),
    "sortbtn_atk":unicode('攻击','utf-8'),
    "sortbtn_hp":unicode('血量','utf-8'),
    "sortbtn_rcv":unicode('回复','utf-8'),
    "sortbtn_get":unicode('入手','utf-8'),
    "sortbtn_lock":unicode('加锁','utf-8'),
    "sortbtn_plus":unicode('武将+','utf-8'),
    "sortbtn_cost":unicode('统御力','utf-8'),

    #/#/求将
    "gachaTip1": unicode('求良将','utf-8'),
    "gachaTip2": unicode('求将','utf-8'),
    "gachaTip3": unicode('求神将','utf-8'),
    "gachaTip4": unicode('基本介绍结束了！如果还有不明白的地方可以点击其他里的帮助文档。现在，开始逆转三国吧！','utf-8'),
    "gachaTip5": unicode('10连抽结果','utf-8'),
    "gachaTip6": unicode('10连抽结果','utf-8'),

    #/*gachaDlg*#/
    "gachaDlgTip1": unicode('每次求良将需花费','utf-8'),
    "gachaDlgTip2": unicode('点援军点数','utf-8'),
    "gachaDlgTip3": unicode('您现在的援军点数是:','utf-8'),
    "gachaDlgTip4": unicode('您的援军点数可以进行','utf-8'),
    "gachaDlgTip5": unicode('次求良将','utf-8'),
    "gachaDlgTip6": unicode('必定会抽出3星及以上的武将,一次求将需消耗','utf-8'),
    "gachaDlgTip7": unicode('个元宝','utf-8'),
    "gachaDlgTip8": unicode('您现在有','utf-8'),
    "gachaDlgTip9": unicode('进行一次求神将','utf-8'),
    "gachaDlgTip10": unicode('您的元宝不够一次求神将','utf-8'),
    "gachaDlgTip11": unicode('购买','utf-8'),
    "gachaDlgTip12": unicode('必定会抽出3星及以上的武将,连续抽11次需消耗%d个元宝','utf-8'),
    "gachaDlgTip13": unicode('连续进行11次求神将','utf-8'),
    "gachaDlgTip14": unicode('良将10连抽','utf-8'),
    "gachaDlgTip15": unicode('神将11抽（赠1次）','utf-8'),
    "gachaDlgTip16": unicode('剩余元宝不足，请先购买','utf-8'),
    "gachaDlgTip17": unicode('求一次','utf-8'),

    #/#/商店
    "shopTip_mainMenu": unicode('尝试下，用现有的元宝来求神将吧！元宝求将会帮你获得珍稀武将!','utf-8'),
    "shopTip1": unicode('元宝商店','utf-8'),
    "shopTip2": unicode('体力回复','utf-8'),
    "shopTip3": unicode('军营扩充','utf-8'),
    "shopTip4": unicode('体力已满无须回复!','utf-8'),
    "shopTip5": unicode('使用','utf-8'),
    "shopTip6": unicode('个元宝可回复全部体力','utf-8'),
    "shopTip7": unicode('元宝不足!进入元宝商店可购买元宝!','utf-8'),
    "shopTip8": unicode('使用','utf-8'),
    "shopTip9": unicode('个元宝,可以使军营扩容','utf-8'),
    "shopTip10": unicode('个位置,现在最大','utf-8'),
    "shopTip11": unicode('元宝不足!进入元宝商店可购买元宝!','utf-8'),
    "shopTip12": unicode('体力值已回复!','utf-8'),
    "shopTip13": unicode('军营已经扩大!','utf-8'),
    "shopTip14": unicode('购买','utf-8'),
    "shopTip15": unicode('购买失败!','utf-8'),
    "shopTip16": unicode('APPStore暂时不能访问,请稍后重试!','utf-8'),
    "shopTip17": unicode('个元宝','utf-8'),
    "shopTip18": unicode('您当前积分：%d，\n您已经兑换了%d个元宝，\n您最多可以兑换%d个元宝，\n兑换比例：%d积分=1元宝\n积分自动转换成元宝','utf-8'),
    "shopTip19": unicode('抢','utf-8'),
    "shopTip21":unicode('好友扩充','utf-8'),
    "shopTip20":unicode('使用%d个元宝，可以增加%d个好友上限，你已经扩充%d个好友，最大可以扩充%d好友','utf-8'),
    "shopTip22":unicode('好友上限已经扩充','utf-8'),
    "shopTip23":unicode('已到最大扩充好友数,无需扩充','utf-8'),
    "shopTip24":unicode('刷新','utf-8'),
    "shopTip25":unicode('查看活动详情','utf-8'),
    "shopTip26":unicode('当前完成的订单数: %d','utf-8'),
    "shopTip27":unicode('您已完成的订单排序:','utf-8'),
    "shopTip28":unicode('活动期间累计充值: %d元','utf-8'),

    #/#/好友
    "FriendTip1": unicode('好友','utf-8'),
    "FriendTip2": unicode('我的好友','utf-8'),
    "FriendTip3": unicode('搜索好友','utf-8'),
    "FriendTip4": unicode('好友请求','utf-8'),
    "FriendTip5": unicode('暂无好友请求!','utf-8'),
    "FriendTip6": unicode('暂无好友!!','utf-8'),
    "FriendTip7": unicode('邀请好友','utf-8'),
    "LastLoginD": unicode('上次登录: %d天前','utf-8'),
    "LastLoginH": unicode('上次登录: %d小时前','utf-8'),
    "LastLoginM": unicode('上次登录: %d分钟前','utf-8'),

    #/*searchFriend*#/
    "searchFriendTip1": unicode('我的ID:','utf-8'),
    "searchFriendTip2": unicode('输入朋友的ID加为好友吧!','utf-8'),
    "searchFriendTip3": unicode('搜索','utf-8'),
    #/*friendInfoLayer*#/
    "friendInfoLayerTip1": unicode('接受友军','utf-8'),
    "friendInfoLayerTip2": unicode('是否接受友军的邀请?','utf-8'),
    "friendInfoLayerTip3": unicode('删除友军','utf-8'),
    "friendInfoLayerTip4": unicode('是否删除该友军?','utf-8'),
    "friendInfoLayerTip5": unicode('拒绝友军','utf-8'),
    "friendInfoLayerTip6": unicode('是否确定拒绝添加该友军?','utf-8'),
    "friendInfoLayerTip7": unicode('友军添加','utf-8'),
    "friendInfoLayerTip8": unicode('是否添加该将士为你的友军?','utf-8'),
    #/#/其他
    "otherMainTip1": unicode('武将图鉴','utf-8'),
    "otherMainTip2": unicode('设置','utf-8'),
    "otherMainTip3": unicode('游戏攻略','utf-8'),
    "otherMainTip4": unicode('关于','utf-8'),
    "otherMainTip5": unicode('绑定新浪微博','utf-8'),
    "otherMainTip6": unicode('绑定腾讯账号','utf-8'),
    "otherMainTip7": unicode('账号绑定成功!','utf-8'),
    "otherMainTip8": unicode('切换账号','utf-8'),
    "otherMainTip56": unicode('暂不绑定','utf-8'),
    #/*设置*#/
    "settingTip1": unicode('背景音乐','utf-8'),
    "settingTip2": unicode('音效','utf-8'),
    "settingTip4": unicode('技能特效','utf-8'),
    "settingTip3": unicode('获得武将。您可以将它加入队伍，帮您更好地战斗！','utf-8'),

    #/#/fightScene
    #/*cardInfoDlg*#/
    "cardInfoDlgTip1": unicode('卡牌名','utf-8'),
    "cardInfoDlgTip2": unicode('剩余','utf-8'),
    "cardInfoDlgTip3": unicode('回合','utf-8'),
    #/*skillDlg*#/
    "skillDlgTip1": unicode('技能名称','utf-8'),
    "skillDlgTip2": unicode('技能描述','utf-8'),
    "skillDlgTip3": unicode('确定要发动技能么？','utf-8'),
    "skillDlgTip4": unicode('回合后可用','utf-8'),
    #/*CTipsDlg*#/
    "tipsDlgTip1": unicode('同色宝石横排或者竖排3个或3个以上时就可以消除，多动动脑筋吧！','utf-8'),
    "tipsDlgTip2": unicode('宝石和武将有5种属性。火、水、木3种属性相互牵制。他们都存在有利和不利的属性。光和暗之间则是互相克制的关系。','utf-8'),
    "tipsDlgTip3": unicode('消除心型宝石，可以回复一定HP值。','utf-8'),
    "tipsDlgTip4": unicode('移动宝石后算一回合。','utf-8'),
    "tipsDlgTip5": unicode('经过一定回合后，敌方武将会攻击哦。','utf-8'),
    "tipsDlgTip6": unicode('所持的武将可以自由组成队伍。队伍内的武将最多5只。','utf-8'),
    "tipsDlgTip7": unicode('进入战场会消耗体力值，不同战场消耗的体力值也是不同的。','utf-8'),
    "tipsDlgTip8": unicode('你觉得队伍平衡么，无法通关的话重新考虑队伍吧！','utf-8'),
    "tipsDlgTip9": unicode('武将要升级到最强级别？去强化转生不同的武将吧！','utf-8'),
    "tipsDlgTip10": unicode('如何才能打出连击？宝石移动时要使不同颜色的宝石连续消除才可以哟~','utf-8'),
    "tipsDlgTip11": unicode('敌方武将过多的时候，同一颜色的宝石消除5个或5个以上，对应宝石颜色属性的武将会对敌方所有武将发动攻击！！','utf-8'),
    "tipsDlgTip12": unicode('战场内我方武将发光时，就是技能发动了！好好利用它会有优势！','utf-8'),
    "tipsDlgTip13": unicode('拥有主将技能的武将，队伍内充当主将时可以发挥其特殊的能力哟！','utf-8'),
    "tipsDlgTip14": unicode('宝石同时消除多行，武将的攻击力会提升哟！','utf-8'),
    "tipsDlgTip15": unicode('敌方武将带有防御力时，伤害会降低。但是所持武将拥有防御击破技能会有帮助！','utf-8'),
    "tipsDlgTip16": unicode('元宝的作用可是很多的哟！可以用来求将、恢复体力值、扩充军营等！','utf-8'),
    "tipsDlgTip17": unicode('触摸选取敌方的武将，可以对该武将进行攻击！','utf-8'),
    "tipsDlgTip18": unicode('宝石的移动有时间限制，注意宝石上出现的倒计时，会显示剩余时间的。','utf-8'),
    "tipsDlgTip19": unicode('有厉害的好友协助，玩游戏事半功倍。','utf-8'),
    "tipsDlgTip20": unicode('每天玩游戏的话，会得到铜钱和援军点数，要天天上线拿奖励哦。总计上线奖励1天玩1次，总计上线可以累积哦。总计上线累积到一定的数量后会得到奖励。','utf-8'),
    "tipsDlgTip21": unicode('等级提升后，体力，统御力，好友上限数也会上升。','utf-8'),
    "tipsDlgTip22": unicode('援军的武将，也可以使用主将技能哦，还能得到更多的援军点！','utf-8'),
    "tipsDlgTip23": unicode('某些武将级别达到最大时，使用转生道具可以使武将转生到更高级的形态哦!','utf-8'),
    "tipsDlgTip24": unicode('强化武将的时候小心不要把转生道具用来强化哟！','utf-8'),
    "tipsDlgTip25": unicode('援军点数一天获赠一次。同一位好友一天内也能得到一次援军点数。','utf-8'),
    "tipsDlgTip26": unicode('同属性的武将间强化，会奖励更多经验值哟！','utf-8'),
    "tipsDlgTip27": unicode('武将级别最大时，使用转生道具可以使武将进化到更高级的形态哦!','utf-8'),
    "tipsDlgTip28": unicode('持有相同技能的武将间合成，技能可以强化哦！','utf-8'),
    "tipsDlgTip29": unicode('会举办各种限时战场活动哦！请注意关注！','utf-8'),
    "tipsDlgTip30": unicode('同一位援军一天只能获得一次援军点数。','utf-8'),
    "tipsDlgTip31": unicode('好的武将除了拥有主动武将技能，还拥有被动的主将技能。 ','utf-8'),
    "tipsDlgTip32": unicode('游戏中的宝石可以随意移动哟~多动动脑筋打出更多的连击吧~','utf-8'),
    "tipsDlgTip33": unicode('找不到道具在那个战场里获得？那就多关心每周的活动战场吧，会有专门获得道具的战场。','utf-8'),
    #/*fightMngr*#/
    "fightMngrTip1": unicode('局数','utf-8'),
    #/*player*#/
    "playerTip1": unicode('现在介绍游戏的玩法：横排或竖排的同色宝石达到3个或以上时可以被消除！消除后，相同颜色对应的武将会发动对敌人的攻击！','utf-8'),
    "playerTip2": unicode('红色宝石成功消除了.接着我们来介绍一下属性相克：针对不同颜色的敌方武将，用相克属性攻击敌人可造成额外伤害！消除蓝色宝石，对红色敌军造成2倍伤害！水→火→木→水  光←→暗','utf-8'),

    "playerTip3": unicode('这次介绍全体攻击。5个以上相同宝石的消除，可以发动对所有敌人的攻击。','utf-8'),

    "playerTip4": unicode('现在我们来了解一下敌方武将的攻击。注意敌人头上的回合数变化哦','utf-8'),
    "playerTip5": unicode('敌人攻击你啦！血量被减少了！消除爱心宝石可以补充血量哦！','utf-8'),
    "playerTip6": unicode('最后教你使用必杀技了！武将里面，有些可以使用强力技能哟！','utf-8'),
    "playerTip7": unicode('宝石消除几次后，武将发光上升就说明此次技能已经准备好了，你可以马上使用，试试吧！','utf-8'),

    "playerTip8": unicode('好了，现在您的队伍已经具备5个属性的武将了，这样消除任意颜色的宝石都会有相应的武将发动攻击了。','utf-8'),
    "playerTip9": unicode('困难的关卡难以通过？说明您的队伍实力不够强，这时候需要提高您队伍的实力，最简单的方法之一就是强化您队伍里的武将了。','utf-8'),

     "comboTip1": unicode('手动选择怪物，可设置为优先攻击目标.','utf-8'),
     "comboTip2": unicode('知道吗？在规定的时间内，珠子是可以自由的移动的。','utf-8'),
     "comboTip3": unicode('当你消除2组或以上的宝石时，会产生连击，连击数越高伤害越高。','utf-8'),

    #/*stoneGrid*#/
    "stoneGridTip1": unicode('敌人头上的回合数减至0时发动攻击！攻击会使您HP减少，当HP减少至0的时候游戏就会结束，千万要注意哦。','utf-8'),

    #/*deadDlg*#/
    "deadDlgtip1": unicode('复活','utf-8'),
    "deadDlgtip2": unicode('使用','utf-8'),
    "deadDlgtip3": unicode('个元宝即可复活,您的元宝数已经不足以复活!','utf-8'),
    "deadDlgtip4": unicode('个元宝即可复活,是否选择复活?','utf-8'),
    "deadDlgtip5": unicode('您现在拥有','utf-8'),
    "deadDlgtip6": unicode('元宝','utf-8'),

    #/*appController 补充的 *#/
    "appCtrlTip1": unicode('服务器繁忙或维护中，请稍后重试！','utf-8'),#/#/翻译
    "appCtrlTip2": unicode('有最新版本，请更新！','utf-8'),#/#/翻译
    "appCtrlTip3": unicode('更新','utf-8'),#/#/翻译
    "appCtrlTip4": unicode('您的网络有问题,请检查网络','utf-8'),#/#/翻译
    "touchFightTip": unicode('*请点击屏幕开始战斗吧*','utf-8'),#/#/翻译

     "eleHeartTip": unicode('心','utf-8'),
    "eleFireTip": unicode('火','utf-8'),
    "eleWaterTip": unicode('水','utf-8'),
    "eleWoodTip": unicode('木','utf-8'),
    "eleLightTip": unicode('光','utf-8'),
    "eleDarkTip": unicode('暗','utf-8'),


    "loginLayerTip1": unicode('重要提示','utf-8'),
    "loginLayerTip2": unicode('如果使用快速登录，游戏从设备中删除后，将无法保存游戏数据','utf-8'),
    "noticeTip1": unicode('公告','utf-8'),
    "noticeTip2": unicode('每日奖励','utf-8'),
    "noticeTip3": unicode('援军点数结算','utf-8'),
    "noticeTip4": unicode('邀请奖励','utf-8'),

    "gainExpTip": unicode('获得经验:','utf-8'),
    "cdTip": unicode('冷却','utf-8'),
    "newBieTip1": unicode('获得的元宝可以用于游戏的各种功能','utf-8'),

    #/*MainSceneTip*#/

    "mainSceneTip1": unicode('国士无双','utf-8'),
    "mainSceneTip2": unicode('攻守兼备','utf-8'),
    "mainSceneTip3": unicode('生生不息','utf-8'),
    "mainSceneTip4": unicode('骁勇善战','utf-8'),
    "mainSceneTip5": unicode('金石之坚','utf-8'),
    "mainSceneTip6": unicode('神将','utf-8'),
    "mainSceneTip7": unicode('转生道具','utf-8'),
    "mainSceneTip8": unicode('强化合成','utf-8'),

    "mainSceneTip9": unicode('您军营已满,超出','utf-8'),
    "mainSceneTip10": unicode('位武将','utf-8'),
    "mainSceneTip11": unicode('军营已满','utf-8'),
    "mainSceneTip12": unicode('您的统御力超过最大值','utf-8'),
    "mainSceneTip13": unicode('统御力超出','utf-8'),
    "mainSceneTip14": unicode('当前有素材在编队中','utf-8'),
    "mainSceneTip15": unicode('无法转生','utf-8'),
    "mainSceneTip16": unicode('有3星或以上的稀有武将被选中确定要作为素材吗？','utf-8'),

    #/*newbielayer*#/
    "newBieLayerTip1": unicode('刘备','utf-8'),
    "newBieLayerTip2": unicode('曹操','utf-8'),
    "newBieLayerTip3": unicode('孙权','utf-8'),
    "newBieLayerTip4": unicode('请选择一位主公作为您的伙伴吧～','utf-8'),
    "noFriendLayerTip1": unicode('无好友申请!','utf-8'),
    "shareTip": unicode('分享','utf-8'),

    "newBieLayerTip5": unicode('基本介绍结束了！如果还有不明白的地方可以点击其他里的帮助文档。现在，开始逆转三国吧！','utf-8'),
    "newBieLayerTip6": unicode('是否确定选择此属性主公?','utf-8'),


    #/* 主动技名称 *#/
    "chiyan": unicode('赤炎','utf-8'),
    "yanliuxing": unicode('炎流星','utf-8'),
    "lieyanfentian": unicode('烈焰焚天','utf-8'),

    "jiliu": unicode('激流','utf-8'),
    "shuiyuezhan": unicode('水月斩','utf-8'),
    "shuilongkuangtao": unicode('水龙狂涛','utf-8'),

    "zhendi": unicode('震地','utf-8'),
    "liediren": unicode('裂地刃','utf-8'),
    "dadikuangxiao": unicode('大地狂啸','utf-8'),

    "leiji": unicode('雷击','utf-8'),
    "tianjianzhan": unicode('天剑斩','utf-8'),
    "tianjianshenwei": unicode('天剑神威','utf-8'),

    "anyue": unicode('暗月','utf-8'),
    "luocharen": unicode('罗刹刃','utf-8'),
    "shenguiluanwu": unicode('神鬼乱舞','utf-8'),

    "liannu": unicode('连弩','utf-8'),
    "chuanyunjian": unicode('穿云箭','utf-8'),
    "lianzhujian": unicode('连珠箭','utf-8'),
    "lienukuangtao": unicode('烈弩狂涛','utf-8'),

    "tujihuo": unicode('突击-火','utf-8'),
    "jixihuo": unicode('急袭-火','utf-8'),

    "tujishui": unicode('突击-水','utf-8'),
    "jixishui": unicode('急袭-水','utf-8'),

    "tujimu": unicode('突击-木','utf-8'),
    "jiximu": unicode('急袭-木','utf-8'),

    "tujiguang": unicode('突击-光','utf-8'),
    "jixiguang": unicode('急袭-光','utf-8'),

    "tujian": unicode('突击-暗','utf-8'),
    "jixian": unicode('急袭-暗','utf-8'),

    "luochahou": unicode('罗刹吼','utf-8'),
    "guiwangpaoxiao": unicode('鬼王咆哮','utf-8'),

    "cuidu": unicode('淬毒','utf-8'),
    "mengdu": unicode('猛毒','utf-8'),
    "shigujudu": unicode('蚀骨剧毒','utf-8'),

    "weixia": unicode('威吓','utf-8'),
    "weiya": unicode('威压','utf-8'),

    "pojia": unicode('破甲','utf-8'),
    "moyanrongjin": unicode('魔焰熔金','utf-8'),

    "zhiliaoshu": unicode('治疗术','utf-8'),
    "zhiyushu": unicode('治愈术','utf-8'),
    "huichunshu": unicode('回春术','utf-8'),
    "qingnangmishu": unicode('青囊秘术','utf-8'),
    "guiyuanshu": unicode('归元术','utf-8'),
    "mingliaoshu": unicode('命疗术','utf-8'),

    "baguazhen": unicode('八卦阵','utf-8'),
    "renwangdun": unicode('仁王盾','utf-8'),

    "chenzhouhuo": unicode('破釜沉舟-火','utf-8'),
    "chenzhouan": unicode('破釜沉舟-暗','utf-8'),
    "weiyingshui": unicode('步步为营-水','utf-8'),
    "weiyingguang": unicode('步步为营-光','utf-8'),
    "huanrihuo": unicode('偷天换日-火','utf-8'),
    "huanrishui": unicode('偷天换日-水','utf-8'),
    "huanrimu": unicode('偷天换日-木','utf-8'),
    "huanriguang": unicode('偷天换日-光','utf-8'),
    "huanrian": unicode('偷天换日-暗','utf-8'),
    "beishui": unicode('背水一战','utf-8'),
    "luanshi": unicode('乱世','utf-8'),
    "luanshitianxia": unicode('乱世天下','utf-8'),

    "guaguliaoshang": unicode('刮骨疗伤','utf-8'),

    "huifushui": unicode('破釜沉舟-水','utf-8'),
    "huifumu": unicode('破釜沉舟-木','utf-8'),
    "huifuguang": unicode('破釜沉舟-光','utf-8'),
    "muhuifu": unicode('步步为营-火','utf-8'),
    "shuihuifu": unicode('步步为营-木','utf-8'),
    "guanghuifu": unicode('步步为营-暗','utf-8'),

    "feidanshui": unicode('猛攻-水','utf-8'),
    "feidanhuo": unicode('猛攻-火','utf-8'),
    "feidanmu": unicode('猛攻-木','utf-8'),
    "feidanguang": unicode('猛攻-光','utf-8'),
    "feidanan": unicode('猛攻-暗','utf-8'),

    "cannonshui": unicode('超猛攻-水','utf-8'),
    "cannonhuo": unicode('超猛攻-火','utf-8'),
    "cannonmu": unicode('超猛攻-木','utf-8'),
    "cannonguang": unicode('超猛攻-光','utf-8'),
    "cannonan": unicode('超猛攻-暗','utf-8'),

    "tiankongshui": unicode('冰刃舞','utf-8'),
    "tiankonghuo": unicode('爆炎击','utf-8'),
    "tiankongmu": unicode('岩铁碎','utf-8'),
    "tiankongguang": unicode('雷龙破','utf-8'),
    "tiankongan": unicode('噬魂炮','utf-8'),

    "mabishui": unicode('美人计 水','utf-8'),
    "mabihuo": unicode('美人计 火','utf-8'),
    "mabimu": unicode('美人计 木','utf-8'),
    "mabiguang": unicode('美人计 光','utf-8'),
    "mabian": unicode('美人计 暗','utf-8'),
    "mabiall": unicode('天下臣服','utf-8'),

    "wudishui": unicode('先祖之魂 水','utf-8'),
    "wudihuo": unicode('先祖之魂 火','utf-8'),
    "wudimu": unicode('先祖之魂 木','utf-8'),
    "wudiguang": unicode('先祖之魂 光','utf-8'),
    "wudian": unicode('先祖之魂 暗','utf-8'),
    "wudiall": unicode('八门金锁阵','utf-8'),

    "rumucf": unicode('如沐春风','utf-8'),
    "huoshaoly": unicode('火烧连营','utf-8'),
    "qiaobian": unicode('巧变','utf-8'),
    "juedifj": unicode('绝地反击','utf-8'),
    "ghostcall": unicode('冥王的召唤','utf-8'),

    "godanger":unicode('神威灭世','utf-8'),

    "huomuxin":unicode('修罗之道','utf-8'),#manSkid_99
    "hateatk":unicode('灭杀一击','utf-8'),#manSkid_100
    "skillsick":unicode('瘟疫','utf-8'),#manSkid_101

    "lieyanfentian30":unicode('圣火燎原','utf-8'),
    "shuilongkuangtao30":unicode('玄冰叹息','utf-8'),
    "dadikuangxiao30":unicode('森罗灭绝','utf-8'),
    "tianjianshenwei30":unicode('雷霆万钧','utf-8'),
    "shenguiluanwu30":unicode('深渊毁灭','utf-8'),


    "ManSillTitle_107":unicode('移形换影-心火','utf-8'),
    "ManSillTitle_108":unicode('移形换影-心水','utf-8'),
    "ManSillTitle_109":unicode('移形换影-心木','utf-8'),
    "ManSillTitle_110":unicode('移形换影-心光','utf-8'),
    "ManSillTitle_111":unicode('移形换影-心暗','utf-8'),

    "ManSillTitle_112":unicode('噬魂烈焰','utf-8'),
    "ManSillTitle_113":unicode('噬魂冰霜','utf-8'),
    "ManSillTitle_114":unicode('噬魂苍木','utf-8'),
    "ManSillTitle_115":unicode('噬魂雷击','utf-8'),
    "ManSillTitle_116":unicode('噬魂暗影','utf-8'),

    "ManSillTitle_117":unicode('先祖守护-火','utf-8'),
    "ManSillTitle_118":unicode('先祖守护-水','utf-8'),
    "ManSillTitle_119":unicode('先祖守护-木','utf-8'),
    "ManSillTitle_120":unicode('先祖守护-光','utf-8'),
    "ManSillTitle_121":unicode('先祖守护-暗','utf-8'),

    "ManSillTitle_122":unicode('苍龙偃月刀','utf-8'),
    "ManSillTitle_123":unicode('凤凰炎流箭','utf-8'),
    "ManSillTitle_124":unicode('破军点钢矛','utf-8'),
    "ManSillTitle_125":unicode('雷龙亮银枪','utf-8'),
    "ManSillTitle_126":unicode('灭杀黑龙枪','utf-8'),

    "ManSillTitle_127":unicode('神机·东风起','utf-8'),
    "ManSillTitle_128":unicode('暗袭箭','utf-8'),
    "ManSillTitle_129":unicode('天机·奇谋','utf-8'),

    "ManSillTitle_130":unicode('蓄势待发·水','utf-8'),
    "ManSillTitle_131":unicode('蓄势待发·火','utf-8'),
    "ManSillTitle_132":unicode('蓄势待发·木','utf-8'),
    "ManSillTitle_133":unicode('蓄势待发·光','utf-8'),
    "ManSillTitle_134":unicode('蓄势待发·暗','utf-8'),

    "ManSkillTitle_135":unicode('舍命一击','utf-8'),
    "ManSkillTitle_136":unicode('蓄势一击·木','utf-8'),
    "ManSkillTitle_137":unicode('破军','utf-8'),
    "ManSkillTitle_138":unicode('劈山击','utf-8'),
    "ManSkillTitle_139":unicode('攻城略地·火','utf-8'),
    "ManSkillTitle_140":unicode('攻城略地·水','utf-8'),
    "ManSkillTitle_141":unicode('攻城略地·木','utf-8'),
    "ManSkillTitle_142":unicode('攻城略地·光','utf-8'),
    "ManSkillTitle_143":unicode('攻城略地·暗','utf-8'),
    "ManSkillTitle_144":unicode('定身','utf-8'),
    "ManSkillTitle_145":unicode('刀枪不入','utf-8'),
    "ManSkillTitle_146":unicode('杀手锏','utf-8'),
    "ManSkillTitle_147":unicode('卸甲','utf-8'),
    "ManSkillTitle_148":unicode('蛊毒','utf-8'),
    "ManSkillTitle_149":unicode('时间静止','utf-8'),
    "ManSkillTitle_150":unicode('幽冥斩','utf-8'),
    "ManSkillTitle_151":unicode('狂澜怒斩','utf-8'),
    "ManSkillTitle_152":unicode('幸运一击','utf-8'),
############################Ver 3.5更新##############################
    "ManSkillTitle_153":unicode('兵贵神速','utf-8'),
    "ManSkillTitle_154":unicode('权倾天下','utf-8'),
    "ManSkillTitle_155":unicode('奥义·雷戟','utf-8'),
    "ManSkillTitle_156":unicode('凄凰镜反','utf-8'),
    "ManSkillTitle_157":unicode('轰炎双刃','utf-8'),
    "ManSkillTitle_158":unicode('裂冰闪光','utf-8'),
    "ManSkillTitle_159":unicode('旋风破空','utf-8'),
    "ManSkillTitle_160":unicode('强袭-火','utf-8'),
    "ManSkillTitle_161":unicode('强袭-水','utf-8'),
    "ManSkillTitle_162":unicode('强袭-木','utf-8'),
    "ManSkillTitle_163":unicode('强袭-光','utf-8'),
    "ManSkillTitle_164":unicode('强袭-暗','utf-8'),
    "ManSkillTitle_165":unicode('惊鸿落雷','utf-8'),
    "ManSkillTitle_166":unicode('破木-火','utf-8'),
    "ManSkillTitle_167":unicode('驱炎-水','utf-8'),
    "ManSkillTitle_168":unicode('断流-木','utf-8'),

    "ManSkillTitle_169":unicode('噬魂-光','utf-8'),
    "ManSkillTitle_170":unicode('斩雷-暗','utf-8'),
    "ManSkillTitle_171":unicode('圣光变幻-火','utf-8'),
    "ManSkillTitle_172":unicode('暗影变幻-水','utf-8'),
    "ManSkillTitle_173":unicode('激流变幻-木','utf-8'),
    "ManSkillTitle_174":unicode('大地变幻-光','utf-8'),
    "ManSkillTitle_175":unicode('爆炎变幻-暗','utf-8'),
    "ManSkillTitle_176":unicode('百万凶炎','utf-8'),
    "ManSkillTitle_177":unicode('滔天巨浪','utf-8'),
    "ManSkillTitle_178":unicode('暴风狂吼','utf-8'),
    "ManSkillTitle_179":unicode('末日咆哮','utf-8'),
    "ManSkillTitle_180":unicode('百万凶炎2','utf-8'),

    "ManSkillTitle_181":unicode('无影之术','utf-8'),
    "ManSkillTitle_182":unicode('黑雷的诅咒','utf-8'),
    "ManSkillTitle_183":unicode('光龙突击','utf-8'),
    "ManSkillTitle_184":unicode('水、心变火','utf-8'),
    "ManSkillTitle_185":unicode('木、心变水','utf-8'),
    "ManSkillTitle_186":unicode('火、心变木','utf-8'),
    "ManSkillTitle_187":unicode('暗、心变光','utf-8'),
    "ManSkillTitle_188":unicode('光、心变暗','utf-8'),
    "ManSkillTitle_189":unicode('所有变火','utf-8'),
    "ManSkillTitle_190":unicode('响尾蛇之击','utf-8'),
    "ManSkillTitle_191":unicode('虹色磁石','utf-8'),
    "ManSkillTitle_192":unicode('圣诞夜的审判','utf-8'),
    "ManSkillTitle_193":unicode('木、光变心','utf-8'),
    "ManSkillTitle_194":unicode('火、暗变心','utf-8'),
    "ManSkillTitle_195":unicode('水、光变心','utf-8'),
    "ManSkillTitle_196":unicode('木、暗变心','utf-8'),
    "ManSkillTitle_197":unicode('火、光变心','utf-8'),
    "ManSkillTitle_198":unicode('心攻击强化','utf-8'),
    "ManSkillTitle_199":unicode('心无敌','utf-8'),

    #/* 主动技描述 *#/
    "chiyanDsp": unicode('自身攻击力3倍的火属性全体攻击','utf-8'),
    "yanliuxingDsp": unicode('自身攻击力5倍的火属性全体攻击','utf-8'),
    "lieyanfentianDsp": unicode('自身攻击力20倍的火属性全体攻击','utf-8'),

    "jiliuDsp": unicode('自身攻击力3倍的水属性全体攻击','utf-8'),
    "shuiyuezhanDsp": unicode('自身攻击力5倍的水属性全体攻击','utf-8'),
    "shuilongkuangtaoDsp": unicode('自身攻击力20倍的水属性全体攻击','utf-8'),

    "zhendiDsp": unicode('自身攻击力3倍的木属性全体攻击','utf-8'),
    "liedirenDsp": unicode('自身攻击力5倍的木属性全体攻击','utf-8'),
    "dadikuangxiaoDsp": unicode('自身攻击力20倍的木属性全体攻击','utf-8'),

    "leijiDsp": unicode('自身攻击力3倍的光属性全体攻击','utf-8'),
    "tianjianzhanDsp": unicode('自身攻击力5倍的光属性全体攻击','utf-8'),
    "tianjianshenweiDsp": unicode('自身攻击力20倍的光属性全体攻击','utf-8'),

    "anyueDsp": unicode('自身攻击力3倍的暗属性全体攻击','utf-8'),
    "luocharenDsp": unicode('自身攻击力5倍的暗属性全体攻击','utf-8'),
    "shenguiluanwuDsp": unicode('自身攻击力20倍的暗属性全体攻击','utf-8'),

    "liannuDsp": unicode('自身攻击力10倍的伤害','utf-8'),
    "chuanyunjianDsp": unicode('自身攻击力15倍的伤害','utf-8'),
    "lianzhujianDsp": unicode('自身攻击力10倍的伤害','utf-8'),
    "lienukuangtaoDsp": unicode('自身攻击力30倍的伤害','utf-8'),

    "tujihuoDsp": unicode('造成1000点火属性全体伤害','utf-8'),
    "jixihuoDsp": unicode('造成3000点火属性全体伤害','utf-8'),

    "tujishuiDsp": unicode('造成1000点水属性全体伤害','utf-8'),
    "jixishuiDsp": unicode('造成3000点水属性全体伤害','utf-8'),

    "tujimuDsp": unicode('造成1000点木属性全体伤害','utf-8'),
    "jiximuDsp": unicode('造成3000点木属性全体伤害','utf-8'),

    "tujiguangDsp": unicode('造成1000点光属性全体伤害','utf-8'),
    "jixiguangDsp": unicode('造成3000点光属性全体伤害','utf-8'),

    "tujianDsp": unicode('造成1000点暗属性全体伤害','utf-8'),
    "jixianDsp": unicode('造成3000点暗属性全体伤害','utf-8'),

    "luochahouDsp": unicode('敌方全体减少15%血量','utf-8'),
    "guiwangpaoxiaoDsp": unicode('敌方全体减少30%血量','utf-8'),

    "cuiduDsp": unicode('使敌方全体中淬毒','utf-8'),
    "mengduDsp": unicode('使敌方全体中猛毒','utf-8'),
    "shigujuduDsp": unicode('使敌方全体中剧毒','utf-8'),

    "weixiaDsp": unicode('敌人攻击延长3回合','utf-8'),
    "weiyaDsp": unicode('敌人攻击延长5回合','utf-8'),

    "pojiaDsp": unicode('一定回合内，减少敌人防御力','utf-8'),
    "moyanrongjinDsp": unicode('一定回合内，敌人防御力大幅下降','utf-8'),

    "zhiliaoshuDsp": unicode('血量回复300','utf-8'),
    "zhiyushuDsp": unicode('血量回复500','utf-8'),
    "huichunshuDsp": unicode('血量回复2000','utf-8'),
    "qingnangmishuDsp": unicode('血量完全回复','utf-8'),
    "guiyuanshuDsp": unicode('回复自身回复力5倍的血量','utf-8'),
    "mingliaoshuDsp": unicode('回复自身回复力10倍的血量','utf-8'),

    "baguazhenDsp": unicode('在3回合内，所受伤害减少','utf-8'),
    "renwangdunDsp": unicode('在5回合内，所受伤害减少','utf-8'),

    "chenzhouhuoDsp": unicode('回复宝石变成火宝石','utf-8'),
    "chenzhouanDsp": unicode('回复宝石变成暗宝石','utf-8'),
    "weiyingshuiDsp": unicode('火宝石变成回复宝石','utf-8'),
    "weiyingguangDsp": unicode('暗宝石变成回复宝石','utf-8'),
    "huanrihuoDsp": unicode('水宝石变成火宝石','utf-8'),
    "huanrishuiDsp": unicode('木宝石变成水宝石','utf-8'),
    "huanrimuDsp": unicode('火宝石变成木宝石','utf-8'),
    "huanriguangDsp": unicode('暗宝石变成光宝石','utf-8'),
    "huanrianDsp": unicode('光宝石变成暗宝石','utf-8'),
    "beishuiDsp": unicode('所有宝石随机变化','utf-8'),
    "luanshiDsp": unicode('在5秒内，可以任意挪动宝石','utf-8'),
    "luanshitianxiaDsp": unicode('在10秒内，可以任意挪动宝石','utf-8'),

    "guaguliaoshangDsp": unicode('血量完全恢复，并且减少敌方全体15%血量','utf-8'),

    "huifushuiDsp": unicode('所有回复宝石变化成水宝石','utf-8'),
    "huifumuDsp": unicode('所有回复宝石变化成木宝石','utf-8'),
    "huifuguangDsp": unicode('所有回复宝石变化成光宝石','utf-8'),
    "muhuifuDsp": unicode('所有木宝石变化成回复宝石','utf-8'),
    "shuihuifuDsp": unicode('所有水宝石变化成回复宝石','utf-8'),
    "guanghuifuDsp": unicode('所有光宝石变化成回复宝石','utf-8'),

    "feidanshuiDsp": unicode('对敌方全体造成20000点水属性伤害','utf-8'),
    "feidanhuoDsp": unicode('对敌方全体造成20000点火属性伤害','utf-8'),
    "feidanmuDsp": unicode('对敌方全体造成20000点木属性伤害','utf-8'),
    "feidanguangDsp": unicode('对敌方全体造成20000点光属性伤害','utf-8'),
    "feidananDsp": unicode('对敌方全体造成20000点暗属性伤害','utf-8'),

    "cannonshuiDsp": unicode('对敌方全体造成30000点水属性伤害','utf-8'),
    "cannonhuoDsp": unicode('对敌方全体造成30000点火属性伤害','utf-8'),
    "cannonmuDsp": unicode('对敌方全体造成30000点木属性伤害','utf-8'),
    "cannonguangDsp": unicode('对敌方全体造成30000点光属性伤害','utf-8'),
    "cannonanDsp": unicode('对敌方全体造成30000点暗属性伤害','utf-8'),

    "tiankongshuiDsp": unicode('对敌方全体造成自身攻击力5倍的水属性伤害','utf-8'),
    "tiankonghuoDsp": unicode('对敌方全体造成自身攻击力5倍的火属性伤害','utf-8'),
    "tiankongmuDsp": unicode('对敌方全体造成自身攻击力5倍的木属性伤害','utf-8'),
    "tiankongguangDsp": unicode('对敌方全体造成自身攻击力5倍的光属性伤害','utf-8'),
    "tiankonganDsp": unicode('对敌方全体造成自身攻击力5倍的暗属性伤害','utf-8'),

    "mabishuiDsp": unicode('2回合内敌方火属性武将回合不减','utf-8'),
    "mabihuoDsp": unicode('2回合内敌方木属性武将回合不减','utf-8'),
    "mabimuDsp": unicode('2回合内敌方水属性武将回合不减','utf-8'),
    "mabiguangDsp": unicode('2回合内敌方暗属性武将回合不减','utf-8'),
    "mabianDsp": unicode('2回合内敌方光属性武将回合不减','utf-8'),
    "mabiallDsp": unicode('2回合内敌方所有武将回合不减','utf-8'),

    "wudishuiDsp": unicode('1回合内敌方火属性攻击无效','utf-8'),
    "wudihuoDsp": unicode('1回合内敌方木属性攻击无效','utf-8'),
    "wudimuDsp": unicode('1回合内敌方水属性攻击无效','utf-8'),
    "wudiguangDsp": unicode('1回合内敌方暗属性攻击无效','utf-8'),
    "wudianDsp": unicode('1回合内敌方光属性攻击无效','utf-8'),
    "wudiallDsp": unicode('1回合内敌方所有攻击无效','utf-8'),

    "rumucfDsp": unicode('3回合内，每回合回复HP总和的20%','utf-8'),
    "huoshaolyDsp": unicode('3回合内，所有敌人的防御力变为0。','utf-8'),
    "qiaobianDsp": unicode('对敌方单体造成自身攻击力20倍的伤害，回复相当于伤害值的血','utf-8'),
    "juedifjDsp": unicode('下一次受到敌方伤害不会使你阵亡，并且有几率反弹多倍伤害','utf-8'),
    "ghostcallDsp": unicode('所有火、木宝石变化成暗宝石','utf-8'),

    "godangerDsp":unicode('敌方全体减少35%血量','utf-8'),

    "huomuxinDsp":unicode('所有火、木宝石变化成回复宝石','utf-8'),

    "hateatkDsp":unicode('对敌将单体造成致命伤害，我方剩余血量越低，伤害越高','utf-8'),

    "skillsickDsp":unicode('使敌方全体感染瘟疫，持续3回合','utf-8'),

    "lieyanfentian30Dsp":unicode('自身攻击力30倍的火属性全体攻击','utf-8'),
    "shuilongkuangtao30Dsp":unicode('自身攻击力30倍的水属性全体攻击','utf-8'),
    "dadikuangxiao30Dsp":unicode('自身攻击力30倍的木属性全体攻击','utf-8'),
    "tianjianshenwei30Dsp":unicode('自身攻击力30倍的光属性全体攻击','utf-8'),
    "shenguiluanwu30Dsp":unicode('自身攻击力30倍的暗属性全体攻击','utf-8'),

    "ManSillDsp_107":unicode('所有火宝石变化成回复宝石，所有木宝石变化为火宝石','utf-8'),
    "ManSillDsp_108":unicode('所有水宝石变化成回复宝石，所有火宝石变化为水宝石','utf-8'),
    "ManSillDsp_109":unicode('所有木宝石变化成回复宝石，所有水宝石变化为木宝石','utf-8'),
    "ManSillDsp_110":unicode('所有光宝石变化成回复宝石，所有暗宝石变化为光宝石','utf-8'),
    "ManSillDsp_111":unicode('所有暗宝石变化成回复宝石，所有光宝石变化为暗宝石','utf-8'),

    "ManSillDsp_112":unicode('对敌方全体造成10000点火属性伤害和30000点心属性伤害','utf-8'),
    "ManSillDsp_113":unicode('对敌方全体造成10000点水属性伤害和30000点心属性伤害','utf-8'),
    "ManSillDsp_114":unicode('对敌方全体造成10000点木属性伤害和30000点心属性伤害','utf-8'),
    "ManSillDsp_115":unicode('对敌方全体造成10000点光属性伤害和30000点心属性伤害','utf-8'),
    "ManSillDsp_116":unicode('对敌方全体造成10000点暗属性伤害和30000点心属性伤害','utf-8'),

    "ManSillDsp_117":unicode('1回合内敌方木属性攻击无效，其他属性伤害减半','utf-8'),
    "ManSillDsp_118":unicode('1回合内敌方火属性攻击无效，其他属性伤害减半','utf-8'),
    "ManSillDsp_119":unicode('1回合内敌方水属性攻击无效，其他属性伤害减半','utf-8'),
    "ManSillDsp_120":unicode('1回合内敌方暗属性攻击无效，其他属性伤害减半','utf-8'),
    "ManSillDsp_121":unicode('1回合内敌方光属性攻击无效，其他属性伤害减半','utf-8'),

    "ManSillDsp_122":unicode('下一次攻击，我方水属性武将的攻击力提升1.5倍','utf-8'),
    "ManSillDsp_123":unicode('下一次攻击，我方火属性武将的攻击力提升1.5倍','utf-8'),
    "ManSillDsp_124":unicode('下一次攻击，我方木属性武将的攻击力提升1.5倍','utf-8'),
    "ManSillDsp_125":unicode('下一次攻击，我方光属性武将的攻击力提升1.5倍','utf-8'),
    "ManSillDsp_126":unicode('下一次攻击，我方暗属性武将的攻击力提升1.5倍','utf-8'),

    "ManSillDsp_127":unicode('1回合内，消除的所有宝石都附加回血效果','utf-8'),
    "ManSillDsp_128":unicode('对敌方单体造成10000点克制属性伤害。','utf-8'),
    "ManSillDsp_129":unicode('当局我方技能最大回合数-1','utf-8'),

    "ManSillDsp_130":unicode('当前面板上，水属性宝石的伤害提升','utf-8'),
    "ManSillDsp_131":unicode('当前面板上，火属性宝石的伤害提升','utf-8'),
    "ManSillDsp_132":unicode('当前面板上，木属性宝石的伤害提升','utf-8'),
    "ManSillDsp_133":unicode('当前面板上，光属性宝石的伤害提升','utf-8'),
    "ManSillDsp_134":unicode('当前面板上，暗属性宝石的伤害提升','utf-8'),

    "ManSkillDsp_135":unicode('对敌将单体造成致命伤害，我方剩余血量越低，伤害越高','utf-8'),
    "ManSkillDsp_136":unicode('下一次攻击，我方木属性武将的攻击力提升1.5倍','utf-8'),
    "ManSkillDsp_137":unicode('3回合内，所有敌人的防御力变为0','utf-8'),
    "ManSkillDsp_138":unicode('敌方全体减少15%血量','utf-8'),
    "ManSkillDsp_139":unicode('自身攻击力40倍的火属性全体攻击','utf-8'),
    "ManSkillDsp_140":unicode('自身攻击力40倍的水属性全体攻击','utf-8'),
    "ManSkillDsp_141":unicode('自身攻击力40倍的木属性全体攻击','utf-8'),
    "ManSkillDsp_142":unicode('自身攻击力40倍的光属性全体攻击','utf-8'),
    "ManSkillDsp_143":unicode('自身攻击力40倍的暗属性全体攻击','utf-8'),
    "ManSkillDsp_144":unicode('敌人攻击延长2回合','utf-8'),
    "ManSkillDsp_145":unicode('一定回合内，所受伤害大幅度减少','utf-8'),
    "ManSkillDsp_146":unicode('对敌方全体造成9999点固定伤害','utf-8'),
    "ManSkillDsp_147":unicode('一定回合内，减少敌人防御力','utf-8'),
    "ManSkillDsp_148":unicode('使敌方全体中猛毒','utf-8'),
    "ManSkillDsp_149":unicode('在6秒内，可以任意挪动宝石','utf-8'),
    "ManSkillDsp_150":unicode('自身攻击力40倍的暗属性单体攻击','utf-8'),
    "ManSkillDsp_151":unicode('对火属性敌人造成37500点水属性伤害','utf-8'),
    "ManSkillDsp_152":unicode('对敌方单体造成随机伤害','utf-8'),
#################################Ver 3.5更新#########################################
    "ManSkillDsp_153":unicode('回复相当于自身回复力3倍的HP','utf-8'),
    "ManSkillDsp_154":unicode('3回合内，所有攻击转化为全体攻击','utf-8'),
    "ManSkillDsp_155":unicode('对敌方全体造成5555点固定伤害','utf-8'),
    "ManSkillDsp_156":unicode('5回合内，受到伤害后，反弹3倍暗属性伤害','utf-8'),
    "ManSkillDsp_157":unicode('对敌方单体造成自身攻击力30倍的火属性伤害','utf-8'),
    "ManSkillDsp_158":unicode('对敌方单体造成自身攻击力30倍的水属性伤害','utf-8'),
    "ManSkillDsp_159":unicode('对敌方单体造成自身攻击力30倍的木属性伤害','utf-8'),
    "ManSkillDsp_160":unicode('对敌方全体造成25000点火属性伤害','utf-8'),
    "ManSkillDsp_161":unicode('对敌方全体造成25000点水属性伤害','utf-8'),
    "ManSkillDsp_162":unicode('对敌方全体造成25000点木属性伤害','utf-8'),
    "ManSkillDsp_163":unicode('对敌方全体造成25000点光属性伤害','utf-8'),
    "ManSkillDsp_164":unicode('对敌方全体造成25000点暗属性伤害','utf-8'),
    "ManSkillDsp_165":unicode('对敌方单体造成自身攻击力30倍的光属性伤害','utf-8'),
    "ManSkillDsp_166":unicode('对木属性敌人造成17500点火属性伤害','utf-8'),
    "ManSkillDsp_167":unicode('对火属性敌人造成17500点水属性伤害','utf-8'),
    "ManSkillDsp_168":unicode('对水属性敌人造成17500点木属性伤害','utf-8'),

    "ManSkillDsp_169":unicode('对暗属性敌人造成15000点光属性伤害','utf-8'),
    "ManSkillDsp_170":unicode('对光属性敌人造成15000点暗属性伤害','utf-8'),
    "ManSkillDsp_171":unicode('所有光宝珠变化成火宝珠','utf-8'),
    "ManSkillDsp_172":unicode('所有暗宝珠变化成水宝珠','utf-8'),
    "ManSkillDsp_173":unicode('所有水宝珠变化成木宝珠','utf-8'),
    "ManSkillDsp_174":unicode('所有木宝珠变化成光宝珠','utf-8'),
    "ManSkillDsp_175":unicode('所有火宝珠变化成暗宝珠','utf-8'),
    "ManSkillDsp_176":unicode('1回合内，把敌将属性转换为火属性','utf-8'),
    "ManSkillDsp_177":unicode('1回合内，把敌将属性转换为水属性','utf-8'),
    "ManSkillDsp_178":unicode('1回合内，把敌将属性转换为木属性','utf-8'),
    "ManSkillDsp_179":unicode('1回合内，把敌将属性转换为暗属性','utf-8'),
    "ManSkillDsp_180":unicode('1回合内，把敌将属性转换为火属性','utf-8'),

    "ManSkillDsp_181":unicode('對敵方單體造成自身攻擊力20倍的傷害，並回復相當於傷害5%的HP，傷害屬性與自身屬性相同，會受到敵人的屬性和防禦的影響','utf-8'),
    "ManSkillDsp_182":unicode('HP变为1，并对敌方一体造成50倍光屬性伤害，受屬性加成和敵人防禦的影響 註：已經一HP後，不可發動','utf-8'),
    "ManSkillDsp_183":unicode('对敌方单体造成自身攻击力40倍的光属性伤害','utf-8'),
    "ManSkillDsp_184":unicode('所有水宝珠和回复宝珠变化成火宝珠','utf-8'),
    "ManSkillDsp_185":unicode('所有木宝珠和回复宝珠变化成水宝珠','utf-8'),
    "ManSkillDsp_186":unicode('所有火宝珠和回复宝珠变化成木宝珠','utf-8'),
    "ManSkillDsp_187":unicode('所有暗宝珠和回复宝珠变化成光宝珠','utf-8'),
    "ManSkillDsp_188":unicode('所有光宝珠和回复宝珠变化成暗宝珠','utf-8'),
    "ManSkillDsp_189":unicode('所有宝珠变化为火宝珠','utf-8'),
    "ManSkillDsp_190":unicode('对敌方单体造成自身攻击力30倍的火属性伤害','utf-8'),
    "ManSkillDsp_191":unicode('7秒内，可以任意挪动宝珠而不会触发消除效果','utf-8'),
    "ManSkillDsp_192":unicode('3回合内，必定对攻击的敌人单体反击，造成3倍于受到伤害值的光属性伤害','utf-8'),
    "ManSkillDsp_193":unicode('所有木宝珠和光宝珠变化成回复宝珠','utf-8'),
    "ManSkillDsp_194":unicode('所有火宝珠和暗宝珠变化成回复宝珠','utf-8'),
    "ManSkillDsp_195":unicode('所有水宝珠和光宝珠变化成回复宝珠','utf-8'),
    "ManSkillDsp_196":unicode('所有木宝珠和暗宝珠变化成回复宝珠','utf-8'),
    "ManSkillDsp_197":unicode('所有火宝珠和光宝珠变化成回复宝珠','utf-8'),
    "ManSkillDsp_198":unicode('1回合内，心属性武将的攻击力变为1.5倍','utf-8'),
    "ManSkillDsp_199":unicode('1回合内敌方心属性攻击无效','utf-8'),

    #/* 被动技名称 *#/
    "jianjiahuo": unicode('坚甲厉兵火','utf-8'),
    "jianjiashui": unicode('坚甲厉兵水','utf-8'),
    "jianjiamu": unicode('坚甲厉兵木','utf-8'),
    "jianjiaguang": unicode('坚甲厉兵光','utf-8'),
    "jianjiaan": unicode('坚甲厉兵暗','utf-8'),

    "jingruihuo": unicode('精锐之师火','utf-8'),
    "jingruishui": unicode('精锐之师水','utf-8'),
    "jingruimu": unicode('精锐之师木','utf-8'),
    "jingruiguang": unicode('精锐之师光','utf-8'),
    "jingruian": unicode('精锐之师暗','utf-8'),

    "jushouhuo": unicode('据守火','utf-8'),
    "jushoushui": unicode('据守水','utf-8'),
    "jushoumu": unicode('据守木','utf-8'),
    "jushouguang": unicode('据守光','utf-8'),
    "jushouan": unicode('据守暗','utf-8'),

    "jintanghuo": unicode('固若金汤火','utf-8'),
    "jintangshui": unicode('固若金汤水','utf-8'),
    "jintangmu": unicode('固若金汤木','utf-8'),
    "jintangguang": unicode('固若金汤光','utf-8'),
    "jintangan": unicode('固若金汤暗','utf-8'),

    "panshi": unicode('盘石','utf-8'),
    "moshou": unicode('墨守','utf-8'),

    "neijing": unicode('黄帝内经','utf-8'),
    "bencao": unicode('神农本草','utf-8'),

    "yeyan": unicode('业炎','utf-8'),
    "yuyan": unicode('狱炎','utf-8'),

    "longpo": unicode('龙之魄','utf-8'),
    "zhenlongpo": unicode('真龙之魄','utf-8'),

    "yanzhi": unicode('延滞术','utf-8'),
    "shiguang": unicode('时光术','utf-8'),
    "yongheng": unicode('永恒术','utf-8'),

    "geyingwuyan": unicode('歌莺舞燕','utf-8'),
    "luangefengwu": unicode('鸾歌凤舞','utf-8'),
    "wujinyuyan": unicode('无尽狱炎','utf-8'),
    "wuxiekeji": unicode('无懈可击','utf-8'),

    "zhanshizhinu": unicode('裸衣','utf-8'),
    "mengjiangxuetong": unicode('野兽之力','utf-8'),
    "baihualiaoluan": unicode('虎女','utf-8'),
    "longzhixue": unicode('虎痴','utf-8'),
    "longqishishi": unicode('历战之驱','utf-8'),
    "longqishinu": unicode('名将无双','utf-8'),
    "sikaha": unicode('百兽王','utf-8'),
    "businiao": unicode('锦帆游侠','utf-8'),
    "shenlangpaoxiao": unicode('将军之怒','utf-8'),
    "waerjili": unicode('巾帼虎女','utf-8'),
    "shendaoyan": unicode('神将之怒','utf-8'),

    "money15": unicode('名门千金','utf-8'),
    "money20": unicode('金枝玉叶','utf-8'),

    "exp12": unicode('百宝袋','utf-8'),
    "exp15": unicode('锦囊妙计','utf-8'),

    "carddrop12": unicode('魅惑','utf-8'),
    "carddrop15": unicode('魅惑之舞','utf-8'),

    "shuihp15": unicode('水之魂','utf-8'),
    "huohp15": unicode('火之魂','utf-8'),
    "muhp15": unicode('木之魂','utf-8'),
    "guanghp15": unicode('光之魂','utf-8'),
    "anhp15": unicode('暗之魂','utf-8'),
    "shuihp20": unicode('葵水之精','utf-8'),
    "huohp20": unicode('离火之精','utf-8'),
    "muhp20": unicode('甲木之精','utf-8'),
    "guanghp20": unicode('圣光之命','utf-8'),
    "anhp20": unicode('幽冥之命','utf-8'),

    "jiangnanstyle": unicode('江南style','utf-8'),

    "jiyun": unicode('无双上将','utf-8'),

    "huo25": unicode('业火焚天','utf-8'),
    "shui25": unicode('玄冰领域','utf-8'),
    "mu25": unicode('森罗地狱','utf-8'),
    "guang25": unicode('雷霆结界','utf-8'),
    "an25": unicode('冥王重狱','utf-8'),

    "lumangshui": unicode('鲁莽水','utf-8'),
    "lumanghuo": unicode('鲁莽火','utf-8'),
    "lumangmu": unicode('鲁莽木','utf-8'),
    "lumangguang": unicode('鲁莽光','utf-8'),
    "lumangan": unicode('鲁莽暗','utf-8'),

    "wjqxshui": unicode('无尽强袭水','utf-8'),
    "wjqxhuo": unicode('无尽强袭火','utf-8'),
    "wjqxmu": unicode('无尽强袭木','utf-8'),
    "wjqxguang": unicode('无尽强袭光','utf-8'),
    "wjqxan": unicode('无尽强袭暗','utf-8'),

    "yanhuo": unicode('焱火','utf-8'),
    "hlyanhuo": unicode('红莲焱火','utf-8'),

    "hanbing": unicode('寒冰','utf-8'),
    "hhhanbing": unicode('瀚海寒冰','utf-8'),
    "senluo": unicode('森罗','utf-8'),
    "senluowx": unicode('森罗万象','utf-8'),
    "xiaojiang": unicode('骁将','utf-8'),
    "lsxiaojiang": unicode('乱世骁将','utf-8'),
    "kuangye": unicode('狂野','utf-8'),
    "kuangyezx": unicode('狂野之血','utf-8'),

    "huofanji": unicode('荒火之噬','utf-8'),
    "shuifanji": unicode('玄冰之噬','utf-8'),
    "mufanji": unicode('苍毒之噬','utf-8'),
    "guangfanji": unicode('勇武之袭','utf-8'),
    "anfanji": unicode('刚烈之袭','utf-8'),

    "teddy": unicode('忠孝双全','utf-8'),

    "jingruicrithuo": unicode('朱雀之怒','utf-8'),
    "jingruicritshui": unicode('青龙之怒','utf-8'),
    "jingruicritmu": unicode('玄武之怒','utf-8'),
    "jingruicritguang": unicode('白虎之怒','utf-8'),
    "jingruicritan": unicode('麒麟之怒','utf-8'),

    "zeus": unicode('无双','utf-8'),#autoskid_96

    "armorhuomu30": unicode('炎藤护盾','utf-8'),#autoskid_97
    "armorhuomu50": unicode('炎藤结界','utf-8'),#autoskid_98
    "armorshuihuo30": unicode('苍炎护盾','utf-8'),#autoskid_99
    "armorshuihuo50": unicode('苍炎结界','utf-8'),#autoskid_100
    "armormushui30": unicode('苍藤护盾','utf-8'),#autoskid_101
    "armormushui50": unicode('苍藤结界','utf-8'),#autoskid_102
    "armorguanghuo30": unicode('雷炎护盾','utf-8'),#autoskid_103
    "armorguanghuo50": unicode('雷炎结界','utf-8'),#autoskid_104
    "armoranmu30": unicode('冥藤护盾','utf-8'),#autoskid_105
    "armoranmu50": unicode('冥藤结界','utf-8'),#autoskid_106
    "armorhuoan30": unicode('炎冥护盾','utf-8'),#autoskid_107
    "armorhuoan50": unicode('炎冥结界','utf-8'),#autoskid_108
    "armorshuian30": unicode('苍冥护盾','utf-8'),#autoskid_109
    "armorshuian50": unicode('苍冥结界','utf-8'),#autoskid_110
    "armormuguang30": unicode('雷藤护盾','utf-8'),#autoskid_111
    "armormuguang50": unicode('雷藤结界','utf-8'),#autoskid_112
    "armorguangshui30": unicode('苍雷护盾','utf-8'),#autoskid_113
    "armorguangshui50": unicode('苍雷结界','utf-8'),#autoskid_114
    "armoranguang30": unicode('雷冥护盾','utf-8'),#autoskid_115
    "armoranguang50": unicode('雷冥结界','utf-8'),#autoskid_116
    "armorxinhuo30": unicode('护盾·心火','utf-8'),#autoskid_117
    "armorxinhuo50": unicode('结界·心火','utf-8'),#autoskid_118
    "armorxinshui30": unicode('护盾·心水','utf-8'),#autoskid_119
    "armorxinshui50": unicode('结界·心水','utf-8'),#autoskid_120
    "armorxinmu30": unicode('护盾·火木','utf-8'),#autoskid_121
    "armorxinmu50": unicode('结界·心木','utf-8'),#autoskid_122
    "armorxinguang30": unicode('护盾·心光','utf-8'),#autoskid_123
    "armorxinguang50": unicode('结界·心光','utf-8'),#autoskid_124
    "armorxinan30": unicode('护盾·心暗','utf-8'),#autoskid_125
    "armorxinan50": unicode('结界·心暗','utf-8'),#autoskid_126

    "atkxinhuo15": unicode('嗜血·心火','utf-8'),#autoskid_127
    "atkxinhuo20": unicode('血祭·心火','utf-8'),#autoskid_128
    "atkxinshui15": unicode('嗜血·心水','utf-8'),#autoskid_129
    "atkxinshui20": unicode('血祭·心水','utf-8'),#autoskid_130
    "atkxinmu15": unicode('嗜血·心木','utf-8'),#autoskid_131
    "atkxinmu20": unicode('血祭·心木','utf-8'),#autoskid_132
    "atkxinguang15": unicode('嗜血·心光','utf-8'),#autoskid_133
    "atkxinguang20": unicode('血祭·心光','utf-8'),#autoskid_134
    "atkxinan15": unicode('嗜血·心暗','utf-8'),#autoskid_135
    "atkxinan20": unicode('血祭·心暗','utf-8'),#autoskid_136


    "3armor50": unicode('鬼神结界','utf-8'),#autoskid_143
    "qiya": unicode('欺压','utf-8'),#autoskid_144
    "ghostinvite": unicode('冥王的邀请','utf-8'),#autoskid_145
    "wenyiligong": unicode('瘟疫离宫','utf-8'),#autoskid_146
    "xianjietupo": unicode('限界突破','utf-8'),#autoskid_147

    "AutoSkillTitle_153": unicode('龙胆','utf-8'),
    "AutoSkillTitle_154": unicode('龙骑','utf-8'),

    "AutoSkillTitle_155": unicode('烈弩之魂','utf-8'),
    "AutoSkillTitle_156": unicode('苍龙之魂','utf-8'),
    "AutoSkillTitle_157": unicode('破军之魂','utf-8'),
    "AutoSkillTitle_158": unicode('龙胆之魂','utf-8'),
    "AutoSkillTitle_159": unicode('龙骑之魂','utf-8'),

    "AutoSkillTitle_160": unicode('离火守护','utf-8'),
    "AutoSkillTitle_161": unicode('葵水守护','utf-8'),
    "AutoSkillTitle_162": unicode('甲木守护','utf-8'),
    "AutoSkillTitle_163": unicode('圣光守护','utf-8'),
    "AutoSkillTitle_164": unicode('幽冥守护','utf-8'),

    "AutoSkillTitle_165": unicode('遁甲·天命','utf-8'),

    "AutoSkillTitle_166": unicode('奇门·八阵图','utf-8'),

    "AutoSkillTitle_167": unicode('弱点追击','utf-8'),

    "AutoSkillTitle_168": unicode('天下无双','utf-8'),

    "AutoSkillTitle_169": unicode('绿林神射之力','utf-8'),
    "AutoSkillTitle_170": unicode('妙手回春','utf-8'),
    "AutoSkillTitle_171": unicode('延缓术','utf-8'),
    "AutoSkillTitle_172": unicode('战神之力','utf-8'),
    "AutoSkillTitle_173": unicode('童环之怒','utf-8'),
    "AutoSkillTitle_174": unicode('樊虎之加持','utf-8'),
    "AutoSkillTitle_175": unicode('金甲反击','utf-8'),
    "AutoSkillTitle_176": unicode('孤注一掷','utf-8'),
    "AutoSkillTitle_177": unicode('冥火领域','utf-8'),
    "AutoSkillTitle_178": unicode('玄冥领域','utf-8'),
    "AutoSkillTitle_179": unicode('冥藤领域','utf-8'),
    "AutoSkillTitle_180": unicode('玄雷领域','utf-8'),
    "AutoSkillTitle_181": unicode('雷冥领域','utf-8'),
    "AutoSkillTitle_182": unicode('劫富济贫','utf-8'),

    "AutoSkillTitle_183": unicode('心2.5倍','utf-8'),
#################################Ver 3.5更新#################################################
    "AutoSkillTitle_184": unicode('南蛮铠甲','utf-8'),
    "AutoSkillTitle_185": unicode('贪狼阵','utf-8'),
    "AutoSkillTitle_186": unicode('乌戈藤甲','utf-8'),
    "AutoSkillTitle_187": unicode('极恶的战意','utf-8'),
    "AutoSkillTitle_188": unicode('三国一统','utf-8'),
    "AutoSkillTitle_189": unicode('司马昭的野心','utf-8'),
    "AutoSkillTitle_190": unicode('九五之尊·天罚','utf-8'),
    "AutoSkillTitle_191": unicode('冢虎·神泣','utf-8'),
    "AutoSkillTitle_192": unicode('凰皇·绝影宫','utf-8'),
    "AutoSkillTitle_193": unicode('仁德枭雄','utf-8'),
    "AutoSkillTitle_194": unicode('乱世奸雄','utf-8'),
    "AutoSkillTitle_195": unicode('东吴雄主','utf-8'),
    "AutoSkillTitle_196": unicode('四世三公','utf-8'),
    "AutoSkillTitle_197": unicode('西凉铁骑','utf-8'),
    "AutoSkillTitle_198": unicode('蜀之魂','utf-8'),
    "AutoSkillTitle_199": unicode('魏之魂','utf-8'),
    "AutoSkillTitle_200": unicode('吴之魂','utf-8'),
    "AutoSkillTitle_201": unicode('乱世之力','utf-8'),
    "AutoSkillTitle_202": unicode('葵花落','utf-8'),
    "AutoSkillTitle_203": unicode('舍身护主','utf-8'),
    "AutoSkillTitle_204": unicode('假传圣旨','utf-8'),
    "AutoSkillTitle_205": unicode('兰花指法','utf-8'),
    "AutoSkillTitle_206": unicode('群邪辟易','utf-8'),
    "AutoSkillTitle_207": unicode('飞花旋','utf-8'),
    "AutoSkillTitle_208": unicode('花雨散','utf-8'),
    "AutoSkillTitle_209": unicode('攻防一体-炎铠','utf-8'),
    "AutoSkillTitle_210": unicode('攻防一体-冰甲','utf-8'),
    "AutoSkillTitle_211": unicode('攻防一体-风盾','utf-8'),
    "AutoSkillTitle_212": unicode('攻防一体-雷铠','utf-8'),
    "AutoSkillTitle_213": unicode('攻防一体-冥盾','utf-8'),
    "AutoSkillTitle_214": unicode('炙天麒麟炎','utf-8'),
    "AutoSkillTitle_215": unicode('冰霜龙之魄','utf-8'),
    "AutoSkillTitle_216": unicode('凶罗刹结界','utf-8'),
    "AutoSkillTitle_217": unicode('雷霆回天术','utf-8'),
    "AutoSkillTitle_218": unicode('漆黑时光术','utf-8'),
    "AutoSkillTitle_219": unicode('爆炎红莲魂','utf-8'),
    "AutoSkillTitle_220": unicode('爆炎红莲魂','utf-8'),
    "AutoSkillTitle_221": unicode('荆棘森罗魂','utf-8'),
    "AutoSkillTitle_222": unicode('雷神的裁决','utf-8'),
    "AutoSkillTitle_223": unicode('暗夜的俘虏','utf-8'),
    "AutoSkillTitle_224": unicode('爆炎麒麟儿','utf-8'),
    "AutoSkillTitle_225": unicode('玄冰之骁将','utf-8'),
    "AutoSkillTitle_226": unicode('森罗之狱将','utf-8'),
    "AutoSkillTitle_227": unicode('雷霆之龙将','utf-8'),
    "AutoSkillTitle_228": unicode('冥域之女帝','utf-8'),

    "AutoSkillTitle_229": unicode('炎凰军势','utf-8'),
    "AutoSkillTitle_230": unicode('炎凰军势·狂','utf-8'),
    "AutoSkillTitle_231": unicode('蛟龙军势','utf-8'),
    "AutoSkillTitle_232": unicode('蛟龙军势·极','utf-8'),
    "AutoSkillTitle_233": unicode('龙将军势','utf-8'),
    "AutoSkillTitle_234": unicode('龙将军势·狂','utf-8'),
    "AutoSkillTitle_235": unicode('猛虎军势','utf-8'),
    "AutoSkillTitle_236": unicode('猛虎军势·极','utf-8'),
    "AutoSkillTitle_237": unicode('黑龙军势','utf-8'),
    "AutoSkillTitle_238": unicode('黑龙军势·极','utf-8'),
    "AutoSkillTitle_239": unicode('浑沌之力','utf-8'),
    "AutoSkillTitle_240": unicode('穷奇之力','utf-8'),
    "AutoSkillTitle_241": unicode('梼杌之力','utf-8'),
    "AutoSkillTitle_242": unicode('饕餮之力','utf-8'),
    "AutoSkillTitle_243": unicode('大乔小乔','utf-8'),

    "AutoSkillTitle_244": unicode('爆炎红莲魂','utf-8'),
    "AutoSkillTitle_245": unicode('玄冰瀚海魂','utf-8'),
    "AutoSkillTitle_246": unicode('荆棘森罗魂','utf-8'),
    "AutoSkillTitle_247": unicode('爆炎麒麟儿','utf-8'),
    "AutoSkillTitle_248": unicode('玄冰之骁将','utf-8'),
    "AutoSkillTitle_249": unicode('森罗之狱将','utf-8'),
    "AutoSkillTitle_250": unicode('雷霆之龙将','utf-8'),
    "AutoSkillTitle_251": unicode('冥域之女帝','utf-8'),

    "AutoSkillTitle_252": unicode('延时5秒','utf-8'),
    "AutoSkillTitle_253": unicode('火&金石攻击2','utf-8'),
    "AutoSkillTitle_254": unicode('水&骁勇攻击2','utf-8'),
    "AutoSkillTitle_255": unicode('木&骁勇攻击2','utf-8'),
    "AutoSkillTitle_256": unicode('光&金石攻击2','utf-8'),
    "AutoSkillTitle_257": unicode('暗&骁勇攻击2','utf-8'),
    "AutoSkillTitle_258": unicode('武将掉率提升','utf-8'),
    "AutoSkillTitle_259": unicode('火HP&攻击2','utf-8'),
    "AutoSkillTitle_260": unicode('水HP&攻击2','utf-8'),
    "AutoSkillTitle_261": unicode('木HP&攻击2','utf-8'),
    "AutoSkillTitle_262": unicode('光HP&回复&攻击1.5','utf-8'),
    "AutoSkillTitle_263": unicode('暗HP&回复&攻击1.5','utf-8'),
    "AutoSkillTitle_264": unicode('古之恶来','utf-8'),
    "AutoSkillTitle_265": unicode('自己&暗攻击2.5','utf-8'),
    "AutoSkillTitle_266": unicode('combo8攻击5','utf-8'),
    "AutoSkillTitle_267": unicode('回复HP200%','utf-8'),
    "AutoSkillTitle_268": unicode('体力HP2.5','utf-8'),
    "AutoSkillTitle_269": unicode('火&光&暗消除攻击2.5','utf-8'),
    "AutoSkillTitle_270": unicode('水&木&暗消除攻击2.5','utf-8'),
    "AutoSkillTitle_271": unicode('水&木&光消除攻击2.5','utf-8'),
    "AutoSkillTitle_272": unicode('火&木&光消除攻击2.5','utf-8'),
    "AutoSkillTitle_273": unicode('火&水&暗消除攻击2.5','utf-8'),
    "AutoSkillTitle_274": unicode('生生HP2','utf-8'),
    "AutoSkillTitle_275": unicode('生生HP2.5','utf-8'),
    "AutoSkillTitle_276": unicode('心HPAtk2','utf-8'),
    "AutoSkillTitle_277": unicode('心HP2.5','utf-8'),
    "AutoSkillTitle_278": unicode('心Atk2.5','utf-8'),
    "AutoSkillTitle_279": unicode('神圣追打','utf-8'),
    "AutoSkillTitle_280": unicode('6cmb火攻3.5','utf-8'),
    "AutoSkillTitle_281": unicode('6cmb水攻3.5','utf-8'),
    "AutoSkillTitle_282": unicode('6cmb木攻3.5','utf-8'),
    "AutoSkillTitle_283": unicode('6cmb光攻3.5','utf-8'),
    "AutoSkillTitle_284": unicode('6cmb暗攻3.5','utf-8'),

    ##/* 被动技描述 *#/
    "jianjiahuoDsp": unicode('我方火属性武将的攻击力提升1.5倍','utf-8'),
    "jianjiashuiDsp": unicode('我方水属性武将的攻击力提升1.5倍','utf-8'),
    "jianjiamuDsp": unicode('我方木属性武将的攻击力提升1.5倍','utf-8'),
    "jianjiaguangDsp": unicode('我方光属性武将的攻击力提升1.5倍','utf-8'),
    "jianjiaanDsp": unicode('我方暗属性武将的攻击力提升1.5倍','utf-8'),

    "jingruihuoDsp": unicode('我方火属性武将的攻击力提升2倍','utf-8'),
    "jingruishuiDsp": unicode('我方水属性武将的攻击力提升2倍','utf-8'),
    "jingruimuDsp": unicode('我方木属性武将的攻击力提升2倍','utf-8'),
    "jingruiguangDsp": unicode('我方光属性武将的攻击力提升2倍','utf-8'),
    "jingruianDsp": unicode('我方暗属性武将的攻击力提升2倍','utf-8'),

    "jushouhuoDsp": unicode('火属性伤害减少','utf-8'),
    "jushoushuiDsp": unicode('水属性伤害减少','utf-8'),
    "jushoumuDsp": unicode('木属性伤害减少','utf-8'),
    "jushouguangDsp": unicode('光属性伤害减少','utf-8'),
    "jushouanDsp": unicode('暗属性伤害减少','utf-8'),

    "jintanghuoDsp": unicode('火属性伤害减少一半','utf-8'),
    "jintangshuiDsp": unicode('水属性伤害减少一半','utf-8'),
    "jintangmuDsp": unicode('木属性伤害减少一半','utf-8'),
    "jintangguangDsp": unicode('光属性伤害减少一半','utf-8'),
    "jintanganDsp": unicode('暗属性伤害减少一半','utf-8'),

    "panshiDsp": unicode('受到的所有伤害小幅减少','utf-8'),
    "moshouDsp": unicode('受到的所有伤害减少','utf-8'),

    "neijingDsp": unicode('每回合恢复少量血量','utf-8'),
    "bencaoDsp": unicode('每回合恢复一定血量','utf-8'),

    "yeyanDsp": unicode('攻击后，追加一次全体攻击','utf-8'),
    "yuyanDsp": unicode('攻击后，追加一次强力全体攻击','utf-8'),

    "longpoDsp": unicode('当受到致死攻击时，有几率生还','utf-8'),
    "zhenlongpoDsp": unicode('当受到致死攻击时，有高几率生还','utf-8'),

    "yanzhiDsp": unicode('宝石移动的最大时限延长少许','utf-8'),
    "shiguangDsp": unicode('宝石移动的最大时限延长较多','utf-8'),
    "yonghengDsp": unicode('宝石移动的最大时限延长许多','utf-8'),

    "geyingwuyanDsp": unicode('每回合恢复较多血量','utf-8'),
    "luangefengwuDsp": unicode('每回合恢复很多血量','utf-8'),
    "wujinyuyanDsp": unicode('攻击后，追加一次超强力全体攻击','utf-8'),
    "wuxiekejiDsp": unicode('受到的所有伤害大幅减少','utf-8'),

    "zhanshizhinuDsp": unicode('金石之坚类武将的攻击提升2倍','utf-8'),
    "mengjiangxuetongDsp": unicode('攻守兼备类武将的血量提升1.5倍','utf-8'),
    "baihualiaoluanDsp": unicode('生生不息类武将的攻击力提升2倍','utf-8'),
    "longzhixueDsp": unicode('金石之坚类武将的攻击提升2.5倍','utf-8'),
    "longqishishiDsp": unicode('国士无双类武将的血量提升2倍','utf-8'),
    "longqishinuDsp": unicode('国士无双类武将的攻击提升2.5倍','utf-8'),
    "sikahaDsp": unicode('攻守兼备类武将的血量提升2.5倍','utf-8'),
    "businiaoDsp": unicode('攻守兼备类武将的回复力提升2.5倍','utf-8'),
    "shenlangpaoxiaoDsp": unicode('攻守兼备类武将的攻击提升2.5倍','utf-8'),
    "waerjiliDsp": unicode('生生不息类武将的攻击力提升2.5倍','utf-8'),
    "shendaoyanDsp": unicode('神类武将的攻击提升2倍','utf-8'),

    "money15Dsp": unicode('额外获取少量金钱','utf-8'),
    "money20Dsp": unicode('额外获取大量金钱','utf-8'),

    "exp12Dsp": unicode('战斗经验小幅提升','utf-8'),
    "exp15Dsp": unicode('战斗经验大幅提升','utf-8'),

    "carddrop12Dsp": unicode('武将掉率小幅提升','utf-8'),
    "carddrop15Dsp": unicode('武将掉率大幅提升','utf-8'),

    "shuihp15Dsp": unicode('水属性武将的血量提升1.5倍','utf-8'),
    "huohp15Dsp": unicode('火属性武将的血量提升1.5倍','utf-8'),
    "muhp15Dsp": unicode('木属性武将的血量提升1.5倍','utf-8'),
    "guanghp15Dsp": unicode('光属性武将的血量提升1.5倍','utf-8'),
    "anhp15Dsp": unicode('暗属性武将的血量提升1.5倍','utf-8'),
    "shuihp20Dsp": unicode('水属性武将的血量提升2倍','utf-8'),
    "huohp20Dsp": unicode('火属性武将的血量提升2倍','utf-8'),
    "muhp20Dsp": unicode('木属性武将的血量提升2倍','utf-8'),
    "guanghp20Dsp": unicode('光属性武将的血量提升2倍','utf-8'),
    "anhp20Dsp": unicode('暗属性武将的血量提升2倍','utf-8'),

    "jiangnanstyleDsp": unicode('宝石消除的声音变为江南style','utf-8'),

    "jiyunDsp": unicode('金石之坚类武将的HP变为原本的2倍','utf-8'),

    "huo25Dsp": unicode('我方火属性武将的攻击力提升2.5倍','utf-8'),
    "shui25Dsp": unicode('我方水属性武将的攻击力提升2.5倍','utf-8'),
    "mu25Dsp": unicode('我方木属性武将的攻击力提升2.5倍','utf-8'),
    "guang25Dsp": unicode('我方光属性武将的攻击力提升2.5倍','utf-8'),
    "an25Dsp": unicode('我方暗属性武将的攻击力提升2.5倍','utf-8'),

    "lumangshuiDsp": unicode('消除水宝石，有低几率提升水属性4倍攻击','utf-8'),
    "lumanghuoDsp": unicode('消除火宝石，有低几率提升火属性4倍攻击','utf-8'),
    "lumangmuDsp": unicode('消除木宝石，有低几率提升木属性4倍攻击','utf-8'),
    "lumangguangDsp": unicode('消除光宝石，有低几率提升光属性4倍攻击','utf-8'),
    "lumanganDsp": unicode('消除暗宝石，有低几率提升暗属性4倍攻击','utf-8'),

    "wjqxshuiDsp": unicode('消除水宝石，有中等几率提升水属性3倍攻击','utf-8'),
    "wjqxhuoDsp": unicode('消除火宝石，有中等几率提升火属性3倍攻击','utf-8'),
    "wjqxmuDsp": unicode('消除木宝石，有中等几率提升木属性3倍攻击','utf-8'),
    "wjqxguangDsp": unicode('消除光宝石，有中等几率提升光属性3倍攻击','utf-8'),
    "wjqxanDsp": unicode('消除暗宝石，有中等几率提升暗属性3倍攻击','utf-8'),

    "yanhuoDsp": unicode('火属性武将攻击力和回复力提升1.5倍','utf-8'),
    "hlyanhuoDsp": unicode('火属性武将HP、攻击力和回复力提升1.5倍','utf-8'),

    "hanbingDsp": unicode('水属性武将攻击力和回复力提升1.5倍','utf-8'),
    "hhhanbingDsp": unicode('水属性武将HP、攻击力和回复力提升1.5倍','utf-8'),
    "senluoDsp": unicode('木属性武将攻击力和回复力提升1.5倍','utf-8'),
    "senluowxDsp": unicode('木属性武将HP、攻击力和回复力提升1.5倍','utf-8'),
    "xiaojiangDsp": unicode('国士无双和神将类武将的HP提升1.5倍','utf-8'),
    "lsxiaojiangDsp": unicode('国士无双和神将类武将的HP提升2倍','utf-8'),
    "kuangyeDsp": unicode('国士无双和神将类武将造成的伤害提升1.5倍','utf-8'),
    "kuangyezxDsp": unicode('国士无双和神将类武将造成的伤害提升2倍','utf-8'),

    "huofanjiDsp": unicode('受到伤害后，低几率反弹大幅火属性伤害','utf-8'),
    "shuifanjiDsp": unicode('受到伤害后，低几率反弹大幅水属性伤害','utf-8'),
    "mufanjiDsp": unicode('受到伤害后，低几率反弹大幅木属性伤害','utf-8'),
    "guangfanjiDsp": unicode('受到伤害后，中几率反弹中幅光属性伤害','utf-8'),
    "anfanjiDsp": unicode('受到伤害后，中几率反弹中幅暗属性伤害','utf-8'),

    "teddyDsp": unicode('满HP时，所有武将的伤害提升2倍','utf-8'),

    "jingruicrithuoDsp": unicode('我方火属性武将的攻击力提升2倍，有几率提升2.5倍','utf-8'),
    "jingruicritshuiDsp": unicode('我方水属性武将的攻击力提升2倍，有几率提升2.5倍','utf-8'),
    "jingruicritmuDsp": unicode('我方木属性武将的攻击力提升2倍，有几率提升2.5倍','utf-8'),
    "jingruicritguangDsp": unicode('我方光属性武将的攻击力提升2倍，有几率提升2.5倍','utf-8'),
    "jingruicritanDsp": unicode('我方暗属性武将的攻击力提升2倍，有几率提升2.5倍','utf-8'),

    "zeusDsp": unicode('满HP时，所有武将的伤害提升3倍','utf-8'),

    "armorhuomu30Dsp": unicode('火木属性伤害小幅减少','utf-8'),
    "armorhuomu50Dsp": unicode('火木属性伤害减少一半','utf-8'),
    "armorshuihuo30Dsp": unicode('水火属性伤害小幅减少','utf-8'),
    "armorshuihuo50Dsp": unicode('水火属性伤害减少一半','utf-8'),
    "armormushui30Dsp": unicode('木水属性伤害小幅减少','utf-8'),
    "armormushui50Dsp": unicode('木水属性敌伤害减少一半','utf-8'),
    "armorguanghuo30Dsp": unicode('光火属性伤害小幅减少','utf-8'),
    "armorguanghuo50Dsp": unicode('光火属性伤害减少一半','utf-8'),
    "armoranmu30Dsp": unicode('暗木属性伤害小幅减少','utf-8'),
    "armoranmu50Dsp": unicode('暗木属性伤害减少一半','utf-8'),
    "armorhuoan30Dsp": unicode('火暗属性伤害小幅减少','utf-8'),
    "armorhuoan50Dsp": unicode('火暗属性伤害减少一半','utf-8'),
    "armorshuian30Dsp": unicode('水暗属性伤害小幅减少','utf-8'),
    "armorshuian50Dsp": unicode('水暗属性伤害减少一半','utf-8'),
    "armormuguang30Dsp": unicode('木光属性伤害小幅减少','utf-8'),
    "armormuguang50Dsp": unicode('木光属性伤害减少一半','utf-8'),
    "armorguangshui30Dsp": unicode('光水伤害小幅减少','utf-8'),
    "armorguangshui50Dsp": unicode('光水伤害减少一半','utf-8'),
    "armoranguang30Dsp": unicode('暗光属性伤害小幅减少','utf-8'),
    "armoranguang50Dsp": unicode('暗光属性伤害减少一半','utf-8'),
    "armorxinhuo30Dsp": unicode('心火属性伤害小幅减少','utf-8'),
    "armorxinhuo50Dsp": unicode('心火属性伤害减少一半','utf-8'),
    "armorxinshui30Dsp": unicode('心水属性伤害小幅减少','utf-8'),
    "armorxinshui50Dsp": unicode('心水属性伤害减少一半','utf-8'),
    "armorxinmu30Dsp": unicode('心木属性伤害小幅减少','utf-8'),
    "armorxinmu50Dsp": unicode('心木属性伤害减少一半','utf-8'),
    "armorxinguang30Dsp": unicode('心光属性伤害小幅减少','utf-8'),
    "armorxinguang50Dsp": unicode('心光属性伤害减少一半','utf-8'),
    "armorxinan30Dsp": unicode('心暗属性伤害小幅减少','utf-8'),
    "armorxinan50Dsp": unicode('心暗属性伤害减少一半','utf-8'),

    "atkxinhuo15Dsp": unicode('心和火属性武将的攻击提升1.5倍','utf-8'),
    "atkxinhuo20Dsp": unicode('心和火属性武将的攻击提升2倍','utf-8'),
    "atkxinshui15Dsp": unicode('心和水属性武将的攻击提升1.5倍','utf-8'),
    "atkxinshui20Dsp": unicode('心和水属性武将的攻击提升2倍','utf-8'),
    "atkxinmu15Dsp": unicode('心和木属性武将的攻击提升1.5倍','utf-8'),
    "atkxinmu20Dsp": unicode('心和木属性武将的攻击提升2倍','utf-8'),
    "atkxinguang15Dsp": unicode('心和光属性武将的攻击提升1.5倍','utf-8'),
    "atkxinguang20Dsp": unicode('心和光属性武将的攻击提升2倍','utf-8'),
    "atkxinan15Dsp": unicode('心和暗属性武将的攻击提升1.5倍','utf-8'),
    "atkxinan20Dsp": unicode('心和暗属性武将的攻击提升2倍','utf-8'),

    "3armor50Dsp": unicode('火水木属性伤害减少一半','utf-8'),

    "qiyaDsp": unicode('回合结束后，对最虚弱敌人追加一次攻击','utf-8'),

    "ghostinviteDsp": unicode('所有武将伤害提升2倍,且每回合回复一定血量','utf-8'),

    "wenyiligongDsp": unicode('所有武将对瘟疫状态的敌将造成的伤害提升3倍','utf-8'),

    "xianjietupoDsp": unicode('当受到致死攻击时，有几率生还；每回合回复一定血量','utf-8'),

    "AutoSkillDsp_153": unicode('光属性武将攻击力和回复力提升1.5倍','utf-8'),
    "AutoSkillDsp_154": unicode('暗属性武将攻击力和回复力提升1.5倍','utf-8'),

    "AutoSkillDsp_155": unicode('火属性武将攻击力和回复力提升2倍','utf-8'),
    "AutoSkillDsp_156": unicode('水属性武将攻击力和回复力提升2倍','utf-8'),
    "AutoSkillDsp_157": unicode('木属性武将攻击力和回复力提升2倍','utf-8'),
    "AutoSkillDsp_158": unicode('光属性武将攻击力和回复力提升2倍','utf-8'),
    "AutoSkillDsp_159": unicode('暗属性武将攻击力和回复力提升2倍','utf-8'),

    "AutoSkillDsp_160": unicode('火属性武将的血量提升2.5倍','utf-8'),
    "AutoSkillDsp_161": unicode('水属性武将的血量提升2.5倍','utf-8'),
    "AutoSkillDsp_162": unicode('木属性武将的血量提升2.5倍','utf-8'),
    "AutoSkillDsp_163": unicode('光属性武将的血量提升2.5倍','utf-8'),
    "AutoSkillDsp_164": unicode('暗属性武将的血量提升2.5倍','utf-8'),

    "AutoSkillDsp_165": unicode('神类武将的攻击力变为2.5倍','utf-8'),

    "AutoSkillDsp_166": unicode('当HP为满时，受到的伤害大幅减少','utf-8'),

    "AutoSkillDsp_167": unicode('攻击后，追加一次全体克制属性攻击','utf-8'),

    "AutoSkillDsp_168": unicode('当HP为满时，所有武将的伤害提升3倍；当HP为1点时，所有武将的伤害提升4倍','utf-8'),

    "AutoSkillDsp_169": unicode('木属性武将攻击力和回复力提升1.5倍','utf-8'),
    "AutoSkillDsp_170": unicode('每回合恢复较多血量','utf-8'),
    "AutoSkillDsp_171": unicode('宝石移动的最大时限延长较多','utf-8'),
    "AutoSkillDsp_172": unicode('国士无双类武将的攻击提升2.5倍','utf-8'),
    "AutoSkillDsp_173": unicode('攻击后，追加一次强力全体攻击','utf-8'),
    "AutoSkillDsp_174": unicode('每回合恢复一定血量','utf-8'),
    "AutoSkillDsp_175": unicode('受到伤害后，中几率反弹中幅火属性伤害','utf-8'),
    "AutoSkillDsp_176": unicode('当HP不足10%时，所有武将攻击力变为3倍','utf-8'),
    "AutoSkillDsp_177": unicode('火属性伤害大幅减少，暗属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_178": unicode('水属性伤害大幅减少，暗属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_179": unicode('木属性伤害大幅减少，暗属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_180": unicode('光属性伤害大幅减少，水属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_181": unicode('暗属性伤害大幅减少，光属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_182": unicode('额外获取大量金钱','utf-8'),
    "AutoSkillDsp_183": unicode('我方心属性武将的攻击力提升2.5倍','utf-8'),
##################################Ver 3.5更新###########################################
    "AutoSkillDsp_184": unicode('受到的所有伤害减少20%','utf-8'),
    "AutoSkillDsp_185": unicode('连击达到7 Combos以上时，所有武将的攻击力变为4.0倍','utf-8'),
    "AutoSkillDsp_186": unicode('木属性和水属性武将的HP变为2倍','utf-8'),
    "AutoSkillDsp_187": unicode('骁勇善战类武将的攻击力变为2倍','utf-8'),
    "AutoSkillDsp_188": unicode('4种属性同时攻击时，所有武将的攻击力变为3.5倍','utf-8'),
    "AutoSkillDsp_189": unicode('3种属性同时攻击时，所有武将的攻击力提升3.0倍','utf-8'),
    "AutoSkillDsp_190": unicode('连击达到4Combos以上时，所有武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_191": unicode('5种属性同时攻击时，所有武将的攻击力提升5倍','utf-8'),
    "AutoSkillDsp_192": unicode('连击达到10 Combos以上时，所有武将的攻击力提升10倍','utf-8'),
    "AutoSkillDsp_193": unicode('火属性武将的攻击力和回复力变为2倍','utf-8'),
    "AutoSkillDsp_194": unicode('水属性武将的攻击力和回复力变为2倍','utf-8'),
    "AutoSkillDsp_195": unicode('木属性武将的攻击力和回复力变为2倍','utf-8'),
    "AutoSkillDsp_196": unicode('光属性武将的攻击力和回复力变为2倍','utf-8'),
    "AutoSkillDsp_197": unicode('暗属性武将的攻击力和回复力变为2倍','utf-8'),
    "AutoSkillDsp_198": unicode('火属性武将的HP和回复力提升2倍','utf-8'),
    "AutoSkillDsp_199": unicode('水属性武将的HP和回复力提升2倍','utf-8'),
    "AutoSkillDsp_200": unicode('木属性武将的HP和回复力提升2倍','utf-8'),
    "AutoSkillDsp_201": unicode('连击达到3 Combos以上时，所有武将的攻击力提升2倍','utf-8'),
    "AutoSkillDsp_202": unicode('攻击后，追加一次强力全体攻击','utf-8'),
    "AutoSkillDsp_203": unicode('受到的所有伤害减少','utf-8'),
    "AutoSkillDsp_204": unicode('火、水、木同时攻击时，所有武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_205": unicode('受到伤害时，有中等几率进行反击，造成5倍于受到伤害的光属性伤害','utf-8'),
    "AutoSkillDsp_206": unicode('暗属性敌人造成的伤害减少','utf-8'),
    "AutoSkillDsp_207": unicode('攻守兼备类武将的攻击力和回复力提升1.5倍','utf-8'),
    "AutoSkillDsp_208": unicode('攻守兼备类武将的HP、攻击力和回复力提升1.5倍','utf-8'),
    "AutoSkillDsp_209": unicode('我方火属性武将的攻击力提升2.5倍，且木属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_210": unicode('我方水属性武将的攻击力提升2.5倍，且火属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_211": unicode('我方木属性武将的攻击力提升2.5倍，且水属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_212": unicode('我方光属性武将的攻击力提升2.5倍，且暗属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_213": unicode('我方暗属性武将的攻击力提升2.5倍，且光属性伤害小幅减少','utf-8'),
    "AutoSkillDsp_214": unicode('我方火属性武将的攻击力提升2.5倍，且每回合追加一次对全体敌人的强力攻击','utf-8'),
    "AutoSkillDsp_215": unicode('我方水属性武将的攻击力提升2.5倍，且当受到一次致死攻击时有几率生还','utf-8'),
    "AutoSkillDsp_216": unicode('我方木属性武将的攻击力提升2.5倍，且火水木属性减伤25%','utf-8'),
    "AutoSkillDsp_217": unicode('我方光属性武将的攻击力提升2.5倍，且每回合回复相当于主将自身回复力300%的HP','utf-8'),
    "AutoSkillDsp_218": unicode('我方暗属性武将的攻击力提升2.5倍，且宝石移动的最大时限加3秒','utf-8'),
    "AutoSkillDsp_219": unicode('我方火属性武将的攻击力提升2.5倍，且火属性武将的HP和回复力提升1.5倍','utf-8'),
    "AutoSkillDsp_220": unicode('我方水属性武将的攻击力提升2.5倍，且水属性武将的HP和回复力提升1.5倍','utf-8'),
    "AutoSkillDsp_221": unicode('我方木属性武将的攻击力提升2.5倍，且木属性武将的HP和回复力提升1.5倍','utf-8'),
    "AutoSkillDsp_222": unicode('我方光属性武将的攻击力提升2.5倍；达到6连击以上时，我方光属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_223": unicode('我方暗属性武将的攻击力提升2.5倍；达到6连击以上时，我方暗属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_224": unicode('我方火属性武将的攻击力提升2.5倍，且火属性武将的回复力提升2倍','utf-8'),
    "AutoSkillDsp_225": unicode('我方水属性武将的攻击力提升2.5倍，且水属性武将的回复力提升2倍','utf-8'),
    "AutoSkillDsp_226": unicode('我方木属性武将的攻击力提升2.5倍，且木属性武将的回复力提升2倍','utf-8'),
    "AutoSkillDsp_227": unicode('我方光属性武将的攻击力提升2.5倍，且光属性武将的回复力提升2倍','utf-8'),
    "AutoSkillDsp_228": unicode('我方暗属性武将的攻击力提升2.5倍，且暗属性武将的回复力提升2倍','utf-8'),

    "AutoSkillDsp_229": unicode('攻守兼备类武将的攻击力变为1.5倍','utf-8'),
    "AutoSkillDsp_230": unicode('攻守兼备类武将的HP和攻击力变为2倍','utf-8'),
    "AutoSkillDsp_231": unicode('生生不息类武将的攻击力和回复力变为1.5倍','utf-8'),
    "AutoSkillDsp_232": unicode('生生不息类武将的HP、攻击力和回复力变为1.5倍','utf-8'),
    "AutoSkillDsp_233": unicode('骁勇善战类武将的攻击力变为1.5倍','utf-8'),
    "AutoSkillDsp_234": unicode('骁勇善战类武将的HP和攻击力变为2倍','utf-8'),
    "AutoSkillDsp_235": unicode('金石之坚类武将的攻击力和回复力变为1.5倍','utf-8'),
    "AutoSkillDsp_236": unicode('金石之坚类武将的HP、攻击力和回复力变为1.5倍','utf-8'),
    "AutoSkillDsp_237": unicode('骁勇善战类武将的攻击力和回复力变为1.5倍','utf-8'),
    "AutoSkillDsp_238": unicode('骁勇善战类武将的HP、攻击力和回复力变为1.5倍','utf-8'),
    "AutoSkillDsp_239": unicode('发动火属性群攻时，我方火属性武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_240": unicode('发动水属性群攻时，我方水属性武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_241": unicode('发动木属性群攻时，我方木属性武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_242": unicode('发动暗属性群攻时，我方暗属性武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_243": unicode('当HP不足20%时，受到的所有伤害大幅减少','utf-8'),

    "AutoSkillDsp_244": unicode('我方火属性武将的攻击力提升2.5倍；达到6连击以上时，我方火属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_245": unicode('我方水属性武将的攻击力提升2.5倍；达到6连击以上时，我方水属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_246": unicode('我方木属性武将的攻击力提升2.5倍；达到6连击以上时，我方木属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_247": unicode('我方火属性和攻守兼备类武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_248": unicode('我方水属性和金石之坚类武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_249": unicode('我方木属性和国士无双类武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_250": unicode('我方光属性和神将类武将的攻击力提升2.5倍','utf-8'),
    "AutoSkillDsp_251": unicode('我方暗属性和生生不息类武将的攻击力提升2.5倍','utf-8'),

    "AutoSkillDsp_252": unicode('宝石移动的最大时限延长少许','utf-8'),
    "AutoSkillDsp_253": unicode('火属性和金石之坚类武将的攻击力变为2倍','utf-8'),
    "AutoSkillDsp_254": unicode('水属性和骁勇善战类武将的攻击力变为2倍','utf-8'),
    "AutoSkillDsp_255": unicode('木属性和骁勇善战类武将的攻击力变为2倍','utf-8'),
    "AutoSkillDsp_256": unicode('光属性和金石之坚类武将的攻击力变为2倍','utf-8'),
    "AutoSkillDsp_257": unicode('暗属性和骁勇善战类武将的攻击力变为2倍','utf-8'),
    "AutoSkillDsp_258": unicode('武将掉率大幅提升','utf-8'),
    "AutoSkillDsp_259": unicode('火属性武将的HP和攻击力变为2倍','utf-8'),
    "AutoSkillDsp_260": unicode('水属性武将的HP和攻击力变为2倍','utf-8'),
    "AutoSkillDsp_261": unicode('木属性武将的HP和攻击力变为2倍','utf-8'),
    "AutoSkillDsp_262": unicode('光属性武将的HP、攻击力和回复力变为1.5倍','utf-8'),
    "AutoSkillDsp_263": unicode('暗属性武将的HP、攻击力和回复力变为1.5倍','utf-8'),
    "AutoSkillDsp_264": unicode('当HP不足20%时，所有武将的攻击力变为4倍','utf-8'),
    "AutoSkillDsp_265": unicode('自身和暗属性武将的攻击力变为2.5倍','utf-8'),
    "AutoSkillDsp_266": unicode('连击达到8 Combos以上时，所有武将的攻击力变为5倍','utf-8'),
    "AutoSkillDsp_267": unicode('每回合回复相当于队长武将自身回复力200%的HP，没有产生消除的话不会触发该效果','utf-8'),
    "AutoSkillDsp_268": unicode('体力类武将的HP变为2.5倍','utf-8'),
    "AutoSkillDsp_269": unicode('火、光、暗同时攻击时，所有武将的攻击力变为2.5倍','utf-8'),
    "AutoSkillDsp_270": unicode('水、木、暗同时攻击时，所有武将的攻击力变为2.5倍','utf-8'),
    "AutoSkillDsp_271": unicode('水、木、光同时攻击时，所有武将的攻击力变为2.5倍','utf-8'),
    "AutoSkillDsp_272": unicode('火、木、光同时攻击时，所有武将的攻击力变为2.5倍','utf-8'),
    "AutoSkillDsp_273": unicode('火、水、暗同时攻击时，所有武将的攻击力变为2.5倍','utf-8'),
    "AutoSkillDsp_274": unicode('生生不息类武将的HP变为2倍','utf-8'),
    "AutoSkillDsp_275": unicode('生生不息类武将的HP变为2.5倍','utf-8'),
    "AutoSkillDsp_276": unicode('心属性武将的HP和攻击力变为2倍','utf-8'),
    "AutoSkillDsp_277": unicode('心属性武将的HP变为2.5倍','utf-8'),
    "AutoSkillDsp_278": unicode('心属性武将的攻击力变为2.5倍','utf-8'),
    "AutoSkillDsp_279": unicode('每回合对所有敌人造成1000点固定伤害','utf-8'),
    "AutoSkillDsp_280": unicode('连击达到6Combos以上时，我方火属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_281": unicode('连击达到6Combos以上时，我方水属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_282": unicode('连击达到6Combos以上时，我方木属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_283": unicode('连击达到6Combos以上时，我方光属性武将的攻击力提升3.5倍','utf-8'),
    "AutoSkillDsp_284": unicode('连击达到6Combos以上时，我方暗属性武将的攻击力提升3.5倍','utf-8'),

    #/* 敌将技能名 *#/
"enemyskill_lianhuan": unicode('连环','utf-8'),
 "enemyskill_lianda": unicode('连打','utf-8'),
 "enemyskill_zhongji": unicode('重击','utf-8'),
 "enemyskill_qiangxi": unicode('强袭','utf-8'),
 "enemyskill_suigu": unicode('碎骨','utf-8'),
 "enemyskill_yishan": unicode('一闪','utf-8'),
 "enemyskill_wushuang":unicode('五点梅花刺','utf-8'),
 "enemyskill_huoxijin":unicode('火系·封印','utf-8'),
 "enemyskill_shuixijin":unicode('水系·封印','utf-8'),
 "enemyskill_muxijin":unicode('木系·封印','utf-8'),
 "enemyskill_guangxijin":unicode('光系·封印','utf-8'),
 "enemyskill_anxijin":unicode('暗系·封印','utf-8'),
 "enemyskill_shenxijin":unicode('神系·封印','utf-8'),
 "enemyskill_luanshijin":unicode('乱世·封印','utf-8'),
 "enemyskill_zhiyu":unicode('命疗术','utf-8'),
 "enemyskill_fuhuo":unicode('圣疗','utf-8'),
 "enemyskill_nizhuanhuo":unicode('逆转·火','utf-8'),
 "enemyskill_nizhuanshui":unicode('逆转·水','utf-8'),
 "enemyskill_nizhuanmu":unicode('逆转·木','utf-8'),
 "enemyskill_nizhuanguang":unicode('逆转·光','utf-8'),
 "enemyskill_nizhuanan":unicode('逆转·暗','utf-8'),
 "enemyskill_nizhuanhuifu":unicode('回复·禁！','utf-8'),
 "enemyskill_nizhuantianxia":unicode('逆转·天下','utf-8'),
 "enemyskill_wushenghuyou":unicode('武圣护佑','utf-8'),
 "enemyskill_shenlingbiyou":unicode('神佑','utf-8'),
 "enemyskill_xushidaifa":unicode('狂怒三绝杀','utf-8'),


    "enemyskill_jinu":unicode('激怒','utf-8'),
    "enemyskill_kuangbao":unicode('狂暴','utf-8'),
    "enemyskill_gongjizitai":unicode('攻击姿态','utf-8'),
    "enemyskill_baonu":unicode('狂暴五锤','utf-8'),
    "enemyskill_shashoujian":unicode('杀手锏','utf-8'),
    "enemyskill_nanmanruqin":unicode('南蛮入侵','utf-8'),
    "enemyskill_zhuqueqi":unicode('双重封印','utf-8'),
    "enemyskill_wohenying":unicode('大王威武','utf-8'),
    "enemyskill_tagengying":unicode('小子！你完了','utf-8'),
    "enemyskill_haoyin":unicode('豪饮','utf-8'),
    "enemyskill_mengshouluanwu":unicode('猛兽乱舞','utf-8'),
    "enemyskill_zhenfuhuo":unicode('福泽苍生','utf-8'),
    "enemyskill_tu":unicode('好酒！','utf-8'),
    "enemyskill_fuhuo":unicode('圣疗','utf-8'),
    "enemyskill_binsi":unicode('濒死','utf-8'),
    "enemyskill_mutengjia":unicode('木藤甲','utf-8'),
    "enmeybuff_shenfa": unicode('神罚','utf-8'),
    "enmeybuff_wenyihuanjing": unicode('瘟疫幻境','utf-8'),
    "enemyskill_luanshitianxia":unicode('横扫千军','utf-8'),
    "enemyskill_luanshitianxia2":unicode('乱世天下2','utf-8'),
    "enemyskill_shuohua20":unicode('寒光闪现','utf-8'),
    "enemyskill_newjinganghuti":unicode('无懈可击','utf-8'),
##################################Ver 3.5更新############################################
    "enemyskill_newjinganghuti2":unicode('无懈可击2','utf-8'),

    "enemyskill_jinu2":unicode('激怒2','utf-8'),
    "enemyskill_lianji5": unicode('5连击','utf-8'),
    "enemyskill_zhuqueqi2": unicode('朱雀旗2','utf-8'),
    "enemyskill_baozou": unicode('暴走','utf-8'),
    "enemyskill_nanmanruqin2": unicode('南蛮入侵2','utf-8'),
    "enemyskill_tongguiyujin": unicode('同归于尽','utf-8'),
    "enemyskill_bingfengshike": unicode('冰封时刻','utf-8'),
    "enemyskill_eyunyiji": unicode('厄运一击','utf-8'),
    "enemyskill_shijianningjie": unicode('时间凝结','utf-8'),
    "enemyskill_jinshuhuo": unicode('禁术·火','utf-8'),
    "enemyskill_dianguanghuoshi": unicode('电光火石','utf-8'),
    "enemyskill_xingyunyiji": unicode('幸运一击','utf-8'),
    "enemyskill_zibao": unicode('自爆','utf-8'),
    "enemyskill_mutengjia2": unicode('木藤甲2','utf-8'),
    "enemyskill_bingfengshike2": unicode('冰封时刻2','utf-8'),
    "enemyskill_quyan": unicode('驱炎','utf-8'),
    "enemyskill_duanliu": unicode('断流','utf-8'),
    "enemyskill_pomu": unicode('破木','utf-8'),
    "enemyskill_zhanlei": unicode('斩雷','utf-8'),
    "enemyskill_shihun": unicode('噬魂','utf-8'),
    "enemyskill_lianji82": unicode('2连击80','utf-8'),
    "enemyskill_lianji83": unicode('6连击100','utf-8'),
    "enemyskill_baozhuyincang": unicode('宝珠隐藏','utf-8'),

    "enemyskill_bingfengshike_ep": unicode('封印5名武将','utf-8'),

    #/* 敌将buff名 *#/
    "enmeyBuffId_1": unicode('金刚加持','utf-8'),
    "enmeyBuffId_2": unicode('无言枷锁','utf-8'),
    "enmeyBuffId_3": unicode('永恒时光','utf-8'),
    "enmeyBuffId_4": unicode('罗刹之凝视','utf-8'),
##################################Ver 3.5更新############################################
    "enmeybuff_liushuifanshi": unicode('流水反噬','utf-8'),
    "enmeybuff_shuxinghudun": unicode('异术属性护盾','utf-8'),
    "enmeybuff_shenyuan": unicode('妖术深渊','utf-8'),
    "enmeybuff_taipingdao": unicode('妖术太平道','utf-8'),
    "enmeybuff_taipingyaoshu": unicode('奥义太平要术','utf-8'),
    "enmeybuff_shuxingzhuanhuan": unicode('属性转换','utf-8'),

##################################Ver 4.0更新############################################
    "enmeybuff_shengguangdun": unicode('圣光盾','utf-8'),
    "enmeybuff_wenyi": unicode('瘟疫','utf-8'),
    "enmeybuff_hunyuandun": unicode('混元盾','utf-8'),
    "enmeybuff_shiguangnizhuan": unicode('时光逆转','utf-8'),
    "enmeybuff_shihunhuo": unicode('噬魂·火','utf-8'),
    "enmeybuff_shihunshui": unicode('噬魂·水','utf-8'),
    "enmeybuff_shihunmu": unicode('噬魂·木','utf-8'),
    "enmeybuff_shihunguang": unicode('噬魂·光','utf-8'),
    "enmeybuff_shihunan": unicode('噬魂·暗','utf-8'),
    "enmeybuff_shiqiangdinruo": unicode('恃强凛弱','utf-8'),
    "enmeybuff_wenyi2": unicode('瘟疫2','utf-8'),
    "enmeybuff_wenyihuanjing2": unicode('瘟疫幻境2','utf-8'),
    "enmeybuff_wenyihuanjing3": unicode('瘟疫幻境3','utf-8'),


    #/* title *#/
    "title_biandui": unicode('编队','utf-8'),
    "title_qianghua": unicode('强化','utf-8'),
    "title_zhuansheng": unicode('转生/超转生/觉醒','utf-8'),
    "title_sell": unicode('出售','utf-8'),
    "title_box": unicode('军营','utf-8'),
    "sk_lv_up_double": unicode('技能强化up','utf-8'),

    "title_yuanbao": unicode('元宝商店','utf-8'),
    "title_expand": unicode('军营扩充','utf-8'),
    "title_huifu": unicode('体力回复','utf-8'),
    "title_friend expand": unicode('好友扩充','utf-8'),

    "title_freegacha": unicode('求良将','utf-8'),
    "title_freegacha2": unicode('求神将','utf-8'),
    "title_swap": unicode('title_swap.png','utf-8'),

    "title_invite": unicode('邀请好友','utf-8'),
    "title_myfrd": unicode('我的好友','utf-8'),
    "title_searchfrd": unicode('搜索好友','utf-8'),
    "title_shenqing": unicode('好友请求','utf-8'),
    "title_country": unicode('国家','utf-8'),
    "title_mail": unicode('邮件','utf-8'),

    "title_tujian": unicode('武将图鉴','utf-8'),
    "title_set": unicode('设置','utf-8'),
    "title_qiehuan": unicode('切换帐号','utf-8'),
    "title_guide": unicode('游戏攻略','utf-8'),
    "title_qqwb": unicode('绑定腾讯微博','utf-8'),
    "title_sinawb": unicode('绑定新浪微博','utf-8'),
    "title_forum": unicode('游戏论坛','utf-8'),

    "title_zhanchang": unicode('战场','utf-8'),
    "title_event": unicode('特殊战场','utf-8'),
    "title_reward": unicode('获得奖励','utf-8'),
    "title_wujiang": unicode('武将','utf-8'),
    "title_gacha": unicode('求将','utf-8'),
    "title_shop": unicode('商店','utf-8'),
    "title_friend": unicode('好友','utf-8'),
    "title_others": unicode('攻略','utf-8'),

    "title_biandui_title": unicode('编队','utf-8'),
    "title_qianghua_title": unicode('强化','utf-8'),
    "title_niepan_png": unicode('涅磐','utf-8'),
    "title_zhuansheng_title": unicode('转生','utf-8'),
    "title_box_title": unicode('军营','utf-8'),
    "title_basecard": unicode('基础武将选择','utf-8'),
    "title_materialchose": unicode('素材选择','utf-8'),
    "title_cardsell": unicode('title_cardsell.png','utf-8'),
    "title_swap_title": unicode('点将台','utf-8'),

     #compGacha
    "compGachaTip1": unicode('剩余:%lld天','utf-8'),
    "compGachaTip2": unicode('剩余:%lld小时','utf-8'),
    "compGachaTip3": unicode('剩余:%lld分','utf-8'),
    "compGachaTip4": unicode('剩余次数：%d','utf-8'),
     "compGachaTip5": unicode('不限次数','utf-8'),
     "compGachaTip6": unicode('兑换武将','utf-8'),
     "compGachaTip7": unicode('请确认是否兑换','utf-8'),
     "compGachaTip8": unicode('帮助','utf-8'),
     "helperTip": unicode('援军选择','utf-8'),
     "confirmDeadTip1": unicode('是否退出','utf-8'),
     "confirmDeadTip2": unicode('警告:退出后，战场上获得的所有武将以及金钱都会消失！','utf-8'),

   # share_sanguo
     "share_copy_code": unicode('拷贝邀请码','utf-8'),
     "share_sanguo": unicode('分享给朋友们吧!','utf-8'),
     "share_Weixin": unicode('分享给微信朋友们吧!','utf-8'),
     "share_TX_XL": unicode('分享给腾讯/新浪微博!','utf-8'),
     "weixin_extInfo": unicode('<xml>逆转三国</xml>','utf-8'),
     "weixinunload":unicode('请确认已安装最新的微信版本','utf-8'),
     "weixininvite":unicode('邀请码:','utf-8'),

     "weixinstopconn":unicode('您已取消了通信！','utf-8'),

     "mainSceneTip17":unicode('编队不正确','utf-8'),
     "mainSceneTip18":unicode('请选择正确的编队','utf-8'),

    "gachaDlgTip18": unicode('求一次','utf-8'),

     "otherMainTip9": unicode('您确定要切换帐号吗？','utf-8'),

    # social
    "title_social": unicode('社交','utf-8'),

    "title_country": unicode('同  盟','utf-8'),
    "title_friend_title": unicode('好  友','utf-8'),
    "title_mail": unicode('邮  件','utf-8'),

    "naviText_social_1": unicode('加入同盟，可以享受同盟福利，还有增益状态哦','utf-8'),
    "naviText_social_2": unicode('选择好友作为友军后，可获得更多的援军点','utf-8'),
    "naviText_social_3": unicode('现在可以发送邮件给绑定账号的好友，更快更及时的交流游戏心得','utf-8'),

    "cfmBtn_Mail": unicode('发邮件','utf-8'),
    "cfmBtn_DeleteFriend": unicode('删除好友','utf-8'),

    #邮件
    "mail_title": unicode('邮件','utf-8'),
    "mail_nomail": unicode('暂无邮件','utf-8'),
    "mail_reply": unicode('回信','utf-8'),
    "mail_open": unicode('收信','utf-8'),
    "mail_none": unicode('系统邮件','utf-8'),
    "mail_close": unicode('关闭','utf-8'),
##################################Ver 3.5更新##########################################
    "mail_clear_all": unicode('清空','utf-8'),
    "mail_clear_all_title": unicode('清空邮件','utf-8'),
    "mail_clear_all_content": unicode('您确定要删除所有邮件吗？','utf-8'),


    # country
    "actionPoint_full": unicode('战斗力已满无需回复！','utf-8'),
    "actionPoint_recover": unicode('使用%d个元宝可回复全部战斗力','utf-8'),
    "actionPoint_recover_title": unicode('战斗力回复','utf-8'),
    "actionPoint_notEnough": unicode('使用%d个元宝回复战斗力吗？','utf-8'),
    "actionPoint_notEnough_title": unicode('战斗力不足','utf-8'),
    "actionPoint_coin_notEnough": unicode('您现有%d个元宝，回复战斗力需要%d个元宝，是否要去商店购买？','utf-8'),
    "cntry_country": unicode('同盟','utf-8'),
    "cntry_country4_1": unicode('在同盟中，可以结交各位英雄豪杰，且收获许多利益','utf-8'),
    "cntry_create_country": unicode('创建同盟','utf-8'),
    "cntry_join_country": unicode('加入同盟','utf-8'),
    "cntry_find_country": unicode('查找同盟','utf-8'),
    "cntry_manage": unicode('内政管理','utf-8'),
    "cntry_member_list": unicode('成员列表','utf-8'),
    "cntry_member_manage": unicode('成员管理','utf-8'),
    "chatmembermanage": unicode('管理','utf-8'),
    "cntry_chatroom": unicode('同盟聊天室','utf-8'),
    "cntry_country_info": unicode('同盟详情','utf-8'),
    "cntry_recent_info": unicode('同盟近况','utf-8'),
    "cntry_country_rank": unicode('同盟排名','utf-8'),
    "cntry_create_country4_1": unicode('国家等级越高，可开启的保卫战级别越多，越高级别的保卫战奖励也越多！','utf-8'),
    "cntry_join_country4_1": unicode('加入同盟后，可以享受同盟福利，还有增益状态哦','utf-8'),
    "cntry_oldest_country": unicode('最早创建的同盟','utf-8'),
    "cntry_newest_country": unicode('最新创建的同盟','utf-8'),
    "cntry_strongest_country": unicode('实力强的同盟','utf-8'),
    "cntry_search_country4_1": unicode('在这里，可以搜索同盟，进行申请操作','utf-8'),
    "cntry_search_country": unicode('搜索同盟','utf-8'),
    "cntry_country_list4_1": unicode('可同时申请多个同盟，成为某个同盟成员后，其他申请自动失效','utf-8'),
    "cntry_country_list": unicode('同盟列表','utf-8'),
    "cntry_country_rank4_1": unicode('同盟等级越高，实力越强','utf-8'),
    "cntry_change_declaration4_1": unicode('在这里您可以修改同盟宣言，召集志同道合的各位英雄豪杰！','utf-8'),
    "cntry_change_declaration": unicode('修改宣言','utf-8'),
    "cntry_manage4_1": unicode('在这里可以进行许多同盟相关操作','utf-8'),
    "cntry_country_donate": unicode('国库捐献','utf-8'),
    "cntry_exchange_p": unicode('藏宝库','utf-8'),
    "cntry_exchange_p0": unicode('你确定要兑换福利吗','utf-8'),
    "cntry_country_fight": unicode('同盟保卫战','utf-8'),
    "cntry_apply": unicode('会员申请','utf-8'),
    "cntry_quit_country": unicode('退出同盟','utf-8'),
    "cntry_deliver_p": unicode('分配战利品','utf-8'),
    "cntry_dismis_country": unicode('解散同盟','utf-8'),
    "cntry_dismis_country_cancel": unicode('取消解散','utf-8'),
    "cntry_country_donate4_1": unicode('捐献元宝后，可为本盟增加同盟元宝','utf-8'),
    "cntry_country_donate4_2": unicode('捐献的元宝上限，不能超过当前账号总充值元宝上限','utf-8'),
    "cntry_exchange_p4_1": unicode('在这里，您可以使用个人军粮兑换各种福利哦','utf-8'),
    "cntry_exchange_p4_2": unicode('同盟等级越高，成员可兑换的福利越多','utf-8'),
    "cntry_share_p4_1": unicode('您可以在当前界面为所有成员分配战利品','utf-8'),
    "cntry_country_fight4_1": unicode('国家等级越高，可开启的保卫战级别越多，越高级别的保卫战奖励也越多！','utf-8'),
    "cntry_country_fight4_2": unicode('成功击杀保卫战BOSS后，还有高额奖励获得','utf-8'),
    "cntry_join": unicode('参与','utf-8'),
    "cntry_rank": unicode('伤害排行','utf-8'),
    "cntry_open": unicode('开启','utf-8'),
    "cntry_open_": unicode('未开启','utf-8'),
    "cntry_recover": unicode('战斗力\n回复','utf-8'),



    "cntry_hint": unicode('提示','utf-8'),
    "cntry_hintcontent1": unicode('主动退出同盟将清除个人军粮等所有的同盟数据，您确定要离开同盟吗？','utf-8'),
    "cntry_hintcontent2": unicode('盟主，您确定要解散同盟吗？','utf-8'),
    "cntry_apply4_1": unicode('查看申请加入的成员','utf-8'),

    "cntry_no_request": unicode('暂无申请加入同盟的请求','utf-8'),
    "cntry_no_cntry": unicode('暂无同盟','utf-8'),
    "cntry_member_list4_1": unicode('成员列表，成员列表，成员列表，成员列表','utf-8'),
    "cntry_member_list4_2": unicode('在这里可以查询当前所有同盟成员信息','utf-8'),
    "cntry_rank_status": unicode('顺序\n职位','utf-8'),
    "cntry_rank_level": unicode('顺序\n等级','utf-8'),
    "cntry_rank_contribution": unicode('顺序\n贡献','utf-8'),
    "cntry_rank_login": unicode('顺序\n登陆','utf-8'),
    "cntry_promotion": unicode('增益状态升级','utf-8'),
    "cntry_promotion4_1": unicode('同盟等级越高，可升级的增益状态越高','utf-8'),
    "cntry_level_up": unicode('升级','utf-8'),
    "cntry_up": unicode('同盟升级','utf-8'),
    "cntry_up4_1": unicode('同盟升级后，可开启更高等级的保卫战，学习更高等级的增益状态，还可以兑换更多福利哦','utf-8'),
    "cntry_recent_info4_1": unicode('在这里，可以查看最近的同盟信息','utf-8'),


    "cntry_createcontent1": unicode('请输入要创建同盟的名字','utf-8'),
    "cntry_createcontent2": unicode('请输入要创建同盟的宣言','utf-8'),
    "cntry_create_alone": unicode('创建','utf-8'),
    "cntry_hintcontent3": unicode('您当前元宝不足，无法创建','utf-8'),

    "cntry_rank_show": unicode('排行榜','utf-8'),
    "cntry_deliver_target": unicode('分配目标','utf-8'),
    "cntry_delivercontent1": unicode('请输入要分配的战利品数','utf-8'),
    "cntry_allmember": unicode('所有成员','utf-8'),
    "cntry_delivercontent2": unicode('请输入要平均分配给每个人的战利品','utf-8'),
    "cntry_delivercontent3": unicode('请输入要按贡献分配给所有人的战利品','utf-8'),
    "cntry_country_money": unicode('战利品：','utf-8'),
    "cntry_country_money2": unicode('当前同盟战利品：','utf-8'),
####################################Ver 3.5更新#########################################
    "cntry_country_coin": unicode('当前可分配元宝：','utf-8'),
    "cntry_assign_coin_lb": unicode('请输入要分配的元宝数','utf-8'),

    "cntry_king": unicode('盟主','utf-8'),
    "cntry_country_id": unicode('同盟ID：','utf-8'),
    "cntry_country_level": unicode('同盟等级：','utf-8'),
    "cntry_country_amount": unicode('同盟人数：','utf-8'),
    "cntry_country_contribution": unicode('同盟军粮：','utf-8'),
    "cntry_country_declaration": unicode('同盟宣言：','utf-8'),
    "cntry_country_exp": unicode('同盟经验：','utf-8'),
    "cntry_next_exp": unicode('升级所需经验：','utf-8'),
    "cntry_lv_max": unicode('已满级','utf-8'),
    "cntry_country_promotion_effect": unicode('同盟增益效果','utf-8'),
    "cntry_time_0": unicode('体力恢复','utf-8'),
    "cntry_attack_0": unicode('攻击力','utf-8'),
    "cntry_recover_0": unicode('回复力','utf-8'),
    "cntry_hp_0": unicode('血量','utf-8'),
    "cntry_promotion_0": unicode('增益提升','utf-8'),
    "cntry_applied_alone": unicode('已申请','utf-8'),
    "cntry_apply_alone": unicode('申请','utf-8'),
    "cntry_donate_ok": unicode('捐献元宝成功！个人军粮、个人贡献、同盟军粮增加。','utf-8'),

    "cntry_deliver_equ": unicode('平均分配战利品','utf-8'),
    "cntry_assign_contribution": unicode('按贡献分配战利品','utf-8'),
    "cntry_prev_page": unicode('上一页','utf-8'),
    "cntry_next_page": unicode('下一页','utf-8'),
###################################Ver 3.5更新########################################################
    "cntry_putongfenpei": unicode('普通战利品分配','utf-8'),
    "cntry_jifengfenpei": unicode('疾风战利品分配','utf-8'),

    "cntry_info_accept": unicode('接受成员','utf-8'),
    "cntry_info_accept0": unicode('是否接受他成为同盟中的一员？','utf-8'),
    "cntry_info_deny": unicode('拒绝成员','utf-8'),
    "cntry_info_deny0": unicode('是否拒绝他成为同盟成员？','utf-8'),
    "cntry_info_delete": unicode('删除成员','utf-8'),
    "cntry_info_delete0": unicode('是否删除该成员？','utf-8'),
    "cntry_info_vice": unicode('任命副盟主','utf-8'),
    "cntry_info_vice0": unicode('是否任命该成员为副盟主？','utf-8'),
    "cntry_info_fire_pre": unicode('解职副盟主','utf-8'),
    "cntry_info_fire_pre0": unicode('是否解职该副盟主？','utf-8'),
    "cntry_info_giveup": unicode('盟主让贤','utf-8'),
    "cntry_info_giveup0": unicode('是否把盟主职位让贤给该成员？','utf-8'),
    "cntry_info_apply": unicode('加入同盟','utf-8'),
    "cntry_info_apply0": unicode('是否申请加入该同盟？','utf-8'),

    "cntry_input_num_of_gold": unicode('请输入要捐献的元宝数:','utf-8'),
    "cntry_donate_alone": unicode('捐献','utf-8'),
    "cntry_input_declaration": unicode('请输入新的同盟宣言','utf-8'),
    "cntry_input_ID": unicode('请输入要搜索同盟的名字或ID','utf-8'),
    "cntry_search_alone": unicode('搜索','utf-8'),
    "cntry_country_up_exp": unicode('同盟升级所需经验值','utf-8'),
    "cntry_country_current_exp": unicode('同盟当前经验值','utf-8'),
    "cntry_content0": unicode('同盟由一位用户发起，发起时需支付300元宝。发起成功后，需在72小时候内，成功邀请10个等级大于等于30级的用户方可创建成功。如超过时限未发起成功，则创建失败，自动退还支付元宝。','utf-8'),
    "cntry_levelup_gold": unicode('升级所需同盟元宝','utf-8'),
    "cntry_levelup_alone": unicode('升级','utf-8'),
    "cntry_next_time_decrease": unicode('下一级缩短','utf-8'),
    "cntry_recover_time": unicode('体力值回复时间','utf-8'),
    "cntry_attack_alone": unicode('攻击','utf-8'),
    "cntry_next_level_promote": unicode('下一级提升','utf-8'),
    "cntry_recover_alone": unicode('回复','utf-8'),
    "cntry_hp_alone": unicode('血量','utf-8'),
    "cntry_JI_alone": unicode('级','utf-8'),
    "cntry_open_money": unicode('开启所需同盟军粮','utf-8'),
    "cntry_time_left": unicode('剩余时间','utf-8'),
    "cntry_hour_alone": unicode('小时','utf-8'),

    "cntry_general_alone": unicode('盟主','utf-8'),
    "cntry_vice_alone": unicode('副盟主','utf-8'),
    "cntry_member_alone": unicode('成员','utf-8'),
    "cntry_stamina_promotion": unicode('体力值增益','utf-8'),
    "cntry_attack_promotion": unicode('攻击增益','utf-8'),
    "cntry_recover_promotion": unicode('回复增益','utf-8'),
    "cntry_hp_promotion": unicode('血量增益','utf-8'),
    "cntry_buffLv_max": unicode('已满级！','utf-8'),
    "cntry_levelup_need": unicode('升级需','utf-8'),
    "cntry_gold_alone": unicode('同盟元宝','utf-8'),
    "cntry_gold_alone2": unicode('同盟元宝：','utf-8'),
    "cntry_exp_alone": unicode('经验','utf-8'),
    "cntry_need_gold": unicode('所需军粮','utf-8'),
    "cntry_content2": unicode('我跟你说这个地方我会改的你信不信呢信也得信不信也得信呀呀','utf-8'),
    "cntry_fbdwords_content1": unicode('您输入的字符中\n不能包含敏感字符','utf-8'),
    "cntry_fbdwords_content2": unicode('同盟的名字\n不能为纯数字','utf-8'),

    "cntry_mail_all": unicode('发同盟邮件','utf-8'),
    "cntry_mail_all_name": unicode('同盟所有成员','utf-8'),
    "cntry_mail_all_gold": unicode('是否使用%d个铜钱发同盟邮件？','utf-8'),
    "cntry_mail_all_shop": unicode('您现有%d个元宝，发同盟邮件需要%d个元宝，是否要去商店购买？','utf-8'),

    "cntry_por_leaderName": unicode('★盟主：','utf-8'),
    "cntry_por_cntryLv": unicode('★等级：%d','utf-8'),
    "cntry_por_memberNum": unicode('★成员：%d/%d','utf-8'),
    "cntry_por_cntryCoin": unicode('★同盟元宝：%ld','utf-8'),

    "cntry_help_title": unicode('同盟帮助','utf-8'),
    "cntry_help_prompt_1": unicode('同盟帮助','utf-8'),
    "cntry_help_not": unicode('同盟帮助将不在显示，如果需要，请到攻略中去查看','utf-8'),

    "cntry_delete_time": unicode('公会解散倒计时：%02d:%02d:%02d','utf-8'),

    "cntry_usebatchitem": unicode('请输入您要批量使用的个数','utf-8'),
    "cntry_cangbaoku": unicode('藏宝库','utf-8'),
    "cntry_askusemore": unicode('您确定要使用%d张(%s)吗','utf-8'),
    "cntry_querenuse": unicode('确认使用','utf-8'),
    "cntry_itemcardnum": unicode('数量: %d','utf-8'),
    "cntry_noitemcard": unicode('暂无道具卡片','utf-8'),
    "cntry_itemcardlvneed": unicode('等级限制: %d级','utf-8'),
    "cntry_itemcardcbuneed": unicode('个人贡献值: %d','utf-8'),

    # confirmlayer.cpp
    "con_select_": unicode('选 择','utf-8'),
    "con_general_info": unicode('武将详情','utf-8'),
    "con_back_": unicode('返 回','utf-8'),
    "con_lock_": unicode('加 锁','utf-8'),
     "con_unlock_": unicode('解 锁','utf-8'),
    "con_send_mail": unicode('发邮件','utf-8'),
    "con_delete_friend": unicode('删除好友','utf-8'),
    "con_dismis_": unicode('解 职','utf-8'),
    "con_giveup_": unicode('让 贤','utf-8'),
    "con_apply_friend": unicode('申请好友','utf-8'),
    "con_delete_member": unicode('删除成员','utf-8'),
    "con_commit_": unicode('任 命','utf-8'),
    "cntry_mail_all_no_gold": unicode('对不起，您的铜钱不足，无法发送邮件','utf-8'),

    #保卫战结算画面
    "cntrydgend_lastatk": unicode('您的最后一击,成功击杀了boss','utf-8'),
    "cntrydgend_atk": unicode('造成伤害:','utf-8'),
    "cntrydgend_wealth": unicode('获得个人军粮:','utf-8'),
    "cntrydgend_cntrbt": unicode('获得贡献:','utf-8'),
    "cntrydgend_coin": unicode('获得铜钱:','utf-8'),
    "cntrydgend_killedbyother": unicode('保卫战BOSS已被本国其他成员击杀','utf-8'),

    #点击用户信息面板，显示升级所需经验
    "usrinf_curexp": unicode('当前经验值:','utf-8'),
    "usrinf_needexp": unicode('下级还需经验值:','utf-8'),

    #保卫战伤害排行
    "orgftcfm_dsp": unicode('伤害前10名玩家将获得丰厚大奖！ 我的伤害','utf-8'),
    "orgftcfm_rank": unicode('排行','utf-8'),
    "orgftcfm_name": unicode('名字','utf-8'),
    "orgftcfm_dmg": unicode('伤害','utf-8'),
    "orgft_last_kill": unicode('最后一击杀死了BOSS','utf-8'),

    #想玩同盟必须绑定账号
    "cntry_authened": unicode('账号绑定','utf-8'),
    "cntry_authened_info": unicode('加入同盟需绑定账号，请到攻略界面绑定','utf-8'),

    #同盟兑换福利，需要冷却时间
    "cntry_welfare_cd": unicode('冷却中:','utf-8'),
    "cntry_welfare_cd_tips": unicode('此项福利还在冷却中，请稍后再兑换。','utf-8'),


    #编队确认
    "TeamCfm_NeedRent":unicode('本战场还需要%s的加入才可以继续,替换系统提供的武将继续战斗？','utf-8'),
    "TeamCfm_NeedRentGold":unicode('本战场还需要%s的加入才可以继续,消耗%d铜钱替换系统提供的武将继续战斗？','utf-8'),
    "TeamCfm_NeedRentCoin":unicode('本战场还需要%s的加入才可以继续,消耗%d元宝替换系统提供的武将继续战斗？','utf-8'),
    "TeamCfm_RentCardPlace":unicode('请移动租借武将至编队中','utf-8'),


    #武将详情界面
    "laiyuan_alone": unicode('来源','utf-8'),
    "xiangqing_alone": unicode('详情','utf-8'),



    #修改同盟名片
    "cntry_cardName": unicode('修改同盟名片','utf-8'),
    "cntry_cardName_title": unicode('修改同盟名片','utf-8'),
    "cntry_cardName_coin": unicode('是否使用%d铜钱修改您的同盟名片？','utf-8'),
    "cntry_cardName_prompt_1": unicode('修改同盟名片， 修改同盟名片','utf-8'),
    "cntry_cardName_rule": unicode('（仅限1~8个字符）','utf-8'),
    "cntry_cardName_sure": unicode('是否确定修改同盟名片为','utf-8'),
    "cntry_cardName_alert": unicode('铜钱不足','utf-8'),

    #道具卡
    "cntry_item_result": unicode('道具卡使用结果','utf-8'),
    "cntry_item_result_exp": unicode('使用道具卡获得%ld经验','utf-8'),
    "cntry_item_result_gold": unicode('使用道具卡获得%ld铜钱','utf-8'),
    "cntry_item_result_coin": unicode('使用道具卡获得%ld元宝','utf-8'),
    "cntry_item_result_stamina": unicode('使用道具卡获得%ld体力','utf-8'),
    "cntry_item_result_supply": unicode('使用道具卡获得%ld军粮','utf-8'),
    "cntry_item_result_cutcd": unicode('使用道具卡减少兑换福利CD','utf-8'),
    "cntry_item_result_rename": unicode('使用道具卡修改同盟名片','utf-8'),
    "cntry_item_result_gacha": unicode('使用道具卡抽一次神将','utf-8'),
    "cntry_item_result_gacha10": unicode('使用道具卡进行神将10连抽','utf-8'),

    "cntry_item_use_notEnough": unicode('批量使用道具卡数量超过目前拥有的数量','utf-8'),
    "cntry_item_use_moreThan10": unicode('批量使用素材卡或玉玺卡不得超过10个','utf-8'),
    "cntry_item_useall": unicode('批量使用','utf-8'),
    "cntry_item_use": unicode('使 用','utf-8'),
    "cntry_item_leveleneed": unicode('等级限制','utf-8'),
    "cntry_item_contributeneed": unicode('个人贡献值','utf-8'),
    "cntry_item_use_notlvneed": unicode('角色等级不足,无法使用','utf-8'),
    "cntry_item_use_notcbuneed": unicode('角色同盟贡献度不足,无法使用','utf-8'),

    #兑换码
    "title_cdKey": unicode('兑换码','utf-8'),
    "naviText_cdkey_1": unicode('输入正确的兑换码，就能获得惊喜礼包哟~！','utf-8'),
    "cdkey_placeholder": unicode('请输入兑换码','utf-8'),
    "cdkey_success": unicode('兑换成功','utf-8'),
    "cdkey_getGift": unicode('恭喜您领取了','utf-8'),
    "cdkey_result_coin": unicode('元宝 x %ld','utf-8'),
    "cdkey_result_gold": unicode('铜钱 x %ld','utf-8'),
    "cdkey_result_wealth": unicode('军粮 x %ld','utf-8'),
    "cdkey_result_gacha_pt": unicode('援军点数 x %ld','utf-8'),
    "cdkey_result_card": unicode('%d★%s x %d','utf-8'),


    #同盟新UI
    "cntry_new_donate": unicode('捐献','utf-8'),
    "cntry_new_rank": unicode('排名','utf-8'),
    "cntry_new_recent": unicode('近况','utf-8'),
    "cntry_new_member": unicode('成员','utf-8'),
    "cntry_new_manage": unicode('管理','utf-8'),
    "cntry_new_chat": unicode('聊天','utf-8'),
    "cntry_click_input": unicode('点击输入','utf-8'),

    #聊天室文本格式
    "chat_ceo": unicode('<font color=\"#FF0000\">【盟主】%s: %s</font><br/>','utf-8'),
    "chat_vp": unicode('<font color=\"#0000FF\">【副盟主】%s</font>: %s<br />','utf-8'),
    "chat_self": unicode('<font color=\"#FF00FF\">%s</font>: %s <br/>','utf-8'),
    "chat_mem": unicode('<font color=\"#0000FF\">%s</font>: %s<br />','utf-8'),
    "chat_div": unicode('<font color=\"#999999\">--------%s--------</font><br/>','utf-8'),
    "chat_head": unicode('<body style=\"font-size:14px;word-break:break-all\">','utf-8'),
    "chat_head_pad": unicode('<body style=\"font-size:26px;word-break:break-all\">','utf-8'),
    "chat_tail": unicode('</body>','utf-8'),
    "chat_err": unicode('<font color=\"#000000\">%s</font><br />','utf-8'),

    #疾风&乱舞
    "jiFengLuanWu_dsp": unicode('排名前10名的同盟与同盟成员将获得丰厚大奖！','utf-8'),
    "jiFengLuanWu_time": unicode('用时','utf-8'),
    "jiFengLuanWu_begin": unicode('开始','utf-8'),
    "jiFengLuanWu_over": unicode('已结束, 下次还未开启','utf-8'),
    "jiFengLuanWu_end": unicode('结束','utf-8'),
    "jiFengLuanWu_cd": unicode('冷却时间','utf-8'),
    "jiFengLuanWu_sure": unicode('您确定开启同盟保卫战%s吗？','utf-8'),
    "jiFengLuanWu_not": unicode('保卫战不在有效时间内，无法开启','utf-8'),
    "jiFengLuanWu_end_time": unicode('时间','utf-8'),


    #隋唐乱入抽神将
    "suitang_gacha": unicode('隋唐英雄参见','utf-8'),
    "suitang_gacha_title": unicode('隋唐英雄参见','utf-8'),
    "suitang_gacha_1": unicode('必定会抽出4星以上的隋唐武将,一次求将需消耗%d个元宝','utf-8'),
    "suitang_gacha_2": unicode('进行一次隋唐乱入求神将','utf-8'),
    "suitang_gacha_3": unicode('您的元宝不够一次隋唐乱入求神将','utf-8'),
    #称号系统
    "title_title": unicode('称 号','utf-8'),
    "title_titlelst": unicode('称号列表','utf-8'),
    "title_newtitle": unicode('恭喜主公获得称号','utf-8'),

    #涅槃
    "con_powup": unicode('强 化','utf-8'),
    "con_niepan": unicode('涅 槃','utf-8'),
    "niepan_dsp": unicode('请选择以上武将作为素材，结果为下列随机一种','utf-8'),
    "naviText_niepan_base_1": unicode('涅槃，涅槃','utf-8'),
    "nipan_nofood": unicode('大兄弟，没素材吃啊！','utf-8'),
    "naviText_niepan_food_1": unicode('涅槃，涅槃','utf-8'),

     #疾风战利品分配
     "jifeng_recentscore": unicode('近5次伤害','utf-8'),
     "jifeng_lastscore": unicode('上次伤害','utf-8'),
     "ttl_suishenjundai": unicode('随身军袋','utf-8'),

     #战场限制(统御力、武将属性)
     "dgrestrict_cost": unicode('战场限定统御力不得高于%d','utf-8'),
     "dgrestrict_singlecost": unicode('战场限定单个武将统御力不得高于%d','utf-8'),
     "dgrestrict_elem": unicode('本战场还需要%s属性的武将才可以继续，请重新编队','utf-8'),
     "dgrestrict_onlyelem": unicode('本战场只能携带%s属性的武将，请重新编队','utf-8'),

     #满体力推送
     "pushinf_stamina": unicode('亲，您的体力已经满了!快来玩逆转三国吧!','utf-8'),

     # 录像
     "arena_record_mem_warning": unicode('为了保证视频顺利录制，您需要保证您的设备剩余容量大于10MB，否则视频可能无法正常录制。','utf-8'),
     "arena_record_bind_content": unicode('本次活动只有绑定新浪或者腾讯微博的玩家才能参加，现在就绑定帐号参与活动来赢取奖励吧！','utf-8'),
     "record_upload_title": unicode('恭喜','utf-8'),
     "record_upload_content": unicode('您成功录制了一段今天离泣鬼神的视频，马上上传到视频网站和你的好友一起分享吧！','utf-8'),
     "record_upload_btn1": unicode('上传并分享视频','utf-8'),
     "record_upload_btn2": unicode('保存到本地相册','utf-8'),
     "record_upload_btn3": unicode('暂不上传','utf-8'),
     "record_other_main_title": unicode('我的视频','utf-8'),
     "arena_fightcfm_record": unicode('录制并挑战','utf-8'),
     "record_time": unicode('录制于','utf-8'),
     "record_upload_progress": unicode('上传进度','utf-8'),
     "record_upload_done": unicode('已上传','utf-8'),
     "record_upload_no": unicode('未上传','utf-8'),
     "record_upload_failed": unicode('上传失败','utf-8'),
     "record_get_award": unicode('领取奖励','utf-8'),
     "record_get_award_done": unicode('已领奖励','utf-8'),
     "record_upload_now": unicode('马上上传','utf-8'),
     "record_upload_ing": unicode('取消上传','utf-8'),
     "record_local_none": unicode('本地没有录制视频','utf-8'),
     "record_local_not_upload_content": unicode('本地未上传视频已到上限，继续录制将覆盖原有视频，是否继续？','utf-8'),
     "record_share_content": unicode('我上传的视频 地址:','utf-8'),
     "record_upload_reviewing": unicode('审核中…','utf-8'),
     "record_reupload": unicode('重新上传','utf-8'),
     "record_view_other_record": unicode('观看录像','utf-8'),
     "record_no_other_record": unicode('没有他人通关视频','utf-8'),
     "record_error": unicode('通讯错误请重试','utf-8'),
     "record_previous_view_record": unicode('查看视频','utf-8'),
     "record_text_uploading_failed": unicode('您有视频正在上传，请等候…','utf-8'),

     # 师徒系统
     "teastu_getTeacher": unicode('拜  师','utf-8'),
     "teastu_manager": unicode('师徒管理','utf-8'),
     "teastu_request": unicode('师徒请求','utf-8'),
     "teastu_remove": unicode('解除关系','utf-8'),
     "teastu_inspire": unicode('鼓舞','utf-8'),
     "teastu_growup": unicode('成长之路','utf-8'),

     # 三国演义本
     "title_sango": unicode('经典战场','utf-8'),
     "naviText_sangoArena": unicode('经典战场，经典战场，经典战场，经典战场','utf-8'),

     # 悬赏系统
     "reward_contribution_done": unicode('贡献度达成:','utf-8'),
     "cntry_post_reward_list": unicode('悬赏列表','utf-8'),
    "cntry_post_reward_canjia": unicode('参加','utf-8'),
    "cntry_baoku_list": unicode('宝库列表','utf-8'),
    "cntry_baoku_kucun": unicode('库存:','utf-8'),
    "cntry_baoku_levelxianzhi": unicode('%ld级以上同盟可以购买','utf-8'),
    "cntry_baoku_jiageyuanbao": unicode('价格: %ld元宝','utf-8'),
    "cntry_baoku_jiagebt": unicode('价格: %ld军粮','utf-8'),
    "cntry_baoku_zongjia": unicode('总价:','utf-8'),
    "cntry_baoku_goumaishuliang": unicode('购买数量:','utf-8'),
    "cntry_baoku_yuanbaobuzu": unicode('同盟元宝不足,无法购买','utf-8'),
    "cntry_baoku_junliangbuzu": unicode('同盟军粮不足,无法购买','utf-8'),
    "cntry_baoku_baokubuysuccess": unicode('恭喜你成功购买了此道具','utf-8'),
    "cntry_baoku_xuanshangnum": unicode('宝物悬赏数量:','utf-8'),

    "cntry_xuanshangfabu": unicode('悬赏发布','utf-8'),
    "cntry_xs_mubiaosheding": unicode('设定目标贡献值:','utf-8'),
    "cntry_xs_wanchengqixian": unicode('设定完成期限:','utf-8'),
    "cntry_xs_canyurenshu": unicode('设定参与人数:','utf-8'),
    "cntry_xs_baozhengjin": unicode('设定保证金:','utf-8'),
    "cntry_xs_shedingjiangli": unicode('设定奖励:','utf-8'),
    "cntry_xs_xuanshangbtn": unicode('悬赏','utf-8'),
    "cntry_fabu_kucunbuzu": unicode('同盟库存不足,无法选择','utf-8'),
    "cntry_xs_querenfabu": unicode('确认发布','utf-8'),
    "cntry_xs_querenzhifu": unicode('确认要支付%d元宝参加此悬赏任务?','utf-8'),

    "cntry_xs_xuanshangname": unicode('悬赏任务：为同盟增加贡献%ld点','utf-8'),
    "cntry_xs_baomingqixian": unicode('报名期限：','utf-8'),
    "cntry_xuyaobaozhengjin": unicode('需要保证金: %d元宝','utf-8'),
    "cntry_canyurenshu": unicode('参与人数: %d/%d','utf-8'),
    "cntry_wanchengqixian": unicode('完成期限:','utf-8'),
    "cntry_xs_havenotask": unicode('暂无悬赏任务!','utf-8'),
    "cntry_xs_havenobaoku": unicode('宝物不足,请购买!','utf-8'),

     "reward_btn_baoku": unicode('悬赏宝库','utf-8'),
     "reward_btn_fabu": unicode('发布悬赏','utf-8'),
     "reward_btn_xiangqing": unicode('查看详情','utf-8'),
     "reward_btn_lingqu": unicode('领取奖励','utf-8'),
     "reward_info_title": unicode('悬赏详情','utf-8'),
     "reward_info_naviText_1": unicode('悬赏详情、悬赏详情','utf-8'),
     "reward_info_no": unicode('没有成员参加此项悬赏！','utf-8'),
     "reward_title_naviText_1": unicode('悬赏、悬赏、悬赏','utf-8'),
     "reward_top_member": unicode('悬赏\n排行榜','utf-8'),
     "reward_top_gonghui": unicode('所属公会:','utf-8'),
     "reward_top_gongxian": unicode('获得贡献值: %ld','utf-8'),
     "reward_top_paihangbang": unicode('悬赏排行榜','utf-8'),

     "reward_alert_item_count": unicode('悬赏有%d个人参加，共需要%d个\"%s\"道具卡，库存不足，无法发布','utf-8'),

 #first layer
     "first_naviText_1": unicode('我是首页、我是首页、我是首页','utf-8'),


   #领奖系统   v4.1
    "rwd_main_qiandao": unicode('签到','utf-8'),
    "rwd_main_shengji": unicode('升级','utf-8'),
    "rwd_main_yuefen": unicode('月份','utf-8'),
    "rwd_main_leiji": unicode('累积','utf-8'),
    "rwd_main_huodong": unicode('活动','utf-8'),
    "rwd_main_buchang": unicode('补偿','utf-8'),
    "rwd_sign_lingqu": unicode('领取','utf-8'),
    "rwd_leiji_tianshu": unicode('%d/%d天','utf-8'),
    "rwd_qiandao_tianshu": unicode('第%d天','utf-8'),
    "rwd_first_canot_lingj": unicode('领奖功能即将开放','utf-8'),
    "rwd_getbonussuccess": unicode('成功领取奖励','utf-8'),

 #新增语言   v4.1
   "text_tujian_png": unicode('武将图鉴','utf-8'),
   "text_guide_png": unicode('游戏攻略','utf-8'),
   "title_basecard2": unicode('基础武将选择','utf-8'),
   "settingTip4": unicode('技能特效','utf-8'),

#新增语言   v4.2
   "title_video_strategy": unicode('视频攻略','utf-8'),
   "ont_video_strategy": unicode('本地暂无视频攻略','utf-8'),
   "cntry_fabu_maxnum": unicode('最大数量:','utf-8'),
   "team_cost_upper_limit": unicode('队伍统御力超过自身上限，请重新编队','utf-8'),

   "enemyskill_kengdiezhuanshui": unicode('坑爹转-水','utf-8'),
   "enemyskill_kengdiezhuanhuo": unicode('坑爹转-火','utf-8'),
   "enemyskill_kengdiezhuanmu": unicode('坑爹转-木','utf-8'),
   "enemyskill_kengdiezhuanguang": unicode('坑爹转-光','utf-8'),
   "enemyskill_kengdiezhuanan": unicode('坑爹转-暗','utf-8'),
   "enmeybuff_1beilianfan": unicode('1连倍返','utf-8'),
   "enmeybuff_2beilianfan": unicode('2连倍返','utf-8'),
   "enmeybuff_3beilianfan": unicode('3连倍返','utf-8'),
   "enmeybuff_4beilianfan": unicode('4连倍返','utf-8'),
   "enmeybuff_5beilianfan": unicode('5连倍返','utf-8'),
   "enmeybuff_6beilianfan": unicode('6连倍返','utf-8'),
   "enmeybuff_7beilianfan": unicode('7连倍返','utf-8'),
   "enmeybuff_8beilianfan": unicode('8连倍返','utf-8'),
   "enmeybuff_9beilianfan": unicode('9连倍返','utf-8'),
   "enmeybuff_10beilianfan": unicode('10连倍返','utf-8'),
   "enmeybuff_1combodun": unicode('1Combo盾','utf-8'),
   "enmeybuff_2combodun": unicode('2Combo盾','utf-8'),
   "enmeybuff_3combodun": unicode('3Combo盾','utf-8'),
   "enmeybuff_4combodun": unicode('4Combo盾','utf-8'),
   "enmeybuff_5combodun": unicode('5Combo盾','utf-8'),
   "enmeybuff_6combodun": unicode('6Combo盾','utf-8'),
   "enmeybuff_combodun2": unicode('Combo盾2','utf-8'),
   "enmeybuff_combodun3": unicode('Combo盾3','utf-8'),

   "enemyskill_zhuqueqi3": unicode('缝影之术','utf-8'),
   "enemyskill_jinu3":unicode('刚力药丸','utf-8'),
   "enemyskill_suigu2": unicode('必杀重击','utf-8'),
   "enemyskill_suigu3": unicode('必杀强击','utf-8'),
   "enEnemySkillShuiXiJin1_3": unicode('水系·封印','utf-8'),
   "enemyskill_huoxijin1_3":unicode('火系·封印','utf-8'),
   "enemyskill_muxijin1_3":unicode('木系·封印','utf-8'),
   "enemyskill_guangxijin1_3":unicode('光系·封印','utf-8'),
   "enemyskill_anxijin1_3":unicode('暗系·封印','utf-8'),
   "enemyskill_shenxijin1_3":unicode('神系·封印','utf-8'),
   "enemyskill_lianji7_3": unicode('3连击','utf-8'),
   "enemyskill_lianji45_4": unicode('4连击','utf-8'),
   "enemyskill_lianji75_3": unicode('强力3连击','utf-8'),
   "enemyskill_luanshijin3_23": unicode('水晶棺材','utf-8'),
   "enemyskill_nizhuantianxia2":unicode('逆转·天下2','utf-8'),
   "enemyskill_luanshijin_run2_3_23":unicode('绝景哉','utf-8'),

   #外挂提示
   "OutsideZhuiAlarm_title": unicode('警告','utf-8'),
   "OutsideZhuiAlarm_message":unicode('检测到该设备安装了作弊软件 \n请删除该应用重新登录。','utf-8'),
   "OutsideZhuiAlarm_oktext":unicode('退出程序','utf-8'),

   # 师徒系统
   "maa_request_master": unicode('拜 师','utf-8'),
   "maa_receive_apprentice_request": unicode('收徒请求','utf-8'),
   "maa_master_manage": unicode('师傅管理','utf-8'),
   "maa_receive_apprentice": unicode('收 徒','utf-8'),
   "maa_request_master_request": unicode('拜师请求','utf-8'),
   "maa_apprentice_manage": unicode('徒弟管理','utf-8'),

   "maa_seek_id": unicode('搜索ID','utf-8'),
   "maa_refresh": unicode('刷 新','utf-8'),
   "maa_seek_master_title": unicode('搜索师傅','utf-8'),
   "maa_seek_apprentice_title": unicode('搜索徒弟','utf-8'),
   "maa_seek_master_hint": unicode('请输入要搜索的师傅ID','utf-8'),
   "maa_seekapprentice_hint": unicode('请输入要搜索的徒弟ID','utf-8'),
}


class MongoTestCase(unittest.TestCase):

    def setUp(self):
        self.mongo = Mongo(DBNAME)
        self.mongo.config.drop_indexes()
        self._setup_config()
        self.log = logging.getLogger('OCMONGO.TEST')

    def tearDown(self):
        self.mongo.conn.drop_database(DBNAME)

    def _setup_config(self):
        self.CONFIG_ID = self.mongo.config.insert(CONFIG_FILE)

    def test_dbname(self):
        db_list = self.mongo.conn.database_names()
        assert_in(DBNAME, db_list)

        self.mongo.conn.drop_database(DBNAME)
        dropped_list = self.mongo.conn.database_names()
        assert_not_in(DBNAME, dropped_list)

    def test_hostname(self):
        host = self.mongo.conn.host
        expected = 'localhost'
        eq_(host, expected)

    def test_getattr(self):
        col = 'config'

        getattr(self.mongo, col)
        collection_list = self.mongo.db.collection_names()
        assert_in(col, collection_list)

        collection_name = self.mongo.collection.name
        eq_(collection_name, col)

    def test_getitem(self):
        col = 'config'

        # __getitem__ is only called when a dict is accessed via []
        # it is not called if it is accessed via get()
        self.mongo[col]

        collection_list = self.mongo.db.collection_names()
        assert_in(col, collection_list)

        collection_name = self.mongo.collection.name
        eq_(collection_name, col)

    def test_get(self):
        doc = self.mongo.config.get('_id', self.CONFIG_ID)
        expected = self.CONFIG_ID
        eq_(doc['_id'], expected)

    def test_find(self):
        query = {'config_id': 123456}
        resultset = self.mongo.find(query)

        # Test output type of find()
        assert_is_instance(resultset, pymongo.cursor.Cursor)
        eq_(resultset.count(), 1)

        # Test the collection that the find output
        eq_(resultset.collection.name, 'config')

        # Validate output doc with actual doc
        doc = resultset[0]
        expected_id = self.CONFIG_ID

        eq_(doc['_id'], expected_id)
        eq_(doc['config_id'], 123456)

        expected_attribute = unicode('请输入要搜索的徒弟ID','utf-8')
        eq_(doc['maa_seekapprentice_hint'], expected_attribute)

    def test_remove(self):
        pk = '_id'
        pk_value = self.CONFIG_ID
        doc = self.mongo.delete(pk, pk_value)

        assert_is_instance(doc, dict)
        eq_(doc['ok'], 1.0)
        assert_is_none(doc['err'])
        eq_(doc['n'], 1)

    def test_fail_remove(self):
        pk = 'id'
        pk_value = self.CONFIG_ID
        doc = self.mongo.delete(pk, pk_value)

        assert_is_instance(doc, dict)
        eq_(doc['ok'], 1.0)
        assert_is_none(doc['err'])
        eq_(doc['n'], 0)

    def test_update(self):
        pk = 'config_id'
        data = {
            '_id': self.CONFIG_ID,
            'config_id': 123456,
            'name': 'Mark Huang',
            'age': 23,
            'tags': ['java', 'javascript', 'html', 'python']
        }
        self.mongo.update(pk, data)

        doc = self.mongo.get(pk, 123456)
        eq_(doc['config_id'], 123456)
        assert_in('age', doc)
        assert_in('tags', doc)
        assert_not_in('maa_request_master', doc)

    def test_ensureIndex(self):
        assert_raises(TypeError, self.mongo.config.ensure_index, {'hello': 1})

        eq_("hello_1", self.mongo.config.create_index("hello"))
        # Using create_index again will only return the name of the index
        eq_("hello_1", self.mongo.config.create_index("hello"))
        eq_("goodbye_1", self.mongo.config.ensure_index("goodbye"))
        eq_(None, self.mongo.config.ensure_index("goodbye"))

        self.mongo.config.drop_indexes()
        name = self.mongo.config.ensure_index('config_id', name='config_index', unique=True)
        eq_(name, 'config_index')
        # Using ensure_index again will return None
        eq_(None, self.mongo.config.ensure_index('config_id', name='config_index', unique=True))

        self.mongo.config.drop_index('config_index')
        eq_("config_index",
            self.mongo.config.ensure_index('config_id', name='config_index', unique=True))
        eq_(None,
            self.mongo.config.ensure_index('config_id', name='config_index', unique=True))

        import time
        self.mongo.config.drop_index('config_index')
        eq_("config_index",
            self.mongo.config.create_index('config_id', name='config_index',
                                           unique=True, cache_for=1.2))
        time.sleep(2)
        eq_("config_index",
            self.mongo.config.ensure_index('config_id', name='config_index',
                                           unique=True))
        eq_(None,
            self.mongo.config.ensure_index('config_id', name='config_index',
                                           unique=True))

    def test_index_cachefor(self):

        import time
        self.mongo.config.create_index('config_id', unique=True)
        time.sleep(2)
        eq_(None, self.mongo.config.ensure_index('config_id', unique=True))

    def test_drop_index(self):

        self.mongo.config.ensure_index("config_id")
        self.mongo.config.ensure_index("maa_request_master")
        eq_(self.mongo.db.system.indexes.find({"ns": u"test_maxstrike.config"}).count(), 3)

        self.mongo.config.drop_indexes()
        eq_(self.mongo.db.system.indexes.find({"ns": u"test_maxstrike.config"}).count(), 1)

        self.mongo.config.ensure_index([("config_id", pymongo.ASCENDING)])
        name = self.mongo.config.ensure_index("maa_request_master")
        eq_(self.mongo.db.system.indexes.find({"ns": u"test_maxstrike.config"}).count(), 3)
        eq_(name, "maa_request_master_1")

    def test_map_reduce(self):
        self.mongo.config.insert({"uid": 1, "tags": ["java", "python", "javascript"]})
        self.mongo.config.insert({"uid": 2, "tags": ["html", "css", "javascript", "django"]})
        self.mongo.config.insert({"uid": 3, "tags": ["django", "python", "numpy"]})
        self.mongo.config.insert({"uid": 4, "tags": ["javascript", "ror", "java"]})
        self.mongo.config.ensure_index("uid")
        doc = self.mongo.config.get("uid", 4)
        assert_in('ror', doc['tags'])

        mapper = """
        function() {
            for(var i in this.tags) {
                emit(this.tags[i], 1);
            }
        }
        """

        reducer = """
        function(keys, values) {
            var total = 0;
            for(var i=0; i<values.length; i++) {
                total += values[i];
            }
            return total;
        }
        """

        result = self.mongo.config.map_reduce(mapper, reducer, out='mrunittests')
        expected_javascript = 3
        expected_python = 2
        assert_is_instance(result, pymongo.collection.Collection)
        eq_(result.find_one({"_id": "javascript"})["value"], expected_javascript)
        eq_(result.find_one({"_id": "python"})["value"], expected_python)




def suite():
    suite = unittest.TestSuite()
    suite.addTest(MongoTestCase())
    return suite

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stderr)
    logging.getLogger("OCMONGO.TEST").setLevel(logging.DEBUG)
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run(test_suite)
