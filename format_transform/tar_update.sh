#!/usr/bin/bash

rm ./demo_for_format.tar.gz
tar zcvf demo_for_format.tar.gz ./*
hadoop fs -rmr /user/ime/wangzehui/language_detect/demo_for_format.tar.gz
hadoop fs -put ./demo_for_format.tar.gz /user/ime/wangzehui/language_detect/demo_for_format.tar.gz
