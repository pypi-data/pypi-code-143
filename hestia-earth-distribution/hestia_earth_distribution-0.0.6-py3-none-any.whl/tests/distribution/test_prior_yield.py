from unittest.mock import patch
import os
from tests.utils import fixtures_path
from hestia_earth.distribution.utils.priors import read_prior_stats

from hestia_earth.distribution.prior_yield import (
    generate_prior_yield_file, calculate_worldwide_mean_sigma, get_prior
)

fixtures_folder = os.path.join(fixtures_path, 'prior_yield')


def test_worldwide_mean_sigma():
    stats = calculate_worldwide_mean_sigma('wheatGrain')
    assert [round(s) for s in stats] == [3197, 1854, 371, 241]


@patch('hestia_earth.distribution.utils.priors.write_to_storage')
def test_generate_prior_yield_file(*args):
    result = generate_prior_yield_file(10, overwrite=True)
    expected = read_prior_stats(os.path.join(fixtures_folder, 'result.csv'))
    assert result.to_csv() == expected.to_csv()


def read_prior_file(*args):
    with open(os.path.join(fixtures_folder, 'result.csv'), 'rb') as f:
        return f.read()


@patch('hestia_earth.distribution.utils.priors.load_from_storage', side_effect=read_prior_file)
def test_get_prior(*args):
    mu, sd = get_prior('GADM-CHE', 'genericCropSeed')
    assert mu == 2710.3
    assert sd == 1488.965668677421


@patch('hestia_earth.distribution.utils.priors.load_from_storage', side_effect=read_prior_file)
def test_get_prior_missing(*args):
    # data is empty
    mu, sd = get_prior('GADM-AFG', 'genericCropSeed')
    assert mu is None
    assert sd is None

    # data is not present
    mu, sd = get_prior('GADM-FRA', 'wheatGrain')
    assert mu is None
    assert sd is None
