import datetime
import os
import random
from business.user_manager import UserManager
from model.message_type import MessageType
from parameters.config import Config


class Parameters:
    MAX_MESSAGE_LENGTH = 2000
    REPORT_PATH = Config.experiments_output_directory
    REPORT_NAME = 'gas_x_message_length'
    REPORT_FORMAT = 'csv'
    REPORT_SEPARATOR = ';'
    REPORT_DATE_FORMAT = '%Y.%m.%d-%H.%M.%S'
    MESSAGE = '!"#$%&\'()*+-,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ '


def generate_random_char() -> str:
    random_index = random.randint(0, len(Parameters.MESSAGE)-1)
    return Parameters.MESSAGE[random_index]


if __name__ == "__main__":

    # Creating directory if necessary
    if not os.path.exists(Parameters.REPORT_PATH):
        os.makedirs(Parameters.REPORT_PATH)

    # Creating report file
    now = datetime.datetime.now().strftime(Parameters.REPORT_DATE_FORMAT)
    filename = Parameters.REPORT_PATH + Parameters.REPORT_NAME +'__' + now + '__.' + Parameters.REPORT_FORMAT
    file = open(filename, "x")
    file.write("%s%s%s%s%s" % ('Message length', Parameters.REPORT_SEPARATOR, 'Gas used', Parameters.REPORT_SEPARATOR, 'Block Length\n'))
    print("%s%s%s%s%s" % ('Message length', Parameters.REPORT_SEPARATOR, 'Gas used', Parameters.REPORT_SEPARATOR, 'Block Length\n'))

    user_manager = UserManager()
    user_manager.create_user_with_ether(9999)

    message = ''
    for i in range(Parameters.MAX_MESSAGE_LENGTH):
        message += generate_random_char()
        _, gas, block_length = user_manager.send_message(message_type=MessageType.PUBLIC_POST, message=message, recipients=[])
        file.write("%d%s%d%s%d\n" % (i+1, Parameters.REPORT_SEPARATOR, gas, Parameters.REPORT_SEPARATOR, block_length))
        print("%d%s%d%s%d" % (i+1, Parameters.REPORT_SEPARATOR, gas, Parameters.REPORT_SEPARATOR, block_length))

    file.close()
