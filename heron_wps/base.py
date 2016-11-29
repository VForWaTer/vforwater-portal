class WpsService:
    """
    Used to define dataset services for apps.
    """

    def __init__(self, name, endpoint, username=None, password=None):
        """
        Constructor
        """
        self.name = name
        self.endpoint = endpoint
        self.username = username
        self.password = password

    def __repr__(self):
        """
        String representation
        """
        return '<WpsService: name={0}, endpoint={1}>'.format(self.name, self.endpoint)