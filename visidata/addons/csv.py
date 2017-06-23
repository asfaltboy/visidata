
from visidata import *
import csv

option('csv_dialect', 'excel', 'dialect passed to csv.reader')
option('csv_delimiter', ',', 'delimiter passed to csv.reader')
option('csv_quotechar', '"', 'quotechar passed to csv.reader')


def open_csv(p):
    vs = Sheet(p.name, p)
    vs.loader = lambda vs=vs: load_csv(vs)
    return vs

def wrapped_next(rdr):
    try:
        return next(rdr)
    except csv.Error as e:
        return [str(e)]

@async
def load_csv(vs):
    """Convert from CSV, first handling header row specially."""
    with vs.source.open_text() as fp:
        samplelen = min(len(wrapped_next(fp)) for i in range(10))
        fp.seek(0)

        rdr = csv.reader(fp,
                         dialect=options.csv_dialect,
                         quotechar=options.csv_quotechar,
                         delimiter=options.csv_delimiter)

        vs.rows = []

        # headers first, to setup columns before adding rows
        headers = [wrapped_next(rdr) for i in range(int(options.headerlines))]

        if headers:
            # columns ideally reflect the max number of fields over all rows
            vs.columns = ArrayNamedColumns('\\n'.join(x) for x in zip(*headers))
        else:
            r = wrapped_next(rdr)
            vs.rows.append(wrapped_next(rdr))
            vs.columns = ArrayColumns(len(vs.rows[0]))

        vs.progressMade = 0
        vs.progressTotal = vs.source.filesize

        try:
            while True:
                vs.rows.append(wrapped_next(rdr))
                vs.progressMade += samplelen

        except StopIteration:
            pass

    vs.progressMade = 0
    vs.progressTotal = 0
    return vs


def save_csv(sheet, fn):
    """Save as single CSV file, handling column names as first line."""
    with open(fn, 'w', newline='', encoding=options.encoding, errors=options.encoding_errors) as fp:
        cw = csv.writer(fp, dialect=options.csv_dialect, delimiter=options.csv_delimiter, quotechar=options.csv_quotechar)
        colnames = [col.name for col in sheet.visibleCols]
        if ''.join(colnames):
            cw.writerow(colnames)
        for r in sheet.rows:
            cw.writerow([col.getDisplayValue(r) for col in sheet.visibleCols])
