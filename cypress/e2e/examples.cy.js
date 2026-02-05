/// <reference types="cypress" />

describe("Example Pages", () => {
  // --- Basic ---
  describe("Basic Player", () => {
    it("renders waveform and controls", () => {
      cy.visit("/examples/basic.html");
      cy.get('[id^="player-"]').should("exist");
      cy.get('[id^="waveform-"]').should("exist");
      cy.get('[id^="play-"]').should("exist");
      cy.get('[id^="time-"]').should("exist");
    });

    it("visual regression", () => {
      cy.visit("/examples/basic.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-basic");
    });
  });

  // --- Bars ---
  describe("Bar-Style Waveforms", () => {
    it("renders 3 players", () => {
      cy.visit("/examples/bars.html");
      cy.get('[id^="player-"]').should("have.length", 3);
      cy.get('[id^="waveform-"]').should("have.length", 3);
    });

    it("visual regression", () => {
      cy.visit("/examples/bars.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-bars");
    });
  });

  // --- Gradients ---
  describe("Gradient Colors", () => {
    it("renders 3 players", () => {
      cy.visit("/examples/gradients.html");
      cy.get('[id^="player-"]').should("have.length", 3);
    });

    it("visual regression", () => {
      cy.visit("/examples/gradients.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-gradients");
    });
  });

  // --- Timeline Plugin ---
  describe("Timeline Plugin", () => {
    it("renders waveform with timeline", () => {
      cy.visit("/examples/timeline.html");
      cy.get('[id^="player-"]').should("exist");
      cy.get('[id^="waveform-"]').should("exist");
    });

    it("visual regression", () => {
      cy.visit("/examples/timeline.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-timeline");
    });
  });

  // --- Minimap Plugin ---
  describe("Minimap Plugin", () => {
    it("renders waveform with minimap", () => {
      cy.visit("/examples/minimap.html");
      cy.get('[id^="player-"]').should("exist");
      cy.get('[id^="waveform-"]').should("exist");
    });

    it("visual regression", () => {
      cy.visit("/examples/minimap.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-minimap");
    });
  });

  // --- Spectrogram Plugin ---
  describe("Spectrogram Plugin", () => {
    it("renders waveform with spectrogram", () => {
      cy.visit("/examples/spectrogram.html");
      cy.get('[id^="player-"]').should("exist");
    });

    it("visual regression", () => {
      cy.visit("/examples/spectrogram.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-spectrogram");
    });
  });

  // --- Regions Plugin ---
  describe("Regions Plugin", () => {
    it("renders waveform with regions", () => {
      cy.visit("/examples/regions.html");
      cy.get('[id^="player-"]').should("exist");
    });

    it("visual regression", () => {
      cy.visit("/examples/regions.html");
      cy.wait(3000);
      cy.matchImageSnapshot("example-regions");
    });
  });

  // --- Controls ---
  describe("Player Controls", () => {
    it("renders 3 players with all control types", () => {
      cy.visit("/examples/controls.html");
      cy.get('[id^="player-"]').should("have.length", 3);
      cy.get('[id^="play-"]').should("have.length", 3);
      cy.get('[id^="volume-"]').should("have.length", 3);
      cy.get('[id^="rate-"]').should("have.length", 3);
    });

    it("visual regression", () => {
      cy.visit("/examples/controls.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-controls");
    });
  });

  // --- Layout Grid ---
  describe("Grid Layout", () => {
    it("renders 4 players in a grid", () => {
      cy.visit("/examples/layout.html");
      cy.get('[id^="player-"]').should("have.length", 4);
      cy.get('[id^="waveform-"]').should("have.length", 4);
    });

    it("visual regression", () => {
      cy.visit("/examples/layout.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-layout");
    });
  });

  // --- Custom Theme ---
  describe("Custom Theme", () => {
    it("renders player with custom styling", () => {
      cy.visit("/examples/custom_theme.html");
      cy.get('[id^="player-"]').should("exist");
    });

    it("visual regression", () => {
      cy.visit("/examples/custom_theme.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-custom-theme");
    });
  });

  // --- Built-in Themes ---
  describe("Built-in Themes", () => {
    it("renders DARK and LIGHT players", () => {
      cy.visit("/examples/themes.html");
      cy.get('[id^="player-"]').should("have.length", 2);
    });

    it("visual regression", () => {
      cy.visit("/examples/themes.html");
      cy.wait(2000);
      cy.matchImageSnapshot("example-themes");
    });
  });
});
