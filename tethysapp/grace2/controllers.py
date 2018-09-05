from django.shortcuts import render
from django.contrib.auth.decorators import login_required,user_passes_test
from tethys_sdk.gizmos import *
from .app import *
from model import *
from utilities import *
from config import thredds_url, GLOBAL_NETCDF_DIR, SHELL_DIR
from update_global_data import *
# @login_required()
def home(request):
    """
    Controller for the app home page.
    """

    # downloadFile(GLOBAL_NETCDF_DIR+'temp/')
    # write_gldas_text_file()
    # download_gldas_data()
    # download_monthly_gldas_data()


    Session = Grace2.get_persistent_store_database('grace_db',as_sessionmaker=True)
    session = Session()
    # Query DB for regions
    regions = session.query(Region).all()
    region_list = []

    for region in regions:
        region_list.append(("%s" % (region.display_name), region.id))

    session.close()
    if region_list:
        region_select = SelectInput(display_text='Select a Region',
                                    name='region-select',
                                    options=region_list, )
    else:
        region_select = None

    context = {
        "region_select": region_select, "regions_length": len(region_list), 'host': 'http://%s' % request.get_host()
    }

    return render(request, 'grace2/home.html', context)

def api(request):

    context = {'host': 'http://%s' % request.get_host()}

    return render(request, 'grace/api.html', context)

# @login_required()
def global_map(request):
    """
    Controller for the app home page.
    """
    thredds_wms = thredds_url

    grace_layer_options = get_global_dates()


    select_signal_process = SelectInput(display_text='Select Signal Processing Method',
                                    name = 'select_signal_process',
                                    multiple=False,
                                    options= [('CSR Solution', "csr"), ('JPL Solution', "jpl"), ('GFZ Solution', "gfz"), ('Ensemble Avg of JPL, CSR, & GFZ', "avg")],
                                    initial=['CSR Solution']
                                    )

    select_layer = SelectInput(display_text='Select a day',
                               name='select_layer',
                               multiple=False,
                               options=grace_layer_options, )

    select_storage_type = SelectInput(display_text='Select Storage Component',
                                      name='select_storage_type',
                                      multiple=False,
                                      options=[('Total Water Storage (GRACE)', "tot"),
                                               ('Surface Water Storage (GLDAS)', "sw"),
                                               ('Soil Moisture Storage (GLDAS)', "soil"),
                                               ('Groundwater Storage (Calculated)', "gw")
                                               ],
                                      initial=['Total Water Storage (GRACE)']
                                      )


    context = {
        "thredds_wms":thredds_wms,
        "select_storage_type":select_storage_type,
        'select_layer':select_layer,
        "select_signal_process":select_signal_process,

    }

    return render(request, 'grace2/global_map.html', context)

# @login_required()
def region(request):
    """
    Controller for the app home page.
    """
    thredds_wms = thredds_url


    context = {}


    info = request.GET

    region_id = info.get('region-select')
    Session = Grace2.get_persistent_store_database('grace_db', as_sessionmaker=True)
    session = Session()

    region = session.query(Region).get(region_id)
    display_name = region.display_name

    bbox = [float(x) for x in region.latlon_bbox.strip("(").strip(")").split(',')]
    json.dumps(bbox)

    regions = session.query(Region).all()
    region_list = []

    for reg in regions:
        region_list.append(("%s" % (reg.display_name), reg.id))
    lower_name= ''.join(display_name.split()).lower()
    session.close()

    if region_list:
        select_region = SelectInput(display_text='Switch Region:',
                                    name='region-select',
                                    multiple=False,
                                    options=region_list,
                                    initial=display_name,
                                    )
    else:
        select_region = None


    grace_layer_options = get_global_dates()

    select_signal_process = SelectInput(display_text='Select Signal Processing Method',
                                    name = 'select_signal_process',
                                    multiple=False,
                                    options= [('JPL Solution', "jpl"), ('CSR Solution', "csr"), ('GFZ Solution', "gfz"), ('Ensemble Avg of JPL, CSR, & GFZ', "avg")],
                                    initial=['CSR Solution']
                                    )

    select_layer = SelectInput(display_text='Select a day',
                               name='select_layer',
                               multiple=False,
                               options=grace_layer_options, )

    select_storage_type = SelectInput(display_text='Select Storage Component',
                                      name='select_storage_type',
                                      multiple=False,
                                      options=[('Total Water Storage (GRACE)',"tot"),
                                               ('Surface Water Storage (GLDAS)',"sw"),
                                               ('Soil Moisture Storage (GLDAS)',"soil"),
                                               ('Groundwater Storage (Calculated)',"gw")],
                                      initial=['Total Water Storage (GRACE)']
                                      )


    if bbox[0] < 0 and bbox[2] < 0:
        map_center = [(int(bbox[1])+int(bbox[3])) / 2, ( (360+(int(bbox[0])))+(360+(int(bbox[2])))) / 2]
    else:
        map_center = [(int(bbox[1]) + int(bbox[3])) / 2, (int(bbox[0]) + int(bbox[2])) / 2]
    json.dumps(map_center)


    context = {"region_id":region_id,
               "thredds_wms":thredds_wms,
               "display_name":display_name,
               "select_layer":select_layer,
               "bbox":bbox,
               "map_center":map_center,
               "select_signal_process":select_signal_process,
               "select_storage_type":select_storage_type,
               "select_region":select_region,
               "lower_name":lower_name
    }

    return render(request, 'grace2/region.html', context)


@user_passes_test(user_permission_test)
def add_region(request):

    region_name_input = TextInput(display_text='Region Display Name',
                                     name='region-name-input',
                                     placeholder='e.g.: Utah',
                                     icon_append='glyphicon glyphicon-home',
                                     ) #Input for the Region Display Name

    Session = Grace2.get_persistent_store_database('grace_db', as_sessionmaker=True)
    session = Session()
    # Query DB for geoservers
    thredds_servers = session.query(Thredds).all()
    thredds_list = []
    for thredds in thredds_servers:
        thredds_list.append(( "%s (%s)" % (thredds.name, thredds.url),
                               thredds.id))

    session.close()
    if thredds_list:
        thredds_select = SelectInput(display_text='Select a Thredds server',
                                       name='thredds-select',
                                       options=thredds_list)
    else:
        thredds_select = None

    add_button = Button(display_text='Add Region',
                        icon='glyphicon glyphicon-plus',
                        style='success',
                        name='submit-add-region',
                        attributes={'id': 'submit-add-region'}, )  # Add region button

    context = {"region_name_input":region_name_input, "thredds_select":thredds_select,"add_button":add_button}

    return render(request, 'grace2/add_region.html', context)


@user_passes_test(user_permission_test)
def add_thredds_server(request):
    """
        Controller for the app add_geoserver page.
    """

    thredds_name_input = TextInput(display_text='Thredds Server Name',
                                     name='thredds-name-input',
                                     placeholder='e.g.: BYU Thredds Server',
                                     icon_append='glyphicon glyphicon-tag', )

    thredds_url_input = TextInput(display_text='Thredds Server REST Url',
                                    name='thredds-url-input',
                                    placeholder='e.g.: http://localhost:9090/thredds/',
                                    icon_append='glyphicon glyphicon-cloud-download')

    thredds_username_input = TextInput(display_text='Thredds Server Username',
                                         name='thredds-username-input',
                                         placeholder='e.g.: admin',
                                         icon_append='glyphicon glyphicon-user', )

    add_button = Button(display_text='Add Thredds Server',
                        icon='glyphicon glyphicon-plus',
                        style='success',
                        name='submit-add-thredds-server',
                        attributes={'id': 'submit-add-thredds-server'}, )

    context = {
        'thredds_name_input': thredds_name_input,
        'thredds_url_input': thredds_url_input,
        'thredds_username_input': thredds_username_input,
        'add_button': add_button,
    }

    return render(request, 'grace2/add_thredds_server.html', context)

@user_passes_test(user_permission_test)
def manage_regions(request):
    """
    Controller for the app manage_geoservers page.
    """
    #initialize session
    Session = Grace2.get_persistent_store_database('grace_db', as_sessionmaker=True)
    session = Session()
    num_regions = session.query(Region).count()

    session.close()

    context = {
                'initial_page': 0,
                'num_regions': num_regions,
              }

    return render(request, 'grace2/manage_regions.html', context)

@user_passes_test(user_permission_test)
def manage_regions_table(request):
    """
    Controller for the app manage_geoservers page.
    """
    #initialize session
    Session = Grace2.get_persistent_store_database('grace_db', as_sessionmaker=True)
    session = Session()
    RESULTS_PER_PAGE = 5
    page = int(request.GET.get('page'))

    # Query DB for data store types
    regions = session.query(Region)\
                        .order_by(Region.display_name) \
                        .all()[(page * RESULTS_PER_PAGE):((page + 1)*RESULTS_PER_PAGE)]

    prev_button = Button(display_text='Previous',
                         name='prev_button',
                         attributes={'class':'nav_button'},)

    next_button = Button(display_text='Next',
                         name='next_button',
                         attributes={'class':'nav_button'},)

    context = {
                'prev_button' : prev_button,
                'next_button': next_button,
                'regions': regions,
              }

    session.close()

    return render(request, 'grace2/manage_regions_table.html', context)

@user_passes_test(user_permission_test)
def manage_thredds_servers(request):
    """
    Controller for the app manage_geoservers page.
    """
    #initialize session
    Session = Grace2.get_persistent_store_database('grace_db', as_sessionmaker=True)
    session = Session()
    num_thredds_servers = session.query(Thredds).count()
    session.close()

    context = {
                'initial_page': 0,
                'num_thredds_servers': num_thredds_servers,
              }

    return render(request, 'grace2/manage_thredds_servers.html', context)

@user_passes_test(user_permission_test)
def manage_thredds_servers_table(request):
    """
    Controller for the app manage_geoservers page.
    """
    #initialize session
    Session = Grace2.get_persistent_store_database('grace_db', as_sessionmaker=True)
    session = Session()
    RESULTS_PER_PAGE = 5
    page = int(request.GET.get('page'))

    # Query DB for data store types
    thredds_servers = session.query(Thredds)\
                        .order_by(Thredds.name, Thredds.url) \
                        .all()[(page * RESULTS_PER_PAGE):((page + 1)*RESULTS_PER_PAGE)]

    prev_button = Button(display_text='Previous',
                         name='prev_button',
                         attributes={'class':'nav_button'},)

    next_button = Button(display_text='Next',
                         name='next_button',
                         attributes={'class':'nav_button'},)

    context = {
                'prev_button' : prev_button,
                'next_button': next_button,
                'thredds_servers': thredds_servers,
              }

    session.close()

    return render(request, 'grace2/manage_thredds_servers_table.html', context)
