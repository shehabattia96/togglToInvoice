import sys
import utilities
import toggl
import togglModels

# CLI Args:
# python generateProjectsJsonFromToggl.py {configToggleApiPath}
# configToggleApiPath: path to configToggleApi.json or similar

configToggleApiPath = sys.argv[1] if len(sys.argv) > 1 else "configToggleApi.json"

if __name__ == "__main__":
    configToggleApi = utilities.readJsonFromFile(configToggleApiPath)

    header = toggl.generateRequestHeader(apiToken=configToggleApi["apiToken"])

    allProjects = toggl.getAllProjects(
        apiEndpoint=configToggleApi["apiEndpoint"],
        requestHeader=header
    )

    projectDict = {}
    
    for project in allProjects:
        project = togglModels.mapTogglePayloadToProject(**project)
        projectDict[project.id] = project

    print(utilities.objectToJson(projectDict, prettify=True))