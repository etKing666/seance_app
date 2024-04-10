from diagrams import Diagram, Edge
from diagrams.c4 import Container, Database, SystemBoundary, Relationship
from diagrams.generic.network import Router, Firewall
from diagrams.onprem.client import User, Users
from .helpers import answers
from dataclasses import dataclass


@dataclass
class Param:
    """
    A dataclass to hold the parameters for the DFD
    """
    multi_admin: bool = False
    employee: bool = False
    multi_employee: bool = False
    remote_employee: bool = False
    multi_computer: bool = False
    onprem_setup: bool = False
    cloud_setup: bool = False
    saas: bool = False
    iot: bool = False
    hosted_webapp: bool = False
    remote_webapp: bool = False
    waf: bool = False
    wifi_share: bool = False
    firewall: bool = False
    website: bool = False

param = Param()

def update_dfd(qid, response):
    """
    Captures the parameters for the DFD
    """
    qid = int(qid)


    if qid == 10400:
        if response == "No":
            param


    if answers.layer1["10400"][0] == "No":  # Checks if there are multiple admins
        param.multi_admin = True

    if int(answers.layer2["20100"][0]) == 1:  # Checks if there is only one employee
        param.employee = True
    elif int(answers.layer2["20100"][0]) > 1:  # Checks if there are multiple employees
        param.multi_employee = True
    else:  # Means that there are no employees other than the admin
        pass

    if answers.layer2["20200"][0] == "Yes":  # Checks if there are remote employees
        param.remote_employee = True

    if int(answers.layer3["30100"][0]) > 1:  # Checks if there are multiple computers
        param.multi_computer = True

    if answers.layer3["30300"][0] == "Yes":  # Checks if there is a server within company trust boundaries
        param.onprem_setup = True

    if answers.layer3["30400"][0] == "Yes":  # Checks if there is a server within cloud service provider trust boundaries
        param.cloud_setup = True

    if answers.layer3["30500"][0] == "Yes":  # Checks if the business is using a SaaS product
        param.saas = True

    if answers.layer3["30600"][0] == "Yes":  # Checks if the business is using an IoT device
        param.iot = True

    if answers.layer5["50300"][0] == "Yes":  # Checks if the customers are able to connect to the internal Wi-Fi network
        param.wifi_share = True

    if answers.layer6["60100"][0] == "Yes":  # Checks if the business has a firewall in place
        param.firewall = True

    if answers.layer["31900"][0] == "Yes":  # Checks if the business has a website
        param.website = True

    if param.website:  # If question 30900 is answered "No", subsequent questions will not be asked
        if answers.layer3["31901"][0] == "Yes":  # Checks if the business website is hosted remotely
            param.remote_webapp = True
        else:
            param.hosted_webapp = True
        if answers.layer3["31903"][0] == "Yes":  # Checks if the business has a WAF in place
            """
            The following conditions are checked:
            - If the business has a web application hosted in a cloud server, a WAF will be displayed within the cloud
            service provider's trust boundaries.
            - If te business doesn't have a web application facing customers, but still uses cloud services (incl. data
            store, etc.), a  WAF will be displayed within the cloud service provider's trust boundaries.
            - If the business doesn't have a cloud server or web app hosted in the cloud, 
            only a firewall will be displayed within business trust boundaries.
             
            """
            if param.remote_webapp:
                param.waf = True
            elif param.cloud_setup:
                param.waf = True
            else:
                param.firewall = True

def create_dfd():
    """
    Create the DFD based on the user's answers
    """

    graph_attr = {
        "splines": "spline",
    }

    with Diagram("Data Flow Diagram of your business", direction="LR", graph_attr=graph_attr):
        with SystemBoundary("Business"):
            if param.multi_admin:
                admin = Users("Business Admins")
            else:
                admin = User("Business Admin")

            admin_computer = Container(
                name="Admin Computer(s)",
                technology="Win/MacOS/Linux",
                description="The workstation(s) that is/are used to configure business assets. The services "
                            "run require admin privileges.",
            )

            if param.employee:
                employee = User("Employee")
            elif param.multi_employee:
                employee = Users("Employees")
            else:
                pass  # Meaning that there are no employees other than the admin

            if param.multi_computer:
                regular_computer = Container(
                    name="Computer(s)",
                    technology="Win/MacOS/Linux",
                    description="The workstations that are used by employees for day-to-day business operations",
                )

            if param.iot:
                iot = Container(
                    name="IoT Device(s)",
                    technology="Self-service terminal, etc.",
                    description="Provides various functions for employees and customers.",
                )

            if param.onprem_setup or param.hosted_webapp:
                prem_server = Container(
                    name="On-premise Server",
                    technology="Various tech.",
                    description="",
                )

                prem_database = Database(
                    name="On-premise Data Store",
                    technology="Various tech.",
                    description="Stores business data",
                )

            with SystemBoundary(" "):
                router = Router("Router")

                if param.firewall:
                    firewall = Firewall("Firewall")

        if param.cloud_setup or param.remote_webapp:
            with SystemBoundary("Cloud Service Provider"):
                cloud_server = Container(
                    name="Web Server",
                    technology="Various tech.",
                    description="",
                )

                cloud_database = Database(
                    name="Data Store",
                    technology="Various tech.",
                    description="Stores business data",
                )
                if param.waf:
                    waf = Firewall("WAF")

        if param.saas:
            with SystemBoundary("SaaS"):
                saas = Container(
                    name="SaaS",
                    technology="Google Workspace, Microsoft 365, etc.",
                    description="Software as a Service solutions",
                )

        customer = User("Customer")

        if param.remote_employee:
            remote_employee = User("Remote Employee")

        #  Edges
        admin - Relationship("Manages business/servers/data using") - admin_computer

        if param.website:
            if param.hosted_webapp:
                customer - Relationship("Visits business website") - router
            if param.remote_webapp:
                if param.waf:
                    customer - Relationship("Visits business website") - waf
                else:
                    customer - Relationship("Visits business website") - cloud_server

        if param.employee or param.multi_employee:
            customer - Relationship("Requests for service") - employee
            if param.multi_computer:
                employee - Relationship("Serves customers using") - regular_computer

        if param.firewall:
            admin_computer - Relationship("") - firewall
            router - Relationship("") - firewall
            if param.multi_computer:
                regular_computer - Relationship("") - firewall
            if param.iot:
                iot - Relationship("") - firewall
            if param.onprem_setup:
                prem_server - Relationship("") - firewall
        else:
            admin_computer - Relationship("") - router
            if param.multi_computer:
                regular_computer - Relationship("") - router
            if param.iot:
                iot - Relationship("") - router
            if param.onprem_setup:
                prem_server - Relationship("") - router

        if param.onprem_setup:
            admin_computer - Relationship("") - prem_server
            prem_server - Relationship("Reads from and writes to") - prem_database
            if param.multi_computer:
                regular_computer - Relationship("") - prem_server

        if param.saas:
            router - Relationship("") - saas

        if param.wifi_share:
            customer - Relationship("Connects to Wi-Fi") - router

        if param.cloud_setup or param.hosted_webapp:
            cloud_server - Relationship("Reads from and writes to") - cloud_database
            if param.waf:
                waf - Relationship("") - cloud_server
                router - Relationship("") - waf
            else:
                router - Relationship("") - cloud_server

        if param.remote_employee:
            if param.onprem_setup:
                remote_employee - Relationship("Accesses business resources") - router
            if param.cloud_setup:
                if param.waf:
                    remote_employee - Relationship("Accesses business resources") - waf
                else:
                    remote_employee - Relationship("Accesses business resources") - cloud_server

    return