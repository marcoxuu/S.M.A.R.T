#coding=utf-8

import sys, os
import yara
from PyQt4 import QtCore, QtGui

sys.path.append("../ssma_python2")
from src import colors
from src.check_file import PEScanner, file_info
from src.blacklisted_domain_ip import ransomware_and_malware_domain_check
from src.check import is_malware, is_file_packed, check_crypto, is_antidb_antivm, is_malicious_document
from src.check_file import PEScanner, file_info
from src.check_updates import check_internet_connection, download_yara_rules_git
from src.check_virustotal import virustotal
from src.file_strings import get_strings

reload(sys)
sys.setdefaultencoding( "utf-8" )

class CheckPacker(QtCore.QThread):
    numberSignal = QtCore.pyqtSignal(int, str)
    valueSignal  = QtCore.pyqtSignal(list)

    def __init__(self, filename, parent=None):
        super(CheckPacker, self).__init__(parent)
        self.filename = filename
    
    def run(self):
        pkdresult = is_file_packed(self.filename)
        result = []
        if pkdresult:
            print "get pkdresult!"
            for n in pkdresult:
                # 能输出描述则输出描述
                # 否则直接输出规则名
                try:
                    print "{} - {}".format(n, n.meta['description'])
                except:
                    print n
                # 最终直接输出评估结果，数据库里存详细内容
                result.append(n)
            self.valueSignal.emit(result)
        else:
            print "no match"

class CheckMalware(QtCore.QThread):
    numberSignal = QtCore.pyqtSignal(int, str)
    valueSignal  = QtCore.pyqtSignal(list)

    def __init__(self, filename, parent=None):
        super(CheckMalware, self).__init__(parent)
        self.filename = filename
    
    def run(self):
        malresult = is_malware(self.filename)
        result = []
        if malresult:
            print "get malresult!"
            for n in malresult:
                try:
                    print "{} - {}".format(n, n.meta['description'])
                except:
                    print n
                result.append(n)
            self.valueSignal.emit(result)
        else:
            print "no match"