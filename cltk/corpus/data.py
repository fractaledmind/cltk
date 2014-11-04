"""Classes to access the `cltk_data/` directory tree"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'
import os

from cltk.cltk.corpus.common.catalogue import CORPORA
from cltk.cltk.data import CLTKData, CorpusError


class CorpusData(object):
    def __init__(self, name):
        self.cltk = CLTKData()
        self.key = name
        # Initialize emptry properties
        self._name = None
        self._encoding = None
        self._languages = None
        self._markup = None
        self._retrieval = None
        self._type = None
        self._location = None
        # Initialize global vars
        self.attributes = CORPORA.get(self.key, None)

  ## Attribute Properties ---------------------------------------------------

    @property
    def name(self):
        if self._name:
            return self._name
        elif self.attributes:
            return self.attributes['name']
        else:
            raise CorpusError("You haven't set `name` yet.")

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def encoding(self):
        if self._encoding:
            return self._encoding
        elif self.attributes:
            return self.attributes['encoding']
        else:
            raise CorpusError("You haven't set `encoding` yet.")

    @encoding.setter
    def encoding(self, value):
        self._encoding = value

    @property
    def languages(self):
        if self._languages:
            return self._languages
        elif self.attributes:
            return self.attributes['languages']
        else:
            raise CorpusError("You haven't set `languages` yet.")

    @languages.setter
    def languages(self, value):
        self._languages = value

    @property
    def markup(self):
        if self._markup:
            return self._markup
        elif self.attributes:
            return self.attributes['markup']
        else:
            raise CorpusError("You haven't set `markup` yet.")

    @markup.setter
    def markup(self, value):
        self._markup = value

    @property
    def retrieval(self):
        if self._retrieval:
            return self._retrieval
        elif self.attributes:
            return self.attributes['retrieval']
        else:
            raise CorpusError("You haven't set `retrieval` yet.")

    @retrieval.setter
    def retrieval(self, value):
        self._retrieval = value

    @property
    def type(self):
        if self._type:
            return self._type
        elif self.attributes:
            return self.attributes['type']
        else:
            raise CorpusError("You haven't set `type` yet.")

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def location(self):
        if self._location:
            return self._location
        elif self.attributes:
            loc = self.attributes.get('location', None)
            if not loc:
                raise CorpusError("You haven't set `location` yet.")
            return loc
        else:
            raise CorpusError("You haven't set `location` yet.")

    @location.setter
    def location(self, value):
        self._location = value

  ## Directory Properties ---------------------------------------------------

    @property
    def primary_language(self):
        if len(self.languages) == 1:
            primary_language = self.languages[0]
        elif 'greek' in self.languages:
            primary_language = 'greek'
        elif 'latin' in self.languages:
            primary_language = 'latin'
        else:
            primary_language = self.languages[0]
        return primary_language

    @property
    def parent_dir(self):
        # Set the language directory
        self.cltk.language_dir = self.primary_language
        # Prepare the corpus type directory name
        type = 'corpora' if self.type == 'text' else self.type
        type_dir = '_'.join([type, 'dir'])
        return getattr(self.cltk, type_dir)

    def _prepare_dir(self, dir_name, named):
        the_dir = os.path.join(self.parent_dir,
                               dir_name)
        if named:
            the_dir = os.path.join(the_dir,
                                   self.name)
        return self.cltk.resolve_path(the_dir)

    def originals_dir(self, named=False):
        return self._prepare_dir('originals', named)

    def structured_dir(self, named=False):
        return self._prepare_dir('structured', named)

    def plain_dir(self, named=False):
        return self._prepare_dir('plain', named)

    def readable_dir(self, named=False):
        return self._prepare_dir('readable', named)
