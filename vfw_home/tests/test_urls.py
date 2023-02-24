from django.test import SimpleTestCase
from django.urls import reverse, resolve
from vfw_home.views import HomeView, LoginView, HelpView, LogoutView, GeoserverView, ToggleLanguageView, \
    FailedLoginView, DatasetDownloadView, entries_pagination, previewplot, short_datainfo, show_info, \
    filter_selection, filter_map_selection, workspace_data, advanced_filter


class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('vfw_home:home')
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_watts_login_url_resolves(self):
        url = reverse('vfw_home:watts_login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_help_url_resolves(self):
        url = reverse('vfw_home:help')
        self.assertEqual(resolve(url).func.view_class, HelpView)

    # TODO: find a better test method when two different classes are used.
    #  django.contrib.auth.views.logoutView vs vfw_home.views.logoutView.
    #def test_logout_url_resolves(self,):
        #url = reverse('vfw_home:logout')
        #self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_geoserver_url_resolves(self):
        url = reverse('vfw_home:geoserver',
                      kwargs={'service': 'wfs',
                              'layer': 'play',
                              'bbox': '-42272,5339297.423305951.9926404953.581306163',
                              'srid': '3857'})
        self.assertEqual(resolve(url).func.view_class, GeoserverView)

    def test_toggle_lang_url_resolves(self):
        url = reverse('vfw_home:togglelang')
        self.assertEqual(resolve(url).func.view_class, ToggleLanguageView)

    def test_failed_login_url_resolves(self):
        url = reverse('vfw_home:failedlogin')
        self.assertEqual(resolve(url).func.view_class, FailedLoginView)

    def test_data_set_download_url_resolves(self):
        url = reverse('vfw_home:datasetdownload')
        self.assertEqual(resolve(url).func.view_class, DatasetDownloadView)

    def test_entries_pagination_url_resolves(self):
        url = reverse('vfw_home:entries_pagination')
        self.assertEqual(resolve(url).func, entries_pagination)

    def test_preview_plot_url_resolves(self):
        url = reverse('vfw_home:previewplot')
        self.assertEqual(resolve(url).func, previewplot)

    def test_short_data_info_url_resolves(self):
        url = reverse('vfw_home:short_datainfo')
        self.assertEqual(resolve(url).func, short_datainfo)

    def test_show_info_url_resolves(self):
        url = reverse('vfw_home:show_info')
        self.assertEqual(resolve(url).func, show_info)

    def test_filter_selection_url_resolves(self):
        url = reverse('vfw_home:filter_selection')
        self.assertEqual(resolve(url).func, filter_selection)

    def test_filter_map_selection_url_resolves(self):
        url = reverse('vfw_home:filter_map_selection')
        self.assertEqual(resolve(url).func, filter_map_selection)

    def test_workspace_data_url_resolves(self):
        url = reverse('vfw_home:workspace_data')
        self.assertEqual(resolve(url).func, workspace_data)

    def test_advanced_filter_url_resolves(self):
        url = reverse('vfw_home:advanced_filter')
        self.assertEqual(resolve(url).func, advanced_filter)
