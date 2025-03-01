from enum import Enum
from typing import List

class Action(Enum):
    CREATE_PROJECT = "CREATE_PROJECT"
    UPDATE_PROJECT = "UPDATE_PROJECT"
    DELETE_PROJECT = "DELETE_PROJECT"
    VIEW_PROJECT = "VIEW_PROJECT"
    INVITE_USER = "INVITE_USER"
    DELETE_USER = "DELETE_USER"

# TODO : 향후 DB에 테이블 생성
ROLE_ACTIONS = {
    "ADMIN" : [
        Action.CREATE_PROJECT,
        Action.UPDATE_PROJECT,
        Action.DELETE_PROJECT,
        Action.VIEW_PROJECT,
        Action.DELETE_USER,
        Action.INVITE_USER
    ],
    "PROJECT_OWNER" : [
        Action.CREATE_PROJECT,
        Action.UPDATE_PROJECT,
        Action.DELETE_PROJECT,
        Action.VIEW_PROJECT,
        Action.INVITE_USER
    ],
    "EDITOR" : [
        Action.UPDATE_PROJECT,
        Action.VIEW_PROJECT
    ],
    "VIEWER" : [
        Action.VIEW_PROJECT
    ]
}