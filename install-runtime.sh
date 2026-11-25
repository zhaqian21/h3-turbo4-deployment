#!/bin/bash
set -euo pipefail
R=/data/users/example/h3-turbo4
export UV_HTTP_TIMEOUT=600
export UV_HTTP_RETRIES=8
export UV_CONCURRENT_DOWNLOADS=8
export UV_CACHE_DIR=$R/cache/uv
export TMPDIR=$R/tmp
export APPTAINER_TMPDIR=$R/tmp
export APPTAINER_CACHEDIR=$R/cache/apptainer
exec "$R/tools/apptainer-mirror/bin/apptainer" exec --nv --bind /data --env LD_LIBRARY_PATH=$R/driver-libs "$R/ubuntu-rootfs" "$R/venv/bin/uv" pip install --python "$R/runtime-venv/bin/python" --python-platform x86_64-manylinux_2_35 'sglang[diffusion]==0.5.22' --index-url https://mirrors.cloud.tencent.com/pypi/simple/ --extra-index-url https://pypi.nvidia.com/
