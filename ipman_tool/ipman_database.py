import sqlite3
import threading

class IPManDbHandler(object):
    ## 单例模式
    _instance_lock = threading.Lock()

    def __init__(self):
        if not hasattr(self, "_init_flag"):
            with self._instance_lock:
                if not hasattr(self, "_init_flag"):
                    self._init_flag = True
                    self.conn = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with IPManDbHandler._instance_lock:
                if not hasattr(cls, '_instance'):
                    IPManDbHandler._instance = super().__new__(cls)

        return IPManDbHandler._instance

    def get_db_conn(self, db_connect_file):
        try:
            if self.conn is not None:
                return self.conn
            else:
                self.conn = sqlite3.connect(db_connect_file)

                return self.conn
        except:
            self.conn = None
            return self.conn

    def close_db_conn(self, conn):
        if conn is not None:
            conn.close()

    """ 把所有的sap写进数据库里面 """
    def add_sap_into_db(self, sap_dict, conn, dev_name):
        sql = "insert into sap_dict (dev_sap, service_type, type_num, type_str, subscriber_interface, group_interface,content, sap_interface, interface_content ,sap_status) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        param_list = []
        for sap in sap_dict.keys():
            type = sap_dict[sap]["type"]
            type_num = sap_dict[sap]["type_num"]
            type_str = sap_dict[sap]["type_str"]
            subscriber_interface = sap_dict[sap]["subscriber_interface"] if sap_dict[sap]["subscriber_interface"] is not None else ""
            group_interface = sap_dict[sap]["group_interface"]  if sap_dict[sap]["group_interface"] is not None else ""
            content = sap_dict[sap]["content"]  if sap_dict[sap]["content"] is not None else ""
            interface = sap_dict[sap]["interface"]  if sap_dict[sap]["interface"] is not None else ""
            interface_content = sap_dict[sap]["interface_content"]  if sap_dict[sap]["interface_content"] is not None else ""
            sap_status = sap_dict[sap]["sap_status"] if sap_dict[sap]["sap_status"] is not None else ""
            param_list.append((dev_name+"_"+sap, type, type_num, type_str, subscriber_interface,group_interface, content, interface, interface_content, sap_status))

        conn.executemany(sql,param_list)
        conn.commit()

    def get_sap_dict_with_devname(self, conn, dev_name):

        sap_dict = dict()

        sql ='select dev_sap, service_type, type_num, type_str, subscriber_interface, group_interface,content, sap_interface, interface_content ,sap_status from sap_dict where dev_sap like "%' + dev_name + '%"'

        cursor = conn.cursor()
        cursor.execute(sql)

        result_list = cursor.fetchall()

        for result in result_list:
            dev_sap, service_type, type_num, type_str, subscriber_interface, group_interface,content, sap_interface, interface_content ,sap_status = result
            sap = dev_sap.split("_")[-1]
            subscriber_interface = subscriber_interface if subscriber_interface.strip() != "" else None
            group_interface = group_interface if group_interface.strip() != "" else None
            content = content
            sap_interface = sap_interface if sap_interface.strip() != "" else None
            interface_content = interface_content
            sap_status = sap_status if sap_status.strip() != "" else None

            sap_dict[sap] = dict()
            sap_dict[sap]["type"] = type
            sap_dict[sap]["type_num"] = type_num
            sap_dict[sap]["type_str"] = type_str
            sap_dict[sap]["subscriber_interface"] = subscriber_interface
            sap_dict[sap]["group_interface"] = group_interface
            sap_dict[sap]["content"] = content
            sap_dict[sap]["interface"] = sap_interface
            sap_dict[sap]["interface_content"] = interface_content
            sap_dict[sap]["status"] = sap_status

        return sap_dict

# import Config as config
# import pickle
#
# with open(config.config_cache_file, "rb") as cd:
#     dev_all_dict = pickle.load(cd)
#
# iph = IPManDbHandler()
# conn = iph.get_db_conn(config.db_connect_file)
# for dev in dev_all_dict.keys():
#     if "AL" not in dev:
#         continue
#
#     ase = AL_sr_extractor(None, dev)
#     ase.extract_sr_cutover_information()
#     iph.add_sap_into_db(ase.sap_dict, conn, dev)

