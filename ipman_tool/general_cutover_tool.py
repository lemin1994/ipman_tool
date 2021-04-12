class GeneralCutTool(object):
    def __init__(self, service_order_file):
        print(service_order_file)

    def get_over_bngs(self):
        """

        :return: 如果有，则反馈一个数组 为（BNG01:端口，BNG02:端口）
        """
        result_bngs = None

        return result_bngs

    def set_cutover_after_bngs(self, bngs):
        """

        :param bngs: （BNG01:端口，BNG02:端口）
        :return:
        """
        self.bngs = bngs

    def add_new_subnet(self, new_subnet):
        self.new_subnet = new_subnet

