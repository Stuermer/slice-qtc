from slice.slice import Slice, Channel


def test_qtc_attributes():
    qtc = Slice(debug=True)

    for attr in dir(qtc):
        if isinstance(getattr(type(qtc), attr, None), property):
            assert getattr(qtc, attr) is None


def test_channel_attributes():
    # get writable channel attributes:
    writeable = [attr for attr, value in vars(Channel).items() if
                 isinstance(value, property) and value.fset is not None]

    qtc = Slice(debug=True)

    for attr in dir(qtc.ch1):
        if isinstance(getattr(type(qtc.ch1), attr, None), property):
            val = getattr(qtc.ch1, attr)
            assert val is None
        if attr in writeable:
            assert setattr(qtc.ch1, attr, 1.0) is None
