# Created by Ankit.Pal at 26-02-2020

from Mailer import MailDraft
from JiraQuery import JiraConnection
import sys

def main(path_root):
    filter_path = path_root[0]
    filters = read_filter_file(filter_path)

    jira = JiraConnection()

    result = jira.get_filter_set(filters)
    mail_param = dict(read_mail_file(filter_path))
    mailer = MailDraft(mail_param['mail_subject'], mail_param['board_header'], mail_param['recepients'])
    mailer.send_mail(result)

def read_filter_file(file_path):
    filters_file = open(file_path+r'\filters.txt', 'r')
    lines = filters_file.readlines()
    my_dict = {}
    for item in lines:
        k = (item.split('|')[0]).strip()
        v = item.split('|')[1].strip()
        my_dict[k] = v
    filters_file.close()
    return my_dict

def read_mail_file(file_path):
    filters_file = open(file_path+r'\mail_settings.txt', 'r')
    lines = filters_file.readlines()
    my_dict = {}
    for item in lines:
        k = (item.split('|')[0]).strip()
        v = item.split('|')[1].strip()
        my_dict[k]=v
    filters_file.close()
    return my_dict

if __name__ == "__main__":
    main(sys.argv[1:])
    print("Report Generated Successfully!")