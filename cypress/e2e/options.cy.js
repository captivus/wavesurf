/// <reference types="cypress" />

describe("Custom Options", () => {
  it("loads the custom options page without errors", () => {
    cy.visit("/custom_options.html");
    cy.get("iframe").should("exist");
    cy.get("iframe").its("0.contentDocument.body").should("not.be.empty");
  });

  it("renders the all-controls page with volume and rate selectors", () => {
    cy.visit("/all_controls.html");
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        // Volume slider
        const volume = doc.querySelector('[id^="volume-"]');
        expect(volume).to.not.be.null;
        expect(volume.type).to.equal("range");
        // Playback rate selector
        const rate = doc.querySelector('[id^="rate-"]');
        expect(rate).to.not.be.null;
        expect(rate.tagName.toLowerCase()).to.equal("select");
      });
  });

  it("visual regression — dark theme", () => {
    cy.visit("/basic_dark.html");
    // Allow time for waveform to render
    cy.wait(1000);
    cy.matchImageSnapshot("dark-theme");
  });

});
