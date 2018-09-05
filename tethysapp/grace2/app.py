from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import PersistentStoreDatabaseSetting, PersistentStoreConnectionSetting, CustomSetting


class Grace2(TethysAppBase):
    """
    Tethys app class for Grace2.
    """

    name = 'GRACE 2.0 test'
    index = 'grace2:home'
    icon = 'grace2/images/logo.jpg'
    package = 'grace2'
    root_url = 'grace2'
    color = '#222222'
    description = 'The GRACE application is a visualization tool for GRACE global satellite data. It also provides visualization for global surface water, soil moisture, and groundwater data.'
    tags = '&quot;Hydrology&quot;, &quot;Groundwater&quot;'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='grace2',
                controller='grace2.controllers.home'
            ),
            UrlMap(
                name='global-map',
                url='global-map',
                controller='grace2.controllers.global_map'
            ),
            UrlMap(
                name='region',
                url='region',
                controller='grace2.controllers.region'
            ),
            UrlMap(
                name='add-region',
                url='add-region',
                controller='grace2.controllers.add_region'
            ),
            UrlMap(
                name='get-plot-global',
                url='global-map/get-plot-global',
                controller='grace2.ajax_controllers.get_plot_global'
            ),
            UrlMap(
                name='get-plot-reg-pt',
                url='region/get-plot-reg-pt',
                controller='grace2.ajax_controllers.get_plot_reg_pt'
            ),




            UrlMap(name='add-region-ajax',
                   url='grace2/add-region/submit',
                   controller='grace2.ajax_controllers.region_add'
            ),
            UrlMap(name='initial-processing-ajax',
                   url='grace2/add-region/initial',
                   controller='grace2.ajax_controllers.subset_initial_processing'
            ),
            UrlMap(name='jpl-tot-ajax',
                   url='grace2/add-region/jpl-tot',
                   controller='grace2.ajax_controllers.subset_jpl_tot'
            ),
            UrlMap(name='jpl-gw-ajax',
                   url='grace2/add-region/jpl-gw',
                   controller='grace2.ajax_controllers.subset_jpl_gw'
            ),
            UrlMap(name='csr-tot-ajax',
                   url='grace2/add-region/csr-tot',
                   controller='grace2.ajax_controllers.subset_csr_tot'
            ),
            UrlMap(name='csr-gw-ajax',
                   url='grace2/add-region/csr-gw',
                   controller='grace2.ajax_controllers.subset_csr_gw'
            ),
            UrlMap(name='gfz-tot-ajax',
                   url='grace2/add-region/gfz-tot',
                   controller='grace2.ajax_controllers.subset_gfz_tot'
            ),
            UrlMap(name='gfz-gw-ajax',
                   url='grace2/add-region/gfz-gw',
                   controller='grace2.ajax_controllers.subset_gfz_gw'
            ),
            UrlMap(name='avg-tot-ajax',
                   url='grace2/add-region/avg-tot',
                   controller='grace2.ajax_controllers.subset_avg_tot'
            ),
            UrlMap(name='avg-gw-ajax',
                   url='grace2/add-region/avg-gw',
                   controller='grace2.ajax_controllers.subset_avg_gw'
            ),
            UrlMap(name='sw-ajax',
                   url='grace2/add-region/sw',
                   controller='grace2.ajax_controllers.subset_sw'
            ),
            UrlMap(name='soil-ajax',
                   url='grace2/add-region/soil',
                   controller='grace2.ajax_controllers.subset_soil'
            ),
            UrlMap(name='cleanup-ajax',
                   url='grace2/add-region/cleanup',
                   controller='grace2.ajax_controllers.subset_cleanup'
            ),
            UrlMap(name='update-ajax',
                   url='grace2/add-region/update',
                   controller='grace2.ajax_controllers.subset_update'
            ),



            UrlMap(
                name='add-thredds-server',
                url='add-thredds-server',
                controller='grace2.controllers.add_thredds_server'
            ),
            UrlMap(name='add-thredds-server-ajax',
                   url='grace2/add-thredds-server/submit',
                   controller='grace2.ajax_controllers.thredds_server_add'
            ),
            UrlMap(name='update-thredds-servers-ajax',
                   url='grace2/manage-thredds-servers/submit',
                   controller='grace2.ajax_controllers.thredds_server_update'
            ),
            UrlMap(name='delete-thredds-server-ajax',
                   url='grace2/manage-thredds-servers/delete',
                   controller='grace2.ajax_controllers.thredds_server_delete'
            ),
            UrlMap(
                name='manage-regions',
                url='manage-regions',
                controller='grace2.controllers.manage_regions'
            ),
            UrlMap(name='manage-regions-table',
                   url='grace2/manage-regions/table',
                   controller='grace2.controllers.manage_regions_table'
            ),
            UrlMap(name='delete-regions-ajax',
                   url='grace2/manage-regions/delete',
                   controller='grace2.ajax_controllers.region_delete'
            ),
            UrlMap(
                name='manage-thredds-servers',
                url='manage-thredds-servers',
                controller='grace2.controllers.manage_thredds_servers'
            ),
            UrlMap(name='manage-thredds-servers-table',
                   url='grace2/manage-thredds-servers/table',
                   controller='grace2.controllers.manage_thredds_servers_table'
            ),
            UrlMap(name='api_get_point_values',
                   url='grace2/api/GetPointValues',
                   controller='grace2.api.api_get_point_values'),
        )

        return url_maps

    def custom_settings(self):
        custom_settings = (
            CustomSetting(
                name='Local Thredds Folder Path',
                type=CustomSetting.TYPE_STRING,
                description='Path to Global NetCDF Directory (Local Folder Mounted to Thredds Docker)',
                required=True,
            ),
            CustomSetting(
                name='Thredds wms URL',
                type=CustomSetting.TYPE_STRING,
                description='URL to thredds Global Directory folder (make sure it paths to the folder and not a specific layer)',
                required=True,
            ),
        )
        return custom_settings

    def persistent_store_settings(self):

        ps_settings = (
            PersistentStoreDatabaseSetting(
                name='grace_db',
                description='For storing Region and Thredds metadata',
                required=True,
                initializer='grace2.model.init_grace_db',
                spatial=False,
            ),
        )

        return ps_settings
