import csv
import os
import urllib.request

class FileLoaderMixin():
    """ The FileLoaderMixin loads files either locally or remotely from Github (if run from an ipython notebook)

    Currently supported filetypes are: .csv, .txt

    """

    def load_file(self, file_path):

        # make sure that we only try to load supported file types
        supported_file_types = {'.csv', '.txt'}
        current_file_type = file_path[file_path.rfind('.'):]
        if not current_file_type in supported_file_types:
            raise ValueError("The FileLoaderMixin currently supports {supported_file_types} but not "
                             "{current_file_type}.")

        # check if we are working locally and in the correct directory
        # __file__ is only available if executed from a file but not from an ipython shell or notebook
        # in those cases, the file has to be loaded remotely from github.
        try:
            local_path = os.path.abspath(os.path.dirname(__file__))
            is_local = True
            if not local_path.endswith('/gender_novels'):
                is_local = False
                print(f"WARNING: The FileLoaderMixin should be placed in the main path of the gender_novels project."
                      f"It's currently in {local_path}. Until the Mixin is in the correct path, files are loaded " \
                      f"from Github.")
        except NameError:
            is_local = False

        if is_local:
            print(f'loading {file_path} locally.')
            return self._load_file_locally(file_path)
        else:
            print(f'loading {file_path} remotely')
            return self._load_file_remotely(file_path)


    def _load_file_locally(self, file_path):



        # I need a way of getting the local path to the base of the repo. This file is currently in the base of the
        # repo so it returns the correct path. But it will change once this function gets moved.
        local_base_path = os.path.abspath(os.path.dirname(__file__))
        file = open(f'{local_base_path}/{file_path}', mode='r')

        if file_path.endswith('.csv'):
            result = file.readlines()
        elif file_path.endswith('.txt'):
            result = file.read()

        file.close()
        return result

    def _load_file_remotely(self, file_path):

        base_path = 'https://raw.githubusercontent.com/dhmit/gender_novels/master/'
        url = f'{base_path}/{file_path}'
        response = urllib.request.urlopen(url)

        if url.endswith('.csv'):
            return [line.decode('utf8') for line in response.readlines()]
        elif url.endswith('.txt'):
            return response.read().decode('utf8')

class Corpus(FileLoaderMixin):

    def __init__(self, corpus_name):
        self.corpus_name = corpus_name
        print("here", type(self))
        self.novels = self._load_novels()

    def _load_novels(self):

        novels = []

        csv_path = f'corpora/{self.corpus_name}/{self.corpus_name}.csv'
        csv_file = self.load_file(csv_path)
        csv_reader = csv.DictReader(csv_file)

        for novel_metadata in csv_reader:
            novel_metadata['corpus_name'] = self.corpus_name
            novels.append(Novel(novel_metadata_dict=novel_metadata))

        return novels

    def load_sample_novels_by_authors(self):
        """ Use this function to get the sample novel texts as four variables
        >>> c = Corpus('sample_novels')
        >>> austen, dickens, eliot, hawthorne = c.load_sample_novels_by_authors()

        :return:
        """

        assert self.corpus_name == 'sample_novels'

        austen = self.novels[0].text
        dickens = self.novels[1].text
        eliot = self.novels[2].text
        hawthorne = self.novels[3].text

        return austen, dickens, eliot, hawthorne

class Novel(FileLoaderMixin):

    def __init__(self, novel_metadata_dict):
        for k, v in novel_metadata_dict.items():
            setattr(self, k, v)

        # Check that the essential attributes for the novel exists.
        # Currently available attributes that are not checked are: country_publication, author_gender, and notes.
        assert hasattr(self, 'author')
        assert hasattr(self, 'date')
        assert hasattr(self, 'title')
        assert hasattr(self, 'corpus_name')
        assert hasattr(self, 'filename')


        if not hasattr(self, 'text'):
            file_path = f'corpora/{self.corpus_name}/texts/{self.filename}'
            self.text = self.load_file(file_path)

            # Extract Project Gutenberg Boilerplate
            if self.text.find('*** START OF THIS PROJECT GUTENBERG EBOOK') > -1:
                end_intro_boilerplate = self.text.find('*** START OF THIS PROJECT GUTENBERG EBOOK')
                start_novel = self.text.find('***', end_intro_boilerplate + 5) + 3 # second set of *** indicates start
                end_novel = self.text.find('*** END OF THIS PROJECT GUTENBERG EBOOK')

                self.text = self.text[start_novel:end_novel]
                print(self.text[:100])


if __name__ == '__main__':

    c = Corpus('sample_novels')
