# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FGDLoaderDialog
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

import os

from qgis.PyQt import QtCore, QtGui, QtWidgets, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fgd_loader_dialog_base.ui'))


class FGDLoaderDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(FGDLoaderDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        # model
        self.fileListXML = QtCore.QStringListModel()
        self.fileListArchive = QtCore.QStringListModel()
        self.selectionXML = QtCore.QItemSelectionModel(self.fileListXML)
        self.selectionArchive = QtCore.QItemSelectionModel(self.fileListArchive)
        self.listViewXML.setModel(self.fileListXML)
        self.listViewArchive.setModel(self.fileListArchive)
        self.listViewXML.setSelectionModel(self.selectionXML)
        self.listViewArchive.setSelectionModel(self.selectionArchive)
        # history
        self.last_open_dir = ""

    def archiveTargets(self):
        return {
            "GCP": self.checkBoxGCP.isChecked(),
            "DEM": self.checkBoxDEM.isChecked(),
            "DGHM": self.checkBoxDGHM.isChecked(),
            "ElevPt": self.checkBoxElevPt.isChecked(),
            "Cntr": self.checkBoxCntr.isChecked(),
            "AdmArea": self.checkBoxAdmArea.isChecked(),
            "AdmBdry": self.checkBoxAdmBdry.isChecked(),
            "CommBdry": self.checkBoxCommBdry.isChecked(),
            "AdmPt": self.checkBoxAdmPt.isChecked(),
            "CommPt": self.checkBoxCommPt.isChecked(),
            "SBArea": self.checkBoxSBArea.isChecked(),
            "SBBdry": self.checkBoxSBBdry.isChecked(),
            "SBAPt": self.checkBoxSBAPt.isChecked(),
            "WA": self.checkBoxWA.isChecked(),
            "WL": self.checkBoxWL.isChecked(),
            "CStline": self.checkBoxCStline.isChecked(),
            "WStrL": self.checkBoxWStrL.isChecked(),
            "WStrA": self.checkBoxWStrA.isChecked(),
            "LeveeEdge": self.checkBoxLeveeEdge.isChecked(),
            "RvrMgtBdry": self.checkBoxRvrMgtBdry.isChecked(),
            "BldA": self.checkBoxBldA.isChecked(),
            "BldL": self.checkBoxBldL.isChecked(),
            "RdEdg": self.checkBoxRdEdg.isChecked(),
            "RdCompt": self.checkBoxRdCompt.isChecked(),
            "RdASL": self.checkBoxRdASL.isChecked(),
            "RdArea": self.checkBoxRdArea.isChecked(),
            "RdSgmtA": self.checkBoxRdSgmtA.isChecked(),
            "RdMgtBdry": self.checkBoxRdMgtBdry.isChecked(),
            "RailCL": self.checkBoxRailCL.isChecked(),
        }

    @QtCore.pyqtSlot()
    def on_toolButton_clicked(self):
        filepath, _filter = QtWidgets.QFileDialog.getOpenFileName(self,
                                                     self.tr("Open JPGIS XML"),
                                                     "",
                                                     self.tr("XML(*.xml)"))
        if not filepath:
            return
        self.setLastOpenPath(filepath)
        self.lineEdit.setText(filepath)

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def on_buttonBoxXML_clicked(self, button):
        # Reset
        if self.buttonBoxXML.standardButton(button) == QtWidgets.QDialogButtonBox.Reset:
            self.fileListXML.setStringList([])
        # Open
        elif self.buttonBoxXML.standardButton(button) == QtWidgets.QDialogButtonBox.Open:
            filelist = self.getOpenFileNamesXML()
            if filelist:
                self.setLastOpenPath(filelist[0])
            self.fileListXML.setStringList(self.fileListXML.stringList() + filelist)
        # Close
        elif self.buttonBoxXML.standardButton(button) == QtWidgets.QDialogButtonBox.Close:
            removes = [x.row() for x in self.selectionXML.selectedIndexes()]
            self.fileListXML.setStringList(
                self.dropIndex(self.fileListXML.stringList(), removes)
            )

    @QtCore.pyqtSlot(QtWidgets.QAbstractButton)
    def on_buttonBoxArchive_clicked(self, button):
        # Reset
        if self.buttonBoxArchive.standardButton(button) == QtWidgets.QDialogButtonBox.Reset:
            self.fileListArchive.setStringList([])
        # Open
        elif self.buttonBoxArchive.standardButton(button) == QtWidgets.QDialogButtonBox.Open:
            filelist = self.getOpenFileNamesArchive()
            if filelist:
                self.setLastOpenPath(filelist[0])
            self.fileListArchive.setStringList(self.fileListArchive.stringList() + filelist)
        # Close
        elif self.buttonBoxArchive.standardButton(button) == QtWidgets.QDialogButtonBox.Close:
            removes = [x.row() for x in self.selectionArchive.selectedIndexes()]
            self.fileListArchive.setStringList(
                self.dropIndex(self.fileListArchive.stringList(), removes)
            )

    def dropIndex(self, values, drop_index):
        return [x for i, x in enumerate(values) if i not in drop_index]

    def setLastOpenPath(self, filepath):
        if not filepath:
            return
        self.last_open_dir = QtCore.QFileInfo(filepath).dir().absolutePath()

    def getOpenFileNameXML(self):
        filename, _filter = QtWidgets.QFileDialog.getOpenFileName(self,
                                                 self.tr("Open JPGIS XML"),
                                                 self.last_open_dir,
                                                 self.tr("XML(*.xml)"))
        return filename

    def getOpenFileNamesXML(self):
        filenames, _filter = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                 self.tr("Open JPGIS XML"),
                                                 self.last_open_dir,
                                                 self.tr("XML(*.xml)"))
        return filenames

    def getOpenFileNamesArchive(self):
        filenames, _filter = QtWidgets.QFileDialog.getOpenFileNames(self,
                                                 self.tr("Open JPGIS Archive"),
                                                 self.last_open_dir,
                                                 self.tr("ZIP file(*.zip)"))
        return filenames
