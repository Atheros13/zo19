from hub.models.hub_user import HubRole

class SeedGenericHubRoles():

    ''' Creates all generic HubRoles for a Hub i.e. Main Contact, Student, Teacher, Parent, Family...
    for a Education Provider. Also contains a method for creating a new role self.create_role(). '''

    def __init__(self, hub, *args, hub_category=None, **kwargs):

        self.hub = hub
        self.data = self.build_data()

        if hub_category != None:
            if hub_category == 'Education Provider':
                self.seed_education_provider()
            elif hub_category == 'Club':
                self.seed_club()

    ## BUILD

    def build_data(self):

        ''' '''

        data = {
            
            'Main Contact':'',
            'Hub Admin':'',

            'Teacher':'',
            'Student':'',
            'Staff':'',
            'Parent':'',
            'Family':'',

            'Member':'',
            'Player':'',
            
            }
         
        return data

    ## CREATE

    def create_role(self, name, description, hub=None, requisite_role=None):

        ''' Creates a HubRole object with the name, description and requisite_role (if included)
        data. Saves the objects and returns it as well. '''

        if hub == None:
            hub = self.hub

        hub_role = HubRole(name=name, description=description, hub=hub)
        if requisite_role != None:
            hub_role.requisite_role = requisite_role
        hub_role.save()

        return hub_role

    def create_requisite_roles(self, role_list, requisite_role):

        ''' Creates one or more HubRoles from a list of lists called role
        i.e. [[name, description]] and links it with a previously created requisite_role HubRole'''

        for roles in role_list:
            self.create_role(roles[0], roles[1], requisite_role=requisite_role)

    ## SEED 

    def seed_main_contact_admin(self):

        ''' Create Hub Admin and Create and return the Main Contact HubRole. '''

        self.create_role('Hub Admin', self.data['Hub Admin'])
        self.main_contact = self.create_role('Main Contact', self.data['Main Contact'])

    def seed_education_provider(self):

        ''' Create the generic HubRoles for an Education Provider, including the roles which are 
        requisite linked to the Student role. '''

        self.seed_main_contact_admin()
        for role in ['Teacher', 'Staff']:
            self.create_role(role, self.data[role])

        student = self.create_role('Student', self.data['Student'])
        role_list = []
        for role in ['Parent', 'Family']:
            role_list.append([role, self.data[role]])
        self.create_requisite_roles(role_list, student)

    def seed_club(self):

        ''' Create the generic HubRoles for a Club. '''

        self.seed_main_contact_admin()

        member = self.create_role('Member', self.data['Member'])
        role_list = []
        for role in ['Family']:
            role_list.append([role, self.data[role]])
        self.create_requisite_roles(role_list, member)        


