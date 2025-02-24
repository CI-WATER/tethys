import { execSync } from "child_process";
import fs from "fs";
import path from "path";
import { screen, fireEvent } from "@testing-library/dom";
import "@testing-library/jest-dom";
import $ from "jquery";

import TETHYS_RANGE_SLIDER from "../../../tethys_gizmos/static/tethys_gizmos/js/range_slider.js";

global.TETHYS_RANGE_SLIDER = TETHYS_RANGE_SLIDER;

let renderedHtml = "";
const RANGE_SLIDER_ID = "test-range-slider";

beforeAll(() => {
    const templateName = "tethys_gizmos/gizmos/range_slider.html";
    const context = JSON.stringify({
        name: RANGE_SLIDER_ID,
        display_text: "Select Range",
        min: 0,
        max: 100,
        step: 5,
        initial: 50,
    });
    
    // Render the template with the context
    execSync(`python render_template.py ${templateName} '${context}' `, { stdio: "inherit" });

    const outputPath = path.resolve("./rendered_templates/test_range_slider_output.html");

    // Read the rendered HTML
    renderedHtml = fs.readFileSync(outputPath, "utf8");
});

beforeEach(() => {
    document.body.innerHTML = renderedHtml;

    // Initialize range slider and add event listeners
    TETHYS_RANGE_SLIDER.init_range_sliders();
});

test("Gizmo renders correctly", () => {
    expect(screen.getByLabelText("Select Range")).toBeInTheDocument();
    expect(screen.getByRole("slider")).toBeInTheDocument();
});

test("Range slider updates display text", () => {
    const rangeSliderInput = document.getElementById(RANGE_SLIDER_ID);
    const rangeSliderDisplay = rangeSliderInput.nextElementSibling;

    // Test for initial value
    expect(rangeSliderDisplay).toHaveTextContent("50");

    // Test for updated value with input
    fireEvent.input(rangeSliderInput, { target: { value: 75 } });
    expect(rangeSliderDisplay).toHaveTextContent("75");
});