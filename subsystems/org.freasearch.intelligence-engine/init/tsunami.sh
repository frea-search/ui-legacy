#!/bin/sh
rm -f /var/frea/tmp/org.freasearch.intelligence-engine/tsunami.sock
su frea -c "python3 /var/frea/subsystems/org.freasearch.intelligence-engine/tsunami.py"
