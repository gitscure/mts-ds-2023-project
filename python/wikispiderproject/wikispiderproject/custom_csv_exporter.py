from scrapy.exporters import CsvItemExporter

class CustomCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['delimiter'] = ';'
        super().__init__(*args, **kwargs)
