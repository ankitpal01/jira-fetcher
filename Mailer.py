# Created by Ankit.Pal at 26-02-2020

from JiraQuery import JiraConnection
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

class MailDraft:
    me = "mail_sender@your_organisation.com" # provide the sender mailing address
    you = []
    recepient_list = []
    mail_subject = ""
    table_heading = ""
    usr_set = ()

    def __init__(self,mail_subject,table_heading, recepient_list):
        print("..............Initializing mailer..............")
        recepients = recepient_list.split(';')

        for arg in recepients:
            self.you.append(arg)
        #print (self.you)
        self.recepient_list = recepients
        self.mail_subject = mail_subject
        self.table_heading = table_heading

    def send_mail(self, result_set):
        print("..............Sending email notification..............")
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.mail_subject
        msg['From'] = self.me
        msg['To'] = ",".join(self.you)

        # Create the body of the message (a plain-text and an HTML version).
        html = """\
                <html>
                  <head></head>
                  <body>
                    <p>Hi All,<br><br>
                       Please find today's JIRA Snapshot below:
                    </p>
                <style type="text/css">
                .bn {text-align:left;color:#FFFFFF;font-family:Arial, sans-serif;background-color:#000A57;}
                .bns {font-size:13px;text-align:left;color:#FFFFFF;font-family:Arial, sans-serif;background-color:#000A57;}
                .tg  {border-collapse:collapse;border-spacing:0;border-color:#999;}
                .tm  {padding-left:5px}
                .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#999;color:#444;background-color:#E4E8F2;text-align:center;}
                .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:0px;overflow:hidden;word-break:normal;border-color:#999;color:#fff;background-color:#000A57;}
                .tg .tg-yw4l{vertical-align:center; text-align:center}
                .tg .tg-yw42{vertical-align:center; text-align:left}
                .tg .tg-yw43{vertical-align:center; text-align:center; color:red}
                </style>
                <h1 align="center"><u>JIRA Snapshot</u></h1>
                <h2 align="center"><u>"""+self.table_heading+"""</u></h2>
                    <table width="100%" border="2" cellpadding="0" cellspacing="0" float="left" bordercolor="#000863">
                        <tr>
                            <td>""" +  self.prepare_table(result_set) + """
                            </td>
                        </tr>
                    </table>
                    <p><i>This is an auto generated email</i></p>
                    <br>
                    <br>
                    <p>Thanks,<br>
                       Ankit Pal<br>
                    </p>
                  </body>
                </html>
                """


        part2 = MIMEText(html, 'html')

        msg.attach(part2)

        # Send the message via local SMTP server.
        s = smtplib.SMTP('smtp.your_organisation.com') # provide your SMTP server here

        s.sendmail(self.me, self.you, msg.as_string())
        s.quit()

	
	#	fetch_issue_fields method controls the data in the table columns in the output report. You can change these as per your requirement. In case of additional fields you might need to refer to JIRA APIs. 
	
    def fetch_issue_fields(self, result_set):
        print("..............Fetching jira fields..............")
        issue_list = ""
        serialNo = 1
        for issue in result_set:
            issue_list = issue_list + ("""<tr>
                   <td class="tg-yw41">""" + str(serialNo) + """</td>            
                   <td class="tg-yw4l" ><a href="https://jira.your_organisation.com/browse/""" +str(issue.key)+"""   "> """ + str(issue.key) + """</a></td> 
                   <td class="tg-yw42">""" + str(issue.fields.summary) + """</td>
                   <td class="tg-yw4l">""" + str(issue.fields.status) + """</td>
                    <td class="tg-yw4l">""" + str(issue.fields.priority) + """</td>
                    <td class="tg-yw4l">""" + str(issue.fields.issuetype) + """</td>
                   <td class="tg-yw4l">""" + str(self.setUnassignedUser(issue.fields.assignee)) + """</td>
                   <td class="tg-yw4l">""" + str(issue.fields.creator) + """</td>
                    <td class="tg-yw4l">""" + str(issue.fields.updated)[:10] + """</td>
                 </tr>""")
            serialNo +=1
        return issue_list

	#	prepare_table method controls the name of the table columns in the output report. You can change these as per your requirement. 
    def prepare_table(self, result_set):
        tables = ""
        for k,v in result_set.items():
            tables = tables + """                
                <table border="1" width="100%" border="1" cellpadding="0" cellspacing="0" class="tg" float="left">
                    <caption class="bn"> <i> <h3> Criteria: """+ k +"""<span class="bns">	&nbsp;&nbsp;	(Total Items: """+str(len(v))+""")</span></h3></i></caption>    
                    <tr>
                        <th class="tg-yw4l">#</th>
                        <th class="tg-yw4l">JiraID</th>
                        <th class="tg-yw4l">Summary</th>
                        <th class="tg-yw4l">Status</th>
                        <th class="tg-yw4l">Priority</th>
                        <th class="tg-yw4l">Issue Type</th>
                        <th class="tg-yw4l">Assignee</th>
                        <th class="tg-yw4l">Reported By</th>
						<th class="tg-yw4l">Last Updated <br>(yyyy/mm/dd)</th>
                    </tr> """ + self.fetch_issue_fields(v) + """          
                </table>
                <br><br>
            """
        return tables

    def get_sprint_no(self, sprint_list):
        refined_list = []
        initial = ",name="
        terminate = ",startDate="
        if sprint_list is not None:
            for item in sprint_list:
                strt = (item.find(initial))
                strt = strt + len(initial)
                end = (item.find(terminate))
                refined_list.append(item[strt:end])
        return refined_list

    def setUnassignedUser(self, usr):
        if usr is None:
            return 'Unassigned'
        else:
            return usr

    def handle_null_field(self, fld):
        if fld is None:
            return ''
        else:
            return fld

    def listListValues(self, lst):
        str_lst =""
        for item in lst:
            str_lst = str_lst + str(item) + ", "
        return  str_lst

    def getUniqueUsers(self, result_set):
        users = set()
        for issue in result_set:
            is_validUser = issue.fields.assignee
            if is_validUser is None:
                users.add("Unassigned")
            else:
                users.add(is_validUser.displayName)

        return users