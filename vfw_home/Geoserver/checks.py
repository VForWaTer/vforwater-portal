import sys

from .geoserver_layer import test_geoserver_env, has_layer, create_layer


def check_geoserver_layers(store: str, workspace: str, layers: list) -> object:
    """
    Check that geoserver is running and has the needed stores, workspace, and layers

    :param store: str
    :param workspace: str
    :param layers: list
    """
    geoserver_alive = False
    try:
        test_geoserver_env(store, workspace)
        geoserver_alive = True
    except:
        print('\033[91mno geoserver\033[0m ', sys.exc_info()[0])

    # check if static layers exist. Build them if not.
    if geoserver_alive:
        for ly in layers:
            if not has_layer(ly[0], store, workspace):
                print(f'--- no layer <{ly[0]}> ---')
                create_layer(request={}, filename=ly[0], datastore=store, workspace=workspace, layertype=ly[1])
