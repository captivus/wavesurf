import { addMatchImageSnapshotCommand } from "@simonsmith/cypress-image-snapshot/command";

addMatchImageSnapshotCommand({
  failureThreshold: 0.03,
  failureThresholdType: "percent",
  customDiffConfig: { threshold: 0.1 },
  capture: "viewport",
});
