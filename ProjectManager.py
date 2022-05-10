import os
import logging
import subprocess
import sys

from Project import Project


class ProjectManager:
    def __init__(self, name, projectName):
        self.projectManagerName = projectName
        self.listOfProject = []

    def getListOfProject(self):
        return self.listOfProject

    def getProjectManagerName(self):
        return self.projectManagerName

    def getProjectIDs(self, logger):
        listProjectsID = ['PRJEB1787', 'PRJNA30125', 'PRJNA471938', 'PRJNA472225']

        return listProjectsID

    def createProjectFromListOfIDs(self, logger, listProjectsID):
        logger.info('[CREATE-PROJECT-BY-LIST-IDs]: ' + str(listProjectsID))
        listOfProjectObj = []
        for item, idProject in enumerate(listProjectsID):
            project = Project(projectID=idProject)
            listOfProjectObj.append(project)

        self.listOfProject = listOfProjectObj
        # return listOfProjectObj

        # scrivo tutti i progetti e, per ogni progetto, la lista degli experiments

    '''
   <projectManager>
       <projects>    
           <project id="PRJEB1787">
               <experiments>
                   <exp1> <samples> <sample> </sample> </samples> </exp1>
                   <exp2> <samples> <sample> </sample> </samples> </exp2>
               </experiments>
           <project>
           <project id="PRJNA471938">
               <experiments>
                   <exp1> <samples> <sample> </sample> </samples> </exp1>
                   <exp2> <samples> <sample> </sample> </samples> </exp2>
               </experiments>
           <project>
       <projects> 
   <projectManager>
       '''

    def projectManagerToXML(self, logger):
        logger.info('[CREATE-XML-PROJECT-MANAGER]: ' + str(self.projectManagerName))
        listXMLNodesProjects = []
        for index, project in enumerate(self.listOfProject):
            listXMLNodesProjects.append(project.toXML())
