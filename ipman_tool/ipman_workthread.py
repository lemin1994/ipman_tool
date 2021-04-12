from ipman_tool.SR_cutover_tool import SR_cutover_tool,SR_cutover_check_tool

from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal

class ServiceHelper(QThread):
    update_str = pyqtSignal(str)

    def __init__(self, sw_file, sr01_file, sr02_file, save_path, target_port, target_lag, vlan_last=None):
        super(QThread, self).__init__()
        self.sw_file = sw_file
        self.sr01_file = sr01_file
        self.sr02_file = sr02_file
        self.save_path = save_path
        self.target_port = target_port
        self.target_lag = target_lag
        if vlan_last is not None and str(vlan_last).strip() != "":
            self.vlan_last = str(vlan_last).split(",")
        else:
            self.vlan_last = None

    def run(self):
        self.update_str.emit("现在开始进行业务分析以及脚本生成！")
        if self.target_port is not None:

            srct = SR_cutover_tool(self.target_port, self.sw_file, [self.sr01_file, self.sr02_file], self.save_path, self.target_lag, self.vlan_last)
            srct.get_target_olt_sap_and_write()
            self.update_str.emit("业务分析以及脚本完成！")
        else:

            srct = SR_cutover_tool(None, self.sw_file, [self.sr01_file, self.sr02_file], self.save_path,
                                   self.target_lag, None)
            srct.get_all_olt_sap_and_write()
            self.update_str.emit("业务分析完成！")

class PTNServiceHelper(QThread):
    update_str = pyqtSignal(str)

    def __init__(self, sw_file, sr01_file, sr02_file, save_path, ptn_file, target_lag):
        super(QThread, self).__init__()
        self.sw_file = sw_file
        self.sr01_file = sr01_file
        self.sr02_file = sr02_file
        self.save_path = save_path
        self.ptn_file = ptn_file
        self.target_lag = target_lag

    def run(self):
        self.update_str.emit("现在开始进行PTN集客业务分析和脚本生成！")
        srct = SR_cutover_tool(None, self.sw_file, [self.sr01_file, self.sr02_file], self.save_path, self.target_lag, None, ptn_file=self.ptn_file)
        srct.get_target_ptn_output()
        self.update_str.emit("业务分析和脚本生成完毕！")

class ServiceCheckHelper(QThread):
    update_str = pyqtSignal(str)

    def __init__(self, sw_file, save_path):
        super(QThread, self).__init__()
        self.sw_file = sw_file
        self.save_path = save_path

    def run(self) -> None:
        self.update_str.emit("现在开始进行PTN集客业务分析和脚本生成！")
        scct = SR_cutover_check_tool(self.sw_file, self.save_path, "config.bin")
        scct.get_all_jk_service()
        self.update_str.emit("业务分析和脚本生成完毕！")

