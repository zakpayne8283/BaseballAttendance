

class DataHelper():

    teams = []
    
    start_year = 2000
    end_year   = 2025

    base_schedule_url = ''

    def __init__(self, **kwargs):
        kw_options = ['start_year', 'end_year']

        for opt in kw_options:
            if opt in kwargs.keys():
                setattr(self, opt, kwargs[opt])


        print('Created DataHelper!')
