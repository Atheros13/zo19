from hub.models.hub_user import HubRole

class SeedGenericHubRoles():

    ''' Creates all generic HubRoles for a Hub i.e. Main Contact, Student, Teacher, Parent, Family...
    for a Education Provider. Also contains a method for creating a new role self.create_role(). '''

    def __init__(self, hub, *args, hub_category=None, **kwargs):

        self.hub = hub
        self.role_data = self.build_role_data()

        if hub_category != None:
            if hub_category == 'Education Provider':
                self.seed_education_provider()
            elif hub_category == 'Club':
                self.seed_club()

    def build_role_data(self):

        ''' '''

        data = {
            
            'Main Contact':'',

            'Teacher':'',
            'Student':'',
            'Staff':'',
            'Parent':'',
            'Family':'',

            'Member':'',
            'Player':'',
            
            }
         
        return data

    def create_role(self, name, description, hub=None, requisite_role=None):

        ''' Creates a HubRole object with the name, description and requisite_role (if included)
        date. Saves the objects and returns it as well. '''

        if hub == None:
            hub = self.hub

        hub_role = HubRole(name=name, description=description, hub=hub)
        if requisite_role != None:
            hub_role.requisite_role - requisite_role
        hub_role.save()

        return hub_role

    def create_requisite_roles(roles, requisite_role):

        ''' Creates one or more HubRoles from a list of lists called role
        i.e. [[name, description]] and links it with a previously created requisite_role HubRole'''

        for role in roles:
            self.create_role(role[0], role[1], requisite_role=requisite_role)

    def seed_main_contact(self):

        ''' Create and return the Main Contact HubRole. '''

        self.main_contact = self.create_role('Main Contact', self.role_data['Main Contact'])

    def seed_education_provider(self):

        ''' Create the generic HubRoles for an Education Provider, including the roles which are 
        requisite linked to the Student role. '''

        self.seed_main_contact()
        for role in ['Teacher', 'Staff']:
            self.create_role(role, self.role_data[role])

        student = self.create_role('Student', self.role_data['Student'])
        roles = []
        for role in ['Parent', 'Family']:
            roles.append([role, self.role_data[role]])
        self.create_requisite_roles(roles, student)

    def seed_club(self):

        ''' Create the generic HubRoles for a Club. '''

        self.seed_main_contact()

        member = self.create_role('Member', self.role_data['Member'])
        roles = []
        for role in ['Family']:
            roles.append([role, self.role_data[role]])
        self.create_requisite_roles(roles, member)        


