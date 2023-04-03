import pandas as pd

LARGE_HR_THRESHOLD = 40


class Watchdog:

    def __init__(self):
        self.dept = None
        self.agg = None
        self.msg = []

    def sniff(self, data):
        self.dept = data
        self.agg = self.aggregate()
        self.msg.append(self.large_hrs())
        # something!

    def aggregate(self):
        big_df = pd.concat([df for df in self.dept.values()])
        agg_funcs = {'hours': 'sum', 'rate': 'first', 'dept': (lambda x: set(list(x))),
                     'name': 'first', 'dept-name': (lambda x: set(list(x)))}
        big_df = big_df.groupby(big_df['id']).aggregate(agg_funcs)
        return big_df

    def large_hrs(self):
        df = self.agg[self.agg['hours'] >= LARGE_HR_THRESHOLD]
        l = []
        for index, row in df.iterrows():
            sn = "  {name} clocked {hours} hours across [{dept_list}]".format(
                name=row['name'], hours=row['hours'],
                dept_list=", ".join(row['dept-name']))
            l.append(sn)
        return "\n".join(l)







