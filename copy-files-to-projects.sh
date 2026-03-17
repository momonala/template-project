#!/bin/bash
# Copy template files to all projects
# Run this script from the projects/ directory

for d in */; do
  # Skip template-project itself
  [ "$d" = "template-project/" ] && continue
  
  project_name="${d%/}"
  
  # Copy pre-commit.sh to project root
  if [ -f "template-project/pre-commit.sh" ]; then
    cp template-project/pre-commit.sh "$d/pre-commit.sh"
    chmod +x "$d/pre-commit.sh"
    
    # Also copy to .git/hooks/pre-commit
    if [ -d "$d/.git/hooks" ]; then
      cp template-project/pre-commit.sh "$d/.git/hooks/pre-commit"
      chmod +x "$d/.git/hooks/pre-commit"
    fi
  fi

  # Copy .gitignore to project root
  if [ -f "template-project/.gitignore" ]; then
    cp template-project/.gitignore "$d/.gitignore"
  fi
  
  
  echo "✅ $project_name"
done

echo "✅ Done copying template files to all projects!"
