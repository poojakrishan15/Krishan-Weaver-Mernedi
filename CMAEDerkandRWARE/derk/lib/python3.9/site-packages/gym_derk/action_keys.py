from enum import Enum

class ActionKeys(Enum):
  """These are the actions a Derkling can take, which you send to the step function.

  Attributes:
    MoveX = 0: A number between -1 and 1. This controlls forward/backwords movement of the Derkling.
    Rotate = 1: A number between -1 and 1. This controlls the rotation of the Derklin. Rotate -1 mean turn left full speed.
    ChaseFocus = 2: A number between 0 and 1. If this is 1, the MoveX and Rotate actions are ignored and instead the Derkling runs towards its current focus. Numbers between 0-1 interpolates between this behavior and the MoveX/Rotate actions, and 0 means only MoveX and Rotate are used.
    CastingSlot = 3: 0=don't cast. 1-3=cast corresponding ability.
    ChangeFocus = 4: 0=keep current focus. 1=focus home statue. 2-3=focus teammates, 4=focus enemy statue, 5-7=focus enemy
  """
  MoveX = 0
  Rotate = 1
  ChaseFocus = 2
  CastingSlot = 3
  ChangeFocus = 4
