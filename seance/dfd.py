"""The classes and functions used to create a Data Flow Diagram (DFD).

This module uses diagrams package (https://pypi.org/project/diagrams/) to create a DFD based on the user's answers. It
includes a dataclass and two functions that are used to create a DFD.

Classes:
--------
Param: The dataclass which holds the parameters for the DFD. It also has a reset() method which is designed to reset
the instantiated Param object to its original state.

Functions:
----------
update_dfd():  A function which captures the parameter for the DFD. It stores the parameters to the Param object.

create_dfd():  The function which creates the DFD using the parameters stored in the Param object.

Imports:
--------
diagrams:  The Python package that is used to create the DFD. More info: https://pypi.org/project/diagrams/

dataclasses:  Dataclasses are used in defining dataclasses instead of regular classes for
              simplicity.

"""


from diagrams import Diagram, Edge
from diagrams.c4 import Container, Database, SystemBoundary, Relationship
from diagrams.generic.network import Router, Firewall
from diagrams.onprem.client import User, Users
from dataclasses import dataclass


@dataclass
class Param:
    """ A dataclass to hold the parameters for the DFD.

    Attributes:
    ----------
    multi_admin: bool
        A boolean to indicate if the organisation has multiple admins or not.
    employee: bool
        A boolean to indicate if the organisation has exactly one employee.
     multi_employee: bool
        A boolean to indicate if the organisation has multiple employees or not.
    remote_employee: bool
        A boolean to indicate if the has remote employees or not.
    multi_computer: bool
        A boolean to indicate if the organisation has multiple computers or not.
    onprem_setup: bool
        A boolean to indicate if the organisation has an on-premises server in place.
    cloud_setup: bool
        A boolean to indicate if the organisation uses cloud services or not.
    saas: bool
        A boolean to indicate if the organisation uses SaaS solutions or not.
    iot: bool
        A boolean to indicate if the organisation uses IoT or not.
    hosted_webapp: bool
        A boolean to indicate if the organisation has a website that is hosted on on-premises servers.
    remote_webapp: bool
        A boolean to indicate if the organisation has a website that is hosted on remote servers.
    waf: bool
        A boolean to indicate if the organisation has a WAF in place or not.
    wifi_share: bool
        A boolean to indicate if the organisation shares the Wi-Fi connection with their customers or not.
    firewall: bool
        A boolean to indicate if the organisation has a firewall in place or not.
    website: bool
        A boolean to indicate if the organisation has a website or not.

    Methods:
    --------
    reset():  Resets the instantiated Param object to its original state.
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

    def reset(self):
        self.__init__()


param = Param()


def update_dfd(qid, response):
    """ Captures the parameters for the DFD. """
    qid = int(qid)

    if qid == 10400:
        if response == "No":
            param.multi_admin = True
    elif qid == 20100:
        if int(response) == 1:
            param.employee = True
        elif int(response) > 1:
            param.multi_employee = True
        else:  # Means that there are no employees other than the admin
            pass
    elif qid == 20200:
        if response == "Yes":
            param.remote_employee = True
    elif qid == 30100:
        if int(response) > 1:
            param.multi_computer = True
    elif qid == 30300:
        if response == "Yes":
            param.onprem_setup = True
    elif qid == 30400:
        if response == "Yes":
            param.cloud_setup = True
    elif qid == 30500:
        if response == "Yes":
            param.saas = True
    elif qid == 30600:
        if response == "Yes":
            param.iot = True
    elif qid == 50300:
        if response == "Yes":
            param.wifi_share = True
    elif qid == 60100:
        if response == "Yes":
            param.firewall = True
    elif qid == 31900:
        if response == "Yes" or response == "IDK":  # Because it is most likely that website is hosted remotely
            param.website = True
    elif qid == 31901:
        if response == "Yes" or response == "IDK":  # Because it is most likely that website is hosted remotely:
            param.remote_webapp = True
        else:
            param.hosted_webapp = True
    elif qid == 31903:
        if response == "Yes":
            if param.remote_webapp:
                param.waf = True
            elif param.cloud_setup:
                param.waf = True
            else:
                param.firewall = True

def create_dfd(filename):
    """ Creates the DFD based on the user's answers. """

    filename = "media/" + filename

    graph_attr = {
        "splines": "spline",
    }

    with Diagram("", direction="LR", graph_attr=graph_attr, show=False, filename=filename):
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
                    technology="Google Workspace, etc.",
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
            employee - Relationship("") - admin
            if param.multi_computer:
                employee - Relationship("Serves customers using") - regular_computer
            else:
                employee - Relationship("Serves customers using") - admin_computer
        else:
            customer - Relationship("Requests for service") - admin

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

        if param.cloud_setup or param.remote_webapp:
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
