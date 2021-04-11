from ipman_tool.al_sr_extractor import AL_sr_extractor,AL_sr_extractor_v2
from ipman_tool.sw_extractor import  SW_extractor

import time
import logging
import pickle
import pandas as pd

def isIpV4AddrLegal(ipStr):
    if str(ipStr).find("/") != -1:
        ipStr = str(str(ipStr).split("/")[0])
    # 切割IP地址为一个列表
    ip_split_list = ipStr.strip().split('.')
    # 切割后列表必须有4个元素
    if 4 != len(ip_split_list):
        return False
    for i in range(4):
        try:
            # 每个元素必须为数字
            ip_split_list[i] = int(ip_split_list[i])
        except:
            print("IP invalid:" + ipStr)
            return False
    for i in range(4):
        # 每个元素值必须在0-255之间
        if ip_split_list[i] <= 255 and ip_split_list[i] >= 0:
            pass
        else:
            print("IP invalid:" + ipStr)
            return False
    return True

class SR_cutover_tool(object):
    def __init__(self, target_port, sw_file, sr_files, save_path, target_lag, vlan_last=None, ptn_file=None):

        self.target_port = target_port
        self.sw_extractor = SW_extractor(sw_file)
        self.save_path = save_path
        self.target_port = target_port
        self.vlan_last = vlan_last
        self.ptn_file = ptn_file
        self.ptn_vlan = []
        self.target_lag = target_lag

        if len(sr_files) != 2:
            logging.error("SR数量必须为2!")
            exit()

        self.al_sr_extractor_1 = AL_sr_extractor(sr_files[0])
        self.al_sr_extractor_2 = AL_sr_extractor(sr_files[1])

        if self.ptn_file is not None:
            df = pd.read_excel(ptn_file)
            for index, row in df.iterrows():
                vlan = str(row["SVLAN"]).strip()
                if vlan not in self.ptn_vlan:
                    self.ptn_vlan.append(vlan)

    def get_olt_jk_vlans(self, target_port):
        vlans = [int(v) for v in self.sw_extractor.eth_trunk_vlan[self.sw_extractor.port_eth_trunk[target_port]]]
        target_vlans = []
        for v in vlans:
            if v < 1000:
                continue
            vlan = str(v)
            if self.vlan_last is not None:
                if vlan[-1] in self.vlan_last:
                    target_vlans.append(vlan)
            elif vlan.endswith("4") or vlan.endswith("3") or vlan.endswith("7"):
                target_vlans.append(vlan)
        return target_vlans

    def get_target_olt_sap_and_write(self):

        targetPorts_vlans = self.get_olt_jk_vlans(self.target_port)

        # 处理 SR01
        sr01_lag = self.sw_extractor.sr_lag[self.al_sr_extractor_1.sr_name]
        sr01_sap = self.get_lag_sap(self.al_sr_extractor_1.sap_dict, sr01_lag, targetPorts_vlans)
        self.write_excel(sr01_sap, self.al_sr_extractor_1.sr_name)
        self.write_script(sr01_sap, self.al_sr_extractor_1.sr_name, sr01_lag, target_lag=self.target_lag)
        # 处理SR02
        sr02_lag = self.sw_extractor.sr_lag[self.al_sr_extractor_2.sr_name]
        sr02_sap = self.get_lag_sap(self.al_sr_extractor_2.sap_dict, sr02_lag, targetPorts_vlans)
        sr02_ptn_sap = self.get_ptn_sap(self.al_sr_extractor_2.sap_dict, sr02_lag)
        
        self.write_excel(sr02_sap, self.al_sr_extractor_2.sr_name)
        self.write_script(sr02_sap, self.al_sr_extractor_2.sr_name, sr02_lag, target_lag=self.target_lag)

    def get_all_olt_sap_and_write(self):
        # 处理 SR01
        sr01_lag = self.sw_extractor.sr_lag[self.al_sr_extractor_1.sr_name]
        sr01_sap = self.get_all_olt_sap(self.al_sr_extractor_1.sap_dict, sr01_lag)
        self.write_excel(sr01_sap, self.al_sr_extractor_1.sr_name)
        # self.write_script(sr01_sap, self.al_sr_extractor_1.sr_name, sr01_lag, target_lag=self.target_lag)
        # 处理SR02
        sr02_lag = self.sw_extractor.sr_lag[self.al_sr_extractor_2.sr_name]
        sr02_sap = self.get_all_olt_sap(self.al_sr_extractor_2.sap_dict, sr02_lag)

        self.write_excel(sr02_sap, self.al_sr_extractor_2.sr_name)
        # self.write_script(sr02_sap, self.al_sr_extractor_2.sr_name, sr02_lag, target_lag=self.target_lag)

    def get_target_ptn_output(self):
        # 处理 SR01
        sr01_lag = self.sw_extractor.sr_lag[self.al_sr_extractor_1.sr_name]
        sr01_ptn_sap = self.get_target_vlan_ptn_sap(self.al_sr_extractor_1.sap_dict, sr01_lag, self.ptn_vlan)
        self.write_excel(sr01_ptn_sap, self.al_sr_extractor_1.sr_name + "_ptn")
        self.write_script(sr01_ptn_sap, self.al_sr_extractor_1.sr_name, sr01_lag, target_lag=self.target_lag)
        # 处理 SR02
        sr02_lag = self.sw_extractor.sr_lag[self.al_sr_extractor_2.sr_name]
        sr02_ptn_sap = self.get_target_vlan_ptn_sap(self.al_sr_extractor_2.sap_dict, sr02_lag, self.ptn_vlan)
        self.write_excel(sr02_ptn_sap, self.al_sr_extractor_2.sr_name + "_ptn")
        self.write_script(sr02_ptn_sap, self.al_sr_extractor_2.sr_name, sr02_lag, target_lag=self.target_lag)

    def get_lag_sap(self, sap_dict, lag, vlans):
        target_dict = dict()
        for vlan in vlans:
            lag_vlan = lag + ":" + vlan
            # print(lag_vlan)
            for sap in sap_dict.keys():

                # print(sap)
                if (lag_vlan + ".") in sap:
                    target_dict[sap] = sap_dict[sap]
        return target_dict
    
    def get_ptn_sap(self,sap_dict, lag):
        target_dict = dict()
        for sap in sap_dict.keys():
            if (lag + ":") in str(sap) and str(sap).endswith(".0"):
                target_dict[sap] =sap_dict[sap]
        return target_dict

    def get_all_olt_sap(self, sap_dict, lag):
        target_dict = dict()
        for sap in sap_dict.keys():
            if (lag + ":") in str(sap) and not str(sap).endswith(".0"):
                target_dict[sap] =sap_dict[sap]

        return target_dict

    def get_target_vlan_ptn_sap(self, sap_dict, lag, vlans):
        target_dict = dict()
        if len(vlans) > 0:
            for vlan in vlans:
                target_lag = lag + ":" + vlan + ".0"
                print(target_lag)
                for sap in sap_dict.keys():
                    if target_lag in str(sap) and str(sap).endswith(".0"):
                        target_dict[sap] =sap_dict[sap]
            return target_dict
        else:
            for sap in sap_dict.keys():
                if (lag + ":") in str(sap) and str(sap).endswith(".0"):
                    target_dict[sap] = sap_dict[sap]
            return target_dict

    def write_excel(self, sap_dict, sr_name):
        df = pd.DataFrame()
        count = 0
        type = None
        for sap in sap_dict.keys():
            print(sap)
            svlan = str(sap).split(":")[-1].split(".")[0]
            cvlan = str(sap).split(":")[-1].split(".")[1]
            if sap_dict[sap]["interface_content"].strip() != "":

                target_ips = []
                ips = str(sap_dict[sap]["interface_content"].strip()).split()
                for ip in ips:
                    if isIpV4AddrLegal(ip):
                        target_ips.append(ip)
                type = "独立网关或者VPRN"
            else:
                target_ips = []
                ips = str(sap_dict[sap]["content"].strip()).split()
                for ip in ips:
                    if isIpV4AddrLegal(ip):
                        target_ips.append(ip)
                type = "共享网关"
            ip_str = ",".join(target_ips)
            df.loc[count, "svlan"] = svlan
            df.loc[count, "cvlan"] = cvlan
            df.loc[count, "ip"] = ip_str
            df.loc[count, "业务类型"] = type
            count += 1
        df.to_excel(self.save_path + "/" + sr_name + "_"+ str(int(time.time())) +".xlsx")

    def write_script(self, sap_dict, sr_name, source_lag,target_lag="50"):
        # 生成割接前的脚本
        source_file = open(self.save_path + "/" + sr_name + "_割接前.txt", "w")

        for sap in sap_dict.keys():

            # if sap_dict[sap]["type"] != "ies" and sap_dict[sap]["type"] != "vprn":
            #     continue
            if sap_dict[sap]["interface"] is None:
                if sap_dict[sap]["content"].strip() != "":
                    source_file.write("/configure service \n")
                    source_file.write(sap_dict[sap]["type_str"] + "\n")
                    source_file.write(sap_dict[sap]["subscriber_interface"] + "\n")
                    source_file.write(sap_dict[sap]["group_interface"] + "\n")
                    source_file.write(sap_dict[sap]["content"])
                    source_file.write("\n")
            else:
                if sap_dict[sap]["interface_content"].strip() != "":
                    source_file.write("/configure service \n")
                    source_file.write(sap_dict[sap]["type_str"] + "\n")
                    source_file.write(sap_dict[sap]["interface"] + "\n")
                    source_file.write(sap_dict[sap]["interface_content"] + "\n")

        source_file.close()

        # 生成删除旧数据的脚本
        del_file = open(self.save_path + "/" + sr_name + "_删除.txt", "w")
        count_1 = 1
        # 生成删除脚本
        for sap in sap_dict.keys():
            if count_1 % 10 == 0:
                del_file.write("================  这里刷一次脚本，避免刷的脚本太多卡顿！ =============\n")
                del_file.write("\n")
            count_1 += 1
            # if sap_dict[sap]["type"] != "ies" and sap_dict[sap]["type"] != "vprn":
            #     continue
            if sap_dict[sap]["interface"] is None:
                if sap_dict[sap]["content"].strip() != "":
                    del_file.write("/configure service \n")
                    del_file.write(sap_dict[sap]["type_str"] + "\n")
                    del_file.write(sap_dict[sap]["subscriber_interface"] + "\n")
                    del_file.write(sap_dict[sap]["group_interface"] + "\n")
                    del_file.write(self.al_sr_extractor_1.tab * 5 + "sap " + sap + " shutdown" + "\n")
                    del_file.write(self.al_sr_extractor_1.tab * 5 + "no sap " + sap + "\n")
                    del_file.write("\n")
            else:
                if sap_dict[sap]["interface_content"].strip() != "":
                    del_file.write("/configure service \n")
                    del_file.write(sap_dict[sap]["type_str"] + "\n")
                    del_file.write(sap_dict[sap]["interface"] + "\n")
                    del_file.write(self.al_sr_extractor_1.tab * 4 + "sap " + sap + " shutdown" + "\n")
                    del_file.write(self.al_sr_extractor_1.tab * 4 + "no sap " + sap + "\n")
                    del_file.write(str(sap_dict[sap]["interface"]).replace("create", "shutdown") + "\n")

        del_file.close()

        # 生成割接后的脚本
        cutover_file = open(self.save_path + "/" + sr_name + "_割接后.txt", "w")
        count_2 = 1
        ies_group_interface_re = ""
        vprn_group_interface_re=""
        for sap in sap_dict.keys():
            if count_2 % 10 == 0:
                cutover_file.write("================  这里刷一次脚本，避免刷的脚本太多卡顿！ =============\n")
                cutover_file.write("\n")
            count_2 += 1

            if sap_dict[sap]["interface"] is None:
                if sap_dict[sap]["content"].strip() != "":
                    cutover_file.write("/configure service \n")
                    cutover_file.write(sap_dict[sap]["type_str"] + "\n")
                    cutover_file.write(sap_dict[sap]["subscriber_interface"] + "\n")

                    if ies_group_interface_re.strip() == "" and "-" in str(sap_dict[sap]["group_interface"]):
                        ies_group_interface_re = str(sap_dict[sap]["group_interface"]).split()[1].replace("-BF", "").replace("\"","")
                    elif vprn_group_interface_re.strip() == "" and "_" in str(sap_dict[sap]["group_interface"]):
                        vprn_group_interface_re = str(sap_dict[sap]["group_interface"]).split()[1].replace("_BF", "").replace("\"","")
                        print(vprn_group_interface_re)

                    if "-" in str(sap_dict[sap]["group_interface"]).split()[1]:
                        cutover_file.write(str(sap_dict[sap]["group_interface"]).replace(ies_group_interface_re, "JK-LAG-" + str(target_lag)) + "\n")
                    elif "_" in str(sap_dict[sap]["group_interface"]):
                        print("ok")
                        cutover_file.write(str(sap_dict[sap]["group_interface"]).replace(vprn_group_interface_re,
                                                                                         "JK_LAG_" + str(
                                                                                             target_lag)) + "\n")

                    cutover_file.write(str(sap_dict[sap]["content"]).replace(source_lag, "lag-"+str(target_lag)))
                    cutover_file.write("\n")
            

        cutover_file.write("\n")

class SR_cutover_check_tool(object):
    def __init__(self, sw_file, save_path, config_bin=None):

        self.sw_extractor = SW_extractor(sw_file)
        self.save_path = save_path

        al_sr01 = list(self.sw_extractor.sr_lag.keys())[0]
        al_sr02 = list(self.sw_extractor.sr_lag.keys())[1]

        if config_bin is not None:
            with open(config_bin, "rb") as cd:
                config_dict = pickle.load(cd)
        else:
            with open("config.bin", "rb") as cd:
                config_dict = pickle.load(cd)

        self.al_sr_extractor_1 = AL_sr_extractor_v2(al_sr01, config_dict[al_sr01])
        self.al_sr_extractor_2 = AL_sr_extractor_v2(al_sr02, config_dict[al_sr02])

    def get_all_jk_service(self):
        # 处理 SR01
        sr01_lag = self.sw_extractor.sr_lag[self.al_sr_extractor_1.sr_name]
        sr01_ptn_sap = self.get_ptn_sap(self.al_sr_extractor_1.sap_dict, sr01_lag)
        self.write_excel(sr01_ptn_sap, self.al_sr_extractor_1.sr_name + "_ptn")
        sr01_olt_sap = self.get_all_olt_sap(self.al_sr_extractor_1.sap_dict, sr01_lag)
        self.write_excel(sr01_olt_sap, self.al_sr_extractor_1.sr_name + "_olt")
        # 处理 SR02
        sr02_lag = self.sw_extractor.sr_lag[self.al_sr_extractor_2.sr_name]
        sr02_ptn_sap = self.get_ptn_sap(self.al_sr_extractor_2.sap_dict, sr02_lag)
        self.write_excel(sr02_ptn_sap, self.al_sr_extractor_2.sr_name + "_ptn")
        sr02_olt_sap = self.get_all_olt_sap(self.al_sr_extractor_2.sap_dict, sr02_lag)
        self.write_excel(sr02_olt_sap, self.al_sr_extractor_2.sr_name + "_olt")

    def get_ptn_sap(self, sap_dict, lag):
        target_dict = dict()
        for sap in sap_dict.keys():
            if (lag + ":") in str(sap) and str(sap).endswith(".0"):
                target_dict[sap] = sap_dict[sap]
        return target_dict

    def get_all_olt_sap(self, sap_dict, lag):
        target_dict = dict()
        for sap in sap_dict.keys():
            if (lag + ":") in str(sap) and not str(sap).endswith(".0"):
                target_dict[sap] =sap_dict[sap]

        return target_dict

    def write_excel(self, sap_dict, sr_name):
        df = pd.DataFrame()
        count = 0
        type = None
        for sap in sap_dict.keys():
            print(sap)
            svlan = str(sap).split(":")[-1].split(".")[0]
            cvlan = str(sap).split(":")[-1].split(".")[1]
            if sap_dict[sap]["interface_content"].strip() != "":

                target_ips = []
                ips = str(sap_dict[sap]["interface_content"].strip()).split()
                for ip in ips:
                    if isIpV4AddrLegal(ip):
                        target_ips.append(ip)
                type = "独立网关或者VPRN"
            else:
                target_ips = []
                ips = str(sap_dict[sap]["content"].strip()).split()
                for ip in ips:
                    if isIpV4AddrLegal(ip):
                        target_ips.append(ip)
                type = "共享网关"
            ip_str = ",".join(target_ips)
            df.loc[count, "svlan"] = svlan
            df.loc[count, "cvlan"] = cvlan
            df.loc[count, "ip"] = ip_str
            df.loc[count, "业务类型"] = type
            count += 1
        df.to_excel(self.save_path + "/" + sr_name + "_"+ str(int(time.time())) +".xlsx")




