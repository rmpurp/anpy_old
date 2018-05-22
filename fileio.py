import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
import itertools as it
from openpyxl.worksheet.cell_range import CellRange

class Column:
    def __init__(self, column, title, num_body_items):
        self.title = title
        self.column = column
        self.num_body_items = num_body_items

    def make(self, ws):
        ws.cell(row=1, column=self.column, value=self.title)
        for row, item in enumerate(self._get_body(self.num_body_items), 2):
            cell = ws.cell(row=row, column=self.column, value=item)
            self._cell_op(cell)
        ws.cell(row=row + 1, column=self.column, value=self._get_footer())

    def _get_body_item(self, item_num):
        return item_num

    def _cell_op(self, cell):
        pass

    def _get_body(self, num_items):
        i = 1
        while i <= num_items:
            yield self._get_body_item(i)
            i += 1

    def _get_footer(self):
        range = CellRange(min_col=self.column,
                          max_col=self.column,
                          min_row=2,
                          max_row=1 + self.num_body_items)
        return '=AVERAGE({})'.format(str(range))

class DateColumn(Column):
    def __init__(self, column, num_body_items, start_date=None):
        if not start_date:
            start_date = get_most_recent_monday()
        self.start_date = start_date
        super().__init__(column, 'Date', num_body_items)

    def _get_body_item(self, item_num):
        if item_num == 1:
            return self.start_date
        else:
            return '= {}{} + 1'.format(get_column_letter(self.column), item_num)

    def _cell_op(self, cell):
        cell.number_format = 'YYYY-MM-DD'

    def _get_footer(self):
        return 'Averages:'

subjects = ['AP Euro', 'AP Bio', 'Band', 'Dab']

def get_subjects(ws, num_titles):
    subjects = []
    index = num_titles + 1
    cell = ws.cell(row=1, column=index)
    while cell.value:
        subjects.append(cell.value)
        index += 1
        cell = ws.cell(row=1, column=index)
    return subjects

def get_most_recent_monday(date=None):
    if not date:
        date = datetime.date.today()
    return date - datetime.timedelta(days=date.weekday())
        

wb = Workbook()
ws = wb.active
# create_headers(ws, TITLES, subjects)
# add_date(ws)
# print(get_subjects(ws, 6))
c = Column(1, title='banana', num_body_items=7)
d = DateColumn(2, num_body_items=7)
c.make(ws)
d.make(ws)
wb.save('test.xlsx')
