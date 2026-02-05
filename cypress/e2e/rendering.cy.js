/// <reference types="cypress" />

describe("Waveform Rendering", () => {
  it("renders a canvas inside the iframe (dark theme)", () => {
    cy.visit("/basic_dark.html");
    cy.get("iframe").should("exist");
    cy.get("iframe").its("0.contentDocument.body").should("not.be.empty");
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const waveformDiv = doc.querySelector('[id^="waveform-"]');
        expect(waveformDiv).to.not.be.null;
      });
  });

  it("renders a canvas inside the iframe (light theme)", () => {
    cy.visit("/basic_light.html");
    cy.get("iframe").should("exist");
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const waveformDiv = doc.querySelector('[id^="waveform-"]');
        expect(waveformDiv).to.not.be.null;
      });
  });

  it("contains correct element IDs", () => {
    cy.visit("/basic_dark.html");
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const playerDiv = doc.querySelector('[id^="player-"]');
        expect(playerDiv).to.not.be.null;
        const uid = playerDiv.id.replace("player-", "");
        expect(doc.querySelector(`#waveform-${uid}`)).to.not.be.null;
        expect(doc.querySelector(`#play-${uid}`)).to.not.be.null;
        expect(doc.querySelector(`#time-${uid}`)).to.not.be.null;
        expect(doc.querySelector(`#icon-${uid}`)).to.not.be.null;
      });
  });
});
