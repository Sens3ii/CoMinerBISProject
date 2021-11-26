__hearst_patterns = [
    (
        '(NP_\\w+ (, )?such as (NP_\\w+ ?(, )?(and |or )?)+)',
        'first'  # H1
    ),
    (
        '(NP_\\w+ (, )?especially (NP_\\w+ ?(, )?(and |or )?)+)',  # H2
        'first'
    ),
    (
        '(NP_\\w+ (, )?include (NP_\\w+ ?(, )?(and |or )?)+)',  # H3
        'first'
    ),
]

__queries = [
    "{EN} versus",
    "versus {EN}",
    "{EN} or",
    "or {EN} ",
    "especially {EN} and",
    "including {EN} and",
    "such as {EN} or"
]
