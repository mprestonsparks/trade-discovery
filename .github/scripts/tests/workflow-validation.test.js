const { expect, test, describe } = require('@jest/globals');
const yaml = require('js-yaml');
const fs = require('fs');
const path = require('path');

describe('GitHub Workflow Validation', () => {
    test('sync-project-to-local.yml is valid', () => {
        const workflowPath = path.join(__dirname, '../../workflows/sync-project-to-local.yml');
        const workflowContent = fs.readFileSync(workflowPath, 'utf8');
        const workflow = yaml.load(workflowContent);

        // Test basic structure
        expect(workflow).toHaveProperty('name');
        expect(workflow).toHaveProperty('on');
        expect(workflow).toHaveProperty('jobs');

        // Test trigger events
        expect(workflow.on).toHaveProperty('projects_v2_item');
        expect(workflow.on.projects_v2_item).toHaveProperty('types');
        expect(workflow.on.projects_v2_item.types).toEqual(
            expect.arrayContaining(['created', 'edited', 'deleted'])
        );

        // Test jobs structure
        expect(workflow.jobs).toHaveProperty('sync_to_local');
        expect(workflow.jobs.sync_to_local).toHaveProperty('runs-on');
        expect(workflow.jobs.sync_to_local).toHaveProperty('steps');
    });
});
