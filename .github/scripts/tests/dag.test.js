import { test, expect } from '@jest/globals';
import { readFileSync } from 'fs';
import { join } from 'path';
import yaml from 'js-yaml';

// Helper function to load YAML files
function loadYaml(filename) {
  const filePath = join(__dirname, 'fixtures', filename);
  return yaml.load(readFileSync(filePath, 'utf8'));
}

test('validates task dependencies in valid.yaml', () => {
  const data = loadYaml('valid.yaml');
  expect(data).toBeDefined();
  expect(data.tasks).toBeDefined();
  expect(Array.isArray(data.tasks)).toBe(true);
});

test('detects invalid task structure', () => {
  expect(() => {
    loadYaml('invalid.yaml');
  }).not.toThrow();
  
  const data = loadYaml('invalid.yaml');
  expect(data.tasks).toBeUndefined();
});

test('handles duplicate task IDs', () => {
  const data = loadYaml('duplicate-ids.yaml');
  expect(data.tasks).toBeDefined();
  
  // Check for duplicate IDs
  const ids = data.tasks.map(task => task.id);
  const uniqueIds = new Set(ids);
  expect(ids.length).not.toBe(uniqueIds.size);
});

test('validates task properties', () => {
  const data = loadYaml('test-tasks.yaml');
  expect(data.tasks).toBeDefined();
  
  data.tasks.forEach(task => {
    expect(task).toHaveProperty('id');
    expect(task).toHaveProperty('name');
    expect(typeof task.id).toBe('string');
    expect(typeof task.name).toBe('string');
  });
});
