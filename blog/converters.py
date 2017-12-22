class FourDigitYearConverter:
    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value
        
class TwoDigitMonthConverter:
    regex = '[0-1]{1}[0-9]{1}'
    
    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%02d' % value
        
class TwoDigitDayConverter:
    regex = '[0-3]{1}[0-9]{1}'
    
    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%02d' % value