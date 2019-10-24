from lib.HttpApiAppLib import HttpApiLib
from lib.InvestSystem import InvestSystem
from lib.LoanSystem import LoanSystem
from lib.CoreSystem import CoreSystem
from lib.MysqlDB import MysqlDB
from lib.RedisDB import RedisDB
# from lib.UserForget import UserForget
# from lib.OpenAccount import OpenAccount
# from lib.RefreshToken import RefreshToken
# from lib.HttpApiMainProcess import HttpApiMainProcess
# from lib.UserCheckMailbox import UserCheckMailbox
# from lib.uploadHeadImg import uploadHeadImg
from lib import version

_version_ = version.VERSION

class lib(HttpApiLib,InvestSystem,LoanSystem,CoreSystem,MysqlDB,RedisDB):

    ROBOT_LIBRARY_SCOPE ='GLOBAL'
