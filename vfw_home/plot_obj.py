class PlotObject:
    """
    Class calculates parameters accroding the parameters.
    """

    def __init__(self, webID="", data=None, date="", full_res=False, plot_size=[700, 500]):
        self.webID = webID
        self.data = data
        self.date = date
        self.full_res = full_res
        self.plot_size = plot_size

        self.dbinput = None
        self.wpsinput = None
        self.title = ""

        # Plot ranges
        self.range_dict = {
            "x_min": None,
            "x_max": None,
            "y_min": None,
            "y_max": None
        }

    def get_data(self):
        if self.webID[0:2] == "db":
            raise

    def preprocess_data(self):
        raise

    # def
