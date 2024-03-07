![](https://www.ansible.com/hubfs/RedHat-Ansible-Automation-Platform_logo-white-1.png) ![](https://fj.com.br/wp-content/uploads/2017/03/Suporte-Zabbix-1024x576.webp)


# Integrated solutions:
- RedHat Ansible Automation Plataform
- Zabbix Server
- Python Script

## Operation:
> Python Script scheduled for read API Ansible Automation Platform and send Zabbix Trappers.

## Configuration:
Create two items on Zabbix Server ( Zabbix Trapper):
```
Name Item: Status Last Job
key: jobs.status

Name Item: Stdout Last Jobs
key: jobs.stdout
```

Set script python on crontab linux:
```
*/5 * * * * python3 /PATH/api_rhel_ansibleAutomation2Zabbbix.py
```

Set variables on the python script, for Zabbix Server endpoint:
```
 zabbix_url = '<ENDPOINT>'
 username   = '<USERNAME>'
 password   = '<PASSWORD>' 
```

Set variables on the python script, for Ansible Automation Plataform endpoint:
```
tower_base_url = '<ENDPOINT>'
tower_username = '<USERNAME>'
tower_password = '<PASSWORD>'
```

## Zabbix Items(GUI) - Type Zabbix Trapper:
![](https://github.com/tsleite/integrations/blob/master/img/items.png)
## Zabbix Latest data (GUI) - Details Errors:
![](https://github.com/tsleite/integrations/blob/master/img/lastest_data.png)
