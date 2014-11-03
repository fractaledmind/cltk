"""Classes to access the `cltk_data/` directory tree"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'

import os
import site

from cltk.cltk.config import CLTK_DATA
from cltk.cltk import logger


class CorpusError(Exception):
    pass


class CLTKData(object):
    """This class provides access to the full directory tree of `cltk_data/`.
    The basic structure of the `cltk_data/` directory is:
        ```
        cltk_data/
            {language}/
                text_corpora/
                    originals/
                        {corpus}/
                    structured/
                        {corpus}/
                    plain/
                        {corpus}/
                    readable/
                        {corpus}/
                treebank/
                    {corpus}/
                training_set/
                    {corpus}/
        ```
    Users can set the path to `cltk_data/` via the ``data_path`` property.
    When dealing with a particular corpus, users will also need to set the
    ``language_dir`` property properly in order to access the corpus.

    """
    def __init__(self):
        self._data_path = None
        self._language_dir = None

  ## Base `cltk_data/` directory --------------------------------------------

    @property
    def data_path(self):
        if self._data_path:
            return self.resolve_path(self._data_path)
        else:
            return self.resolve_path(CLTK_DATA)

    @data_path.setter
    def data_path(self, value):
        self._data_path = value

  ## 2nd level language directories -----------------------------------------

    @property
    def language_dir(self):
        if self._language_dir:
            return self.resolve_path(os.path.join(self.data_path,
                                                  self._language_dir))
        else:
            # TODO: Fix error message
            raise CorpusError('Define `language_dir`!')

    @language_dir.setter
    def language_dir(self, value):
        self._language_dir = value

    ## 3rd level corpus type directories --------------------------------------

    @property
    def corpora_dir(self):
        return self.resolve_path(os.path.join(self.language_dir,
                                              'text_corpora'))

    @property
    def treebank_dir(self):
        return self.resolve_path(os.path.join(self.language_dir,
                                              'treebank'))

    @property
    def training_dir(self):
        return self.resolve_path(os.path.join(self.language_dir,
                                              'training_set'))

    ## Misc. ------------------------------------------------------------------

    # What does this do?
    @property
    def bin_path(self):
        return os.path.join(site.getsitepackages()[0], 'cltk')

    def resolve_path(self, path):
        # Resolve absolute path
        if os.path.isabs(path):
            full_path = path
        elif path.startswith('~'):
            full_path = os.path.expanduser(path)
        elif path.startswith('.'):
            full_path = os.path.abspath(path)
        # Ensure absolute path exists
        if not os.path.exists(full_path):
            # If directory
            if os.path.splitext(full_path)[1] == '':
                os.makedirs(full_path)
                logger.info('Directory created at : {}'.format(full_path))
            # If file
            else:
                open(full_path).close()
                logger.info('File created at : {}'.format(full_path))
        return full_path


# Alias
cltk_data = CLTKData()
