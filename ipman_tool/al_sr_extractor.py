class AL_sr_extractor(object):
    def __init__(self, sr_config_file, tab_num=4):

        self.sr_name = None

        file = open(sr_config_file)

        tab = " " * tab_num
        self.tab = tab
        start_flag = False

        sap_dict = dict()

        sap = None
        type = None
        type_num = None
        type_str = None
        subscriber_interface = None
        group_interface = None
        content = ""
        interface = None
        interface_content = ""
        # gateway_address = None

        sap_flag = False
        sap_status = "open"
        count = 0
        for cmd_line in file.readlines():
            count += 1
            if cmd_line.startswith(tab * 2 + "name"):
                self.sr_name = str(cmd_line.strip().split()[1].replace("\"", ""))
            cmd_line = cmd_line.replace("\n", "")
            # 设置开始解析业务脚本
            if cmd_line.startswith(tab + "service"):
                start_flag = True
            # 可以开始了
            if start_flag:
                if cmd_line.startswith(tab * 2) and cmd_line[tab_num * 2 + 1] != " " and cmd_line.strip() != "exit":
                    type_str = cmd_line
                    type = cmd_line.strip().split()[0]
                    type_num = cmd_line.strip().split()[1]
                if cmd_line.startswith(tab * 3) and cmd_line[tab_num * 3 + 1] != " " and cmd_line.strip() != "exit":
                    # 不是共享网关的情况下
                    if cmd_line.startswith(tab * 3 + "interface"):
                        subscriber_interface = None
                        interface = cmd_line

                    elif cmd_line.startswith(tab * 3 + "subscriber-interface"):
                        interface = None
                        subscriber_interface = cmd_line
                # 处理独立网关和vpn
                if cmd_line.startswith(tab * 4) and cmd_line[tab_num * 4 + 1] != " " and interface is not None:
                    if cmd_line.strip().startswith("shutdown"):
                        sap_status = "shutdown"
                    interface_content = interface_content + cmd_line + "\n"
                    # print(interface_content)
                    if cmd_line.startswith(tab * 4 + "sap"):
                        sap = str(cmd_line.strip().split()[1])
                    # if cmd_line.startswith(tab * 4 + "address"):
                    #     gateway_address = cmd_line.strip().split()[-1]
                    #     print(gateway_address)
                    if cmd_line.strip() == "exit" and sap is not None:
                        sap_dict[sap] = dict()
                        sap_dict[sap]["type"] = type
                        sap_dict[sap]["type_num"] = type_num
                        sap_dict[sap]["type_str"] = type_str
                        sap_dict[sap]["subscriber_interface"] = subscriber_interface
                        sap_dict[sap]["group_interface"] = group_interface
                        sap_dict[sap]["content"] = content
                        sap_dict[sap]["interface"] = interface
                        sap_dict[sap]["interface_content"] = interface_content
                        sap_dict[sap]["sap_status"] = sap_status

                        sap_status = "open"
                        interface = None
                        interface_content = ""
                # 处理非独立网关
                if cmd_line.startswith(tab * 4) and cmd_line[
                    tab_num * 4 + 1] != " " and subscriber_interface is not None:
                    if cmd_line.startswith(tab * 4 + "group-interface") or cmd_line.strip().startswith(
                            "group-interface"):
                        group_interface = cmd_line
                if group_interface is not None and subscriber_interface is not None and cmd_line.strip().startswith(
                        "sap"):
                    sap_flag = True
                    sap = str(cmd_line.strip().split()[1])

                # sap 结束
                if group_interface is not None and subscriber_interface is not None and cmd_line.startswith(
                        tab * 5 + "exit") and sap is not None:
                    content += cmd_line
                    # print(content)

                    sap_dict[sap] = dict()
                    sap_dict[sap]["type"] = type
                    sap_dict[sap]["type_num"] = type_num
                    sap_dict[sap]["type_str"] = type_str
                    sap_dict[sap]["subscriber_interface"] = subscriber_interface
                    sap_dict[sap]["group_interface"] = group_interface
                    sap_dict[sap]["content"] = content
                    sap_dict[sap]["interface"] = interface
                    sap_dict[sap]["interface_content"] = interface_content
                    sap_dict[sap]["sap_status"] = sap_status

                    sap_status = "open"
                    content = ""
                    sap = None
                    sap_flag = False
                if group_interface is not None and cmd_line.startswith(tab * 4 + "exit"):
                    group_interface = None
                if subscriber_interface is not None and cmd_line.startswith(tab * 3 + "exit"):
                    subscriber_interface = None
                if sap_flag:
                    if cmd_line.startswith(tab * 6 + "shutdown"):
                        sap_status = "shutdown"
                    content += cmd_line + "\n"

            if start_flag and cmd_line.startswith(tab + "exit"):
                break

            # 设置获取
        self.sap_dict = sap_dict
        file.close()

class AL_sr_extractor_v2(object):
    def __init__(self, sr_name, sr_config, tab_num=4):
        self.sr_name=  sr_name

        tab = " " * tab_num
        self.tab = tab
        start_flag = False

        "sap : {type, type_num, subscriber_interface, group_interface, content, interface, interface_content, gateway_address}"
        sap_dict = dict()

        sap = None
        type = None
        type_num = None
        type_str = None
        subscriber_interface = None
        group_interface = None
        content = ""
        interface = None
        interface_content = ""
        # gateway_address = None

        sap_flag = False
        sap_status = "open"
        count = 0
        for cmd_line in sr_config.split("\n"):
            count += 1
            # cmd_line = cmd_line.replace("\n", "")
            # 设置开始解析业务脚本
            if cmd_line.startswith(tab + "service"):
                start_flag = True
            # 可以开始了
            if start_flag:
                if cmd_line.startswith(tab * 2) and cmd_line[tab_num * 2 + 1] != " " and cmd_line.strip() != "exit":
                    type_str = cmd_line
                    type = cmd_line.strip().split()[0]
                    type_num = cmd_line.strip().split()[1]
                if cmd_line.startswith(tab * 3) and cmd_line[tab_num * 3 + 1] != " " and cmd_line.strip() != "exit":
                    # 不是共享网关的情况下
                    if cmd_line.startswith(tab * 3 + "interface"):
                        subscriber_interface = None
                        interface = cmd_line

                    elif cmd_line.startswith(tab * 3 + "subscriber-interface"):
                        interface = None
                        subscriber_interface = cmd_line
                # 处理独立网关和vpn
                if cmd_line.startswith(tab * 4) and cmd_line[tab_num * 4 + 1] != " " and interface is not None:
                    if cmd_line.strip().startswith("shutdown"):
                        sap_status = "shutdown"
                    interface_content = interface_content + cmd_line + "\n"
                    # print(interface_content)
                    if cmd_line.startswith(tab * 4 + "sap"):
                        sap = str(cmd_line.strip().split()[1])
                    # if cmd_line.startswith(tab * 4 + "address"):
                    #     gateway_address = cmd_line.strip().split()[-1]
                    #     print(gateway_address)
                    if cmd_line.strip() == "exit" and sap is not None:
                        sap_dict[sap] = dict()
                        sap_dict[sap]["type"] = type
                        sap_dict[sap]["type_num"] = type_num
                        sap_dict[sap]["type_str"] = type_str
                        sap_dict[sap]["subscriber_interface"] = subscriber_interface
                        sap_dict[sap]["group_interface"] = group_interface
                        sap_dict[sap]["content"] = content
                        sap_dict[sap]["interface"] = interface
                        sap_dict[sap]["interface_content"] = interface_content
                        sap_dict[sap]["sap_status"] = sap_status

                        sap_status = "open"
                        interface = None
                        interface_content = ""
                # 处理非独立网关
                if cmd_line.startswith(tab * 4) and cmd_line[
                    tab_num * 4 + 1] != " " and subscriber_interface is not None:
                    if cmd_line.startswith(tab * 4 + "group-interface") or cmd_line.strip().startswith(
                            "group-interface"):
                        group_interface = cmd_line
                if group_interface is not None and subscriber_interface is not None and cmd_line.strip().startswith(
                        "sap"):
                    sap_flag = True
                    sap = str(cmd_line.strip().split()[1])

                # sap 结束
                if group_interface is not None and subscriber_interface is not None and cmd_line.startswith(
                        tab * 5 + "exit") and sap is not None:
                    content += cmd_line
                    # print(content)

                    sap_dict[sap] = dict()
                    sap_dict[sap]["type"] = type
                    sap_dict[sap]["type_num"] = type_num
                    sap_dict[sap]["type_str"] = type_str
                    sap_dict[sap]["subscriber_interface"] = subscriber_interface
                    sap_dict[sap]["group_interface"] = group_interface
                    sap_dict[sap]["content"] = content
                    sap_dict[sap]["interface"] = interface
                    sap_dict[sap]["interface_content"] = interface_content
                    sap_dict[sap]["sap_status"] = sap_status

                    sap_status = "open"
                    content = ""
                    sap = None
                    sap_flag = False
                if group_interface is not None and cmd_line.startswith(tab * 4 + "exit"):
                    group_interface = None
                if subscriber_interface is not None and cmd_line.startswith(tab * 3 + "exit"):
                    subscriber_interface = None
                if sap_flag:
                    if cmd_line.startswith(tab * 6 + "shutdown"):
                        sap_status = "shutdown"
                    content += cmd_line + "\n"

            if start_flag and cmd_line.startswith(tab + "exit"):
                break

            # 设置获取
        self.sap_dict = sap_dict


