"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.validateSarif = validateSarif;
// src/validateSarif.ts
const ajv_1 = __importDefault(require("ajv"));
const ajv_formats_1 = __importDefault(require("ajv-formats"));
const utils_1 = require("./utils");
function validateSarif(sarifContent) {
    const schema = (0, utils_1.loadSchema)();
    const ajv = new ajv_1.default({ allErrors: true });
    (0, ajv_formats_1.default)(ajv); // Add support for formats like "uri"
    const validate = ajv.compile(schema);
    if (!validate(sarifContent)) {
        throw new Error('Invalid SARIF file: ' + (validate.errors?.[0]?.message || 'Unknown error'));
    }
    console.log('✅: Successfully Validated Input against OASIS Schema.');
}
