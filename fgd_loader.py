# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FGDLoader
                                 A QGIS plugin
 FGD(JPGIS) file loader
                              -------------------
        begin                : 2017-10-29
        git sha              : $Format:%H$
        copyright            : (C) 2017 by mugwort_rc
        email                : mugwort.rc@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import *
from qgis.gui import QgsMapLayerProxyModel
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtCore import QFileInfo, QVariant
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from fgd_loader_dialog import FGDLoaderDialog
import jpgis
from jpgis import layer as jpgis_layer
import os.path
import xml.sax
import zipfile


class FGDLoader:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'FGDLoader_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&FGDLoader')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'FGDLoader')
        self.toolbar.setObjectName(u'FGDLoader')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('FGDLoader', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = FGDLoaderDialog()
        self.dlg.comboBoxLayer.setFilters(QgsMapLayerProxyModel.VectorLayer)

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/FGDLoader/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'FGDLoader'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&FGDLoader'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            layers = jpgis_layer.JPGISLayers(tr=self.elementTranslations())
            # Test
            if self.dlg.tabWidget.currentWidget() == self.dlg.tabTest:
                filepath = self.dlg.lineEdit.text()
                with open(filepath) as fp:
                    handler = self.loadJPGIS(fp)
                kwargs = {}
                if self.dlg.checkBoxInto.isChecked():
                    kwargs["into"] = self.dlg.comboBoxLayer.currentLayer()
                layers.addFeatures(handler, **kwargs)
            # XML
            elif self.dlg.tabWidget.currentWidget() == self.dlg.tabXML:
                for filepath in self.dlg.fileListXML.stringList():
                    with open(filepath) as fp:
                        handler = self.loadJPGIS(fp)
                    layers.addFeatures(handler)
            # Archive
            elif self.dlg.tabWidget.currentWidget() == self.dlg.tabArchive:
                for filepath in self.dlg.fileListArchive.stringList():
                    try:
                        with zipfile.ZipFile(filepath) as zfp:
                            for name in zfp.namelist():
                                if not name.endswith(".xml"):
                                    continue
                                for key, test in self.dlg.archiveTargets().items():
                                    if not test:
                                        continue
                                    if key not in name:
                                        continue
                                    with zfp.open(name) as fp:
                                        handler = self.loadJPGIS(fp)
                                        layers.addFeatures(handler)
                                    break
                    except:
                        raise
            for layer in layers.values():
                QgsMapLayerRegistry.instance().addMapLayer(layer)


    def loadJPGIS(self, fp):
        handler = jpgis.JPGISHandler()
        parser = xml.sax.make_parser()
        parser.setContentHandler(handler)
        parser.setFeature(xml.sax.handler.feature_namespaces, True)
        parser.parse(fp)
        return handler

    def elementTranslations(self):
        return {
            "GCP": self.tr("GCP"),
            "DEM": self.tr("DEM"),
            "DGHM": self.tr("DGHM"),
            "ElevPt": self.tr("ElevPt"),
            "Cntr": self.tr("Cntr"),
            "AdmArea": self.tr("AdmArea"),
            "AdmBdry": self.tr("AdmBdry"),
            "CommBdry": self.tr("CommBdry"),
            "AdmPt": self.tr("AdmPt"),
            "CommPt": self.tr("CommPt"),
            "SBArea": self.tr("SBArea"),
            "SBBdry": self.tr("SBBdry"),
            "SBAPt": self.tr("SBAPt"),
            "WA": self.tr("WA"),
            "WL": self.tr("WL"),
            "CStline": self.tr("CStline"),
            "WStrL": self.tr("WStrL"),
            "WStrA": self.tr("WStrA"),
            "LeveeEdge": self.tr("LeveeEdge"),
            "RvrMgtBdry": self.tr("RvrMgtBdry"),
            "BldA": self.tr("BldA"),
            "BldL": self.tr("BldL"),
            "RdEdg": self.tr("RdEdg"),
            "RdCompt": self.tr("RdCompt"),
            "RdASL": self.tr("RdASL"),
            "RdArea": self.tr("RdArea"),
            "RdSgmtA": self.tr("RdSgmtA"),
            "RdMgtBdry": self.tr("RdMgtBdry"),
            "RailCL": self.tr("RailCL"),
        }
