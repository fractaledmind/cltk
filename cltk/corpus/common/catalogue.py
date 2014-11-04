CORPORA = {
    "greek_corpus_perseus": {
        "encoding": "utf-8",
        "languages": [
            "greek"
        ],
        "location": "https://github.com/cltk/greek_treebank_perseus/raw/master/greek_treebank_perseus.tar.gz",
        "markup": "tei_xml",
        "name": "perseus",
        "retrieval": "remote",
        "type": "text"
    },
    "greek_training_set_sentence": {
        "encoding": "utf-8",
        "languages": [
            "greek"
        ],
        "location": "https://github.com/cltk/greek_training_set_sentence/blob/master/greek.tar.gz",
        "markup": "plaintext",
        "name": "training_set_sentence",
        "retrieval": "remote",
        "type": "training_set"
    },
    "greek_treebank_perseus": {
        "encoding": "utf-8",
        "languages": [
            "greek"
        ],
        "location": "https://github.com/cltk/greek_treebank_perseus/blob/master/greek_treebank_perseus.tar.gz",
        "markup": "xml",
        "name": "perseus_treebank",
        "retrieval": "remote",
        "type": "treebank"
    },
    "latin_corpus_lacus_curtius": {
        "encoding": "utf-8",
        "languages": [
            "latin"
        ],
        "location": "https://github.com/cltk/latin_corpus_lacus_curtius/blob/master/lacus_curtius.tar.gz",
        "markup": "plaintext",
        "name": "lacus_curtius",
        "retrieval": "remote",
        "type": "text"
    },
    "latin_corpus_latin_library": {
        "encoding": "utf-8",
        "languages": [
            "latin"
        ],
        "location": "https://github.com/cltk/latin_corpus_latin_library/blob/master/latin_library.tar.gz",
        "markup": "plaintext",
        "name": "latin_library",
        "retrieval": "remote",
        "type": "text"
    },
    "latin_corpus_perseus": {
        "encoding": "utf-8",
        "languages": [
            "latin"
        ],
        "location": "https://github.com/cltk/latin_corpus_perseus/raw/master/latin_corpus_perseus.tar.gz",
        "markup": "tei_xml",
        "name": "perseus",
        "retrieval": "remote",
        "type": "text"
    },
    "latin_training_set_sentence": {
        "encoding": "utf-8",
        "languages": [
            "latin"
        ],
        "location": "https://github.com/cltk/latin_training_set_sentence/blob/master/latin.tar.gz",
        "markup": "plaintext",
        "name": "training_set_sentence",
        "retrieval": "remote",
        "type": "training_set"
    },
    "latin_treebank_perseus": {
        "encoding": "utf-8",
        "languages": [
            "latin"
        ],
        "location": "https://github.com/cltk/latin_treebank_perseus/raw/master/latin_treebank_perseus.tar.gz",
        "markup": "xml",
        "name": "perseus_treebank",
        "retrieval": "remote",
        "type": "treebank"
    },
    "phi5": {
        "encoding": "latin-1",
        "languages": [
            "latin",
            "coptic"
        ],
        "markup": "phi_beta_code",
        "name": "phi5",
        "retrieval": "local",
        "type": "text"
    },
    "phi7": {
        "encoding": "latin-1",
        "languages": [
            "greek",
            "latin"
        ],
        "markup": "phi_beta_code",
        "name": "phi7",
        "retrieval": "local",
        "type": "text"
    },
    "tlg": {
        "encoding": "latin-1",
        "languages": [
            "greek"
        ],
        "markup": "tlg_beta_code",
        "name": "tlg",
        "retrieval": "local",
        "type": "text"
    }
}


def get_all(key):
    if key.endswith('s'):       # for `languages`
        flat_l = [x for k, v in CORPORA.items()
                  for x in v[key]]
        return list(set(flat_l))
    else:
        return list(set([v[key] for k, v in CORPORA.items()]))


def filter_corpora(**kwargs):
    corpora = CORPORA.keys()
    for key, query in kwargs.items():
        corpora = [k for k, v in CORPORA.items()
                   if k in corpora
                   if query in v[key]]
    return list(set(corpora))


# Information about the various attributes
encodings = get_all('encoding')
languages = get_all('languages')
markups = get_all('markup')
retrievals = get_all('retrieval')
types = get_all('type')

# Lists of corpora based on attribute queries
## Language collections
greek_corpora = filter_corpora(languages='greek')
latin_corpora = filter_corpora(languages='latin')
## Markup collections
xml_corpora = filter_corpora(markup='xml')
beta_code_corpora = filter_corpora(markup='beta_code')
plain_corpora = filter_corpora(markup='plain')
## Retrieval collections
local_corpora = filter_corpora(retrieval='local')
remote_corpora = filter_corpora(retrieval='remote')
## Type collections
text_corpora = filter_corpora(type='text')
treebank_corpora = filter_corpora(type='treebank')
training_corpora = filter_corpora(type='training')
