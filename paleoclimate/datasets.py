"""
Data sets from the Paleoclimatology Reconstructions Network.
"""

import os
import sys

if sys.version_info.major == 2:
    from urllib import urlretrieve
else:
    from urllib.request import urlretrieve

from scipy.io import netcdf_file


BASE_URL = "https://www1.ncdc.noaa.gov/pub/data/paleo/reconstructions/pcn/"
MANN2008A_URL = BASE_URL + "/proxy/mann2008/"


def mann2008a(infilled=True, data_home=None, download_if_missing=True):
    """
    Data for the 2008 PNAS paper on proxy-based climate reconstructions.

    This data set contains the 2000 year hemispheric and global surface
    temperature reconstructions for:

      - Northern Hemisphere
      - Land only
      - Composite plus scale method

    The original paper employing this dataset is [1]_.

    Parameters
    ----------
    infilled: bool, optional
        Whether to return the infilled (default) or raw data.
    data_home : optional, default: None
        Specify another download and cache folder for the datasets. By default
        all data is stored in ``'~/.paleoclimate_scipy/'``.
    download_if_missing : bool, optional
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    Returns
    -------
    data: ``netcdf_file`` instance
        The mann2008a dataset, as a `scipy.io.netcdf_file` object.

    Notes
    -----
    This dataset was extracted from the Paleoclimatology Reconstructions
    Network v1.0.1 [2,3]_.

    The data is contained in NetCDF files, one for the infilled and one for
    the original (raw) data.  Each NetCDF file is ~100 MB in size.

    References
    ----------
    .. [1] M.E. Mann, Z. Zhang, M.K. Hughes, R.S. Bradley, S.K. Miller,
           S. Rutherford, and F. Ni, "Proxy-based reconstructions of
           hemispheric and global surface temperature variations over
           the past two millennia", Proceedings of the National Academy of
           Sciences, vol. 105, pp. 13252-13257, 2008.
    .. [2] E.R. Wahl et al., "An archive of high-resolution temperature
           reconstructions over the past 2+ millennia", Geochemistry,
           Geophysics, Geosystems, vol. 11, 2010.
    .. [3] NOAA Paleoclimatology Reconstructions Network,
           http://www.ncdc.noaa.gov/paleo/study/8407, accessed 21 Sep 2016.

    Examples
    --------
    >>> data = mann2008a()
    >>> data
    <scipy.io.netcdf.netcdf_file object at ...>

    >>> data.title
    '2,000 Year Hemispheric and Global Surface Temperature Reconstructions: Infilled Proxy Data'
    >>> data.history
    'Data formatted for Paleoclimate Network v2.0.0 by NOAA-Paleoclimatology, September 2010'

    >>> data.dimensions
    {'network_info': 3, 'strlen': 40, 'site': 1209, 'time': None}
    >>> data.variables.keys()
    ['site_name', 'proxy_data', 'data_type', 'sample_depth', 'lon', 'site', 'proxy_network_info', 'time', 'lat']

    """
    data_home = get_data_home(data_home)
    if not os.path.exists(data_home):
        os.makedirs(data_home)

    if infilled:
        FILENAME = "mann2008infilled.nc"
    else:
        FILENAME = "mann2008original.nc"

    archive_path = os.path.join(data_home, FILENAME)
    if not os.path.exists(archive_path):
        if not download_if_missing:
            raise IOError("Data not found and `download_if_missing` is False")

        FULL_URL = MANN2008A_URL + FILENAME
        print('Downloading data from %s to %s' % (FULL_URL, data_home))
        urlretrieve(FULL_URL, filename=archive_path)

    return netcdf_file(archive_path, mode='r', mmap=False)



def get_data_home(data_home=None):
    """Return the path of the directory to store the data.

    This folder is used by some large dataset loaders to avoid
    downloading the data several times.

    By default the data dir is set to a folder named 'paleoclimate_scipy'
    in the user home folder.

    Alternatively, it can be set by the 'PALEOCLIMATE_SCIPY_DATA' environment
    variable or programmatically by giving an explicit folder path. The
    '~' symbol is expanded to the user home folder.

    If the folder does not already exist, it is automatically created.

    Notes
    -----
    Adapted from ``sklearn.datasets``.

    """
    if data_home is None:
        data_home = os.environ.get('PALEOCLIMATE_SCIPY_DATA',
                                   os.path.join('~', 'paleoclimate_scipy'))

    data_home = os.path.expanduser(data_home)
    if not os.path.exists(data_home):
        os.makedirs(data_home)

    return data_home

