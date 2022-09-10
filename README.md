# Toggl to Invoice

Uses the [Toggl API](https://developers.track.toggl.com/docs/) to fetch workspace data and generate a Jinja2-templated invoice.

## How to use

1. Please clone and remove the `_` prefix from [_configToggleApi.json](_configToggleApi.json) so that it becomes [configToggleApi.json](configToggleApi.json) and update its missing fields.
   - Get API Token from here: [https://support.toggl.com/en/articles/3116844-where-is-my-api-key-located](https://support.toggl.com/en/articles/3116844-where-is-my-api-key-located).
2. Follow the steps in [Development](#development) to set up virtual environment and install dependencies.
3. Run `generateProjectsJson.sh > configProjects.json` (OR `generateProjectsJson.py > configProjects.json` if you're not using the venv) to create a dump of projects. WARNING: `>` will override the current file.
4. Update the `hourlyRate` fields in [project.json](configProjects.json)
5. Run `fetchTogglDataAndGenerateInvoice.sh > invoice.html` (OR `fetchTogglDataAndGenerateInvoice.py > invoice.html` if you're not using the venv). WARNING: `>` will override the current file.

## Development

Please read the [development README](./development/README.md) for notes on installing a virtual environment, pip dependencies and git hook(s).
