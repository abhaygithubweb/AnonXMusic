#!/bin/bash

apt-get update
apt-get install -y ffmpeg

curl -fsSL https://deno.land/install.sh | sh
export DENO_INSTALL="/root/.deno"
export PATH="$DENO_INSTALL/bin:$PATH"
