"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.convert = convert;
// src/convert.ts
const extractFindings_1 = require("./extractFindings");
const formatSummaryComment_1 = require("./formatSummaryComment");
function convert(sarifContent) {
    return (0, formatSummaryComment_1.formatSummaryComment)((0, extractFindings_1.extractFindings)(sarifContent), sarifContent);
}
