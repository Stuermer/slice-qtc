import os.path
import pathlib

from slice.slice import Slice, Channel


def test_qtc_attributes():
    qtc = Slice(debug=True)
    # get all writable Slice attributes
    writeable = [
        attr
        for attr, value in vars(Slice).items()
        if isinstance(value, property) and value.fset is not None
    ]

    # test readable attributes
    for attr in dir(qtc):
        if isinstance(getattr(type(qtc), attr, None), property):
            assert getattr(qtc, attr) is None or (None, None, None, None)

        # test writable attributes
        if attr in writeable:
            # test single value
            assert setattr(qtc, attr, 1.0) is None
            # test tuple
            assert setattr(qtc, attr, (1.0, 1.0, 1.0, 1.0)) is None
            # test list
            assert setattr(qtc, attr, [1.0, 1.0, 1.0, 1.0]) is None


def test_channel_attributes():
    # get writable channel attributes:
    writeable = [
        attr
        for attr, value in vars(Channel).items()
        if isinstance(value, property) and value.fset is not None
    ]

    qtc = Slice(debug=True)

    for attr in dir(qtc.ch1):
        if isinstance(getattr(type(qtc.ch1), attr, None), property):
            val = getattr(qtc.ch1, attr)
            assert val is None
        if attr in writeable:
            assert setattr(qtc.ch1, attr, 1.0) is None


def test_settings_to_file():
    qtc = Slice(debug=True)
    qtc.save_json("test.json")
    assert os.path.isfile("test.json")
    qtc.load_json("test.json")
    pathlib.Path.cwd().joinpath("test.json").unlink(missing_ok=True)


def test_save():
    qtc = Slice(debug=True)
    qtc.save()


def test_temperature_lookup():
    qtc = Slice(debug=True)
    qtc.TEMPLUT()


def test_status_print(capfd):
    qtc = Slice(debug=True)
    qtc.print_status(temperatures=False, pid=False)
    out, err = capfd.readouterr()
    assert len(out.split("\n")) == 5

    qtc.print_status(temperatures=True, pid=False)
    out, err = capfd.readouterr()
    assert len(out.split("\n")) == 8

    qtc.print_status(temperatures=True, pid=True)
    out, err = capfd.readouterr()
    assert len(out.split("\n")) == 22

    qtc.print_status(temperatures=False, pid=True)
    out, err = capfd.readouterr()
    assert len(out.split("\n")) == 19

    qtc.print_status(temperatures=True, pid=True, channels=[1, 3, 4])
    out, err = capfd.readouterr()
    assert len(out.split("\n")) == 22
