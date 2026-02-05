/// <reference types="cypress" />

describe("Playback Controls", () => {
  beforeEach(() => {
    cy.visit("/cypress/fixtures/basic_dark.html");
    // Wait for iframe to load
    cy.get("iframe").its("0.contentDocument.body").should("not.be.empty");
  });

  it("has a play button that exists", () => {
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const playBtn = doc.querySelector('[id^="play-"]');
        expect(playBtn).to.not.be.null;
      });
  });

  it("shows initial time as 0:00", () => {
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const timeEl = doc.querySelector('[id^="time-"]');
        expect(timeEl).to.not.be.null;
        // Initially shows "0:00 / 0:00" (before audio loads)
        expect(timeEl.textContent).to.include("0:00");
      });
  });

  it("play icon starts with play symbol", () => {
    cy.get("iframe")
      .its("0.contentDocument")
      .then((doc) => {
        const iconEl = doc.querySelector('[id^="icon-"]');
        expect(iconEl).to.not.be.null;
        // Unicode play triangle (▶)
        expect(iconEl.innerHTML).to.include("▶");
      });
  });
});
