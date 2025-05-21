"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadJsonFile = loadJsonFile;
exports.loadSchema = loadSchema;
// src/utils.ts
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
function loadJsonFile(filePath) {
    if (!fs_1.default.existsSync(filePath)) {
        throw new Error(`File not found at ${filePath}`);
    }
    const content = fs_1.default.readFileSync(filePath, 'utf-8');
    return JSON.parse(content);
}
function loadSchema() {
    return loadJsonFile(path_1.default.resolve(__dirname, '../sarif-schema-2.1.0.json'));
}
