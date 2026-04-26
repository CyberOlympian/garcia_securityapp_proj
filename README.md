# secure-app DevSecOps Example

This repository is a compact, realistic GitHub Actions example for an advanced DevSecOps pipeline that stays entirely inside GitHub Actions and local build artifacts.

## Included Files

- `app/main.py`: small Flask service with a health endpoint and a validated echo API.
- `requirements.txt`: minimal pinned dependencies.
- `Dockerfile`: hardened container build with a non-root user and security updates.
- `.github/workflows/devsecops-pipeline.yml`: multi-job GitHub Actions pipeline for SAST, dependency scanning, secret scanning, container scanning, SBOM generation, and artifact publication.
- `.semgrep.yml`: custom Semgrep rules for basic application security checks.
- `README.md`: this overview.

## Pipeline Design

The workflow uses two jobs with an explicit dependency chain:

1. `scan`
   - Installs Python dependencies.
   - Runs `pip-audit` against pinned requirements.
   - Runs Semgrep using the repository-local `.semgrep.yml`.
   - Runs a Trivy filesystem secret scan.
   - Uploads scan outputs as artifacts.

2. `build`
   - Runs only after `scan` succeeds.
   - Builds the container image locally and tags it with the commit SHA.
   - Runs a Trivy container vulnerability scan.
   - Generates a CycloneDX SBOM for the container image.
   - Writes trusted-build metadata only after all checks pass.
   - Uploads build-time artifacts.

## Produced Artifacts

The workflow produces the following auditable artifacts:

- `dependency-audit.txt`
  - Records the dependency vulnerability scan outcome.

- `semgrep.sarif`
  - SAST output in a machine-readable format suitable for security tooling.

- `secret-scan.txt`
  - Secret-scanning output from Trivy.

- `scan-summary.md`
  - Human-readable summary of the scan stage.

- `container-vulns.txt`
  - Container vulnerability scan summary for the built image.

- `sbom.cdx.json`
  - CycloneDX SBOM for the container image.

- `image-identifier.txt`
  - Image reference tied directly to the commit SHA.

- `trusted-build.txt`
  - Explicit marker that the image is considered trusted only after all required checks succeed.

## Why This Is More Mature Than a Basic Pipeline

A basic pipeline usually stops at linting or a single unit test step. This example adds several DevSecOps controls:

- It separates pre-build security scanning from the image build stage using `needs:`.
- It enforces dependency, SAST, and secret checks before the image can even be built.
- It scans the resulting image and produces an SBOM without leaving GitHub Actions.
- It stores outputs as artifacts so the run is auditable after the fact.
- It marks the image as trusted only after all required checks succeed.

## Local Build Reference

The container image is intended to be built locally inside GitHub Actions with the tag `secure-app:${{ github.sha }}`. That keeps the build traceable to a specific commit without requiring an external registry.

## Notes

The example is deliberately small, but the control flow mirrors a production-grade GitHub-native security pipeline.
