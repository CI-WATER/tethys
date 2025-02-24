import { execSync } from "child_process";
import fs from "fs";
import path from "path";
const { screen, fireEvent } = require("@testing-library/dom");

import $ from "jquery";

import DataTable from "datatables.net";
$.fn.DataTable = DataTable;

import TETHYS_DATATABLE_VIEW from "../../../tethys_gizmos/static/tethys_gizmos/js/datatable_view.js";

global.TETHYS_DATATABLE_VIEW = TETHYS_DATATABLE_VIEW;

global.Node = window.Node;
global.Option = window.Option || function Option() {};

let renderedHtml = '';

const DATATABLE_VIEW_ID = "test_datatable_view_id";

beforeAll(() => {
    const templateName = "tethys_gizmos/gizmos/datatable_view.html";
    const context = JSON.stringify({
        title: "Testing the datatable view gizmo",
        id: DATATABLE_VIEW_ID,

        column_names: ["Column 1", "Column 2", "Column 3"],
        rows: [
            ["Row 1 Column 1", "Row 1 Column 2", "Row 1 Column 3"],
            ["Row 2 Column 1", "Row 2 Column 2", "Row 2 Column 3"],
            ["Row 3 Column 1", "Row 3 Column 2", "Row 3 Column 3"],
        ]
        
    });

    execSync(`python render_template.py ${templateName} '${context}' `, { stdio: "inherit" });

    const outputPath = path.resolve("./rendered_templates/test_datatable_view_output.html");
    renderedHtml = fs.readFileSync(outputPath, "utf8");
});

beforeEach(() => {
    document.body.innerHTML = renderedHtml;

    // Initialize datatable view
    TETHYS_DATATABLE_VIEW.initTableView(".data_table_gizmo_view");
});

test("Gizmo renders correctly", () => {
    expect(screen.getByText("Column 1")).toBeInTheDocument();
    expect(screen.getByText("Column 2")).toBeInTheDocument();
    expect(screen.getByText("Column 3")).toBeInTheDocument();
    expect(screen.getByText("Row 1 Column 1")).toBeInTheDocument();
    expect(screen.getByText("Row 1 Column 2")).toBeInTheDocument();
    expect(screen.getByText("Row 1 Column 3")).toBeInTheDocument();
});

test("Datatable is initialized", () => {
    const dataTable = document.querySelector(".data_table_gizmo_view");
    expect(dataTable).toHaveClass("dataTable");
});

