#!/usr/bin/bash

tar="ugc_classify.tar.gz"
path="/user/ime/fengchaobing/targz/${tar}"

rm -f ${tar}
tar zcvf ${tar} ./*
hadoop fs -rmr ${path}
hadoop fs -put ${tar} ${path}
