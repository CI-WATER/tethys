import { TextEncoder, TextDecoder } from "util";

if (typeof global.TextEncoder === "undefined") {
  global.TextEncoder = TextEncoder;
}

if (typeof global.TextDecoder === "undefined") {
  global.TextDecoder = TextDecoder;
}

try {
    require("cesium");
  } catch (e) {
    jest.mock("cesium", () => require("./__mocks__/cesium"));
  }

import { JSDOM } from "jsdom";

const dom = new JSDOM("<!DOCTYPE html><html><body></body></html>", {
    url: "http://localhost",
});

global.window = dom.window;
global.document = dom.window.document;

const $ = require("jquery");

global.$ = $;
global.jQuery = $;

global.$.fn = global.$.fn || {};

import "@testing-library/jest-dom";