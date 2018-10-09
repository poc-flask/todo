from core import utils


def test_parse_string_to_datetime(fake):
    """Test parse string to date time"""
    test_date = fake.date_time()
    datetime_as_string = test_date.strftime('%Y-%m-%dT%H:%M:%S')
    converted_datetime = utils.date_time_parsing(datetime_as_string, 'a test case')

    assert test_date == converted_datetime


def test_parse_invalid_string_to_date(fake):
    """Test parse invalid string to date time"""
    test_date = fake.date_time()
    datetime_as_string = test_date.strftime('%Y-%m-%dT%H:%M')
    try:
        utils.date_time_parsing(datetime_as_string, 'a test case')
    except ValueError:
        assert True


def test_parse_datetime_to_string(fake):
    """Test parse datetime to string"""
    test_date = fake.date_time()
    datetime_as_string = test_date.strftime('%Y-%m-%dT%H:%M:%S')

    serializeDateTime = utils.SerializeDateTime()
    output = serializeDateTime.format(test_date)

    assert datetime_as_string == output
    

def test_parse_error_datetime_to_string():
    """Test parse error datetime to string"""
    datetime_as_string = "A String"

    serializeDateTime = utils.SerializeDateTime()
    output = serializeDateTime.format(datetime_as_string)

    assert None == output
