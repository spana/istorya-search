# class institution is a model of a institution. It contains all important data about given institution: name, type, location, important events and dates.
# It also contains tags (both current and old ones) that are used for search. Tags are generated from other object properties.
# Tags include: name, past names, location, past locations, type, past types,
# all higher types (college -> university -> educational) and all higher locations (city -> province -> country -> continent).
# Higer types/locations are used for broader search, for example,
# school located in Palo Alto will be shown as a search result when user is searching schools in Palo Alto,
# but it will be also included when user is searching schools in California or USA.


class institution:
    def __init__(self, name, inst_type, location):
        self.name = name
        self.type = inst_type
        self.names = []
        self.location = location
        self.locations = []
        self.languages = []
        self.tags = []
        self.tags_old = []
        self.tags_oldt = []
        self.events = []

    def add_names(self, name, date1, date2):
        self.names.append([name, date1, date2])

    def add_locations(self, location, date1, date2):
        self.locations.append([location, date1, date2])

    def add_languages(self, language, date1, date2):
        self.languages.append([language, date1, date2])

    def add_event(self, event, date):
        self.events.append([event, date])

    def add_tags(self):
        self.tags.append(self.name)
        self.tags = union(self.tags, location_tree(self.location))
        self.tags = union(self.tags, institution_tree(self.type))
        self.tags = union(self.tags, self.languages)
        for name in self.names:
            self.tags_old = union(self.tags_old, [name[0]])
        my_town = town_list[self.location]
        country_list = []
        for country in my_town.countries:
            country_list.append(country[0])
        self.tags_oldt = union(self.tags_oldt, country_list)
        

class town:
    def __init__(self, name, country):
        self.name = name
        self.names = []
        self.country = country
        self.countries = []
        self.events = []
        self.population = []

    def add_names(self, name, date1, date2):
        self.names.append([name, date1, date2])

    def add_country(self, country, date1, date2):
        self.countries.append([country, date1, date2])

    def add_event(self, event, date):
        self.events.append([event, date])

    def add_population(self, population, date):
        self.population.append([date, population])
        
# contants used in indexes
up = 0
down = 1


#location_index defines hierarchy of teritories.

location_index = {'Europe': {   up: [],
                                down: ['Serbia', 'Germany', 'Hungaria', 'Austria', 'Romania', 'Spain', 'France']},
                  'Serbia': {   up: ['Europe', 'Balkans'],
                                down: ['Vojvodina', 'Kosovo', 'Central Serbia']},
                  'Vojvodina': {up: ['Serbia'],
                                down: ['Backa', 'Banat', 'Srem']},
                  'Backa': {    up: ['Vojvodina'],
                                down:['Sombor', 'Subotica', 'Novi Sad', 'Vrbas', 'Kula']},
                  'Sombor county': {   up: ['Backa'],
                                down: ['Sombor', 'Conoplja', 'Kljajicevo', 'Stanisic', 'Ridjica']},
                  'Conoplja': { up: ['Sombor county'],
                                down: []},
                  'Sombor': {   up: ['Sombor county'],
                                down: []},
                  'Balkans' : { up: ['Europe'],
                                down: ['Serbia', 'Montenegro', 'Bulgaria', 'Bosnia']}
                  }

#institution_index defines hierarchy of institutional types.

institution_index = {'educational': {       up: [],
                                            down: ['elementary school', 'high school', 'university']},
                     'elementary school': { up: ['educational'],
                                            down: []},
                     'high school': {       up: ['educational'],
                                            down: []},
                     'university': {        up: ['educational'],
                                            down: ['college']},
                     'college': {           up: ['university'],
                                            down: []},
                     'sports': {            up: [],
                                            down: ['football', 'basketball', 'tennis']},
                     'football': {          up: ['sports'],
                                            down: []},
                     'basketball': {          up: ['sports'],
                                            down: []},
                     'tennis': {          up: ['sports'],
                                            down: []}
                    }

object_index = {}
town_index = {}
town_list = {}


# Defines union of two lists.

def union(a, b):
    res = []
    for e in a:
        res.append(e)
    for e in b:
        if e not in a:
            res.append(e)
    return res

# Defines union of two lists.

def intersection(a, b):
    res = []
    for e in b:
        if e in a:
            res.append(e)
    return res

# location_tree returns all higher levels of location defined in location_index.

def location_tree(loc):
    current = location_index[loc][up]
    res = [loc]
    if current != []:
        for el in current:
            res = union(res, location_tree(el))
    return res


#institution_tree returns all higer levels of institutional types defined in institution_index.
        
def institution_tree(inst_type):
    current = institution_index[inst_type][up]
    res = [inst_type]
    if current != []:
        for el in current:
            res = union(res, institution_tree(el))
    return res


# Adds object to an object_index.
# object_index is a dictionary where keywords are tags from objects. Each value is a list of two elements:
# list of objects that have given tag in obj.tags and list of objects that have given tag in obj.tags_old.
# Each object is added to the index right after creation or modification and that eliminates need for crawling.

def add_object_to_index(obj):
    for tag in obj.tags:
        if tag in object_index:
            object_index[tag][0].append(obj)
        else:
            object_index[tag] = [[obj],[],[]]
    for tag in obj.tags_old:
        if tag in object_index:
            object_index[tag][1].append(obj)
        else:
            object_index[tag] = [[],[obj],[]]
    for tag in obj.tags_oldt:
        if tag in object_index:
            object_index[tag][2].append(obj)
        else:
            object_index[tag] = [[],[],[obj]]
        


def add_town_to_index(my_town):
    for country in my_town.countries:
        if country[0] in town_index:
            town_index[country[0]].append(my_town.name)
        else:
            town_index[country[0]] = [my_town.name]


# To make it simple, we supose that each town has unique name.
# In some future version, this dictionary will have list of town objects with the same name, instead of just one object.

def add_town_to_list(my_town):
    town_list[my_town.name] = my_town
    


NO_INPUT = 1
NOT_FOUND = 2
TODAY = 2012


error_message = {}
error_message[NO_INPUT] = ['Please enter at least one of these parameters: name, type, location.']
error_message[NOT_FOUND] = ['No results found.']


def search_institution(name, institution, location, date1_str, date2_str, past_flag, pt_flag):
    res = []
    error_code = 0
    if name != '' or institution != '' or location != '':
        if (name != '' and name not in object_index) or (institution != '' and institution not in object_index) or (location != '' and location not in object_index):
            error_code = NOT_FOUND
            res = error_message[error_code]
            return error_code, res
        if name in object_index:
            names_all = object_index[name][0]
            if past_flag:
                names_all = union(names_all,object_index[name][1])
            res = union(res, names_all)
        if institution in object_index:
            inst_all = object_index[institution][0]
            if past_flag:
                inst_all = union(inst_all,object_index[institution][1])
            res = union(res, inst_all)
        if location in object_index:
            loc_all = object_index[location][0]
            if past_flag:
                loc_all = union(loc_all,object_index[location][1])
            if pt_flag:
                loc_all = union(loc_all, object_index[location][2])
            res = union(res, loc_all)
        if name != '':
            res = intersection(res, names_all)
        if institution != '':
            res = intersection(res, inst_all)
        if location != '':
            res = intersection(res, loc_all)
    else:
        error_code = NO_INPUT
        res = error_message[error_code]
        return error_code, res


    date1 = -10000
    date2 = TODAY
    flag_date_input = True
    if date1_str == '' and date2_str == '':
        flag_date_input = False
    else:
        if date1_str != '': 
            date1 = int(date1_str)
        if date2_str != '':
            date2 = int(date2_str)

    flags = []
    for i in range(len(res)):
        flags.append(False)
        obj = res[i]
        if flag_date_input:
            if check_existance(obj, date1, date2):
                if past_flag and name != '':
                    if not check_names(obj, name, date1, date2):
                        flags[i] = True
                if pt_flag and location != '':
                    if not check_territory(obj, location, date1, date2):
                        flags[i] = True
            else:
                flags[i] = True
        else:
            if pt_flag and location != '':
                if not check_territory(obj, location, date1, date2):
                    flags[i] = True
   
    for i in reversed(range(len(res))):
        if flags[i]:
            del(res[i])

    if res == []:
        error_code = NOT_FOUND
        res = error_message[error_code]
                
    return error_code, res

def check_existance(obj, date1, date2):
    ret = False
    inst_date2 = TODAY
    for event in obj.events:
        if event[0] == 'founded':
            inst_date1 = event[1]
        if event[0] == 'closed':
            inst_date2 = event[2]
    if max(date1, inst_date1) <= min(date2, inst_date2):
        ret = True
    return ret


def find_loc_interval(obj, location, date1, date2):
    loc_flag = False
    inst_date2 = TODAY
    for event in obj.events:
        if event[0] == 'founded':
            inst_date1 = event[1]
        if event[0] == 'closed':
            inst_date2 = event[2]

    if location in obj.tags:
        loc_flag = True
        terr_date2 = inst_date2
        terr_date1 = inst_date1

    town = town_list[obj.location]
    for country in town.countries:
        if country[0] == location:
            loc_flag = True
            terr_date1 = country[1]
            terr_date2 = country[2]

    if loc_flag:
        loc_date1 = max(date1, inst_date1, terr_date1)
        loc_date2 = min(date2, inst_date2, terr_date2)
    else:
        loc_date1 = TODAY + 1
        loc_date2 = TODAY

    return loc_date1, loc_date2


def check_territory(obj, location, date1, date2):
    d1, d2 = find_loc_interval(obj, location, date1, date2)
    if d1 > d2:
        return False
    return True


def check_names(obj, name, date1, date2):
    ret = False
    for inst_name in obj.names:
        if name == inst_name[0]:
            name_date1 = inst_name[1]
            name_date2 = inst_name[2]
            if max(date1, name_date1) <= min(date2, name_date2):
                ret = True
    return ret
    
   

# search_events searches for events (within institutions defined by name, type and location)
# from a given time interval. If interval is not specified, it returns all events.
# If event is 'all' it returns all events from given time interval.
# If name, institution and location parameters are not defined, it returns error.


def search_events(name, institution, location, event, date1_str, date2_str, past_flag, pt_flag):
    date1 = -10000
    date2 = TODAY
    flag_date_input = True
    if date1_str != '': 
        date1 = int(date1_str)
    if date2_str != '':
        date2 = int(date2_str)

    events_found = []
    error_code, res = search_institution(name, institution, location, date1_str, date2_str, past_flag, pt_flag)
    #print res
    if error_code == 0:
        for i in range(len(res)):
            obj = res[i]
            if location != '':
                loc_date1, loc_date2 = find_loc_interval(obj, location, date1, date2)
            else:
                loc_date1, loc_date2 = date1, date2
            if name == '':
                name_date1 = -10000
                name_date2 = TODAY
            else:    
                for inst_name in obj.names:
                    if inst_name[0] == name:
                        name_date1 = inst_name[1]
                        name_date2 = inst_name[2]
            int1, int2 = max(loc_date1, name_date1), min(loc_date2, name_date2)
            if int1 <= int2:
                for ev in obj.events:
                    if (ev[0] == event or event == 'all') and ev[1] >= int1 and ev[1] <= int2:

                        events_found.append([ev[1], obj, ev])
                        
        if events_found == []:
            error_code = NOT_FOUND
            res = error_message[error_code]
            return error_code, res
        
        events_found.sort()
    else:
        return error_code, res

    return error_code, events_found
                
                

            
    

def search(name, institution, location, event, date1, date2, past_flag, pt_flag):
    print_out = []
    if event == '':
        error, res = search_institution(name, institution, location, date1, date2, past_flag, pt_flag)
        if error == 0:
            for i in range(len(res)):
                print_out.append(str(i+1) + '. ' + res[i].name + ', ' + res[i].type + ', ' + res[i].location)
        else:
            print_out = res
    else:
        error, res = search_events(name, institution, location, event, date1, date2, past_flag, pt_flag)
        if error == 0:
            for i in range(len(res)):
                print_out.append(str(i+1) + '. ' + res[i][1].name + ', ' + res[i][1].type + ', ' + res[i][1].location)
                print_out.append(str(res[i][2][0]) + ', ' + str(res[i][2][1]))
        else:
            print_out = res

    return print_out        



def fill_in():

    my_town = town('Conoplja','Serbia')
    my_town.add_country('Serbia', 2006, 2012)
    my_town.add_country('Yugoslavia', 1918, 2005)
    my_town.add_country('Austria-Hungary', 1700, 1917)
    my_town.add_country('Turkey', 1500, 1699)
    my_town.add_event('founded', 1350)
    add_town_to_index(my_town)
    add_town_to_list(my_town)


    my_town = town('Sombor','Serbia')
    my_town.add_country('Serbia', 2006, 2012)
    my_town.add_country('Yugoslavia', 1918, 2005)
    my_town.add_country('Austria-Hungary', 1700, 1917)
    my_town.add_country('Turkey', 1500, 1699)
    my_town.add_event('founded', 1340)
    add_town_to_index(my_town)
    add_town_to_list(my_town)

    
    school = institution('Miroslav Antic', 'elementary school', 'Conoplja')
    school.add_names('Bratstvo-Jedinstvo', 1946, 1992)
    school.add_names('Miroslav Antic', 1992, 2012)
    school.add_event('name change', 1992)
    school.add_event('founded', 1946)
    school.add_tags()
    add_object_to_index(school)

    school = institution('Bratstvo-Jedinstvo', 'elementary school', 'Sombor')
    school.add_event('founded', 1946)
    school.add_names('Bratstvo-Jedinstvo', 1946, 2012)
    school.add_tags()
    add_object_to_index(school)

    school = institution('Pedagoski fakultet', 'college', 'Sombor')
    school.add_names('Uciteljski fakultet', 1993, 2010)
    school.add_names('Pedagoski fakultet', 2010, 2012)
    school.add_event('name change', 2010)
    school.add_event('name change', 1991)
    school.add_event('founded', 1778)
    school.add_tags()
    add_object_to_index(school)




fill_in()

print search('','','','','','', False, False)




