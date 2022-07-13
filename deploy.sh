#!/bin/bash

fission spec init
fission env create --spec --name update-w8-ben-signature-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name update-w8-ben-signature-fn --env update-w8-ben-signature-env --src "./func/*" --entrypoint main.update_w8_ben_signature
fission route create --spec --name update-w8-ben-signature-rt --method PUT --url /update-w8-ben-signature --function update-w8-ben-signature-fn