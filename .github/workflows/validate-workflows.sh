#!/bin/bash

# Validate all workflow files
for file in .github/workflows/*.yml; do
  echo "Validating $file..."
  if ! yamllint "$file"; then
    echo "Error in $file"
    exit 1
  fi
done

echo "All workflows validated successfully"
