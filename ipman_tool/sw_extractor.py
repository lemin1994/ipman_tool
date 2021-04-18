class SW_extractor(object):
    def __init__(self, sw_config_file):
        config_file = open(sw_config_file)

        self.port_eth_trunk = dict()
        self.eth_trunk_vlan = dict()
        self.sr_lag = dict()
        self.bng_lag = dict()

        port = None
        eth_trunk_port = None

        for config in config_file.readlines():
            # 说明进入接口配置
            # ============= 做好端口和虚拟端口的映射 ============= #
            if "interface GigabitEthernet" in config and config.startswith("interface"):
                port = config.split("GigabitEthernet")[-1].strip()
            elif "interface XGigabitEthernet4" in config and config.startswith("interface"):
                port = config.split("XGigabitEthernet")[-1].strip()


            if port is not None and "eth-trunk" in config:
                eth_trunk = config.split()
                self.port_eth_trunk[port] = eth_trunk[-1]

            # ============= 做好虚拟端口和vlan的映射 ============= #
            if "interface Eth-Trunk" in config and config.startswith("interface"):
                eth_trunk_port = config.split("Eth-Trunk")[-1].strip()

            if eth_trunk_port is not None and "port trunk allow-pass vlan" in config:
                config = config.replace("port trunk allow-pass vlan", "")
                config = config.replace("undo", "")
                vlans = config.split()
                if eth_trunk_port not in self.eth_trunk_vlan.keys():
                    self.eth_trunk_vlan[eth_trunk_port] = list()
                for i in range(len(vlans)):
                    if vlans[i].strip() != "to" and vlans[i].strip() != "":
                        if vlans[i] not in self.eth_trunk_vlan[eth_trunk_port]:
                            self.eth_trunk_vlan[eth_trunk_port].append(vlans[i])
                    elif vlans[i].strip() == "to":
                        start = int(vlans[i - 1])
                        end = int(vlans[i + 1])
                        vlans_range = list(range(start + 1, end + 1))
                        vlans_range = [str(x) for x in vlans_range]
                        self.eth_trunk_vlan[eth_trunk_port].extend(vlans_range)
            # SR 和 LAG
            if "SR" in config and "lag" in config.lower():
                prefix = "GDGZ-MS-IPMAN-"
                info = config.split("GDGZ-MS-IPMAN-")[-1]
                sr_name = "GDGZ-MS-IPMAN-" + "-".join(info.split("-")[0:2]) + "-AL"
                lag = "lag-" + info.split("-")[-1].replace("\n", "")
                if sr_name not in self.sr_lag.keys():
                    self.sr_lag[sr_name] = lag
            # BNG 和 LAG
            if "BNG" in config and "lag" in config.lower():
                prefix = "GDGZ-MS-IPMAN-"
                info = config.split("GDGZ-MS-IPMAN-")[-1]
                bng_name = "GDGZ-MS-IPMAN-" + "-".join(info.split("-")[0:2]) + "-AL"
                lag = "lag-" + info.split("-")[-1].replace("\n", "")
                if bng_name not in self.bng_lag.keys():
                    self.bng_lag[bng_name] = lag
            # 结束
            if "#" in config:
                port = None
                eth_trunk_port = None
                continue
        config_file.close()


# sw_ext = SW_extractor("../信源的配置文件/session.log(XY-SW01)")
# print(sw_ext.sr_lag)