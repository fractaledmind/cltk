"""Classes to import and compile corpora into `cltk_data/` directory tree"""
__author__ = 'Stephen Margheim <stephen.margheim@gmail.com>'
__license__ = 'MIT License. See LICENSE.'
import os
import tarfile
import tempfile
import requests

from cltk.cltk.corpus.wrappers.tlgu import tlgu
from cltk.cltk.corpus.data import CorpusData
from cltk.cltk.data import CorpusError
from cltk.cltk import logger


class CorpusImporter(object):
    def __init__(self, corpus_obj):
        self.corpus = corpus_obj
        self.tar_file = None

    ## Main API call ----------------------------------------------------------

    def retrieve(self, location=None):
        """Retrieve corpus data and move into the corpus' `/originals`
        directory within the CLTK's `/cltk_data` directory. Corpus data
        can either be `remote` (online) or `local` (on disk).

        :param location: location of corpus data
        :type location: ``unicode``

        """
        # Set location (default to corpus attribute)
        location = self._prepare_location(location)

        # Prepare local file
        tar_name = self.corpus.name + '.tar.gz'
        self.tar_file = os.path.join(self.corpus.originals_dir(),
                                     tar_name)
        if os.path.exists(self.tar_file):
            msg = 'Tar file already exists at : {}'.format(self.tar_file)
        else:
            if self.corpus.retrieval == 'local':
                msg = 'Retrieving local data from : {}'.format(location)
                self._retrieve_local(location)
            elif self.corpus.retrieval == 'remote':
                msg = 'Retrieving remote data from : {}'.format(location)
                self._retrieve_remote(location)
            else:
                raise CorpusError('Corpus must be either `remote` or \
                                   `local`!')
        logger.info(msg)
        return True

    ### Primary two Code Paths ------------------------------------------------

    def _retrieve_local(self, path):
        """Copy compressed corpus data from `path` to
        `/originals` directory.

        :param path: file path of corpus data
        :type path: ``unicode``

        """
        if os.path.exists(path):
            # Compress directory tree into gzipped tarball
            self._dir2tar(path)
        else:
            raise CorpusError('Local path does not exist!')

    def _retrieve_remote(self, url):
        """Download corpus data from `url` and move into
        `/originals` directory.

        :param url: URL of corpus data
        :type url: ``unicode``

        """
        # Ensure reading raw data
        url = self._prepare_github_url(url)
        # Open HTTP data stream to tar data
        remote_data = requests.get(url, stream=True)
        # Write tar data to file in originals dir
        self._tar2tar(remote_data)

    #### Compress to `tar` methods --------------------------------------------

    def _tar2tar(self, tar):
        """Write a tar file to disk, without unpacking."""
        with open(self.tar_file, 'wb') as f:
            for chunk in tar.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        msg = 'Wrote tar file to : {}'.format(self.tar_file)
        logger.info(msg)

    def _dir2tar(self, path):
        """Compress an entire directory tree into a tar file."""
        with tarfile.open(self.tar_file, "w:gz") as tar:
            tar.add(path, arcname=os.path.basename(path))
        msg = 'Compressed directory at : {}'.format(path)
        logger.info(msg)

    ##### Low level helper methods --------------------------------------------

    def _prepare_github_url(self, url):
        """Ensure GitHub url points to raw data."""
        if url.startswith('https://github.com/'):
            if not url.endswith('?raw=true'):
                url = url + '?raw=true'
            return url
        else:
            raise CorpusError('Remote corpus must be in GitHub repo!')

    def _prepare_location(self, location):
        """Set `location`, default to corpus attribute."""
        if location is None:
            return self.corpus.location
        else:
            return location


class CorpusCompiler(object):
    def __init__(self, corpus_obj):
        self.corpus = corpus_obj

    ## Main API call ----------------------------------------------------------

    def compile(self):
        """Unpack original tarfile into directory tree
        with fully structured files.

        """
        dir_path = self.corpus.structured_dir(named=True)
        check = self._path_exists(dir_path)
        if not check:
            if self.corpus.encoding == 'latin-1':
                self._compile_binary()
            elif self.corpus.encoding == 'utf-8':
                self._compile_unicode()
            else:
                raise CorpusError()
        else:
            msg = 'Structured dir already exists at : {}'.format(dir_path)
            logger.info(msg)
        return True

    def _path_exists(self, path):
        if os.path.exists(path):
            if os.listdir(path):
                print(path)
                return True
            else:
                return False
        else:
            return False

    ### Primary two Code Paths ------------------------------------------------

    def _compile_binary(self):
        msg = 'Starting `{}` corpus compilation'.format(self.corpus.name)
        logger.info(msg)

        # Define function to process files within tar
        def process(tar, file):
            # Ignore non-text files
            if ((not file.name.endswith('.IDT') or file.name.endswith('.BIN'))
               and file.isfile()):
                orig_content = tar.extractfile(file).read()
                struct_file = os.path.basename(file.name).lower()
                struct_path = os.path.join(self.corpus.structured_dir(True),
                                           struct_file)
                with tempfile.NamedTemporaryFile(suffix='.txt') as temp:
                    temp.write(orig_content)
                    # Use `tlgu` utility to compile to Unicode text
                    tlgu.convert(temp.name,
                                 markup='full',
                                 break_lines=True,
                                 divide_works=False,
                                 output_path=struct_path)
                msg = 'Compiled {} to : {}'.format(file.name, struct_path)
                logger.info(msg)
        return self.unpack_tar(process)

    def _compile_unicode(self):
        msg = 'Starting `{}` corpus compilation'.format(self.corpus.name)
        logger.info(msg)

        # Define function to process files within tar
        def process(tar, file):
            if file.isfile():
                struct_file = file.name.lower()
                struct_path = os.path.join(self.corpus.structured_dir(),
                                           struct_file)
                tar.extractall(self.corpus.structured_dir())
                msg = 'Compiled {} to : {}'.format(file.name, struct_path)
                logger.info(msg)
        return self.unpack_tar(process)

    #### Tar Unpacker ---------------------------------------------------------

    def unpack_tar(self, process):
        """Unpack original tarfile using `process` function.

        """
        tar_file = os.path.join(self.corpus.originals_dir(),
                                self.corpus.name + '.tar.gz')
        # Iterate over original files
        with tarfile.open(tar_file, "r") as tar:
            for file in tar.getmembers():
                process(tar, file)
        return True


def retrieve(arg, location=None):
    """Wrapper function to utilize `CorpusImporter` class

    """
    corpus = CorpusData(arg)
    importer = CorpusImporter(corpus)
    return importer.retrieve(location=location)


def compile(arg):
    """Wrapper function to utilize `CorpusCompiler` class

    """
    corpus = CorpusData(arg)
    compiler = CorpusCompiler(corpus)
    return compiler.compile()


def download(arg=None, location=None):
    """Wrapper function to retrieve and compile a corpus.

    """
    if arg is None:
        # Download all
        return 'all'
    elif isinstance(arg, list):
        # Download set
        return 'set'
    elif isinstance(arg, str):
        # Download one
        retrieve(arg, location=location)
        compile(arg)
        return True
