ALIGN_BOTTOM_CENTER = 1
ALIGN_CENTER_CENTER = 2
ALIGN_TOP_CENTER = 3
ALIGN_TOP_LEFT = 4
ALIGN_BOTTOM_RIGHT = 5

CATEGORY_DEFAULT = 0x0001
CATEGORY_CHARACTER = 0x0002
CATEGORY_PROJECTILE = 0x0004
CATEGORY_WEAPON = 0x0008

MASK_DEFAULT = 0xFFFF
MASK_CHARACTER = CATEGORY_DEFAULT ^ CATEGORY_PROJECTILE ^ CATEGORY_CHARACTER
MASK_PROJECTILE = CATEGORY_DEFAULT ^ CATEGORY_CHARACTER
MASK_WEAPON = 0

FILTER_DEFAULT = ( CATEGORY_DEFAULT, MASK_DEFAULT )
FILTER_CHARACTER = ( CATEGORY_CHARACTER, MASK_CHARACTER )
FILTER_PROJECTILE = ( CATEGORY_PROJECTILE, MASK_PROJECTILE )
FILTER_WEAPON = ( CATEGORY_WEAPON, MASK_WEAPON )

INPUT_TYPE_NULL = 0
INPUT_TYPE_KEYBOARD_MOUSE = 1
INPUT_TYPE_JOYSTICK = 2

JOYSTICK_BUTTON_PICKUP = 3
JOYSTICK_BUTTON_USE = 5
JOYSTICK_BUTTON_START = 7
JOYSTICK_BUTTON_ADD_HEALTY = 0
JOYSTICK_BUTTON_ADD_POWER = 1
JOYSTICK_BUTTON_ADD_FIRERATE = 2
JOYSTICK_BUTTON_LEVEL_UP = 4
JOYSTICK_BUTTON_SUPER = 6

JOYSTICK_AXIS_HORIZONTAL_MOVE = 0
JOYSTICK_AXIS_VERTICAL_MOVE = 1
JOYSTICK_AXIS_HORIZONTAL_TURN = 3
JOYSTICK_AXIS_VERTICAL_TURN = 4

SCENE_TYPE_MENU = 0
SCENE_TYPE_GAME = 1

DAMAGE_TYPE_PHYSICAL = 0
DAMAGE_TYPE_FIRE = 1
DAMAGE_TYPE_ICE = 2
DAMAGE_TYPE_LIGHTNING = 3

XBOX_KEY_MAP = {
    JOYSTICK_BUTTON_PICKUP : 3,
    JOYSTICK_BUTTON_USE : 5,
    JOYSTICK_BUTTON_START : 7,
    JOYSTICK_BUTTON_LEVEL_UP: 4,
    JOYSTICK_BUTTON_ADD_HEALTY: 2,
    JOYSTICK_BUTTON_ADD_POWER: 0,
    JOYSTICK_BUTTON_ADD_FIRERATE: 1,
    JOYSTICK_BUTTON_SUPER: 2,
    JOYSTICK_AXIS_HORIZONTAL_MOVE : 0,
    JOYSTICK_AXIS_VERTICAL_MOVE : 1,
    JOYSTICK_AXIS_HORIZONTAL_TURN : 4,
    JOYSTICK_AXIS_VERTICAL_TURN : 3,
}

GENERIC_KEY_MAP = {
    JOYSTICK_BUTTON_PICKUP : 3,
    JOYSTICK_BUTTON_USE : 5,
    JOYSTICK_BUTTON_START : 9,
    JOYSTICK_BUTTON_LEVEL_UP: 4,
    JOYSTICK_BUTTON_ADD_HEALTY: 0,
    JOYSTICK_BUTTON_ADD_POWER: 1,
    JOYSTICK_BUTTON_ADD_FIRERATE: 2,
    JOYSTICK_BUTTON_SUPER: 6,
    JOYSTICK_AXIS_HORIZONTAL_MOVE : 0,
    JOYSTICK_AXIS_VERTICAL_MOVE : 1,
    JOYSTICK_AXIS_HORIZONTAL_TURN : 2,
    JOYSTICK_AXIS_VERTICAL_TURN : 3,
}

DEFEAT_GROUP_AI = 0
DEFEAT_GROUP_PLAYERS = 1
