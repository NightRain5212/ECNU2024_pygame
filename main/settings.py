'''
这里是设置游戏常数的地方，修改常数请在这里修改，使用时在其他文件import即可
'''
import pygame as pg
import sys
# 游戏全局设置

##################################
#         GENERAL SETTING        #
##################################

#窗口大小
WIDTH = 1600
HEIGTH = 900
#游戏格子参数
ROW=30
COL=360
#每个格子的大小
TILE_SIZE=HEIGTH//ROW
#地图编辑器相关参数
TILE_TYPES=65
SIDESIZE=300
GAP=30
#标题
TITLE = "失落的星辉v1.0"

# 帧率
FPS = 60
CLOCK=pg.time.Clock()

##################################
#         COLOR SETTING          #
##################################
# 颜色
WHITE = (255,255,255)
GRAY = (192,192,192)
LIGHT_BLUE = (173, 216, 230)
BLUE = (0, 0, 255)
GREEN = (0,255,0)
RED = (200, 25, 25)
BLACK = 'black'
YELLOW=(255,255,0)



####################################
#         FILE PATH SETTING        #
####################################

# 文件路径(相对路径)
STARTMENU_BACKGROUND = "src/img/StartMenu/background.png"
LEVEL1_BACKGROUND1="src/img/Map/background/level1background.png"
LEVEL1_BACKGROUND2="src/img/Map/background/1-house.png"
LEVEL2_BACKGROUND1="src/img/Map/background/level2background1.png"
LEVEL2_BACKGROUND2="src/img/Map/background/level2background2.png"
LEVEL3_BACKGROUND1="src/img/Map/background/level3background1.png"
LEVEL3_BACKGROUND2="src/img/Map/background/level3background2.png"
LEVEL3_BACKGROUND3="src/img/Map/background/level3background3.png"
LEVEL4_BACKGROUND1="src/img/Map/background/level4background1.png"
LEVEL4_BACKGROUND2="src/img/Map/background/level4background2.png"
LEVEL4_BACKGROUND3="src/img/Map/background/level4background3.png"
LEVEL5_BACKGROUND="src/img/Map/background/level5background.png"

#这里是后期已经编辑好的关卡地图种子
WORLD_1_SEED=[]
WORLD_2_SEED=[]
WORLD_3_SEED=[]
WORLD_4_SEED=[]
WORLD_5_SEED=[]

# 开始菜单音乐
START_BGM = "src/music/startBGM.mp3"
# 全局字体
FONT = "src/fonts/Silver.ttf"
FONT1="src/fonts/DeathMachine.ttf"
FONT2="src/fonts/DungeonFont.ttf"
FONT3="src/fonts/GlitchGoblin.ttf"
FONT4="src/fonts/Halloweenpixels.ttf"
#音乐
startmusic="src/music/back/Piano Instrumental 3.mp3"
level1music="src/music/back/startBGM.mp3"
level2music="src/music/back/3. Darkwood Path.mp3"
level3music="src/music/back/Piano Instrumental 8.mp3"
level4music="src/music/back/Pawel Blaszczak.mp3"
level5music="src/music/back/Piano Instrumental 3.mp3"
backmusics=[startmusic,level1music,level2music,level3music,level4music,level5music]

#音效
PLAYER_HURT_SOUND="src/sound/player_hurt.ogg"
PLAYER_CURE_SOUND="src/sound/player_health.wav"
PLAYER_ATTACK_SOUND="src/sound/player_attack.wav"
ERROR_SOUND="src/sound/error.wav"
LEVELUP_SOUND="src/sound/levelup.wav"
CLICK_SOUND="src/sound/click.wav"

#PLAYER
PLAYER_JUMP_SHEET_PATH="src/img/Character/JumpSheet.png"
PLAYER_IDLE_SHEET_PATH="src/img/Character/IdleSheet.png"
PLAYER_WALK_SHEET_PATH="src/img/Character/RunRightSheet.png"
PLAYER_ATTACK_SHEET_PATH="src/img/Character/AttackSheet.png"
PLAYER_MAGIC_ARROW_SHEET_PATH="src/img/magic/magic_arrow.png"

#ICON
MENU_ICON_PATH="src/img/Map/buttons/menu1.png"
MENU_ICON_SCALE=(80,80) #菜单按钮大小
CURE_READY_ICON_PATH="src/img/Character/heal_ready.png"
CURE_READY_ICON_SCALE=(32,32) #回血术准备状态图标大小
CURE_CD_ICON_PATH="src/img/Character/heal_cd.png"
CURE_CD_ICON_SCALE=(32,32) #回血术cd状态图标大小
MAGIC_ARROW_READY_ICON_PATH="src/img/Character/magic_ready.png"
MAGIC_ARROW_READY_ICON_SCALE=(32,32) #魔法箭准备状态图标大小
MAGIC_ARROW_CD_ICON_PATH="src/img/Character/magic_cd.png"
MAGIC_ARROW_CD_ICON_SCALE=(32,32) #魔法箭cd状态图标大小
LV_ICON_PATH="src/img/lv_icons/star.png"
LV_ICON_SCALE=(32,32) #等级图标大小

#NPC
EILIN_PATH="src/img/npc/Eilin"
RENAULT_PATH="src/img/npc/Renault"
#对话框
GALLERY_PATH="src/img/npc/gallery.png"
GALLERY_SCALE=(600,400)
GALLERY_TEXT_SIZE=30
GALLERY_TEXT_DURATION=2000
#LOCK
LOCK_PATH="src/img/Lock/locked.png"
LOCK_SCALE=(50,50)
UNLOCK_PATH="src/img/Lock/unlocked.png"
UNLOCK_SCALE=(50,50)
#BUTTON
BACK_BUTTON_PATH="src/img/Map/buttons/pic_goback.png"

#FILE_SYSTEM
FILE_BACKGROUND_PATH="src/img/Map/buttons/savefile.png"
FILE_PIC_PATH="src/img/Map/buttons/gear.png"
FILE_GO_BACK_BUTTON_PATH="src/img/Map/buttons/pic_goback.png"
FILE_MENU_PIC_PATH="src/img/Map/buttons/menu.png"
FILE_SAVE_PIC_PATH="src/img/Map/buttons/pic-save.png"
FILE_LOAD_PIC_PATH="src/img/Map/buttons/pic-load.png"
FILE_CLEAR_PIC_PATH="src/img/Map/buttons/pic-clear.png"
FILE_BACK_BUTTON_PATH="src/img/Map/buttons/back.png"

#HELP_SYSTEM
HELP_BACKGROUND_PATH="src/img/Map/buttons/savefile.png"
HELP_BACK_BUTTON_PATH="src/img/Map/buttons/back.png"

#MAP_EDITOR
MAP_EDITOR_SAVE_BUTTON_PATH="src/img/Map/buttons/pic-save.png"
MAP_EDITOR_LOAD_BUTTON_PATH="src/img/Map/buttons/pic-load.png"
MAP_EDITOR_QUIT_BUTTON_PATH="src/img/Map/buttons/pic-quit.png"
MAP_EDITOR_CLEAR_BUTTON_PATH="src/img/Map/buttons/pic-clear.png"
MAP_EDITOR_UP_BUTTON_PATH="src/img/Map/buttons/button_up.png"
MAP_EDITOR_DOWN_BUTTON_PATH="src/img/Map/buttons/button_down.png"
MAP_EDITOR_LEFT_BUTTON_PATH="src/img/Map/buttons/left.png"
MAP_EDITOR_RIGHT_BUTTON_PATH="src/img/Map/buttons/left.png"

#PLOTSYSTEM
PLOT_BACKBUTTON_PATH="src/img/Map/buttons/back.png"
PLOT_LEFTBUTTON_PATH="src/img/Map/buttons/left.png"
PLOT_RIGHTBUTTON_PATH="src/img/Map/buttons/right.png"

#MONSTER
########################

#DRAGON
DRAGON_IDLE_PATH="src/monsters/dragon/idle.png"
DRAGON_WALK_PATH="src/monsters/dragon/walk.png"
DRAGON_ATK1_PATH="src/monsters/dragon/atk_1.png"
DRAGON_ATK2_PATH="src/monsters/dragon/atk_2.png"
DRAGON_ATK3_PATH="src/monsters/dragon/atk_3.png"
DRAGON_FIREBALL_PATH="src/monsters/dragon/fireball.png"
DRAGON_FIREBALL_HORIZON_PATH="src/monsters/dragon/fireball_horizon.png"

#SNAKE
SNAKE_WALK_PATH="src/monsters/snake/LSnake.png"
SNAKE_ATTACK_PATH="src/monsters/snake/Rsnakeangry.png"

# WARRANT
WARRANT_WALK_PATH="src/monsters/warrent/Rwarrant.png"
WARRANT_SYM_PATH="src/monsters/warrent/symmetry_warrant.png"
PUPPET_1_PATH="src/monsters/warrent/Lchild1.png"
PUPPET_2_PATH="src/monsters/warrent/Lchild2.png"

#WOLF
WOLF_WALK_PATH="src/monsters/wolf/Lwolfsign.png"
WOLF_ATK_PATH="src/monsters/wolf/Lwolfsign.png"
WOLF_FIRE_PATH="src/monsters/wolf/Lgreenfire.png"

#TILES
TILES_PATH="src/img/Map/level"

#ZHIYINBOX
ZHIYINBOX_WALK_PATH="src/monsters/box_hen/Lhenwalk.png"
ZHIYINBOX_ATTACK1_PATH="src/monsters/box_hen/Lcall1.png"
ZHIYINBOX_ATTACK2_PATH="src/monsters/box_hen/Lcall2.png"

#BOX
BOX_CLOSE_PATH="src/monsters/box_hen/box1.png"
BOX_OPEN_PATH="src/monsters/box_hen/box2.png"

#Flower
FLOWER_PATH="src/monsters/flower/eyeflower4.png"
FLOWER_ATTACK1_PATH="src/monsters/flower/purple1.png"
FLOWER_ATTACK2_PATH="src/monsters/flower/purple2.png"
FLOWER_ATTACK3_PATH="src/monsters/flower/purple3.png"

#Luckyrain
LUCKY_RAIN_PATH="src/monsters/prop/lucky_money.png"
#################################
#         PLAYER SETTING        #
#################################
# 引力因子
GRAVITY = 0.7
WATER_GRAVITY=0.3#水区重力因子
# 加速度因子
ACC = 0.40
# 摩擦因子
FRICTION = 0.2
# 玩家参数
MAXHP = 100
ATK_PER_FAMRE = 20
MAXMP = 100
MAXVX= 6
MAXAX = 0.8
SPEED = 5
# 玩家图片大小
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 90
#血条参数
HP_BAR_WIDTH = 200
HP_BAR_HEIGHT = 20
HP_RECT_X = 50
HP_RECT_Y = 10
#mp参数
MP_BAR_WIDTH = 200
MP_BAR_HEIGHT = 20
MP_RECT_X = 50
MP_RECT_Y = 50
# 回血术cd
CURE_CD = 30000 #单位：ms
# 回血术COST
CURE_COST_MP = 30
# 魔法箭cd
MAGIC_ARROW_CD = 3000 #单位：ms
# 魔法箭COST
MAGIC_ARROW_COST_MP = 10
# 魔法箭攻击力(倍率)
MAGIC_ARROW_ATK_RATE = 0.75
# 魔法箭攻击范围
MAGIC_ARROW_ATK_RANGE = 500
# 魔法箭速度
MAGIC_ARROW_SPEED = 10

# 跳跃力量
JUMP_POWER = 18
# 攻击cd
ATK_CD = 500 #单位：ms
# 攻击范围
ATK_RANGE = 2*PLAYER_WIDTH
# 自然魔力恢复速度
MP_RECOVER_SPEED = 0.01
# 数值随等级增长率
HPRATE_PER_LV = 0.25
MPRATE_PER_LV = 0.25
ATKRATE_PER_LV = 0.2

#################################
#        MONSTER SETTING        #
#################################

#DRAGON
DRAGON_SCALE = (256,256)
DRAGON_MAXHP = 800
DRAGON_ATK = 40
DRAGON_SPEEDX = 2
DRAGON_ATTACK_RADIUS = 200
DRAGON_NOTICE_RADIUS = 600
DRAGON_MIN_DISTANCE = 300
DRAGON_ATTACK_COOLDOWN = 1000
DRAGON_ATK1_RANGE = 200
#atk1--近身攻击
DRAGON_ATK1_CD = 500  #单位：ms
#atk2--全屏火球攻击
DRAGON_ATK2_CD = 10000  #单位：ms
DRAGON_ATK2_FIREBALL_NUM = 10
#atk3--直线火球攻击
DRAGON_ATK3_CD = 1000  #单位：ms

ATK2_FIREBALL_DAMAGE = 60
ATK2_FIREBALL_LIFETIME = 5000  #单位：ms
ATK2_SPEED_Y = 8
ATK2_FIREBALL_SCALE = (80,80)

ATK3_FIREBALL_DAMAGE = 50
ATK3_FIREBALL_LIFETIME = 5000  #单位：ms
ATK3_FIREBALL_SPEED = 5

#SNAKE
SNAKE_MAXHP = 100
SNAKE_ATK = 20
SNAKE_SPEED = 2
SNAKE_ATTACK_RANGE = 150
SNAKE_DETECT_RANGE = 300
SNAKE_ATTACK_COOLDOWN = 2000  

#WOLF
WOLF_MAXHP = 70
WOLF_ATK = 10
WOLF_SPEED = 2
WOLF_ATTACK_RANGE = 200
WOLF_NOTICE_RANGE = 700
WOLF_MIN_DISTANCE = 300
WOLF_ATTACK_COOLDOWN = 2000
WOLF_FIRE_LIFETIME = 2000
WOLF_FIRE_SPEED = 4
WOLF_FIRE_ATK = 10

#Flower
FLOWER_MAXHP = 50
FLOWER_ATK = 15
FLOWER_SPEED = 2
FLOWER_DETECT_RANGE = 300
FLOWER_ATTACK_COOLDOWN = 1000
FLOWER_ATTACK_RANGE=150
#ZHIYINBOX
ZHIYINBOX_MAXHP = 100
ZHIYINBOX_ATK = 6
ZHIYINBOX_SPEED = 3
ZHIYINBOX_ATTACK_COOLDOWN = 1000

#WARRANT
WARRANT_MAXHP = 300
WARRANT_ATK = 20
WARRANT_SPEED = 2
WARRANT_ATTACK_COOLDOWN = 1000

#################################
#          NPC SETTING          #
#################################

#EILIN
EILIN_POSITION=[570,696]

#RENAULT
RENAULT_POSITION=[1350,570]

#################################
#          TP SETTING           #
#################################

#LEVEL2
TP_GATE_LEVEL2=[4710,540]
TP_TARGET_LEVEL2=[4860,680]
#LEVEL3
TP_GATE_LEVEL3=[6280,690]
TP_TARGET_LEVEL3=[6510,710]
#LEVEL4
TP_GATE_LEVEL4=[6315,720]
TP_TARGET_LEVEL4=[6605,740]
#LEVEL5
TP_GATE_LEVEL5=[5305,570]
TP_TARGET_LEVEL5=[5625,530]

#################################
#          LEVEL SETTING        #
#################################

LEVEL1_START_POSITION=[40,750]
LEVEL2_START_POSITION=[300,200]
LEVEL3_START_POSITION=[300,200]
LEVEL4_START_POSITION=[300,200]
LEVEL5_START_POSITION=[300,200]


#################################
#          PLOT TEXT            #
#################################
GAME_WIN_TEXTS = {
1:"从梦境的启示到现实的征途，卡伊尔怀揣着圣龙的召唤，\n踏上了寻觅星辉的旅程。与神秘吟游诗人艾琳的相遇，\n为他指引了前往古老遗迹的方向。未知的冒险即将展开，\n他们能否揭开星辉的秘密，迎接光明的回归？",
2:"经过“风息之塔”中的冒险，卡伊尔、艾琳与雷诺的队伍愈发坚不可摧。\n他们深知，每一块星辉碎片背后都隐藏着黑暗势力的重重阻挠。\n带着对未知的勇气，他们毅然前往北部深渊之湖，\n誓要揭开那里的秘密，继续他们的寻光之旅。",
3:"当“焰火之谷”的焰火照亮真相一角，黑影龙·诺克斯即将现身，\n艾琳的身世之谜是什么？\n最终的危险又是什么？他们深知，唯有直面恐惧，\n才能揭开所有谜团，迎接最终的试炼。",
4:"在“焰火之谷”中侥幸击退诺克斯，他们也得知了一切的真相。\n彼此心中既怀揣着对未知的恐惧，也燃烧着对光明的渴望。\n前往星之坠落地的途中，每一步都踏在历史的尘埃上，每一战都是对命运的抗争。\n最终决战在即，他们能否战胜内心的疑惑与外在的黑暗，\n让圣龙之星重新闪耀？",
 5:"随着最后一颗流星坠落，光明与黑暗的终极较量落下帷幕。\n卡伊尔、艾琳与雷诺，以无畏的勇气与坚定的信念，\n战胜了强大的黑影龙·诺克斯。\n而圣龙之星的重现，使夜空被璀璨的光芒所照亮，希望与和平再次降临大地。\n他们的旅程，见证了友谊的力量，揭示了命运的真相，\n更书写了一段关于勇气、牺牲与爱的传奇。\n而艾琳，作为圣龙之星的化身，她的记忆与力量在战斗中觉醒，完成了她的使命，\n也为这片大陆带来了永恒的守护。",
}

GAME_OVER_TEXTS = "YOU DIED!"

EILIN_PLOT_TEXTS = [
"旅人，你的脚步匆匆，眼中却藏着迷茫。\n这片大地已经很久没有见到像你这样坚定的眼神了\n……你是在寻找什么吗？",
"我只是一个吟游诗人，名字叫艾琳。\n至于为什么在这里……或许是因为命运让我在此等候一位勇者。\n你呢？你的名字是什么？",
"星辉碎片吗？有趣……我恰好知道一些关于它们的传说。\n它们散落在大陆的古老遗迹中，\n每一块都蕴含着强大的力量，但也伴随着巨大的危险。",
"我有一个条件——让我与你同行。\n这片大陆的黑暗正在蔓延，\n而我……也有一些未完成的使命。",
"作为交换，我会指导你习得治疗术。"
]

RENAULT_PLOT_TEXTS = [
"我不需要帮助。这些怪物……我一个人就能解决。",
"我叫雷诺。我不需要休息，也不需要同伴。\n我还有更重要的事情要做。",
"星辉碎片……你们也在找它们？",
"拯救？呵……我的家人已经死在了这片黑暗之中。\n我寻找碎片，只是为了复仇。",
"好吧。我会指导你习得魔法箭，\n但我警告你们，不要拖我的后腿。"
]

HELP_TEXTS = [
"《失落的星辉》帮助手册",
"一、开始游戏\n角色移动\n- W 为跳跃\n- A 为向左移动\n- D 为向右移动\n- 鼠标左键点击 为普通攻击\n- 按下esc 可以进入暂停页面\n- 按下F键可以显示碰撞矩形\n- 按下P键可以显示人物坐标\n",
"二、加载、存档\n一共只有6个档位，请开始你的冒险！\n注：请一定要记得存档，角色死亡后，存档会销毁（即无法游玩），享受一命通关的快乐吧~",
"三、剧情\n你可以在这里浏览过往所有剧情，以及相关人物介绍\n",
"四、地图编辑器\n-开发者工具（非开发者请小心使用），绘制每一章节\n-键盘左右键控制视野左右移动\n-按住shift加速\n",
"五、技能与等级机制\n-技能1：治疗术：\n释放方式：按下H键释放\n效果：消耗一定魔力值，恢复自身生命值\n描述：由艾琳传授给你的，或许在陷入绝境之时使用效果更佳？\n-技能2：魔法箭：\n施放方式：按下G键释放\n效果：向前发出一道魔力箭矢，对路径上的敌人造成伤害。\n描述：由雷诺 指导你习得，雷诺大叔总是刀子嘴豆腐心，看不惯卡伊尔被怪物折磨，还是指导了卡伊尔这个技能。\n等级机制：\n- 打一关，升一级\n等级数可由血量下方的星星数目得知\n角色基础属性会随等级提升而提升\n",
"六、角色介绍\n-卡伊尔：一名年轻的勇者，曾是圣龙教会的一名见习骑士，他的家园因怪物袭击而毁灭，立志收集星辉碎片拯救世界。\n-艾琳：一位神秘的吟游诗人，擅长魔法与歌声。她总是知道很多隐秘的事情，似乎与圣龙之星有某种特殊的联系。（第二关出现，触碰触发互动）\n-雷诺：一名流浪的战士，身形魁梧却性格沉默寡言。他的家人也因星辰坠落后的灾难而丧生，他加入队伍是为了寻找复仇的机会。（第三关出现，触碰触发互动）\n-黑影龙·诺克斯：传闻是圣龙堕落后化身的邪恶存在，它觊觎散落的星辉碎片，企图将其吸收以获得无尽的力量。\n",
"七、反派介绍\n小怪\n\n普通怪物（旅途中的常见敌人）\n- 暗影狼\n外观：通体漆黑，毛发像流动的烟雾，眼睛发出猩红的光芒。它们身上会散发微弱的符文标志。\n\n背景：在圣龙之星坠落后，这些狼受到了黑暗力量的侵蚀，变得狂暴无比，专门猎杀人类。\n-幻紫之眼\n外观：外形像一朵巨大的花，中心是一颗发光的“眼珠”\n\n背景：这些植物原本生长在圣龙之星的坠落地附近，星辉碎片的辐射使它们变得异常危险。\n\n-内有乾坤：\n外观：一只雄健的鸡，伴生于部分宝箱之间\n背景：它觉得篮球与music与中分背带裤的结合真是酷毙了\n\n-裂地虫\n外观：巨大如牛的甲虫，坚硬的外壳上布满裂纹，会发出淡淡的蓝光。它们的背部有类似星辉碎片的结晶。\n背景：裂地虫生活在地下，但圣龙之星坠落后，能量辐射使它们变得巨大且具有攻击性。\nA\n遗迹守护者（星辉守护者）\n- 虚空守卫（精英）\n外观：一具高大的盔甲，盔甲表面遍布符文\nBoss怪物（关键战斗中的敌人）\n- 黑影龙·诺克斯\n外观：一条巨大的金龙，或许还尚存一丝当年的风范？。\n背景：诺克斯是圣龙的堕落之形，它的目标是吸收所有星辉碎片的力量，彻底摧毁圣龙的遗产，成为唯一的世间支配者\n 为什么小怪的具体信息不会告诉你呢？因为雷诺大叔特意删掉了艾琳给卡伊尔的小册子中的内容，并表示卡伊尔这小家伙还需要成长~"
]

PLOT_TEXTS = [
["第一章：星辉的召唤/n卡伊尔住在一个偏远的小村庄，十年前的圣龙之星坠落时，他的父母在村庄被怪物摧毁的混乱中丧生。/n一天夜里，他在一场奇异的梦中见到了圣龙的身影，圣龙的声音对他说：“拾起失落的星辉，唤回光明。”/n醒来后，他发现村庄附近出现了一块发光的星辉碎片，周围的怪物疯狂地守护着它。卡伊尔击败了怪物，获得了第一块星辉碎片。他意识到，/n这或许是自己的命运，他决定离开村庄，寻找其他碎片。/"],
["第二章：遗迹与盟友/n途中，他遇到了艾琳，一位神秘的吟游诗人。艾琳告诉他，星辉碎片散落在大陆的古老遗迹中，但她没有解释为何自己对这些秘密了如指掌。/n 卡伊尔与艾琳踏上旅途，来到了第一座遗迹——“风息之塔”。/n遗迹中充满了危险的机关和守护者，但在艾琳的歌声魔法帮助下，他们成功找到了第二块星辉碎片。/n他们遇到了雷诺，一名孤独的战士，他正试图击败魔物，却因寡不敌众而陷入危机。卡伊尔救下了雷诺，三人决定结伴同行。/n随着旅程的深入，他们发现每一块星辉碎片都被某种强大的黑暗力量保护着。每当他们找到一块碎片，/n总会感受到一股邪恶的力量在暗中窥探。/n "],
["第三章：深渊之湖/n随着旅程的深入，他们发现每一块星辉碎片都被某种强大的黑暗力量保护着。/n卡伊尔、艾琳和雷诺前往位于北部的深渊之湖，寻找第三块星辉碎片。/n湖水宁静、四周弥漫着腐化气息，艾琳感知到黑暗力量的存在。/n历经恶战，获取到了第四块星辉碎片，他们离目标越来越近了，但黑暗的力量依然未曾消散，接下来的路将更加危险。/n "],
["第四章：焰火之谷的试炼/n卡伊尔、艾琳和雷诺来到“焰火之谷”，这里是传说中圣龙之火燃烧的地方，也是第四块星辉碎片的所在地。/n然而，谷里的空气中弥漫着一种不安的气息。/n在前往谷深处的途中，卡伊尔开始感到一种无形的压力。/n他的脑海中不断浮现出父母在村庄毁灭时的场景，以及他未能保护他们的内疚。/n艾琳察觉到卡伊尔的异常，试图用歌声安抚他，但卡伊尔却显得有些烦躁。他告诉艾琳和雷诺，他需要一个人静一静。/n雷诺提醒卡伊尔，团队需要他的领导，但卡伊尔却反问道：“如果我的力量不够，我们还能成功吗？”雷诺沉默片刻，回答道：“力量不是一切，信念才是。”/n卡伊尔在战斗中仿佛看到了村庄毁灭的惨状、艾琳和雷诺在战斗中倒下、以及自己被黑暗吞噬的画面。他必须克服内心的恐惧，重新坚定自己的信念。/n 怀着一颗伤痕累累的心，他目光中浑浊却带着一丝澄澈。三人带着星辉碎片离开焰火之谷，卡伊尔的神情变得坚定，他告诉艾琳和雷诺，他们已经离目标越来越近了。/n艾琳注意到卡伊尔的变化，微笑着说道：“你终于找到了自己的光。”雷诺则拍了拍卡伊尔的肩膀，表示认可。/n 三人继续踏上旅程，前往最后的战场——“星之坠落地”"],
["第五章：星之坠落地/n最终，卡伊尔、艾琳和雷诺来到了“星之坠落地”，这里是一片荒芜的废土，遍布巨大的陨石坑，所有的星辉碎片都源于此地。/n他们找到了最后一块碎片，却遭到了诺克斯的阻击。/n诺克斯吸收了最后一块碎片的力量，变成了无比强大的暗龙形态。它试图吞噬艾琳，以彻底摧毁圣龙之星的希望。/n卡伊尔和雷诺拼尽全力，与诺克斯展开了最终决战。在战斗中，艾琳的力量觉醒，她用歌声召唤出了圣龙的灵魂，与卡伊尔一起发动最后的/n攻击。/n最终，诺克斯被彻底击败，星辉碎片重新聚合成圣龙之星，飞向天空，点亮了夜空。/n "],
["尾声：/n卡伊尔从梦中醒来，捡起类床边的‘碎片’，不禁想起了自己的过往。但是，如今黑暗已经不复存在，光明笼罩着整片大陆。/n然而，地平线的一个角落，一个不起眼的身影悄悄略过。/n--真正的冒险才刚刚开始/n"]
]

END_PLOT_TEXTS = [
"你已经通关了游戏，感谢你的游玩，希望你能喜欢这个故事。",
]