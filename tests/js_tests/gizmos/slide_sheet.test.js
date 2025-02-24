import { execSync } from "child_process";
import fs from "fs";
import path from "path";
const { screen, fireEvent } = require("@testing-library/dom");

import SLIDE_SHEET from "../../../tethys_gizmos/static/tethys_gizmos/js/slide_sheet.js"

global.SLIDE_SHEET = SLIDE_SHEET;

let renderedHtml = '';

const SLIDE_SHEET_ID = "test_slide_sheet_id"

beforeAll(() => {
    const templateName = "tethys_gizmos/gizmos/slide_sheet.html";
    const context = JSON.stringify({
        title: "Testing the slide sheet gizmo",
        id: SLIDE_SHEET_ID,
        content_template: "test_template.html"
    });

    execSync(`python render_template.py ${templateName} '${context}' `, { stdio: "inherit" });

    const outputPath = path.resolve("./rendered_templates/test_slide_sheet_output.html");
    renderedHtml = fs.readFileSync(outputPath, "utf8");
})

beforeEach(() => {
    document.body.innerHTML = renderedHtml;
    let testOpenButton = document.createElement("button");
    testOpenButton.textContent = "Open Slide Sheet";
    testOpenButton.onclick = () => SLIDE_SHEET.open(SLIDE_SHEET_ID);
    document.body.appendChild(testOpenButton);

    // Add event listeners to all elements with an inline onclick attribute
    document.querySelectorAll("[onclick]").forEach((el) => {
        const onClickAttr = el.getAttribute("onclick");

        // Create a new function from the onclick attribute string
        if (onClickAttr) {
            el.addEventListener("click", function () {
                eval(onClickAttr); // 🔥 Execute the original inline script
            });
        }
    });
});



test("Gizmo renders correctly", () => {
    expect(screen.getByText("Testing the slide sheet gizmo")).toBeInTheDocument();
});

test("Clicking open button opens slide sheet", () => {
    const slideSheet = document.getElementById(SLIDE_SHEET_ID);
    fireEvent.click(screen.getByText("Open Slide Sheet"));
    expect(slideSheet.classList.contains("show")).toBe(true);
    
})

test("Clicking close button closes slide sheet", () => {
    const slideSheet = document.getElementById(SLIDE_SHEET_ID);
    SLIDE_SHEET.open(SLIDE_SHEET_ID);
    expect(slideSheet.classList.contains("show")).toBe(true);

    const closeButton = screen.getByLabelText("Close");
    fireEvent.click(closeButton);
    expect(slideSheet.classList.contains("show")).toBe(false);
});

