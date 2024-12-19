# Files to Verify/Update in market-analysis

This is a temporary task list to ensure we copy and adapt all necessary files from the market-analysis repo.

## .project Directory

### docs/
- [] ai_integration.md (1,335 bytes) - AI integration guidelines
- [] customization.md (1,372 bytes) - Project customization docs
- [] setup.md (1,378 bytes) - Project setup instructions
- [] workflow.md (1,596 bytes) - Development workflow docs

### scripts/
- [] github_setup.ps1 (2,970 bytes) - COMPLETED
- [] setup.ps1 (1,024 bytes) - Project setup script
- [] update_status.ps1 (1,536 bytes) - Status update script

### status/
- [] DEVELOPMENT_STATUS.yaml (2,048 bytes) - Project status tracking 
- [] DEVELOPMENT_STATUS.yaml.bak (1,613 bytes) - COMPLETED

## .github Directory

### Root
- [] SYNC_IMPLEMENTATION_PLAN.md (4,559 bytes)

### actions/
*(empty directory - may need to be created)*

### scripts/
#### sync/ (CI Utility)
```
sync/
├── src/              # Source code
│   ├── dag.js        # DAG implementation
│   ├── github.js     # GitHub API integration
│   ├── logger.js     # Logging utility
│   ├── task-decomposition.js  # Task management
│   └── yaml.js       # YAML processing
├── tests/            # Tests for sync utility
│   ├── dag.test.js
│   ├── github.test.js
│   ├── logger.test.js
│   ├── task-decomposition.test.js
│   └── yaml.test.js
├── package.json      # Dependencies and scripts
├── jest.config.js    # Test configuration
├── babel.config.js   # JavaScript transpilation
├── Dockerfile.test   # Test container definition
└── docker-compose.test.yml  # Test orchestration
```

Files to implement:
- [] src/dag.js (24,212 bytes) - DAG implementation
- [] src/github.js (8,605 bytes) - GitHub API integration
- [] src/logger.js (2,535 bytes) - Logging utility
- [] src/task-decomposition.js (4,096 bytes) - Task management
- [] src/yaml.js (3,072 bytes) - YAML processing
- [] tests/dag.test.js - Test suite for DAG
- [] tests/github.test.js - Test suite for GitHub integration
- [] tests/logger.test.js - Test suite for logging
- [] tests/task-decomposition.test.js - Test suite for task management
- [] tests/yaml.test.js - Test suite for YAML processing
- [] package.json - Project dependencies and scripts
- [] jest.config.js - Jest test configuration
- [] babel.config.js - Babel configuration
- [] Dockerfile.test - Test environment container
- [] docker-compose.test.yml - Test orchestration

## .github/workflows Directory
- [] project-v2-trigger.yml

## Root Directory Files
- [] .env.example (1,581 bytes) - Contains GitHub configuration templates **NOTE: this file will be unique to each repo**
- [] .pre-commit-config.yaml (506 bytes) - Git hooks configuration
- [] pyproject.toml (624 bytes) - Project metadata and dependencies **NOTE: this file will be unique to each repo**

## Progress Tracking
- [] Initial .project structure setup
- [] DEVELOPMENT_STATUS.yaml updated with new fields
- [] github_setup.ps1 updated with project validation
- [] Copy and adapt remaining .project files
- [] Copy and adapt .github directory structure
- [] Test GitHub project integration
- [] Verify cross-repo synchronization

## Notes
- Files marked with [x] have been completed
- File sizes are listed for reference to ensure complete copies
- Some files may need adaptation for market-analysis specific content
- Root directory files are needed for complete GitHub integration

## Infrastructure Test Implementation

### Project Structure
```tests/infrastructure/```
├── __tests__/
├── babel.config.js
├── dag.js
├── dag.test.js
├── github.js
├── github.test.js
├── index.js
├── index.test.js
├── jest.config.js
├── jest.setup.js
├── logger.js
├── logger.test.js
├── package.json
├── task-decomposition.js
├── task-decomposition.test.js
├── test.yaml
├── yaml.js
└── yaml.test.js

### Configuration Files

#### package.json
```json
{
  "name": "market-analysis-infrastructure-tests",
  "version": "1.0.0",
  "description": "Infrastructure tests for market analysis",
  "scripts": {
    "test:infrastructure": "jest tests/infrastructure"
  },
  "dependencies": {
    "ajv": "^8.12.0",
    "js-yaml": "^4.1.0"
  },
  "devDependencies": {
    "@babel/core": "^7.23.6",
    "@babel/preset-env": "^7.23.6",
    "babel-jest": "^29.7.0",
    "jest": "^29.7.0"
  }
}
```

#### jest.config.js
```javascript
module.exports = {
  testEnvironment: 'node',
  roots: ['<rootDir>'],
  moduleFileExtensions: ['js', 'json'],
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js'],
  transform: {
    '^.+\\.js$': 'babel-jest'
  },
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1'
  },
  modulePathIgnorePatterns: ['<rootDir>/node_modules/'],
  setupFiles: ['<rootDir>/tests/infrastructure/jest.setup.js']
};
```

#### babel.config.js
```javascript
module.exports = {
  presets: [
    ['@babel/preset-env', {
      targets: {
        node: 'current'
      }
    }]
  ]
};
```

#### jest.setup.js
```javascript
// This file is used to set up the test environment
// No need to import jest as it's already available in the test environment
```

### Core Implementation

#### yaml.js
```javascript
const { readFileSync } = require('fs');
const yaml = require('js-yaml');
const Ajv = require('ajv');

class YamlValidator {
    constructor(schemaPath) {
        const schema = JSON.parse(readFileSync(schemaPath, 'utf8'));
        this.ajv = new Ajv();
        this.validate = this.ajv.compile(schema);
    }

    validateFile(filePath) {
        try {
            const content = readFileSync(filePath, 'utf8');
            const data = yaml.load(content);
            
            if (!data) {
                return {
                    valid: false,
                    errors: [{ message: 'Empty or invalid YAML' }]
                };
            }

            const valid = this.validate(data);
            return {
                valid,
                errors: this.validate.errors || []
            };
        } catch (error) {
            return {
                valid: false,
                errors: [{ message: error.message }]
            };
        }
    }

    validateTaskIds(data) {
        const taskIds = new Set();
        const errors = [];

        for (const task of data.next_available_tasks) {
            if (taskIds.has(task.id)) {
                errors.push({ message: `Duplicate task ID: ${task.id}` });
            }
            taskIds.add(task.id);
        }

        return {
            valid: errors.length === 0,
            errors
        };
    }
}

function validateYaml(filePath) {
    const content = readFileSync(filePath, 'utf8');
    const data = yaml.load(content);
    
    if (!data || typeof data !== 'object') {
        throw new Error('Invalid YAML: Document must be a valid object');
    }
    return true;
}

module.exports = { YamlValidator, validateYaml };
```

#### yaml.test.js
```javascript
const { expect, test, describe } = require('@jest/globals');
const { YamlValidator, validateYaml } = require('./yaml.js');
const { readFileSync } = require('fs');
const yaml = require('js-yaml');

jest.mock('fs');
jest.mock('js-yaml');

describe('YamlValidator', () => {
    const mockSchema = {
        type: 'object',
        required: ['next_available_tasks'],
        properties: {
            next_available_tasks: {
                type: 'array',
                items: {
                    type: 'object',
                    required: ['id', 'name', 'status'],
                    properties: {
                        id: { type: 'number' },
                        name: { type: 'string' },
                        status: { type: 'string' }
                    }
                }
            }
        }
    };

    beforeEach(() => {
        jest.resetAllMocks();
        readFileSync.mockReturnValueOnce(JSON.stringify(mockSchema));
    });

    test('should validate valid YAML', () => {
        const validator = new YamlValidator('schema.json');
        const validYaml = `
next_available_tasks:
  - id: 1
    name: Task 1
    status: ready
  - id: 2
    name: Task 2
    status: blocked
`;
        const validData = {
            next_available_tasks: [
                { id: 1, name: 'Task 1', status: 'ready' },
                { id: 2, name: 'Task 2', status: 'blocked' }
            ]
        };

        readFileSync.mockReturnValueOnce(validYaml);
        yaml.load.mockReturnValueOnce(validData);
        
        const result = validator.validateFile('test.yaml');
        expect(result.valid).toBe(true);
        expect(result.errors).toHaveLength(0);
    });

    test('should catch invalid YAML', () => {
        const validator = new YamlValidator('schema.json');
        const invalidYaml = `
next_available_tasks:
  - id: "not a number"
    name: Task 1
    status: ready
`;
        const invalidData = {
            next_available_tasks: [
                { id: "not a number", name: 'Task 1', status: 'ready' }
            ]
        };

        readFileSync.mockReturnValueOnce(invalidYaml);
        yaml.load.mockReturnValueOnce(invalidData);
        
        const result = validator.validateFile('test.yaml');
        expect(result.valid).toBe(false);
        expect(result.errors).toHaveLength(1);
    });

    test('should validate task IDs', () => {
        const validator = new YamlValidator('schema.json');
        const data = {
            next_available_tasks: [
                { id: 1, name: 'Task 1', status: 'ready', blocking: [2] },
                { id: 2, name: 'Task 2', status: 'blocked', blocked_by: [1] }
            ]
        };
        const result = validator.validateTaskIds(data);
        expect(result.valid).toBe(true);
        expect(result.errors).toHaveLength(0);
    });

    test('should catch duplicate task IDs', () => {
        const validator = new YamlValidator('schema.json');
        const data = {
            next_available_tasks: [
                { id: 1, name: 'Task 1', status: 'ready' },
                { id: 1, name: 'Task 2', status: 'blocked' }
            ]
        };
        const result = validator.validateTaskIds(data);
        expect(result.valid).toBe(false);
        expect(result.errors[0].message).toContain('Duplicate task ID: 1');
    });
});

describe('YAML Validation', () => {
    beforeEach(() => {
        jest.resetAllMocks();
    });

    test('should validate correct YAML', () => {
        const mockYaml = {
            next_available_tasks: [
                {
                    id: 1,
                    name: 'Task 1',
                    description: 'Description 1',
                    blocking: [2]
                }
            ]
        };

        readFileSync.mockReturnValueOnce('mock yaml content');
        yaml.load.mockReturnValueOnce(mockYaml);

        expect(() => validateYaml('test.yaml')).not.toThrow();
    });

    test('should reject invalid YAML', () => {
        readFileSync.mockReturnValueOnce('mock yaml content');
        yaml.load.mockReturnValueOnce(null);

        expect(() => validateYaml('test.yaml')).toThrow('Invalid YAML: Document must be a valid object');
    });
});

### Docker Configuration

#### docker-compose.js.test.yml
```yaml
version: '3.8'
services:
  js-tests:
    build:
      context: .
      dockerfile: Dockerfile.js.test
    volumes:
      - ./tests/infrastructure:/app/tests/infrastructure
```

#### Dockerfile.js.test
```dockerfile
FROM node:18-slim

WORKDIR /app

COPY tests/infrastructure/package*.json ./
COPY tests/infrastructure/babel.config.js ./
COPY tests/infrastructure/jest.config.js ./

RUN npm install

COPY tests/infrastructure/ ./tests/infrastructure/

CMD ["npm", "run", "test:infrastructure"]
```

## Running Tests
To run the infrastructure tests:
```bash
docker-compose -f docker-compose.js.test.yml up --build
```

## Test Results Should Look Like:
All 35 tests across 7 test suites are passing:
- yaml.test.js: 4 tests
- index.test.js: 2 tests
- task-decomposition.test.js: 5 tests
- github.test.js: 8 tests
- logger.test.js: 6 tests
- dag.test.js: 10 tests
