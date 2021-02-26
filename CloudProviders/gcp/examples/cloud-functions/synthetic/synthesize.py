import hypothesis_jsonschema as hjs
import random
from hypothesis import strategies as st
import string


def gen_uniques(generator, n: int):
    seen_to_val = {}
    attempts = 0

    while len(seen_to_val) < n and attempts < 50:
        v = generator.example()
        str_v = str(v)
        if str_v not in seen_to_val:  # str to make dict comparison easy
            seen_to_val[str_v] = v
        attempts += 1

    return list(seen_to_val.values())


strats = {
    'ascii': st.text(alphabet=string.ascii_letters, min_size=6, max_size=25),
    'short_ascii': st.text(alphabet=string.ascii_letters, min_size=2, max_size=6),
    'long_ascii':  st.text(alphabet=string.ascii_letters, min_size=50),
    'money': st.decimals(min_value=-1e+8, max_value=1e+8, places=2),
    'date': st.dates().map(str)
    }


def generate_examples(dataset: str, schema, n: int = 10):

    n = 10 if not n else n
    gen_num = int(n**0.5)

    hjs.from_schema(schema).example()  # force local reference resolution/substitution

    properties = schema['properties'][dataset]['properties']
    examples = {p: gen_uniques(hjs.from_schema(properties[p], custom_formats=strats), gen_num) for p in properties}

    return [{p: random.choice(examples[p]) for p in properties} for _ in range(n)]
