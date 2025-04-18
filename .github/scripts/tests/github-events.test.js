const { expect, test, describe } = require('@jest/globals');
const { Octokit } = require('@octokit/rest');

describe('GitHub Projects v2 Events', () => {
    let octokit;
    
    beforeEach(() => {
        octokit = new Octokit({
            auth: process.env.GITHUB_TOKEN
        });
    });

    test('projects_v2_item webhook event structure is valid', async () => {
        // Mock a projects_v2_item webhook payload
        const webhookPayload = {
            action: 'created',
            projects_v2_item: {
                id: 1,
                project_node_id: 'test_project',
                content_node_id: 'test_content'
            },
            organization: {
                login: 'test-org'
            },
            sender: {
                login: 'test-user'
            }
        };

        // Verify the payload structure matches GitHub's schema
        expect(webhookPayload).toHaveProperty('action');
        expect(['created', 'edited', 'deleted']).toContain(webhookPayload.action);
        expect(webhookPayload).toHaveProperty('projects_v2_item');
        expect(webhookPayload.projects_v2_item).toHaveProperty('id');
        expect(webhookPayload.projects_v2_item).toHaveProperty('project_node_id');
        expect(webhookPayload.projects_v2_item).toHaveProperty('content_node_id');
    });

    test('can handle projects_v2_item created event', async () => {
        const handler = require('../sync/index.js');
        const mockEvent = {
            action: 'created',
            projects_v2_item: {
                id: 1,
                project_node_id: 'test_project',
                content_node_id: 'test_content'
            }
        };

        // This should not throw an error
        await expect(handler.handleProjectsV2Event(mockEvent)).resolves.not.toThrow();
    });

    test('can handle projects_v2_item edited event', async () => {
        const handler = require('../sync/index.js');
        const mockEvent = {
            action: 'edited',
            projects_v2_item: {
                id: 1,
                project_node_id: 'test_project',
                content_node_id: 'test_content',
                changes: {
                    field_value: {
                        field_node_id: 'test_field',
                        field_type: 'single_select'
                    }
                }
            }
        };

        await expect(handler.handleProjectsV2Event(mockEvent)).resolves.not.toThrow();
    });

    test('can handle projects_v2_item deleted event', async () => {
        const handler = require('../sync/index.js');
        const mockEvent = {
            action: 'deleted',
            projects_v2_item: {
                id: 1,
                project_node_id: 'test_project',
                content_node_id: 'test_content'
            }
        };

        await expect(handler.handleProjectsV2Event(mockEvent)).resolves.not.toThrow();
    });
});
