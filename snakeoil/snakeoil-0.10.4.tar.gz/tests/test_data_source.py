from functools import partial

import pytest
from snakeoil import compression, data_source


class TestDataSource:

    supports_mutable = True

    @pytest.fixture(autouse=True)
    def _setup(self, tmp_path):
        self.dir = tmp_path

    def get_obj(self, data="foonani", mutable=False):
        return data_source.data_source(data, mutable=mutable)

    def _test_fileobj_ro(self, attr, converter=str):
        obj = self.get_obj()
        # ensure that requesting mutable from an immutable isn't allowed
        with pytest.raises(TypeError):
            getattr(obj, attr)(True)
        with getattr(obj, attr)() as handle:
            assert handle.read() == converter("foonani")
            with pytest.raises(handle.exceptions):
                handle.write(converter("monkey"))

    def _test_fileobj_wr(self, attr, converter=str):
        obj = self.get_obj(mutable=True)
        handle_f = getattr(obj, attr)
        with handle_f() as f:
            assert f.read() == converter("foonani")
        with handle_f(True) as f:
            f.write(converter("dar"))
        with handle_f(True) as f:
            assert f.read() == converter("darnani")

    def test_text_fileobj(self):
        self._test_fileobj_ro("text_fileobj", str)
        if self.supports_mutable:
            self._test_fileobj_wr("text_fileobj", str)

    def test_bytes_fileobj(self):
        self._test_fileobj_ro("bytes_fileobj", lambda s: s.encode())
        if self.supports_mutable:
            self._test_fileobj_wr("bytes_fileobj", lambda s: s.encode())

    def assertContents(self, reader, writer):
        with reader.bytes_fileobj() as reader_f:
            reader_data = reader_f.read()
        with writer.bytes_fileobj() as writer_f:
            writer_data = writer_f.read()
        assert reader_data == writer_data

    def _mk_data(self, size=(100000)):
        return ''.join(str(x % 10) for x in range(size))

    def test_transfer_to_data_source(self):
        data = self._mk_data()
        reader = self.get_obj(data=data)
        if self.supports_mutable:
            writer = self.get_obj(data='', mutable=True)
        else:
            writer = data_source.data_source('', mutable=True)
        reader.transfer_to_data_source(writer)

        self.assertContents(reader, writer)

    def test_transfer_to_path(self, tmp_path):
        data = self._mk_data()
        reader = self.get_obj(data=data)
        if isinstance(reader, data_source.bz2_source):
            writer = data_source.bz2_source(tmp_path / 'transfer_to_path', mutable=True)
        else:
            writer = data_source.local_source(tmp_path / 'transfer_to_path', mutable=True)

        reader.transfer_to_path(writer.path)

        self.assertContents(reader, writer)

    def test_transfer_data_between_files(self):
        data = self._mk_data()
        reader = self.get_obj(data=data)
        if self.supports_mutable:
            writer = self.get_obj(data='', mutable=True)
        else:
            writer = data_source.data_source('', mutable=True)

        with reader.bytes_fileobj() as reader_f, writer.bytes_fileobj(True) as writer_f:
            data_source.transfer_between_files(reader_f, writer_f)

        self.assertContents(reader, writer)


class TestLocalSource(TestDataSource):

    def get_obj(self, data="foonani", mutable=False, test_creation=False):
        self.fp = self.dir / "localsource.test"
        if not test_creation:
            mode = None
            if isinstance(data, bytes):
                mode = 'wb'
            elif mode is None:
                mode = 'w'
            with open(self.fp, mode) as f:
                f.write(data)
        return data_source.local_source(self.fp, mutable=mutable)

    def test_bytes_fileobj(self):
        data = b"foonani\xf2"
        obj = self.get_obj(data=data)
        # this will blow up if tries to ascii decode it.
        with obj.bytes_fileobj() as f:
            assert f.read() == data

    def test_bytes_fileobj_create(self):
        data = b"foonani\xf2"
        obj = self.get_obj(test_creation=True, mutable=True)
        # this will blow up if tries to ascii decode it.
        with obj.bytes_fileobj(True) as f:
            assert f.read() == b''
            f.write(data)
        with obj.bytes_fileobj() as f:
            assert f.read() == data


class TestBz2Source(TestDataSource):

    def get_obj(self, data="foonani", mutable=False, test_creation=False):
        self.fp = self.dir / "bz2source.test.bz2"
        if not test_creation:
            if isinstance(data, str):
                data = data.encode()
            with open(self.fp, 'wb') as f:
                f.write(compression.compress_data('bzip2', data))
        return data_source.bz2_source(self.fp, mutable=mutable)

    def test_bytes_fileobj(self):
        data = b"foonani\xf2"
        obj = self.get_obj(data=data)
        # this will blow up if tries to ascii decode it.
        with obj.bytes_fileobj() as f:
            assert f.read() == data


class Test_invokable_data_source(TestDataSource):

    supports_mutable = False

    def get_obj(self, data="foonani", mutable=False):
        if isinstance(data, str):
            data = data.encode("utf8")
        return data_source.invokable_data_source(
            partial(self._get_data, data))

    @staticmethod
    def _get_data(data, is_text=False):
        if is_text:
            data = data.decode("utf8")
            return data_source.text_ro_StringIO(data)
        return data_source.bytes_ro_StringIO(data)


class Test_invokable_data_source_wrapper_text(Test_invokable_data_source):

    supports_mutable = False
    text_mode = True

    def get_obj(self, mutable=False, data="foonani"):
        return data_source.invokable_data_source.wrap_function(
            partial(self._get_data, data),
            self.text_mode)

    def _get_data(self, data='foonani'):
        if isinstance(data, str):
            if not self.text_mode:
                return data.encode("utf8")
        elif self.text_mode:
            return data.encode("utf8")
        return data


class Test_invokable_data_source_wrapper_bytes(Test_invokable_data_source_wrapper_text):

    text_mode = False
