# This is an ECNU2024-pygame project

# 游戏名：The Starry Veil -- 星辰之幕

### 游戏风格

- 2D,横板，闯关，动作。

## 如何运行

- 直接运行main目录下的main.py即可

## 运行展示

### 开始
![startmenu](https://s2.loli.net/2025/01/14/bSoZV8DUflGRNg7.png)

### 过场剧情
![plot](https://s2.loli.net/2025/01/14/doeDuZQzJwN8Glm.png)

### Boss战
![bossbattle](https://s2.loli.net/2025/01/14/1TiDVpKYU9bdlkS.png)
![bossbattle2](https://s2.loli.net/2025/01/14/3Jes9Cpi1TtWHKY.png)

### 地图编辑器
![mapeditor](https://s2.loli.net/2025/01/14/lSZ6rGosE7NHeQh.png)

### 存档功能
![save](https://s2.loli.net/2025/01/14/N59E1XYWZJGbuhk.png)

### npc对话
![npc](https://s2.loli.net/2025/01/14/OQDC64LZu7fwRN9.png)

# 项目介绍

## 整体框架

- 基于此项目的框架和实现，Python的面向对象编程也是露出了它的獠牙。

### 项目结构

- main:
  - lib(库函数)
    - menu
      - StartMenu.py
      - ...
    - monsters
      - dragon.py
      - ...
    - saves
      - saveManager.py 
      - ...
    - Player.py
    - ...
  - mapseed(地图种子)
    - level1_seed.csv
    - ...
  - save(存档)
    - save1.json
    - ...
  - src(素材图片)
  - main.py(游戏执行主体)
  - settings.py(参数设置)

### 实现功能

- 动作游戏最基本的功能：角色与怪物的交互，角色与地形的检测（也是最麻烦的部分）
- 玩家：实现监听键盘移动，技能，监听鼠标攻击，hp/mp更新，碰撞检测等等。
- 小怪：实现自动攻击机制，自动移动机制，跟随玩家移动，以及一些小怪攻击特效。
- 游戏地图：是由一块块的tile搭建起来的，可以通过地图种子保存和加载
- 地图编辑器：实现用来编辑关卡地图的功能，可以选用不同类型的tile，编辑每一块tile的位置，可以设置怪物出生点。
- 帮助文档：便于玩家游玩
- 剧情文档：便于查阅剧情
- 等级系统：实现每过一关升一级，玩家数值随等级基于一定的倍率而提高，并且实时显示
- 技能系统：实现了技能冷却，技能冷却状态实时更新，技能释放的反馈（技能效果）如：回血，耗蓝，造成伤害等
- 关卡系统：设置了每个关卡的解锁状态，实现了过一关解锁一关的功能，实现判定游戏的失败（玩家死亡）和胜利（杀死全部小怪且获取碎片/杀死全部小怪）
- 存档系统：实现了六个槽位的分别存储，在槽位显示存储日期的信息，存档记录了每个关卡的状态和每个关卡中的信息。
- 菜单功能：实现了不同菜单之间的切换功能，以及选关菜单。
- npc：实现了两个npc，以及触碰时触发对话，解锁技能的功能。
- 存档机制：角色死亡后无法再游玩本关（一个存档中，不影响其他存档）（即要求一命通关才可能通关本游戏），一关胜利后无法在游玩本关
- 辅助功能：显示角色坐标的功能（可开关），显示矩形碰撞箱的功能（可开关）

## 制作过程中的困难（一些实现思路）

- 地图编辑器
- 十分低级，并且只能应对没有角色移动的情况，实现简单”背景图移动
- 细节:Screen对象左上角始终为（0，0）右下角始终为（WIDTH,H EIGTH ),所以当按下<->健时，用scroll值记录，每次在横坐标为0-scroll位置开始画图（ 其实就是在x负半轴开始画，Screen原地踏步），在Screen范围之外的不显示，于是就有了背景图的“ 左 右移动”。

- tile相关:用编号记录，包括角色也会用编号记录。刷新每帧地图时会逐行比对编号然后贴图。地图编辑器中tile具体位置要计算相对位置保存在二维数组中（排除scroll）。关卡中每个tile都会被添加到pygame的Spritegroup中，好像是方便角色移动。

- 菜单。一个菜单页面一个类，因为菜单往往要负责创建类，以及功能实现。主要，游戏中所有类不会被销毁，只创建一次，因此如果run函数中有,ispausing，isrunning等标志，需要在每次调用run函数时刷新，最好不要把这类变量设为self而是直接当做函数的局部变量。处理事件注意顺序。最后菜单相关代码需要简化，重复代码太多，会被打低分的。

- 关卡。设置Sprite组（pg内置的）（障碍物，爆炸物，角色，敌人，boss，NPC，液体等），方便管理。处理事件注意顺序，角色相关一般滞后，画图应该优先。由于每个关卡的基本骨架都相同，为了不不断重复无意义的代码，采用继承的方式，定义关卡基类，再导出每一关的子类。画图统一在主循环里面画，杜绝角色update自行绘图.处理事件遵循流水线原则，主线尽量只有一条输入线。

- 背景图
- camera:原理和地图编辑器差不多，只是拓展了xy轴，其topleft就是其世界坐标取负值，用于使用move函数直接计算相对位移
- 由于缺乏超长背景图，所以游戏背景图采用拼贴或者反复放映的形式

- 角色：
- 加载动画通过连续帧的更新，达到视觉暂留的效果实现动画，要从一张包含每个帧的图片中切分出每个帧的图像，保存起来方便后面调用。通过一个字典存储状态名到动画帧列表的键值对，向左的动画由向右的动画翻转得到，每次开始游戏时先预处理读取状态帧字典，减少了后续游戏运行的性能开销。

- 还需要响应键盘来达到移动效果，通过检测键盘按键按下更改角色矩形的移动参数，计算角色矩形的坐标增长量，再应用到矩形的坐标上。

- 难点：碰撞检测，因为地形是一块块的tile搭起来的，而且pygame自带的检测碰撞的函数不包括检测方向的函数，因此需要手动实现水平和竖直两个方向的与地形的碰撞检测。我通过暂时不应用偏移量，而是先分别判断作用两个方向的偏移量后的矩形是否与地形碰撞，若碰撞则重新计算偏移量，水平方向直接变化量dx=0，竖直方向计算玩家矩形下部与地形矩形顶部之差，再应用，即可实现碰撞后不穿过障碍物的效果。

- 存档：
- 涉及到文件操作，通过查阅资料，可以将关卡状态用一个字典储存起来保存到json文件中以供读取。且有六个槽位分别存储，并且还要显示存档日期。于是通过设计一个字典，存储了存档日期，玩家信息（玩家属性），小怪信息，保存到save+num的格式化文件名中以便区分不同槽位，槽位每次显示日期时只要读取对应槽位的日期即可，读取存档时，分别对每一个关卡进行恢复。json文件打开不能为空.

- 小怪如何跟随主角，增加，水平方向定位，和遇障碍起跳逻辑，小怪能有70%概率追上主角
- 小怪素材的搜集和处理步骤
得到原始素材：网络搜集连帧的简单原始图片；
gif转为图片使用python的PIL进行帧分解；豆包帮助生成
然后主要使用PS进行原始素材处理，使用联系表进行图片拼接。运用不同素材给部分小怪皮肤加上符文效果。使用仿制图章工具，去掉了素材水印。抠图形成透明背景，用python库cv2逐像素去色加上PS的蒙版叠加。
- 小怪和攻击效果的组织方式
原来是单独在类内设置blit，并且将攻击效果和正常状态全部放在一个类中，错综复杂，不易调试，产生诸多问题，也增加了代码量。之后查资料，将离体攻击效果单独都成立类，使攻击效果成为本体类的子类，逻辑变清晰，更好维护。
- 小怪的死亡机制
小怪和攻击效果都各自有独立类，怎么销毁比较统一和普适比较纠结。尝试定义levels中的garbage_bin精灵组，小怪内自动检测生命值小于零情况，死亡时将本体类对象，攻击效果类对象，血条对象都投递到levels中的garbage_bin精灵组，统一销毁。

# 写在最后 

- 首先感谢参与制作项目的成员，没有这个团队是很难独立做出来的。
- 其次实际上代码还有很多可以改进的地方，还可能有一些小bug（角色图片偏离矩形，有的时候地形检测碰撞卡地形等等，不过不影响正常游玩吧）
- 最后这是一个宝贵的项目经验，作为一个小游戏，它的完成度还是挺高的。
- 最后吐槽一句,就是pygame游戏引擎太底层了，如果还有第二次，希望使用更高级的游戏引擎
- 希望为后续这门课程这个作业允许更多人数
