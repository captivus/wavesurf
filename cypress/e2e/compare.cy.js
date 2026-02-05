/// <reference types="cypress" />

describe("Compare Grid Layout", () => {
  beforeEach(() => {
    cy.visit("/compare_grid.html");
    cy.get("iframe").should("exist");
    cy.get("iframe").its("0.contentDocument.body").should("not.be.empty");
  });

  it("renders multiple players inside a single iframe", () => {
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const players = doc.querySelectorAll('[id^="player-"]');
        expect(players.length).to.equal(3);
      });
  });

  it("each player has its own waveform container", () => {
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const waveforms = doc.querySelectorAll('[id^="waveform-"]');
        expect(waveforms.length).to.equal(3);
        // All IDs should be unique
        const ids = Array.from(waveforms).map((el) => el.id);
        const unique = new Set(ids);
        expect(unique.size).to.equal(3);
      });
  });

  it("displays correct labels", () => {
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const body = doc.body.innerHTML;
        expect(body).to.include("440 Hz");
        expect(body).to.include("660 Hz");
        expect(body).to.include("880 Hz");
      });
  });

  it("uses a grid layout container", () => {
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const gridDiv = doc.querySelector('div[style*="display: grid"]');
        expect(gridDiv).to.not.be.null;
      });
  });
});
