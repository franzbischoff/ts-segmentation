#!/usr/bin/env bash
# Robust post-create helper for devcontainer
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "[post-create] Creating or updating virtualenv at $ROOT_DIR/.venv"
# create venv (if it fails, surface the error)
python -m venv .venv

VE_PY=".venv/bin/python"
if [ ! -x "$VE_PY" ]; then
  echo "ERROR: expected interpreter not found at $VE_PY"
  exit 1
fi

echo "[post-create] Upgrading pip, setuptools, wheel"
"$VE_PY" -m pip install -U pip setuptools wheel

# Install minimal requirements first when present. Many packages (e.g.
# scikit-multiflow) require numpy already available during build time, so we
# install a minimal set first to bootstrap wheels/build deps, then the full
# requirements list.
if [ -f requirements_minimal.txt ]; then
  echo "[post-create] Installing minimal requirements from requirements_minimal.txt (bootstrap)"
  # Some packages (like scikit-multiflow) require numpy to be present **before**
  # building wheels. Try to install the pinned numpy version first if present
  if grep -E '^\s*numpy' requirements_minimal.txt >/dev/null 2>&1; then
    NUMPY_SPEC=$(grep -E '^\s*numpy' requirements_minimal.txt | head -n1 | tr -d '[:space:]')
    echo "[post-create] Bootstrapping numpy using spec: $NUMPY_SPEC"
    "$VE_PY" -m pip install --no-cache-dir "$NUMPY_SPEC"
  else
    echo "[post-create] Bootstrapping numpy (no pinned spec found)"
    "$VE_PY" -m pip install --no-cache-dir numpy
  fi

  # If scikit-multiflow is present in the minimal set it often requires
  # building against an already-installed numpy. Install it explicitly using
  # --no-build-isolation so the build runs inside the current venv that
  # already contains numpy.
  SKIP_SCIMF=0
  if grep -E '^\s*scikit-multiflow' requirements_minimal.txt >/dev/null 2>&1; then
    SCIMF_SPEC=$(grep -E '^\s*scikit-multiflow' requirements_minimal.txt | head -n1 | tr -d '[:space:]')
    echo "[post-create] Found scikit-multiflow in minimal requirements, trying to install using --no-build-isolation: $SCIMF_SPEC"
    set +e
    "$VE_PY" -m pip install --no-cache-dir --no-build-isolation "$SCIMF_SPEC"
    SCIMF_RC=$?
    set -e
    if [ $SCIMF_RC -ne 0 ]; then
      echo "[post-create] Warning: installing scikit-multiflow failed (build issues). Will continue and skip it for automatic installation." >&2
      SKIP_SCIMF=1
    else
      echo "[post-create] scikit-multiflow installed successfully"
    fi
  fi

  # Now install the rest of the minimal requirements (numpy/scikit-multiflow handled or skipped)
  if [ "$SKIP_SCIMF" -eq 1 ]; then
    echo "[post-create] Installing remaining minimal requirements while skipping scikit-multiflow"
    TEMP_MIN=$(mktemp)
    grep -v -E '^\s*scikit-multiflow' requirements_minimal.txt > "$TEMP_MIN"
    "$VE_PY" -m pip install --no-cache-dir -r "$TEMP_MIN"
    rm -f "$TEMP_MIN"
  else
    "$VE_PY" -m pip install --no-cache-dir -r requirements_minimal.txt
  fi
fi

if [ -f requirements.txt ]; then
  echo "[post-create] Installing full Python requirements from requirements.txt"

  # If scikit-multiflow was skipped earlier, remove it from the full install too so
  # we don't fail the whole process.
  if [ "$SKIP_SCIMF" -eq 1 ] && grep -E '^\s*scikit-multiflow' requirements.txt >/dev/null 2>&1; then
    echo "[post-create] scikit-multiflow previously failed to build; skipping it in requirements.txt install"
    TEMP_FULL=$(mktemp)
    grep -v -E '^\s*scikit-multiflow' requirements.txt > "$TEMP_FULL"
    "$VE_PY" -m pip install --no-cache-dir -r "$TEMP_FULL"
    rm -f "$TEMP_FULL"
  else
    # If scikit is present but hasn't failed previously, try to install it with
    # --no-build-isolation first so it will see numpy and other venv packages.
    if grep -E '^\s*scikit-multiflow' requirements.txt >/dev/null 2>&1; then
      SCIMF_SPEC=$(grep -E '^\s*scikit-multiflow' requirements.txt | head -n1 | tr -d '[:space:]')
      echo "[post-create] scikit-multiflow found in requirements.txt; attempting dedicated install with --no-build-isolation: $SCIMF_SPEC"
      set +e
      "$VE_PY" -m pip install --no-cache-dir --no-build-isolation "$SCIMF_SPEC"
      SCIMF_RC=$?
      set -e
      if [ $SCIMF_RC -ne 0 ]; then
        echo "[post-create] Warning: scikit-multiflow failed to build; it will be skipped and other dependencies will be installed." >&2
        SKIP_SCIMF=1
        TEMP_FULL=$(mktemp)
        grep -v -E '^\s*scikit-multiflow' requirements.txt > "$TEMP_FULL"
        "$VE_PY" -m pip install --no-cache-dir -r "$TEMP_FULL"
        rm -f "$TEMP_FULL"
      else
        # scikit-multiflow installed ok, proceed to install rest
        "$VE_PY" -m pip install --no-cache-dir -r requirements.txt
      fi
    else
      "$VE_PY" -m pip install --no-cache-dir -r requirements.txt
    fi
  fi
else
  echo "[post-create] No requirements.txt found, skipping dependency installation."
fi

echo "[post-create] Completed successfully"
