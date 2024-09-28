from sphinxcontrib_nixdomain._utils import option_key_fun, option_lt, split_attr_path

# ruff: noqa: D100, D103, S101


def test_options_sorting_lt() -> None:
    assert option_lt("a.a.a", "a.a.b")
    assert option_lt("a.a.a", "a.b.a")
    assert option_lt("a.a.a", "b.a.a")
    assert not option_lt("a.a.b", "a.a.a")
    assert not option_lt("a.b.a", "a.a.a")
    assert not option_lt("b.a.a", "a.a.a")

    assert option_lt("a.a.enable", "a.a.a")
    assert not option_lt("a.a.a", "a.a.enable")

    assert option_lt("a.a", "a.a.enable")
    assert not option_lt("a.a.enable", "a.a")


def test_options_sorting_key_fun() -> None:
    assert sorted(
        [
            "b.a.c.enable",
            "b.a.c",
            "a.b.c",
            "b.a.c.d",
            "b.b.a",
        ],
        key=option_key_fun,
    ) == [
        "a.b.c",
        "b.a.c",
        "b.a.c.enable",
        "b.a.c.d",
        "b.b.a",
    ]


def test_options_path_split() -> None:
    assert split_attr_path('services.javaThingy.settings."com.package/config"') == [
        "services",
        "javaThingy",
        "settings",
        '"com.package/config"',
    ]

    assert split_attr_path('a.b."hello".b."bla\\"bla"."".enable') == [
        "a",
        "b",
        '"hello"',
        "b",
        '"bla\\"bla"',
        '""',
        "enable",
    ]
