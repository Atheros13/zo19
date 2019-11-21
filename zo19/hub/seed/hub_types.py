from hub.models.hub import HubType, HubTypeCategory

class SeedHubTypes():

    '''  '''

    def __init__(self, *args, **kwargs):

        self.data = self.build_data()

    def build_data(self):

        data = {
            
            'Education Provider': ['School', 'Kura Kaupapa Māori', 'Tertiary Institute'],
            'Club': ['Sports Club'],            
            
            }

        return data

    def create_category(self, category):

        ''' '''

        if HubTypeCategory.objects.filter(category=category):
            return HubTypeCategory.objects.filter(category=category)[0]
        c = HubTypeCategory(category=category)
        c.save()
        return c

    def create_type(self, hub_type_category, type):

        ''' '''

        if HubType.objects.filter(type=type).filter(category=hub_type_category):
            return HubType.objects.filter(type=type).filter(category=hub_type_category)[0]
        t = HubType(category=hub_type_category, type=type)
        t.save()
        return t

    def seed_all(self):

        ''' '''

        for c in self.data:
            category = self.create_category(c)
            for t in self.data[c]:
                type = self.create_type(category, t)