// src/utils.ts
import fs from 'fs';
import path from 'path';

export function loadJsonFile<T = any>(filePath: string): T {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found at ${filePath}`);
  }
  const content = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(content);
}

export function loadSchema(): any {
  return loadJsonFile(path.resolve(__dirname, '../sarif-schema-2.1.0.json'));
}
