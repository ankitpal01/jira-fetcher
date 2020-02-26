# Created by Ankit.Pal at 26-02-2020

from jira import JIRA
import re

class JiraConnection:
    result_set = {}
    jira = JIRA(
            basic_auth=('jira_username', 'jira_password'), # Provide your jira user credentials here (username,password)
            options={
                'server': 'https://jira.your_organisation.com'  # provide your jira base URL
            }
        )
    def __init__(self):
        print("..............Initializing jira connection..............")


    def get_filter_set(self, jql_query_list, max_results=500): # max_results control the maximum no. of items to be fetched, currently it is set to 500, adjust it as per your requirement
        print("..............Fetching jira issues..............")
        for head,filter in jql_query_list.items():
            self.result_set[head]=(self.jira.search_issues(filter,maxResults=max_results))
            #self.result_set[head] = (self.jira.search_issues(filter, 2))

        return self.result_set
