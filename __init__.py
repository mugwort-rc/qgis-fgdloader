# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FGDLoader
                                 A QGIS plugin
 FGD(JPGIS) file loader
                             -------------------
        begin                : 2017-10-29
        copyright            : (C) 2017 by mugwort_rc
        email                : mugwort.rc@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load FGDLoader class from file FGDLoader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .fgd_loader import FGDLoader
    return FGDLoader(iface)
