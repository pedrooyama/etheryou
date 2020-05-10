import datetime
import os

from business.user_manager import UserManager
from model.message_type import MessageType
from parameters.config import Config
from parameters.constants import Constants


class Parameters:
    MAX_NUMBER_OF_RECIPIENTS = 200
    REPORT_PATH = Config.experiments_output_directory
    REPORT_NAME = 'gas_x_number_of_recipients'
    REPORT_FORMAT = 'csv'
    REPORT_SEPARATOR = ';'
    REPORT_DATE_FORMAT = '%Y.%m.%d-%H.%M.%S'
    MESSAGE = '!"#$%&\'()*+-,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~ '


def generate_public_key() -> str:
    return Constants.PUBLIC_KEY_ALGORITHM().generate_random_key_pair().public_key.to_bytes().hex()


if __name__ == "__main__":

    # Creating directory if necessary
    if not os.path.exists(Parameters.REPORT_PATH):
        os.makedirs(Parameters.REPORT_PATH)

    # Creating report file
    now = datetime.datetime.now().strftime(Parameters.REPORT_DATE_FORMAT)
    filename = Parameters.REPORT_PATH + Parameters.REPORT_NAME +'__' + now + '__.' + Parameters.REPORT_FORMAT
    file = open(filename, "x")
    file.write("%s%s%s%s%s" % ('# of recipients', Parameters.REPORT_SEPARATOR, 'Gas used', Parameters.REPORT_SEPARATOR, 'Block Length\n'))
    print("%s%s%s%s%s" % ('# of recipients', Parameters.REPORT_SEPARATOR, 'Gas used', Parameters.REPORT_SEPARATOR, 'Block Length\n'))

    user_manager = UserManager()
    user_manager.create_user_with_ether(9999)

    recepients = []
    for i in range(Parameters.MAX_NUMBER_OF_RECIPIENTS):
        recepients.append(generate_public_key())
        _, gas, block_length = user_manager.send_message(message_type=MessageType.DIRECT_MESSAGE, message=Parameters.MESSAGE, recipients=recepients)
        file.write("%d%s%d%s%d\n" % (i+1, Parameters.REPORT_SEPARATOR, gas, Parameters.REPORT_SEPARATOR, block_length))
        print("%d%s%d%s%d" % (i+1, Parameters.REPORT_SEPARATOR, gas, Parameters.REPORT_SEPARATOR, block_length))

    file.close()
