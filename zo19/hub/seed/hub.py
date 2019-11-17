from hub.models.hub_user import HubRole

class SeedGenericHubRoles():

    ''' Creates all generic HubRoles for a Hub i.e. Main Contact, Student, Teacher, Parent, Family...
    for a Education Provider. '''

    def __init__(self, hub, *args, **kwargs):

        self.hub = hub


    def main_contact(self):

        hub_role = HubRole(name="Main Contact", 
                           hub=self.hub)

    def education_provider(self):

        pass

