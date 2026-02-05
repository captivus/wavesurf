const { defineConfig } = require("cypress");
const {
  addMatchImageSnapshotPlugin,
} = require("@simonsmith/cypress-image-snapshot/plugin");

module.exports = defineConfig({
  e2e: {
    baseUrl: "http://localhost:8765",
    supportFile: "cypress/support/e2e.js",
    specPattern: "cypress/e2e/**/*.cy.js",
    fixturesFolder: "cypress/fixtures",
    screenshotsFolder: "cypress/snapshots",
    video: false,
    setupNodeEvents(on, config) {
      addMatchImageSnapshotPlugin(on, config);
    },
  },
  // Force consistent rendering across environments
  viewportWidth: 800,
  viewportHeight: 600,
});
