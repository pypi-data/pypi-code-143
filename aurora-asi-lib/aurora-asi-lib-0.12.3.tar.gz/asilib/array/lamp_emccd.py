from datetime import datetime, timedelta
import re
import warnings
import pathlib
import copy

import numpy as np
import scipy.io

import asilib
import asilib.utils as utils
import asilib.io.download as download


image_base_url = 'https://ergsc.isee.nagoya-u.ac.jp/psa-pwing/pub/raw/lamp/sav_img/'
skymap_base_url = 'https://ergsc.isee.nagoya-u.ac.jp/psa-pwing/pub/raw/lamp/sav_fov/'
local_base_dir = asilib.config['ASI_DATA_DIR'] / 'lamp_emccd'


def lamp(location_code, time=None, time_range=None, redownload=False, missing_ok=True, alt=90):
    """
    Create an Imager instance using the LAMP's ground-based EMCCD ASI.

    Parameters
    ----------
    location_code: str
        The ASI's location code (four letters).
    time: str or datetime.datetime
        A time to look for the ASI data at. Either time or time_range
        must be specified (not both or neither).
    time_range: list
        A length 2 list of string-formatted times or datetimes to bracket
        the ASI data time interval.
    redownload: bool
        If True, will download the data from the internet, regardless of
        wether or not the data exists locally (useful if the data becomes
        corrupted).
    missing_ok: bool
        Wether to allow missing data files inside time_range (after searching
        for them locally and online).
    alt: int
        The mapping altitude.
    """
    if location_code.lower() == 'vee':
        meta = {
            'array': 'LAMP',
            'location': 'VEE',
            'lat': 67.0139,
            'lon': -146.4186,
            'alt': 0.174,
            'cadence': 0.01,
            'resolution': (256, 256),
        }
    elif location_code.lower() == 'pkf':
        meta = {
            'array': 'LAMP',
            'location': 'PKF',
            'lat': 65.1256,
            'lon': -147.4919,
            'alt': 0.213,
            'cadence': 0.01,
            'resolution': (256, 256),
        }
    else:
        raise NotImplementedError

    _skymap = load_skymap(location_code, alt, redownload)
    skymap = {
        'lat': _skymap['gla'],
        'lon': _skymap['glo'],
        'alt': alt,
        'el': _skymap['ele'],
        'az': _skymap['azm'],
        'path': _skymap['path'],
    }

    # Download and find one-minute image file(s). If the user supplies both or
    # neither time and time_range, the loader will crash here.
    file_paths = _get_files(location_code, time, time_range, redownload, missing_ok)

    if time_range is not None:  # Prepare the loader for multiple files
        start_times = len(file_paths) * [None]
        end_times = len(file_paths) * [None]
        for i, file_path in enumerate(file_paths):
            date_match = re.search(r'\d{8}_\d{4}', file_path.name)
            start_times[i] = datetime.strptime(date_match.group(), '%Y%m%d_%H%M')
            end_times[i] = start_times[i] + timedelta(minutes=1)

        data = {
            'path': file_paths,
            'start_time': start_times,
            'end_time': end_times,
            'loader': lamp_reader,
            'time_range': time_range,
        }

    elif time is not None:  # Load the LAMP file and find the nearest time and image.
        _times, _images = lamp_reader(file_paths[0])
        image_index = np.argmin(np.abs([(time - t_i).total_seconds() for t_i in _times]))
        if np.abs((time - _times[image_index]).total_seconds()) > meta['cadence']:
            raise IndexError(
                f'Cannot find a time stamp within of {meta["cadence"]} s of '
                f'{time}. Closest time stamp is {_times[image_index]}.'
            )
        data = {'time': _times[image_index], 'image': _images[image_index]}
    else:
        raise ValueError(
            "Not sure we got here. Whoops! You need to provide either a " "time or time_range."
        )
    return asilib.Imager(data, meta, skymap)


def _get_files(location_code, time, time_range, redownload, missing_ok):
    """ """
    if (time is None) and (time_range is None):
        raise ValueError('time or time_range must be specified.')
    elif (time is not None) and (time_range is not None):
        raise ValueError('both time and time_range can not be simultaneously specified.')

    local_dir = local_base_dir / 'images' / location_code.lower()

    # Find one image file.
    if time is not None:
        time = utils.validate_time(time)
        filename = f'{location_code.lower()}_{time.strftime("%Y%m%d_%H%M")}.sav'
        file_paths = list(pathlib.Path(local_dir).rglob(filename))

        if (len(file_paths) == 0) or redownload:
            d = download.Downloader(image_base_url + f'/{filename}')
            file_paths = d.download(local_dir, redownload=redownload, stream=True)
        else:
            return file_paths

    # Find multiple image files.
    if time_range is not None:
        time_range = utils.validate_time_range(time_range)
        file_times = utils.get_filename_times(time_range, dt='minutes')
        file_paths = []

        for file_time in file_times:
            filename = f'{location_code.lower()}_{file_time.strftime("%Y%m%d_%H%M")}.sav'
            _matched_file_paths = list(pathlib.Path(local_dir).rglob(filename))

            if redownload:
                d = download.Downloader(image_base_url + f'/{filename}')
                file_paths.append(d.download(local_dir, redownload=redownload, stream=True))
            else:
                if len(_matched_file_paths) == 1:
                    file_paths.append(_matched_file_paths[0])

                elif len(_matched_file_paths) == 0:
                    d = download.Downloader(image_base_url + f'/{filename}')
                    try:
                        file_paths.append(d.download(local_dir, redownload=redownload, stream=True))
                    except (FileNotFoundError, AssertionError, ConnectionError) as err:
                        if missing_ok and (
                            ('does not contain any hyper references containing' in str(err))
                            or ('Only one href is allowed' in str(err))
                            or ('error response' in str(err))
                        ):
                            continue
                        raise
                else:
                    raise ValueError(f'{len(_matched_file_paths)} files found.')
    return file_paths


def lamp_reader(file_path):
    """ """
    sav_data = scipy.io.readsav(str(file_path), python_dict=True)
    images = np.moveaxis(sav_data['img'], 2, 0)
    # images = images[:, :, :]  # Flip from column- to row-major.
    times = np.array(
        [
            datetime(y, mo, d, h, m, s, 1000 * ms)
            for y, mo, d, h, m, s, ms in zip(
                sav_data['yr'],
                sav_data['mo'],
                sav_data['dy'],
                sav_data['hh'],
                sav_data['mm'],
                sav_data['ss'],
                sav_data['ms'],
            )
        ]
    )
    return times, images


def find_skymap(location_code, alt, redownload=True):
    """
    Find the path to the skymap file.
    """
    local_dir = local_base_dir / 'skymaps' / location_code.lower()

    # Check if the skymaps are already downloaded.
    local_skymap_paths = list(pathlib.Path(local_dir).rglob(f'{location_code.lower()}*.sav'))

    if (len(local_skymap_paths) == 0) or redownload:
        # Download the skymaps.
        d = download.Downloader(skymap_base_url)
        ds = d.ls(f'{location_code.lower()}_*.sav')
        local_skymap_paths = []
        for d in ds:
            local_skymap_paths.append(d.download(local_dir))

    for local_skymap_path in local_skymap_paths:
        if local_skymap_path.name == f'{location_code.lower()}_{alt:03}.sav':
            return local_skymap_path

    raise FileNotFoundError(
        f'Unable to find the "{location_code.lower()}_{alt:03}.sav" LAMP skymap.'
    )


def load_skymap(location_code, alt, redownload):
    """
    Load the skymap file and apply the transformations.
    """
    skymap_path = find_skymap(location_code, alt, redownload)
    skymap = _load_skymap(skymap_path)
    skymap = _tranform_longitude_to_180(skymap)
    skymap = _transform_azimuth_to_180(skymap)
    # skymap = _flip_skymap(skymap)
    return skymap


def _load_skymap(skymap_path):
    """
    A helper function to load a THEMIS skymap and transform it.
    """
    # Load the skymap file and convert it to a dictionary.
    _skymap_dict = scipy.io.readsav(str(skymap_path), python_dict=True)
    skymap_dict = copy.deepcopy(_skymap_dict)

    for key, val in skymap_dict.items():
        invalid_idx = np.where(val == -999)
        if invalid_idx[0].shape[0]:
            skymap_dict[key][invalid_idx] = np.nan

    # Mask all elevations < 0
    invalid_idx = np.where(skymap_dict['ele'] < 0)
    for key in skymap_dict.keys():
        skymap_dict[key][invalid_idx] = np.nan
    skymap_dict['path'] = skymap_path
    return skymap_dict


def _flip_skymap(skymap):
    """
    IDL is a column-major language while Python is row-major. This function
    tranposes the 2- and 3-D arrays to make them compatable with the images
    that are saved in row-major.
    """
    for key in skymap:
        if hasattr(skymap[key], 'shape'):
            shape = skymap[key].shape
            if (len(shape) == 2) and (shape[0] == shape[1]):
                skymap[key] = skymap[key][:, :]  # For Az/El maps.
    return skymap


def _tranform_longitude_to_180(skymap):
    """
    Transform the glo array from (0 -> 360) to (-180 -> 180).
    """
    # Don't take the modulus of NaNs
    valid_val_idx = np.where(~np.isnan(skymap['glo']))
    skymap['glo'][valid_val_idx] = np.mod(skymap['glo'][valid_val_idx] + 180, 360) - 180
    return skymap


def _transform_azimuth_to_180(skymap):
    """
    Transform the azm array from (-180 -> 180) to (0 -> 360).
    """
    # Don't take the modulus of NaNs
    valid_val_idx = np.where(~np.isnan(skymap['azm']))
    skymap['azm'][valid_val_idx] = np.mod(skymap['azm'][valid_val_idx], 360)
    return skymap


if __name__ == '__main__':
    import cProfile, pstats, io
    from pstats import SortKey

    with cProfile.Profile() as pr:
        img = lamp(
            'vee',
            time_range=[datetime(2022, 3, 5, 11, 0), datetime(2022, 3, 5, 11, 3)],
            # time=datetime(2022, 3, 5, 11, 0),
            redownload=False,
        )
    ps = pstats.Stats(pr).sort_stats('cumulative')
    ps.strip_dirs()
    print('Cumulative time\n', ps.print_stats(10))

    ps = pstats.Stats(pr).sort_stats('time')
    ps.strip_dirs()
    print('Total time\n', ps.print_stats(10))
