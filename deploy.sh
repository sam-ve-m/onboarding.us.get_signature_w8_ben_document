#!/bin/bash

fission spec init
fission env create --spec --name update-w8-ben-env --image nexus.sigame.com.br/fission-async:0.1.7 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name update-w8-ben-fn --env update-w8-ben-env --src "./func/*" --entrypoint main.update_w8_ben --executortype newdeploy --maxscale 1
fission route create --spec --name update-w8-ben-rt --method PUT --url /onboarding/update_w8_ben --function update-w8-ben-fn