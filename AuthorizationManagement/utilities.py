import os

def get_opposite_os_directory_sep():
    if os.sep == '/':
        return '\\'
    else:
        return '/'
    
    
def get_one_level_lower_path(relative_path):   
    relative_path_elements = relative_path.split('/')
    del relative_path_elements[len(relative_path_elements)-1]
    return ('/').join(relative_path_elements)

def get_relative_path_with_parameters(request):
    path = request.path
    param = list()
    
    
    if 'q' in request.GET and request.GET['q']:      
        param.append('q='+request.GET['q'])
    
    if 'page' in request.GET and request.GET['page']:
        param.append('page='+request.GET['page'])
    
    if len(param)== 0:
        return path
    else:
        path+=('?'+('&').join(param))
        
    return path
        
    